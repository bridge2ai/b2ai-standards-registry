import os
from synapseclient import Synapse
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

    The config file must contain an authentication token. See the README for information on how to set this up.

    :return: The authentication token found in the config tile.
    :raises:
        FileNotFoundError: If the ~/.synapseConfig file does not exist
        ValueError: If the 'authtoken' line is missing, malformed, or empty
        RuntimeError: If an unexpected error occurs while reading the file.
    """
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

AUTH_TOKEN = get_auth_token()

def initialize_synapse() -> None:
    """
    Initialize the synapse client
    """
    try:
        syn = Synapse()
        syn.login(authToken=AUTH_TOKEN)
        return syn
    except (SynapseAuthenticationError, SynapseNoCredentialsError) as e:
        raise Exception(f"Failed to authenticate with Synapse: {str(e)}")

def copy_list_omit_property(list_of_dicts, property_to_omit):
    return [{key: value for key, value in d.items() if key != property_to_omit}
            for d in list_of_dicts]

def create_or_clear_table(syn: Synapse, table_name: str) -> None:
    """
    Delete all rows from a table if it already exists in Synapse. Takes a snapshot version for history.

    :param syn: Authenticated Synapse client
    :param table_name: Name of the Synapse table to check and clear (if it already exists)
    """
    try:
        existing_tables = syn.getChildren(PROJECT_ID, includeTypes=['table'])
        for table in existing_tables:
            if table['name'] == table_name:
                query_result = syn.tableQuery(f"SELECT * FROM {table['id']}")
                syn.create_snapshot_version(table["id"])
                print(f"Table '{table_name}' already exists. Deleting {len(query_result)} rows.")
                syn.delete(query_result)
                break
    except Exception as e:
        print(f"Error checking for existing table: {e}")
