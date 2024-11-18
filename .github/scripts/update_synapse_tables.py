import csv
import sys
from synapseclient import Synapse, Table
import os


# the paths detected as changes from the "Get changed files" job mapped to their corresponding synapse table ids
PATHS_TO_IDS = {
    "project/data/DataStandardOrTool.tsv": "syn63096833",
    "project/data/DataSubstrate.tsv": "syn63096834",
    "project/data/DataTopic.tsv": "syn63096835",
    "project/data/Organization.tsv": "syn63096836",
    "project/data/UseCase.tsv": "syn63096837",
}


def delete_table_rows(syn: Synapse, table_id: str) -> None:
    """Delete all the rows for a table, given its id
    :param syn: synapse client
    :param table_id: table id to delete rows for
    """
    print("Deleting rows from table {table_id}")
    results = syn.tableQuery(f"select * from {table_id}")
    syn.delete(results)
    print("Finished deleting rows")


def get_rows_from_tsv(file_path: str):
    """Read a TSV file and return a list of lists, where each inner list represents a row.
    NOTE: The first row of the file is expected to be the headers, which is skipped
    :param file_path: path to tsv file
    :return: list of lists representing rows of the tsv file"""
    rows = []
    with open(file_path, mode="r", newline="", encoding="utf-8") as tsv_file:
        reader = csv.reader(tsv_file, delimiter="\t")
        # Skip the header row
        next(reader)
        for row in reader:
            rows.append(row)
    return rows


def populate_table(syn: Synapse, update_file: str, table_id: str) -> None:
    """Populate the table with updated data
    :param syn: synapse client
    :param update_file: path for tsv file containing data to populate the table
    :param table_id: synapse id for table to populate
    """
    rows_to_add = get_rows_from_tsv(update_file)
    print(f"Populating table for file: {update_file}")
    table = syn.store(Table(table_id, rows_to_add))
    print("Finished populating table")


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
