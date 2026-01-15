import os
import pickle
from synapseclient import Synapse
from synapseclient.models import Column, ColumnType, FacetType, Table
from synapseclient.core.exceptions import SynapseAuthenticationError, SynapseNoCredentialsError

PROJECT_ID = 'syn63096806'
table_name = 'DST_denormalized'
table_id = 'syn65676531'

def replicate_error():
    with open('dst_denormalized_df.pickle', 'rb') as f:
        df = pickle.load(f)

    with open('columnDefs.pickle', 'rb') as f:
        columnDefs = pickle.load(f)

    table = Table(name=table_name, parent_id=PROJECT_ID, columns=columnDefs)
    if table_id:
        table.id = table_id
    table = table.store()
    table.store_rows(values=df)

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

    token = os.getenv('SYNAPSE_AUTH_TOKEN') or os.getenv(
        'AUTH_TOKEN') or os.getenv('auth_token')
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
                        raise ValueError(
                            "The 'authtoken' line is malformed or empty.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Authentication file not found: {auth_file}")
    except Exception as e:
        raise RuntimeError(
            f"An error occurred while reading the auth file: {e}")

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


if __name__ == "__main__":
    initialize_synapse()
    replicate_error()
