"""
Build the registry's source tables (one per project/data/*.json file) for
upload to Synapse, inferring each table's Synapse schema from its data.

Manifest.json isn't uploaded as-is; denormalized_manifest builds the Manifest
table from it.
"""
import json
import os
from typing import List, Tuple

import pandas as pd
from synapseclient.models import Column, ColumnType

from scripts.publishing.utils import DATA_PATH, configure_column_from_data, infer_column_type

# Uploaded as-is to the Synapse table of the same name (ids in generate_tables_config.TABLE_IDS)
SOURCE_TABLES = ['DataStandardOrTool', 'DataSubstrate', 'DataTopic', 'Organization', 'UseCase', 'DataSet']

DATATYPE_OVERRRIDES = {
    # maybe will only work for JSON cols, which is fine for now
    'DataStandardOrTool': {
        'has_application': ColumnType.JSON
    },
}


def build_source_table(table_name: str) -> Tuple[List[Column], pd.DataFrame]:
    """
    Load project/data/<table_name>.json and infer its Synapse schema.

    :param table_name: Name of the source table (and of its json file)
    :return: (column definitions, DataFrame)
    :raises ValueError: if the file has no list of records
    """
    with open(os.path.join(DATA_PATH, f"{table_name}.json"), "r") as file:
        data = json.load(file)
    # each json file begins with a key that maps to the list of records, so we're accessing that list here
    data = next(iter(data.values()), [])

    if not isinstance(data, list):
        raise ValueError(f"No list of records in {table_name}.json")

    df = pd.DataFrame(data=data)
    return get_col_defs(df, table_name), df


def get_col_defs(new_data_df: pd.DataFrame, table_name: str) -> List[Column]:
    """
    Returns Column definitions for Synapse schema based on data in df.

    :param new_data_df: DataFrame with new data
    :param table_name: Name of table (used for datatype overrides)
    :return: Column definitions
    """
    coldefs = []
    for col_name in new_data_df.columns:
        # Check for datatype override first
        overridden = DATATYPE_OVERRRIDES.get(table_name, {}).get(col_name)
        if overridden is not None:
            col_type = overridden
        else:
            col_type = infer_column_type(new_data_df[col_name])

        col = Column(name=col_name, column_type=col_type)
        col = configure_column_from_data(col, new_data_df[col_name])
        coldefs.append(col)

    return coldefs
