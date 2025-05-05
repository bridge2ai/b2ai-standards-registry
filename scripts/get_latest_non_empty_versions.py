"""
For the SRC_TABLES and DEST_TABLES defined in create_denormalized_tables.py,
find the most recent non-empty versions and store in CurrentTableVersions.

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
    denormalize_tables()
"""

# from typing import Any, Dict, List
from synapseclient import Table # Synapse, Column, Schema
# from synapseclient.core.exceptions import SynapseAuthenticationError, SynapseNoCredentialsError
import pandas as pd
import numpy as np
# import re
from scripts.utils import get_auth_token
from scripts.create_denormalized_tables import SRC_TABLES, PROJECT_ID, DEST_TABLES, create_or_clear_table, initialize_synapse
from datetime import datetime

AUTH_TOKEN = get_auth_token()
CurrentTableVersionsId = 'syn66330007'

def find_latest_non_empty_versions():
    syn = initialize_synapse()

    currentTableVersions = syn.tableQuery(f"SELECT table_name, table_id, version_to_use FROM {CurrentTableVersionsId} WHERE version_to_use IS NOT NULL")
    ctvSchema = syn.get(CurrentTableVersionsId)

    versions_to_use = {}
    for i, row in currentTableVersions.asDataFrame().iterrows():
        table_name = row['table_name']
        versions_to_use[table_name] = row['version_to_use']

    table_names = [t['name'] for t in SRC_TABLES.values()] + list(DEST_TABLES.keys())

    synapse_tables = [tbl for tbl in syn.getChildren(PROJECT_ID, includeTypes=['table']) if tbl['name'] in table_names]

    current_versions = {}
    for tbl in synapse_tables:
        version_to_use: str = versions_to_use.get(tbl['name'], '')
        version_number: int = version_to_use
        # in order to select from current version, can't use version number
        while True:
            versionStr = f".{version_number}" if version_number else ""
            tbl_id = f"{tbl['id']}{versionStr}"
            results = syn.tableQuery(f"SELECT count(*) AS cnt FROM {tbl_id}")
            row_cnt = results.asDataFrame().iloc[0].iloc[0]
            print(f"{tbl['name']} {tbl_id} -- {row_cnt} rows")
            if row_cnt == 0:
                # if still on current, get latest previous version, otherwise decrement version_number we're on since still empty
                version_number = (version_number if version_number else tbl['versionNumber']) - 1
                if version_to_use:
                    raise ValueError(f"{tbl['name']} version_to_use {version_to_use} is empty")
                continue
            else:
                current_versions[tbl['name']] = {
                    'table_name': tbl['name'],
                    'table_id': tbl_id,
                    'version_to_use': version_to_use,
                    'latest_non_empty_version': '' if version_to_use else str(version_number),
                    'row_cnt': row_cnt,
                    'as_of': datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                break

    newCtvDf = pd.DataFrame(current_versions.values()).fillna('')
    newCtvDf = newCtvDf.astype(dtype={'row_cnt': 'int64', 'latest_non_empty_version': 'str'})
    ctv = syn.store(Table(ctvSchema, newCtvDf))

    for tbl in current_versions.values():
        schema = syn.get(tbl['table_id'])
        # x = { col['name']: col for col in syn.getTableColumns(syn_table) }
        table = syn.store(Table(schema, final_df))

    for tbl in current_versions.values():
        schema = syn.get(tbl['table_id'])
        # x = { col['name']: col for col in syn.getTableColumns(syn_table) }
        table = syn.store(Table(schema, final_df))
        pass

    pass
    # all_src_tables = {tbl: get_src_table(syn, tbl) for tbl in SRC_TABLES}
    #
    # for dest_table in DEST_TABLES.values():
    #     base_tbl_name = dest_table['base_table']
    #     base_df = all_src_tables[base_tbl_name]['df']
    #     src_tables = [j['join_tbl'] for j in dest_table['join_columns']]
    #
    #     if base_df.empty:
    #         print(f"Skipping '{dest_table['dest_table_name']}' — base table '{base_tbl_name}' has no data.")
    #         continue
    #
    #     make_dest_table(syn, dest_table, src_tables)




if __name__ == "__main__":
    find_latest_non_empty_versions()
