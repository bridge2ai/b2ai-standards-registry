import os
from typing import Any, Dict, List, Optional
import pandas as pd
from synapseclient import Synapse, Table, Schema, Column
from synapseclient.core.exceptions import SynapseAuthenticationError, SynapseNoCredentialsError
"""
Expected Environment:
    - AUTH_TOKEN will be retrieved by scripts.utils.get_auth_token()
      Instructions for setting up your auth token are documented in the README.
"""
PROJECT_ID='syn63096806'

def get_auth_token():
    """
    Retrieves the Synapse authentication token from the user's ~/.synapseConfig file.

    Some tests have started failing during GitHub actions. Going to try looking for token
    in evironment variables as well.

    The config file must contain an authentication token. See the README for information on how to set this up.

    :return: The authentication token found in the config tile.
    :raises:
        FileNotFoundError: If the ~/.synapseConfig file does not exist
        ValueError: If the 'authtoken' line is missing, malformed, or empty
        RuntimeError: If an unexpected error occurs while reading the file.
    """

    token = os.getenv('SYNAPSE_AUTH_TOKEN') or os.getenv('AUTH_TOKEN') or os.getenv('auth_token')
    if token:
        return token

    auth_file = os.path.expanduser("~/.synapseConfig")

    try:
        with open(auth_file, "r") as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line.startswith("authtoken"):
                    key, value = map(str.strip, stripped_line.split("=", 1))
                    if key == "authtoken" and value:
                        return value
                    else:
                        raise ValueError("The 'authtoken' line is malformed or empty.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Authentication file not found: {auth_file}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the auth file: {e}")

    raise ValueError(f"'authtoken' not found in {auth_file}")

def initialize_synapse() -> Synapse:
    """
    Initialize the Synapse client
    :return: A logged-in Synapse client object
    """
    try:
        syn = Synapse()
        syn.login(authToken=get_auth_token())
        return syn
    except (SynapseAuthenticationError, SynapseNoCredentialsError) as e:
        raise Exception(f"Failed to authenticate with Synapse: {str(e)}")

def copy_list_omit_property(list_of_dicts, property_to_omit):
    return [{key: value for key, value in d.items() if key != property_to_omit}
            for d in list_of_dicts]

def clear_populate_snapshot_table(syn: Synapse, table_name: str, columnDefs: List[Column], df: pd.DataFrame, table_id: Optional[str] = None) -> None:
    """
    - Update or create Synapse table and create snapshot.
    - Delete all rows if table already exists in Synapse.
    - Upload new data.
    - Take a snapshot version for history.

    :param syn: Authenticated Synapse client
    :param table_name: Name of the Synapse table to upload
    :param columnDefs: List of Column definitions to upload
    :param df: Dataframe to upload
    :param table_id: Optionally, Table ID, function will confirm or figure it out if not provided
    """
    print(f"Clearing, populating, and snapshotting {table_name} table")

    try:
        existing_tables = syn.getChildren(PROJECT_ID, includeTypes=['table'])
        for table in existing_tables:
            if table['name'] == table_name:
                if table_id:
                    if table['id'] != table_id:
                        raise Exception(f"got table_id mismatch for {table_name}: {table['id']} != {table_id}")
                else:
                    table_id = table['id']
                query_result = syn.tableQuery(f"SELECT * FROM {table_id}")
                print(f"Table '{table_name}' already exists. Deleting {len(query_result)} rows.")
                syn.delete(query_result)
                break
    except Exception as e:
        print(f"Error checking for and clearing existing table {table_name}: {e}")

    schema = Schema(name=table_name, columns=columnDefs, parent=PROJECT_ID)
    table = Table(name=table_name, parent_id=PROJECT_ID, schema=schema, values=df)
    table.tableId = table_id
    table = syn.store(table)
    table_id = table_id or table['id']
    syn.create_snapshot_version(table_id)
    print(f"Created table: {table.schema.name} ({table.tableId})")
