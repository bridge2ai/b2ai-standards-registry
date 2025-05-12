import os

from synapseclient import Synapse
from synapseclient.core.exceptions import SynapseAuthenticationError, SynapseNoCredentialsError


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


def get_df_max_lengths(original_cols, df):
    """
    Get the maximum length of each column in a pandas DataFrame.
    For columns with lists of strings, finds the length of the longest string in any list.
    """
    max_lengths = {}
    # synapse defaults
    default_maximumSize = 50
    default_maximumListLength = 100

    orig_cols = {c['name']: c for c in original_cols}

    for column in df.columns:
        # for both maximumSize and maximumListLength, take the value from the original column if specified
        #   otherwise, the synapse default; except if the data max value is bigger, then use that
        orig_col = orig_cols[column]
        # Check if the column potentially contains lists
        contains_lists = False
        maximumSize = orig_col.get('maximumSize', default_maximumSize) # override if data is bigger

        # Check if this column contains lists with strings
        for value in df[column].dropna():
            if isinstance(value, list):
                contains_lists = True
                maximumListLength = orig_col.get('maximumListLength', default_maximumListLength)
                maximumListLength = max(maximumListLength, len(value))
                # Find longest string in this list
                if value:  # Check if list is not empty
                    item_lengths = [len(str(item)) for item in value]
                    max_item_in_this_list = max(item_lengths) if item_lengths else 0
                    maximumSize = max(maximumSize, max_item_in_this_list)

        # Store results
        if contains_lists:
            max_lengths[column] = {
                'maximumSize': maximumSize,
                'maximumListLength': maximumListLength,
            }
        else:
            maximumSize = max(maximumSize, df[column].astype(str).str.len().max())
            max_lengths[column] = maximumSize

    return max_lengths

def copy_list_omit_property(list_of_dicts, property_to_omit):
    return [{key: value for key, value in d.items() if key != property_to_omit}
            for d in list_of_dicts]


AUTH_TOKEN = get_auth_token()
PROJECT_ID='syn63096806'


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
