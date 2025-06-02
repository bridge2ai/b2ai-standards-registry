'''
This script analyzes and updates Synapse tables based on JSON data files.
It infers appropriate Synapse table schemas from the data, creates or clears
tables as needed, and uploads the data to Synapse. The script can be run from
the command line to update all tables, specific files, or by table names.

Main functionalities:
- Maps data file paths to Synapse table IDs.
- Infers column types and sizes from the data using pandas and Synapse
  schema definitions.
- Supports both scalar and list columns, adjusting Synapse schema parameters
  accordingly.
- Provides a command-line interface for flexible operation, including options
  to update all tables or specific ones.
- Handles authentication and error reporting for Synapse operations.

Key functions:
- `file_path_to_table_name(path)`: Extracts the table name from a file path.
- `populate_table(syn, update_file, table_id)`: Loads data from a JSON file,
  infers schema, and uploads it to the specified Synapse table.
- `get_col_defs(new_data_df)`: Analyzes a DataFrame to determine Synapse column
  definitions, including type and size constraints.
- `analyze_and_update(files, all=False, table_names=False)`: Orchestrates the
  update process for one or more tables.
- `cli()`: Command-line interface for user interaction.

Usage:
    python analyze_and_update_synapse_tables.py [options] [files]

Options:
    -a, --all           Upload all tables.
    -t, --table-names   Provide table names instead of file paths.
    files               List of files or table names to upload.

Example:
    python analyze_and_update_synapse_tables.py --all
    python analyze_and_update_synapse_tables.py project/data/DataSet.json
    python analyze_and_update_synapse_tables.py -t DataSet DataTopic

'''

import json
import sys
from typing import Any, Dict, List, Optional
from argparse import ArgumentParser
from synapseclient import Synapse, Table, Schema, Column
from pandas.api.types import infer_dtype
import pandas as pd
from scripts.utils import initialize_synapse, clear_populate_snapshot_table, PROJECT_ID


# the paths detected as changes from the "Get changed files" job mapped to their corresponding synapse table ids
PATHS_TO_IDS = {
    "project/data/DataStandardOrTool.json": "syn63096833",
    "project/data/DataSubstrate.json": "syn63096834",
    "project/data/DataTopic.json": "syn63096835",
    "project/data/Organization.json": "syn63096836",
    "project/data/UseCase.json": "syn63096837",
    "project/data/DataSet.json": "syn66330217",
}


def file_path_to_table_name(path: str) -> str:
    """
    Extracts and returns the table name from a file path.

    :param path: The file path.
    """
    return path.split('/')[-1].split('.')[0]


TABLE_IDS = {file_path_to_table_name(
    p): PATHS_TO_IDS[p] for p in PATHS_TO_IDS.keys()}


def populate_table(syn: Synapse, update_file: str, table_id: str) -> None:
    """
    Populate the table with updated data

    :param syn: synapse client
    :param update_file: path for json file containing data to populate the table
    :param table_id: synapse id for table to populate
    """
    with open(update_file, "r") as file:
        data = json.load(file)
    # each json file begins with a key that maps to the list of records, so we're accessing that list here
    data = next(iter(data.values()), [])

    if not isinstance(data, list):
        print("Could not get list of data from json file")
        return

    df = pd.DataFrame(data=data)

    coldefs = get_col_defs(df)

    table_name = file_path_to_table_name(update_file)

    clear_populate_snapshot_table(syn, table_name, coldefs, df, table_id)


# synapse defaults
# ignoring this because some tables will be too big if defaulting to it
default_maximumSize = 50
#   instead, make maximumSize just big enough to fit the longest column value
default_maximumListLength = 100

def get_col_defs(new_data_df: pd.DataFrame) -> List[Column]:
    """
    Returns Column definitions for Synapse schema based on data in df
    TODO: If ever refactoring, this could be combined into a shared function with
          ./create_denormalized_tables.py:configure_column_metadata

    :param new_data_df: DataFrame with new data
    :return: Column definitions
    """
    is_list_cols = (new_data_df.map(type).astype(str) == "<class 'list'>").any()
    list_cols = set(is_list_cols[is_list_cols == True].index)
    scalar_types = {c: infer_dtype(new_data_df[c], skipna=True).upper() for c in new_data_df.columns}  # infer_dtype gives 'mixed' for list types
    # assuming all list columns are string lists, at least for now
    def get_col_type(
        col_name): return 'STRING_LIST' if col_name in list_cols else scalar_types[col_name]

    new_cols = {col_name: {'name': col_name, 'columnType': get_col_type(
        col_name)} for col_name in new_data_df.columns}

    for col_name in new_cols:
        new_col = new_cols[col_name]
        actual_max_size = 0

        if new_col['columnType'].endswith('_LIST'):
            actual_max_list_len = 0
            for value in new_data_df[col_name].dropna():
                actual_max_list_len = max(actual_max_list_len, len(value))
                # Find longest string in this list
                if value:  # Check if list is not empty
                    item_lengths = [len(str(item)) for item in value]
                    max_item_in_this_list = max(
                        item_lengths) if item_lengths else 0
                    actual_max_size = max(
                        actual_max_size, max_item_in_this_list)
            if actual_max_list_len > default_maximumListLength:
                new_col['maximumListLength'] = int(actual_max_list_len)
        else:
            actual_max_size = new_data_df[col_name].astype(str).str.len().max()
            if new_col['columnType'] == 'STRING':
                if actual_max_size > 2000:
                    new_col['columnType'] = 'LARGETEXT'
                elif actual_max_size > 1000:
                    new_col['columnType'] = 'MEDIUMTEXT'
        new_col['maximumSize'] = int(actual_max_size)

    return [Column(**col) for col in new_cols.values()]


def analyze_and_update(files: List[str], all: bool = False, table_names: List[str] = False):
    """
    - Upload json files to Synapse
    - Requires one parameter (files, all, or table_names) to be provided
    - Paths will be checked against PATHS_TO_IDS

    :param files: List of file paths (relative or absolute)
    :param all: Boolean, whether to upload all files in PATHS_TO_IDS
    :param table_names: List of table names to upload
    """
    try:
        if all:
            files = list(PATHS_TO_IDS.keys())

        if table_names:
            files = [f"project/data/{table_name}.json" for table_name in files]

        for file in files:
            if file not in PATHS_TO_IDS:
                raise ValueError(f"File is not a valid table: {file}")

        if not files:
            raise ValueError(f"No files given")

        print("Signing in...")
        syn = initialize_synapse()

        for file in files:
            table_id = PATHS_TO_IDS.get(file)
            populate_table(syn, file, table_id)

    except Exception as e:
        print(f"An error occurred when trying to update synapse tables: {e}")
        sys.exit(1)


def cli():
    """Command line interface"""
    parser = ArgumentParser(
        description="Uploads registry tables to Synapse, analyzing data to create appropriate schema. "
                    f"Possible tables are {', '.join(TABLE_IDS.keys())}."
    )

    parser.add_argument('-a', '--all', action='store_true',
                        help='Upload all tables')

    parser.add_argument('-t', '--table-names', action='store_true', default=False,
                        help='Just provide table names. They will be converted to /project/data/<table-name>.json')

    parser.add_argument(
        'files', nargs='*', help='Files to upload. Should include path from root. Usually /project/data/')

    args = parser.parse_args()

    if not args.all and not args.files:
        parser.error(
            "Either --all flag must be provided or at least one file must be specified")

    if args.all and args.files:
        parser.error("No files expected if using -a/--all flag")

    analyze_and_update(**vars(args))


if __name__ == '__main__':
    cli()
