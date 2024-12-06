import csv
import json
import sys
from synapseclient import Synapse, Table
import os
import pandas as pd


# the paths detected as changes from the "Get changed files" job mapped to their corresponding synapse table ids
PATHS_TO_IDS = {
    "project/data/DataStandardOrTool.json": "syn63096833",
    "project/data/DataSubstrate.json": "syn63096834",
    "project/data/DataTopic.json": "syn63096835",
    "project/data/Organization.json": "syn63096836",
    "project/data/UseCase.json": "syn63096837",
}


def delete_table_rows(syn: Synapse, table_id: str) -> None:
    """Delete all the rows for a table, given its id
    :param syn: synapse client
    :param table_id: table id to delete rows for
    """
    print(f"Deleting rows from table {table_id}")
    results = syn.tableQuery(f"select * from {table_id}")
    syn.delete(results)
    print("Finished deleting rows")


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
    if isinstance(data, list):
        df = pd.DataFrame(data=data)
        print(f"Populating table for file: {update_file}")
        table = syn.store(Table(table_id, df))
        print("Finished populating table")
    else:
        print("Could not get list of data from json file")


def main():
    try:
        changed_files = sys.argv[1:]

        if not changed_files:
            print("No relevant files passed to the script.")
            return

        print("Creating synapse client...")
        syn = Synapse()
        auth_token = os.getenv("SYNAPSE_AUTH_TOKEN")
        if not auth_token:
            raise ValueError("SYNAPSE_AUTH_TOKEN environment variable is not set")
        print("Signing in...")
        syn.login(authToken=auth_token)

        for changed_file in changed_files:
            table_id = PATHS_TO_IDS.get(changed_file)
            print(f"Creating snapshot for table {changed_file}")
            syn.create_snapshot_version(table_id)
            delete_table_rows(syn, table_id)
            populate_table(syn, changed_file, table_id)

    except Exception as e:
        print(f"An error occurred when trying to update synapse tables: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
