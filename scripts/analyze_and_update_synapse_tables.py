import json
import sys
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
    return path.split('/')[-1].split('.')[0]

TABLE_IDS = {file_path_to_table_name(p): PATHS_TO_IDS[p] for p in PATHS_TO_IDS.keys()}

def populate_table(syn: Synapse, update_file: str, table_id: str) -> None:
    """Populate the table with updated data
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

    cols = get_col_defs(df)
    coldefs = [Column(**col) for col in cols.values()]

    table_name = file_path_to_table_name(update_file)

    # moved this from main() so we don't delete rows till the last minute
    # replacing this with snapshotting new version
    # print(f"Creating snapshot and clearing table {update_file}")
    # create_or_clear_table(syn, table_name)

    clear_populate_snapshot_table(syn, table_name, coldefs, df, table_id)

    schema = Schema(name=table_name, columns=coldefs, parent=PROJECT_ID)
    table = Table(name=table_name, parent_id=PROJECT_ID, schema=schema, values=df)
    table.tableId = table_id

    print(f"Clearing, populating, and snapshotting table for file: {update_file}")
    table = syn.store(table)
    print("Finished populating table")


# synapse defaults
default_maximumSize = 50    # ignoring this because some tables will be too big if defaulting to it
                            #   instead, make maximumSize just big enough to fit the longest column value
default_maximumListLength = 100

def get_col_defs(new_data_df):
    is_list_cols = (new_data_df.map(type).astype(str) == "<class 'list'>").any()
    list_cols = set(is_list_cols[is_list_cols == True].index)
    scalar_types = {c: infer_dtype(new_data_df[c], skipna=True).upper() for c in new_data_df.columns} # infer_dtype gives 'mixed' for list types
    # assuming all list columns are string lists, at least for now
    get_col_type = lambda col_name: 'STRING_LIST' if col_name in list_cols else scalar_types[col_name]

    new_cols = {col_name: {'name': col_name, 'columnType': get_col_type(col_name)} for col_name in new_data_df.columns}


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
                    max_item_in_this_list = max(item_lengths) if item_lengths else 0
                    actual_max_size = max(actual_max_size, max_item_in_this_list)
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
    return new_cols


def analyze_and_update(files, all=False, table_names=False):
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
        description='Uploads registry tables to Synapse, analyzing data to create appropriate schema. '
                    f'Possible tables are {', '.join(TABLE_IDS.keys())}.'
    )

    parser.add_argument('-a', '--all', action='store_true', help='Upload all tables')

    parser.add_argument('-t', '--table-names', action='store_true', default=False,
                        help='Just provide table names. They will be converted to /project/data/<table-name>.json')

    parser.add_argument('files', nargs='*', help='Files to upload. Should include path from root. Usually /project/data/')

    args = parser.parse_args()

    if not args.all and not args.files:
        parser.error("Either --all flag must be provided or at least one file must be specified")

    if args.all and args.files:
        parser.error("No files expected if using -a/--all flag")

    analyze_and_update(**vars(args))


if __name__ == '__main__':
    cli()
