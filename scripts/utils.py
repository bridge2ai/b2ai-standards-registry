import json
import os
from dataclasses import replace
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from synapseclient import Synapse
from synapseclient.models import Column, ColumnType, FacetType, Table
from synapseclient.core.exceptions import SynapseAuthenticationError, SynapseNoCredentialsError
import csv
import sys
"""
Expected Environment:
    - AUTH_TOKEN will be retrieved by scripts.utils.get_auth_token()
      Instructions for setting up your auth token are documented in the README.
"""
PROJECT_ID = 'syn63096806'

# Base path for JSON data files
DATA_PATH = 'project/data'


def load_json_to_dataframe(table_name: str) -> pd.DataFrame:
    """
    Load a JSON data file into a pandas DataFrame.

    :param table_name: Name of the table (e.g., 'DataStandardOrTool')
    :return: DataFrame with the table data, NaNs replaced with empty strings for non-numeric columns
    """
    file_path = os.path.join(DATA_PATH, f"{table_name}.json")

    with open(file_path, "r") as file:
        data = json.load(file)

    # Each JSON file begins with a key that maps to the list of records
    data = next(iter(data.values()), [])

    if not isinstance(data, list):
        raise ValueError(f"Could not get list of data from {file_path}")

    df = pd.DataFrame(data=data)

    # Replace NaNs with empty strings for all non-numeric columns
    for col in df.columns:
        df[col] = df[col].apply(lambda x: '' if isinstance(x, float) and np.isnan(x) else x)

    return df

SYNAPSE_MIN_LIST_SIZE = 2


def infer_column_type(values: pd.Series) -> ColumnType:
    """
    Infer Synapse column type from a pandas Series.
    Handles NaN values and empty strings by inferring from non-null/non-empty values only.
    """
    # Filter out NaN, None, and empty strings for type inference
    non_null = values.dropna()
    non_empty = non_null[non_null.apply(lambda x: x != '')]

    if len(non_empty) == 0:
        return ColumnType.STRING

    # Check types of non-empty values
    types = non_empty.map(type).unique()

    if len(types) == 1:
        t = types[0]
        if t == bool:
            return ColumnType.BOOLEAN
        elif t == int:
            return ColumnType.INTEGER
        elif t == float:
            return ColumnType.DOUBLE
        elif t == list:
            return ColumnType.STRING_LIST
        else:
            return ColumnType.STRING
    else:
        return ColumnType.STRING


def configure_column_from_data(col: Column, values: pd.Series, faceted: bool = False) -> Column:
    """
    Configure a Column's metadata (sizes, faceting) based on actual data values.

    This handles STRING, STRING_LIST, INTEGER_LIST column types by calculating
    appropriate maximum_size and maximum_list_length values from the data.

    :param col: Column object to configure
    :param values: pandas Series containing the column's data
    :param faceted: Whether this column should be faceted
    :return: New Column object with updated metadata
    """
    col = replace(col, id=None)

    if faceted:
        col = replace(col, facet_type=FacetType.ENUMERATION)

    if col.column_type == ColumnType.STRING_LIST:
        list_values = [v for v in values if isinstance(v, list)]
        if list_values:
            max_item_length = max((max(len(item), 20) for items in list_values for item in items), default=20)
            max_items = max(len(items) for items in list_values)
        else:
            max_item_length = 20
            max_items = SYNAPSE_MIN_LIST_SIZE
        col = replace(col, maximum_list_length=max(max_items, SYNAPSE_MIN_LIST_SIZE), maximum_size=max_item_length)
    elif col.column_type == ColumnType.INTEGER_LIST:
        list_values = [v for v in values if isinstance(v, list)]
        max_items = max((len(items) for items in list_values), default=SYNAPSE_MIN_LIST_SIZE)
        col = replace(col, maximum_list_length=max(max_items, SYNAPSE_MIN_LIST_SIZE))
    elif col.column_type == ColumnType.STRING:
        max_size = int(values.astype(str).str.len().max())
        if max_size > 2000:
            col = replace(col, column_type=ColumnType.LARGETEXT)
        elif max_size > 1000:
            col = replace(col, column_type=ColumnType.MEDIUMTEXT, maximum_size=max_size)
        else:
            col = replace(col, maximum_size=max(max_size, 1))

    return col


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

    csv.field_size_limit(sys.maxsize)

    # Resolve table_id if not provided
    if not table_id:
        for existing_table in syn.getChildren(PROJECT_ID, includeTypes=['table']):
            if existing_table['name'] == table_name:
                table_id = existing_table['id']
                break

    if table_id:
        # Delete all rows first (using only ROW_ID/ROW_VERSION to avoid
        # SELECT * failures when column types have changed)
        print(f"  Deleting rows from {table_name}...")
        Table(id=table_id).delete_rows(query=f"SELECT ROW_ID, ROW_VERSION FROM {table_id}")

        # Delete all existing columns so the new schema starts clean.
        # Table.store() adds columns but doesn't remove old ones and can't
        # change column types in place.
        existing_table = Table(id=table_id).get(include_columns=True)
        for existing_col in list(existing_table.columns.values()):
            existing_table.delete_column(name=existing_col.name)
        existing_table.store()
        print(f"  Cleared rows and columns from {table_name}")

    table = Table(name=table_name, parent_id=PROJECT_ID, columns=columnDefs)
    if table_id:
        table.id = table_id
    table = table.store()

    # Synapse JSON columns need JSON strings. Replace \" with \u0022 to avoid
    # ambiguity with CSV quote-doubling during upload (\" becomes \"" in CSV,
    # which Synapse's server-side CSV parser can misinterpret).
    for col in columnDefs:
        if col.column_type == ColumnType.JSON and col.name in df.columns:
            df[col.name] = df[col.name].apply(
                lambda v: json.dumps(v).replace('\\"', '\\u0022') if isinstance(v, (list, dict)) else '[]'
            )

    table.store_rows(values=df)
    table_id = table_id or table.id
    if not table_id:
        raise Exception(f"Couldn't find table_id for {table_name}")
    try:
        syn.create_snapshot_version(table_id)
    except Exception as e:
        print(f"Error creating new version of table {table_name}: {e}\nRetrying...")
        table_id = table_id.split('.')[0]
    print(f"Created table: {table.name} ({table.id})")
