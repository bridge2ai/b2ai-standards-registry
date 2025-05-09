"""
For the SRC_TABLES and DEST_TABLES defined in create_denormalized_tables.py,
find the most recent non-empty versions and store in CurrentTableVersions.
Copy the version that should be used (CurrentTableVersions.force_version,
if specified, otherwise latest_non_empty_version, to a table called <table_name>_latest.

Usage:
    Run this script directly (e.g., `python -m scripts.get_latest_non_empty_versions`)
    Authentication is handled via a personal access token fetched from utils.py.
    It expects an auth token to be stored in ~/.synapseConfig. For instructions on setting up your auth token,
    see scripts/README.md.

Expected Environment:
    - AUTH_TOKEN will be retrieved by scripts.utils.get_auth_token()
      Instructions for setting up your auth token are documented in the README.
    - The SRC_TABLES and DEST_TABLES definitions must be updated with valid Synapse table IDs

Main entry point:
    find_latest_non_empty_versions()
"""
# from typing import Any, Dict, List
from synapseclient import Table, Schema, PartialRowset, Column # build_table, Synapse, Schema
from synapseclient.models import Table as modelTable, SchemaStorageStrategy
# from synapseclient.core.exceptions import SynapseAuthenticationError, SynapseNoCredentialsError
import pandas as pd
# import re
from scripts.utils import get_auth_token, get_df_max_lengths
from scripts.create_denormalized_tables import SRC_TABLES, PROJECT_ID, DEST_TABLES, create_or_clear_table, initialize_synapse
from datetime import datetime

AUTH_TOKEN = get_auth_token()
CurrentTableVersionsId = 'syn66330007'

def find_latest_non_empty_versions():
    """
    First, review and update CurrentTableVersions so that latest_non_empty_version is correct.
    If any table appearing in SRC_TABLES or DEST_TABLES is not yet in CurrentTableVersions, add it.
    If the latest non-empty version is the current version (e.g., 4), latest_non_empty_version must be blank
        because you can't select from <table_id>.4, you have to select from <table_id>.
    """
    syn = initialize_synapse()

    # if latest_non_empty_version hasn't changed, don't make new record. but maybe add column for last_checked in addition to as_of

    currentTableVersions = syn.tableQuery(f"SELECT * FROM {CurrentTableVersionsId}")
    current_versions = currentTableVersions.asDataFrame()

    # need to add rowId to current_versions dataframe to allow update (of no_change_as_of) later
    rowset = currentTableVersions.asRowSet()
    # make sure rowIds in the right order
    if [row['values'][0] for row in rowset.rows] != list(current_versions['table_name']):
        raise Exception("current_versions and rowset not in the same order")
    current_versions['rowId'] = [row['rowId'] for row in rowset.rows]

    # format dataframe as needed (or for easier reading)
    current_versions = current_versions.fillna({'row_cnt': 0})  # row_cnt is an int
    current_versions = current_versions.fillna('')              # everything else is a string
    current_versions = current_versions.astype(dtype={'row_cnt': 'int64'})

    # no_change_as_of will either be the datetime the row was added (as_of), or the last datetime
    # it was checked and hadn't changed. current_versions should only include one row per table_name,
    # the one with the most recent no_change_as_of. The other rows are kept just as a record.
    current_versions = current_versions.sort_values('no_change_as_of').drop_duplicates('table_name', keep='last')

    current_version_table_names = list(current_versions['table_name'])  # grab this before indexing on table_name
    current_versions.set_index('table_name', inplace=True) # to look up by table_name below

    # tracked_table_names is any table accessed in create_denormalized_tables.py
    tracked_table_names = [tbl['name'] for tbl in SRC_TABLES.values()] + list(DEST_TABLES.keys())
    # tracked_table_names = ['test'] # COMMENT OUT AFTER TESTING

    all_synapse_tables = {tbl['name']: tbl for tbl in syn.getChildren(PROJECT_ID, includeTypes=['table'])}
    # synapse_tables is the metadata for the tracked tables, which contains the current versionNumber
    synapse_tables = {tbl['name']: tbl for tbl in all_synapse_tables.values() if tbl['name'] in tracked_table_names}

    # get dict of all tables with name ending in '_latest'
    latest_table_copies = {tbl['name']: tbl for tbl in all_synapse_tables.values() if tbl['name'].endswith('_latest')}

    def get_row_cnt(table_id):
        results = syn.tableQuery(f"SELECT count(*) AS cnt FROM {table_id}")
        row_cnt: int = results.asDataFrame().iloc[0].iloc[0]
        return row_cnt

    def get_latest_non_empty_version(table_name):
        synapse_table = synapse_tables[table_name]
        actual_current_version: int = synapse_table['versionNumber']
        version_number: int = actual_current_version
        while True:
            table_id = synapse_table['id'] \
                if version_number == actual_current_version \
                else f"{synapse_table['id']}.{version_number}"
            row_cnt = get_row_cnt(table_id)
            if row_cnt == 0: # decrement version_number we're on since this version is empty
                version_number = version_number - 1
                if version_number < 1:
                    raise Exception(f"No non-empty versions of {table_name} found")
            else:
                break

        latest_non_empty_version: int = version_number
        return synapse_table, latest_non_empty_version, table_id, row_cnt

    no_latest_version_change = {}   # just update no_change_as_of
    latest_versions = {}            # add new record

    tables_not_in_CurrentTableVersions = set(tracked_table_names) - set(current_version_table_names)

    for table_name in tables_not_in_CurrentTableVersions:
        synapse_table, latest_non_empty_version, table_id, row_cnt = get_latest_non_empty_version(table_name)

        # If there's no record in CurrentTableVersions, we probably haven't made a latest copy
        #   so go ahead and make it. Should just overwrite if it does already exist.
        copy_table_id = copy_table_to_latest(syn, latest_table_copies, table_name, table_id)

        latest_versions[table_name] = {
            'table_name': table_name,
            'table_id': table_id,
            'force_version': 0,    # since no CurrentTableVersion, can't have set a force_version
            'latest_non_empty_version': latest_non_empty_version,
            'as_of': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'no_change_as_of': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'row_cnt': row_cnt,
            'table_id_copied': table_id,
            'copy_table_id': copy_table_id,
        }

    for table_name in synapse_tables:
        if table_name in tables_not_in_CurrentTableVersions: # already added to latest_versions
            continue

        synapse_table, latest_non_empty_version, table_id, row_cnt = get_latest_non_empty_version(table_name)

        current_versions_row = current_versions.loc[table_name]

        if current_versions_row['latest_non_empty_version'] == latest_non_empty_version: # just update no_change_as_of
            no_latest_version_change[current_versions_row['rowId']] = {
                'no_change_as_of': datetime.now().strftime("%Y-%m-%d %H:%M")}
            continue

        force_version: int = current_versions_row['force_version'] or 0
        if force_version and force_version < latest_non_empty_version:
            print(f"Latest non-empty version of {table_name} ({latest_non_empty_version}) is newer than force_version ({force_version}). Should update?")

        # make copy
        copy_table_id = copy_table_to_latest(syn, latest_table_copies, table_name, table_id)

        latest_versions[table_name] = {
            'table_name': table_name,
            'table_id': table_id,  # will include .<version> if using a version other than current
            'force_version': force_version,
            'latest_non_empty_version': latest_non_empty_version,
            'as_of': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'no_change_as_of': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'row_cnt': row_cnt,
            'table_id_copied': table_id,
            'copy_table_id': copy_table_id,
        }

    # for unchanged tables, just update no_change_as_of
    partial_rowset = PartialRowset.from_mapping(no_latest_version_change, currentTableVersions)
    syn.store(partial_rowset)

    # add rows to CurrentTableVersions only for latest_versions
    if latest_versions:
        newCtvDf = pd.DataFrame(latest_versions.values()) # .fillna('')
        newCtvDf = newCtvDf.astype(dtype={'row_cnt': 'int', 'force_version': 'int', 'latest_non_empty_version': 'int'})
        table_cols = get_col_defs(currentTableVersions.headers, newCtvDf)
        save_table_infer_from_data(syn, 'CurrentTableVersions', newCtvDf, table_cols, clear=False)

    pass

def get_col_defs(original_cols, df):
    max_lengths = get_df_max_lengths(original_cols, df)

    columns = [Column(**col) for col in original_cols if 'id' in col] # want to skip ROW_ID and ROW_VERSION
    for col in columns:
        name = col['name']
        max_length = max_lengths[name]

        if col['columnType'] == 'STRING':
            if type(max_length) != int:
                raise Exception(f"STRING col {name} has a non-integer max_length")
            col.pop('id', None) # Remove the column id so new column gets created
            col['maximumSize'] = int(max_length)
        elif col['columnType'] == 'STRING_LIST':
            if type(max_length) != dict:
                raise Exception(f"STRING_LIST col {name} has a non-dict max_length")
            col.pop('id', None) # Remove the column id so new column gets created
            col['maximumSize'] = int(max_length['maximumSize'])
            col['maximumListLength'] = max_length['maximumListLength']
        elif col['columnType'] == 'FILEHANDLEID':
            # in copy, have to convert file handle types to INTEGER because file handles only work on the table they came from
            col.pop('id', None) # Remove the column id so new column gets created
            col['columnType'] = 'INTEGER'

        # for other types (BOOLEAN, MEDIUMTEXT) do nothing

    return columns

def save_table_infer_from_data(syn, copy_table_name, df, table_cols, clear=True):
    # this approach works if the _latest table already exists but if it doesn't, it converts STRING_LISTs to STRINGs
    # if the table does exist, but the schema has changed, it throws an error
    try:
        if clear:
            create_or_clear_table(syn, copy_table_name)
        table = modelTable(name=copy_table_name, parent_id=PROJECT_ID)
        table = table.store()
        table.store_rows(values=df, schema_storage_strategy=SchemaStorageStrategy.INFER_FROM_DATA)
        return table.id
    except Exception as e: # happens if data won't fit in schema
        return save_table_specify_schema(syn, copy_table_name, df, table_cols)

        print(e)
        pass

def save_table_specify_schema(syn, copy_table_name, df, table_cols):
    # this approach preserves STRING_LISTS even if the table is new or if the schema has changed
    # but if the schema has changed, it updates the schema and either save_table_specify_schema or save_table_infer_from_data has to be run again
    try:
        schema = Schema(name=copy_table_name, columns=table_cols, parent=PROJECT_ID)
        table = Table(name=copy_table_name, parent_id=PROJECT_ID, schema=schema, values=df)
        table = syn.store(table)
        return table.tableId
    except Exception as e:
        return save_table_infer_from_data(syn, copy_table_name, df, table_cols)

def copy_table_to_latest(syn, latest_table_copies, table_name, table_id_to_copy):
    """
    Copies table to <table_name>_latest and returns the id of the copied table.
    """
    syn.create_snapshot_version(table_id_to_copy)
    copy_table_name = f"{table_name}_latest"
    table_query = syn.tableQuery(f"SELECT * FROM {table_id_to_copy}")
    df = table_query.asDataFrame()
    table_cols = get_col_defs(table_query.headers, df)

    if copy_table_name in latest_table_copies:
        # table_cols_to_compare = copy_list_omit_property(table_cols, 'concreteType')
        latest_copy = syn.tableQuery(f"SELECT * FROM {latest_table_copies[copy_table_name]['id']}")
        latest_copy_cols = [Column(**col) for col in latest_copy.headers if 'id' in col]  # want to skip ROW_ID and ROW_VERSION
        if [[c['name'], c['columnType']] for c in table_cols] != \
           [[c['name'], c['columnType']] for c in latest_copy_cols]:
            return save_table_specify_schema(syn, copy_table_name, df, table_cols) # otherwise schema won't be updated

        try:
            table_id = save_table_infer_from_data(syn, copy_table_name, df, table_cols)
        except Exception as e:  # if latest table exists already but schema has changed, above won't work
            table_id = save_table_specify_schema(syn, copy_table_name, df, table_cols)
    else:
        table_id = save_table_specify_schema(syn, copy_table_name, df, table_cols)

    return table_id

if __name__ == "__main__":
    find_latest_non_empty_versions()
