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
from synapseclient import Table, PartialRowset # Synapse, Column, Schema
# from synapseclient.core.exceptions import SynapseAuthenticationError, SynapseNoCredentialsError
import pandas as pd
# import re
from scripts.utils import get_auth_token
from scripts.create_denormalized_tables import SRC_TABLES, PROJECT_ID, DEST_TABLES, create_or_clear_table, initialize_synapse
from datetime import datetime
import warnings

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

    # synapse_tables is the metadata for the tracked tables, which contains the current versionNumber
    synapse_tables = {tbl['name']: tbl for tbl in syn.getChildren(PROJECT_ID, includeTypes=['table']) if tbl['name'] in tracked_table_names}

    # get dict of all tables with name ending in '_latest'
    latest_table_copies = {synapse_table['name']: synapse_table for synapse_table in syn.getChildren(PROJECT_ID, includeTypes=['table']) if synapse_table['name'].str.endwith('_latest')}
    tables_without_latest_copy = set(tracked_table_names) - set([t['name'] for t in latest_table_copies.values()])

    def get_row_cnt(table_id):
        results = syn.tableQuery(f"SELECT count(*) AS cnt FROM {table_id}")
        row_cnt = results.asDataFrame().iloc[0].iloc[0]
        return row_cnt

    def get_latest_non_empty_version(table_name):
        synapse_table = synapse_tables[table_name]
        actual_current_version = synapse_table['versionNumber']
        version_number = actual_current_version
        while True:
            table_id = synapse_table['id'] \
                if version_number == actual_current_version \
                else f"{synapse_table['id']}.{synapse_table['versionNumber']}"
            row_cnt = get_row_cnt(table_id)
            if row_cnt == 0: # decrement version_number we're on since this version is empty
                version_number = version_number - 1
                if version_number < 1:
                    raise Exception(f"No non-empty versions of {table_name} found")
            else:
                break

        latest_non_empty_version = version_number
        return synapse_table, latest_non_empty_version, table_id, row_cnt

    def copy_table_to_latest(table_id):
        results = syn.tableQuery(f"SELECT * FROM {table_id}")
        syn.store(results)

    no_latest_version_change = {}   # just update no_change_as_of
    latest_versions = {}            # add new record

    tables_not_in_CurrentTableVersions = set(tracked_table_names) - set(current_version_table_names)
    for table_name in tables_not_in_CurrentTableVersions:
        synapse_table, latest_non_empty_version, table_id, row_cnt = get_latest_non_empty_version(table_name)
        # if there's no record in CurrentTableVersions, we probably haven't made a latest copy
        copy_table_to_latest(table_id)

        latest_versions[table_name] = {
            'table_name': table_name,
            'table_id': table_id,   # will include .<version> if using a version other than current
            'force_version': '',
            'latest_non_empty_version': str(latest_non_empty_version),
            'as_of': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'no_change_as_of': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'row_cnt': row_cnt,
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

        force_version: str = current_versions_row['force_version']
        if force_version and int(force_version) < latest_non_empty_version:
            warnings.warn(f"Latest non-empty version of {table_name} ({latest_non_empty_version}) is newer than force_version ({force_version}). Should update?")

        latest_versions[table_name] = {
            'table_name': table_name,
            'table_id': table_id,  # will include .<version> if using a version other than current
            'force_version': force_version,
            'latest_non_empty_version': latest_non_empty_version,
            'as_of': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'no_change_as_of': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'row_cnt': row_cnt,
        }

    # for unchanged tables, just update no_change_as_of
    partial_rowset = PartialRowset.from_mapping(no_latest_version_change, currentTableVersions)
    syn.store(partial_rowset)

    if latest_versions:
        # add rows to CurrentTableVersions only for latest_versions
        newCtvDf = pd.DataFrame(latest_versions.values()).fillna('')
        newCtvDf = newCtvDf.astype(dtype={'row_cnt': 'int64', 'latest_non_empty_version': 'str'})
        ctvSchema = syn.get(CurrentTableVersionsId)
        ctv = syn.store(Table(ctvSchema, newCtvDf))

    # copy force_version (if it's been specified) or latest_non_empty_version (otherwise) to <table_name>_latest
    #   if <table_name>_latest does not exist, create it
    #   otherwise, replace it only if it would be different -- that is, if there's a latest_version for it

    for current_latest_table in synapse_tables.values():
        name = current_latest_table['name']
        id = current_latest_table['id']


        if name in latest_versions:
            latest_version = latest_versions[name]
            if latest_version['force_version']:
                pass
                # and latest_version['force_version'] != current_latest_table['force_version']:
            # make a copy of this new latest (non-empty) version


        for lv in latest_versions.values():
            table = syn.tableQuery(f"SELECT * FROM {lv['table_id']}")

    # create_or_clear_table(syn, dest_table['dest_table_name'])
    # table = syn.store(Table(schema, final_df))

    pass

if __name__ == "__main__":
    find_latest_non_empty_versions()
