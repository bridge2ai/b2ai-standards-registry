"""
Denormalize Synapse Tables into defined destination table(s) for Standards Registry Explorer UI use.

This script connects to Synapse, retrieves a set of normalized source tables,
joins them together according to a defined schema, and creates a new denormalized
Synapse table for use in the Explore landing page and detail views.

It supports:
- Mapping ID fields in the base table to human-readable values from related tables
- Allows columns to be flagged for faceting
- Allows column renaming -- use camelCase and Synapse will automatically convert to title case (ex; camelCase -> Camel Case)
- Allows transforming data values
- Automatically configuring string list and JSON columns
- Replacing missing values (NaNs) with empty strings (pandas converts empty non-numeric fields to NaN)
- Snapshotting and clearing destination tables before updates

Usage:
    Run this script directly (e.g., `python -m scripts.create_denormalized_tables`) to populate the DEST_TABLES output.
    Authentication is handled via a personal access token fetched from utils.py.
    It expects an auth token to be stored in ~/.synapseConfig. For instructions on setting up your auth token,
    see scripts/README.md.

Expected Environment:
    - AUTH_TOKEN will be retrieved by scripts.utils.get_auth_token()
      Instructions for setting up your auth token are documented in the README.
    - The SRC_TABLES and DEST_TABLES definitions must be updated with valid Synapse table IDs

Main entry point:
    denormalize_tables()
"""

from typing import Any, Dict, List
from synapseclient import Synapse, Column, Schema, Table
from synapseclient.core.exceptions import SynapseAuthenticationError, SynapseNoCredentialsError
import pandas as pd
import numpy as np
import re
from scripts.utils import get_auth_token

AUTH_TOKEN = get_auth_token()
PROJECT_ID='syn63096806'

# The synapse tables that hold source data
SRC_TABLES = {      # getting rid of version numbers for now
    'DataStandardOrTool': {        # convention in code, this abbreviation will be referred to as ..._tbl
                    #   ..._table will usually refer to some kind of table object
        'id': 'syn63096833', 'name': 'DataStandardOrTool',
    },
    'DataTopic': {
        'id': 'syn63096835', 'name': 'DataTopic',
    },
    'Organization': {
        'id': 'syn63096836', 'name': 'Organization',
    },
    #   Not currently using these, but leave here for the future
    # 'UseCase': { 'id': 'syn63096837', 'name': 'UseCase', },
    # 'DataSubstrate': { 'id': 'syn63096834', 'name': 'DataSubstrate', },
    # 'DataSet': {'id': 'syn66330217', 'name': 'DataSet', },
    # 'Challenges': {'id': 'syn65913973', 'name': 'Challenges', },
}

# The table used for the explore landing page and to provide data for the home and detailed pages
DEST_TABLES = {
    'DST_denormalized': {
        'dest_table_name': 'DST_denormalized',
        'base_table': 'DataStandardOrTool',
        'columns': [
            {'faceted': False, 'name': 'id',                        'alias': 'id'},
            {'faceted': False, 'name': 'name',                      'alias': 'acronym'},
            {'faceted': False, 'name': 'description',               'alias': 'name'},
            {'faceted': True,  'name': 'category',                  'alias': 'category', 'transform': 'camel_to_title_case'},
            {'faceted': False, 'name': 'purpose_detail',            'alias': 'description'},
            {'faceted': False, 'name': 'collection',                'alias': 'collections'},
            {'faceted': False, 'name': 'concerns_data_topic',       'alias': 'concerns_data_topic'},
            {'faceted': False, 'name': 'has_relevant_organization', 'alias': 'has_relevant_organization'},
            {'faceted': False, 'name': 'responsible_organization',  'alias': 'responsible_organization'},
            {'faceted': True,  'name': 'is_open',                   'alias': 'isOpen'},
            {'faceted': True,  'name': 'requires_registration',     'alias': 'registration'},
            {'faceted': False, 'name': 'url',                       'alias': 'URL'},
            {'faceted': False, 'name': 'formal_specification',      'alias': 'formalSpec'},
            {'faceted': False, 'name': 'publication',               'alias': 'publication'},
            {'faceted': False, 'name': 'has_training_resource',     'alias': 'trainingResources'},
            {'faceted': False, 'name': 'subclass_of',               'alias': 'subclassOf'},
            {'faceted': False, 'name': 'contribution_date',         'alias': 'contributionDate'},
            {'faceted': False, 'name': 'related_to',                'alias': 'relatedTo'},
        ],
        'join_columns': [
            {'join_tbl': 'DataTopic', 'join_type': 'left', 'from': 'concerns_data_topic', 'to': 'id',
             'dest_cols': [
                {'faceted': True, 'name': 'name', 'alias': 'topic'},
            ]},
            {'join_tbl': 'Organization', 'join_type': 'left', 'from': 'has_relevant_organization', 'to': 'id',
             'dest_cols': [
                 {'faceted': True,  'name': 'name', 'alias': 'relevantOrgNames'},
                 {'faceted': False, 'name': 'description', 'alias': 'relevantOrgDescriptions'},
             ]},
            {'join_tbl': 'Organization', 'join_type': 'left', 'from': 'responsible_organization', 'to': 'id',
             'dest_cols': [
                 {'faceted': False,  'name': 'name', 'alias': 'responsibleOrgAcronym'},
                 {'faceted': False,  'name': 'description', 'alias': 'responsibleOrgName'},
             ]},
        ],
    },
}

TRANSFORMS = {
    # camel_to_title_case
    #   removes 'B2AI_STANDARD:'
    #   inserts a space before any uppercase letter that follows a lowercase letter
    #   converts to title case
    #
    #   Converts category, strips prefix and outputs title case
    #       'B2AI_STANDARD:BiomedicalStandard' becomes 'Biomedical Standard'
    'camel_to_title_case': lambda s: re.sub(r'([a-z])([A-Z])', r'\1 \2', re.sub(r'^B2AI_STANDARD:','', s)).title(),
}

def denormalize_tables():
    syn = initialize_synapse()
    src_tables = {tbl: get_src_table(syn, tbl) for tbl in SRC_TABLES}

    for dest_table in DEST_TABLES.values():
        base_tbl_name = dest_table['base_table']
        base_df = src_tables[base_tbl_name]['df']

        if base_df.empty:
            print(f"Skipping '{dest_table['dest_table_name']}' — base table '{base_tbl_name}' has no data.")
            continue

        make_dest_table(syn, dest_table, src_tables)



def make_dest_table(syn: Synapse, dest_table: Dict[str, Any], src_tables: Dict[str, Dict[str, Any]]) -> None:
    """
    Create and upload a Synapse table by joining a base table with related tables.

    :param syn: Authenticated Synapse client used to query and store tables
    :param dest_table: Dictionary defining the destination table configuration. Includes:
        - 'base_table': str, name of the source table to use as the base
        - 'dest_table_name': str, name for the resulting Synapse table
        - 'columns': list of base columns to be used in the destination table
        - 'join_columns' (optional): list of join config dicts for enriching base data
    :param src_tables: Dictionary of available source tables. Each entry is keyed by table name
                       and contains:
        - 'df': pd.DataFrame of the table
        - 'name': Synapse table name
        - 'id': Synapse table ID
    """

    def build_base_columns() -> List[Dict[str, Any]]:
        """
        Extract base table columns and attach their data from the DataFrame.

        :return: List of column definition dictionaries with 'data' and 'col' keys
        """
        base_table_name = dest_table['base_table']
        base_df = src_tables[base_table_name]['df']
        columns = []

        for col_config in dest_table['columns']:
            col_def = make_col(dest_table, col_config, src_tables)
            if col_def:
                col_data = base_df[col_def['name']]
                if 'transform' in col_def:
                    col_data = col_data.apply(TRANSFORMS[col_def['transform']])
                col_def['data'] = col_data
                columns.append(col_def)

        return columns

    def build_join_columns() -> List[Dict[str, Any]]:
        """
        Extract and populate join columns from related tables based on join configuration.

        :return: List of column definitions from join tables
        """
        base_table_name = dest_table['base_table']
        base_df = src_tables[base_table_name]['df']
        join_columns = []

        for join_config in dest_table.get('join_columns', []):
            join_tbl = join_config['join_tbl']
            join_table = src_tables[join_tbl]
            join_df = join_table['df']

            join_config['join_table_name'] = join_table['name']
            join_config['join_table_id'] = join_table['id']

            from_col = join_config['from']
            to_col = join_config['to']

            for dest_col in join_config['dest_cols']:
                faceted = dest_col.get('faceted', False)

                if dest_col.get('fields'):
                    col_def = create_json_column(base_table_name, base_df, join_df, from_col, to_col, join_config, dest_col)
                else:
                    col_def = create_list_column(base_table_name, base_df, join_df, from_col, to_col, join_config, dest_col)

                if col_def:
                    col_def['faceted'] = faceted
                    join_columns.append(col_def)

        return join_columns

    def configure_column_metadata(columns: List[Dict[str, Any]], df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Set metadata on each column definition, including list sizes and faceting.

        :param columns: List of column definition dicts to update
        :param df: Final combined DataFrame, used to calculate sizes and lengths
        :return: Updated list of column definitions with metadata
        """
        for col_def in columns:
            col = col_def['col']
            # Remove the column id so new column gets created in Synapse schema - this is also so we can update the new max
            # list length and size
            col.pop('id', None)

            if col_def.get('faceted'):
                col['facetType'] = 'enumeration'

            if col['columnType'] == 'STRING_LIST':
                values = df[col['name']]
                max_items = max(len(items) for items in values)
                max_item_length = max(len(item) for items in values for item in items)

                # The 2 and 10 here are are buffers to try to accommodate for slightly more data than we may currently have
                # They're arbitrary right now, but we can always increase or decrease as needed if we run into issues later
                col['maximumListLength'] = max_items + 2
                col['maximumSize'] = max_item_length + 10

        return columns

    def create_or_clear_table(schema_name: str) -> None:
        """
        Delete all rows from a table if it already exists in Synapse. Takes a snapshot version for history.

        :param schema_name: Name of the Synapse table to check and clear (if it already exists)
        """
        try:
            existing_tables = syn.getChildren(PROJECT_ID, includeTypes=['table'])
            for table in existing_tables:
                if table['name'] == schema_name:
                    query_result = syn.tableQuery(f"SELECT * FROM {table['id']}")
                    syn.create_snapshot_version(table["id"])
                    print(f"Table '{schema_name}' already exists. Deleting {len(query_result)} rows.")
                    syn.delete(query_result)
                    break
        except Exception as e:
            print(f"Error checking for existing table: {e}")

    # Step 1: Build all columns and their data
    base_columns = build_base_columns()
    join_columns = build_join_columns()
    all_columns = base_columns + join_columns

    # Step 2: Construct the full data frame
    data_dict = {col['alias']: col['data'] for col in all_columns if 'data' in col}
    final_df = pd.DataFrame(data_dict).reset_index(drop=True)

    # Step 3: Configure column metadata
    configured_columns = configure_column_metadata(all_columns, final_df)

    # Step 4: Create Synapse schema
    schema_cols = [Column(**col_def['col']) for col_def in configured_columns]
    schema = Schema(
        name=dest_table['dest_table_name'],
        columns=schema_cols,
        parent=PROJECT_ID
    )

    # Step 5: Clear existing table rows if applicable
    create_or_clear_table(dest_table['dest_table_name'])

    # Step 6: Upload the table
    table = syn.store(Table(schema, final_df))
    print(f"Created table: {table.schema.name} ({table.tableId})")


def make_col(
    dest_table: Dict[str, Any],
    dest_col: Dict[str, Any],
    src_tables: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Construct a destination column definition based on the source table's column schema.

    This function looks up the source column metadata (from the base table), copies it,
    updates the name to the desired alias (destination column name), and returns the updated column definition
    to be included in the output schema.

    :param dest_table: Configuration for the destination table, including the base table name
    :param dest_col: Column definition with keys:
                     - 'name': name of the source column
                     - 'alias': desired column name in the destination table
                     - 'faceted': whether the column should be faceted
                     - 'transform': optional function for transforming data values
    :param src_tables: Dictionary of available source tables, keyed by name. Each value includes:
                       - 'columns': dict of column metadata definitions
    :return: Updated dest_col dict with a new 'col' key containing the modified column metadata
    """
    src_col_name = dest_col['name']
    dest_col_name = dest_col['alias']

    # Get the key to use in SRC_TABLES for the base table
    base_table_name = dest_table['base_table']
    src_table = src_tables[base_table_name]

    # Copy the column schema and update the name to use the alias
    dest_col['col'] = src_table['columns'][src_col_name].copy()
    dest_col['col']['name'] = dest_col_name

    return dest_col


def create_list_column(
    base_table_name: str,
    base_df: pd.DataFrame,
    join_df: pd.DataFrame,
    from_col: str,
    to_col: str,
    join_config: Dict[str, Any],
    dest_col: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a column containing lists of values from a join table, based on matching ID relationships.

    For each row in the base DataFrame, this function looks up related entries in the join table
    and extracts a list of values for a specified field (e.g., names or labels) that correspond
    to a column of IDs in the base table.

    Clarification: For columns like topic and relevant org, which, in the base table appear as string lists of topic or org ids,
    this function fetches data (e.g., name, acronym) from the topic or org table for inclusion in the
    destination table

    NOTE: This function is intended for use only with columns containing StringList or other List types.

    :param base_table_name: The base table name, for error message if needed
    :param base_df: The source base table DataFrame containing the rows to enrich (e.g., main entities)
    :param join_df: The join table DataFrame containing additional values (e.g., names for IDs)
    :param from_col: Column in base_df that contains one or more IDs (list or scalar) to match
    :param to_col: Column in join_df that should match the IDs from `from_col`
    :param join_config: Dictionary containing metadata about the join (e.g., join table name)
    :param dest_col: Dictionary defining the output column, with:
                     - 'name': the field in join_df to extract
                     - 'alias': the name to assign to the new output column
    :return: Dictionary with keys:
             - 'src': source join table name
             - 'name': name of the field used from the join table
             - 'alias': output column name
             - 'col': Synapse Column definition
             - 'data': list of lists with extracted values per row
    """
    field_name = dest_col['name']          # field in join_df to extract (e.g., 'name')
    column_name = dest_col['alias']        # name for the new output column
    result = []                            # list of lists to hold values for each base row

    for _, row in base_df.iterrows():
        related_ids = row[from_col]

        # Handle empty or missing relationships
        if not related_ids or (isinstance(related_ids, list) and len(related_ids) == 0):
            result.append([])
            continue

        # Fail unless related_ids is a list
        if not isinstance(related_ids, list):
            raise ValueError(f"Expected list column from '{base_table_name}.{from_col}', but got scalar.")
            # We could coerce it into a list (related_ids = [related_ids]), but it is not currently expected
            #   that the user would want to create a list column from a non-list column

        # Filter join_df for rows with matching IDs
        matching_rows = join_df[join_df[to_col].isin(related_ids)]

        # Extract the requested field values and store as list
        field_values = matching_rows[field_name].tolist()
        result.append(field_values)

    # Create column definition and data
    column_def = {
        'src': join_config['join_table_name'],
        'name': field_name,
        'alias': column_name,
        'col': Column(name=column_name, columnType='STRING_LIST'),
        'data': result
    }

    return column_def


def create_json_column(
    base_table_name: str,
    base_df: pd.DataFrame,
    join_df: pd.DataFrame,
    from_col: str,
    to_col: str,
    join_config: Dict[str, Any],
    dest_col: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a column containing structured JSON objects from related records in a join table.

    For each row in the base table, this function gathers related entries from the join table
    (based on matching IDs), extracts a subset of fields, and formats them as a list of
    dictionaries (JSON-like structure). This list is stored as the row's value in the output column.

    Expected configuration for destination table definition would look like the following:
        'join_columns': [
        {'join_tbl': 'DataTopic', 'join_type': 'left', 'from': 'concerns_data_topic', 'to': 'id',
         'dest_cols': [
              {'faceted': False,'name': 'topics_json', 'alias': 'Topics',
               'fields': [{ 'name': 'name', 'alias': 'Topic'},
                          { 'name': 'description', 'alias': 'Description'}, ]},
        ]},
    ]

    :param base_table_name: The base table name, for error message if needed
    :param base_df: The base DataFrame containing the primary records (e.g., DSTs)
    :param join_df: The join table DataFrame with additional data (e.g., topic metadata)
    :param from_col: Column name in base_df that contains one or more IDs (list or scalar)
    :param to_col: Column name in join_df to match against those IDs
    :param join_config: Dictionary describing the join (includes the join table name)
    :param dest_col: Dictionary defining the new column to be created, including:
                     - 'alias': name for the resulting column
                     - 'fields': list of dicts with field mappings (e.g., {'name': 'id', 'alias': 'topic_id'})
    :return: Dictionary containing metadata and data for the new column, including:
             - 'src': join table name
             - 'name': join table key
             - 'alias': output column name
             - 'col': Synapse Column definition (type JSON)
             - 'data': list of JSON-like structures (one per base row)
    """
    column_name = dest_col['alias']
    fields = dest_col['fields']
    result = []  # Will hold the output data: one JSON array per row in base_df

    for _, row in base_df.iterrows():
        related_ids = row[from_col]

        # Handle empty or missing values
        if not related_ids or (isinstance(related_ids, list) and len(related_ids) == 0):
            result.append([])
            continue

        # Fail unless related_ids is a list
        if not isinstance(related_ids, list):
            raise ValueError(f"Expected list column from '{base_table_name}.{from_col}', but got scalar.")
            # We could coerce it into a list (related_ids = [related_ids]), but it is not currently expected
            #   that the user would want to create a list column from a non-list column

        # Match related records in the join_df
        matching_rows = join_df[join_df[to_col].isin(related_ids)]

        # Build a list of JSON-style dicts for selected fields
        json_objects = []
        for _, related_row in matching_rows.iterrows():
            obj = {}
            for field in fields:
                field_name = field['name']
                field_alias = field.get('alias', field_name)
                obj[field_alias] = related_row[field_name]
            json_objects.append(obj)

        # Append the JSON structure (list of dicts) as this row's value
        result.append(json_objects)

    column_def: Dict[str, Any] = {
        'src': join_config['join_table_name'],
        'name': dest_col['name'],
        'alias': column_name,
        'col': Column(name=column_name, columnType='JSON'),
        'data': result
    }

    return column_def


def get_src_table(syn: Synapse, tbl: str) -> Dict[str, Any]:
    """
    Retrieve and validate a source table from Synapse, populate it with metadata and a cleaned DataFrame.

    This function:
    - Retrieves the Synapse table and confirms its name matches the expected one
    - Extracts column metadata
    - Queries the full table contents into a DataFrame
    - Cleans NaNs from the DataFrame (replacing them with empty strings)
    - Stores the DataFrame, table object, and column info in the returned dictionary

    :param syn: Authenticated Synapse client
    :param tbl: Key for the source table in the global SRC_TABLES dictionary
    :return: Dictionary with keys:
             - 'id': Synapse table ID
             - 'name': expected name of the table
             - 'syn_table': the retrieved Synapse table object
             - 'columns': dict of Synapse column metadata keyed by column name
             - 'df': cleaned DataFrame of table contents
    :raises ValueError: if the retrieved Synapse table has a different name than expected
    """
    table_info = SRC_TABLES[tbl]  # global lookup
    syn_table = syn.get(table_info['id'])

    # Confirm table name matches what's expected
    if syn_table.name != table_info['name']:
        raise ValueError(f"Expected table '{table_info['name']}', but got '{syn_table.name}'.")

    # Store the retrieved Synapse table and column metadata
    table_info['syn_table'] = syn_table
    table_info['columns'] = {
        col['name']: col for col in syn.getTableColumns(syn_table)
    }

    # Query the table and clean up the resulting DataFrame
    query_result = syn.tableQuery(f"SELECT * FROM {table_info['id']}")
    df = query_result.asDataFrame()

    # Replace NaNs with empty strings for all non-numeric columns (since df converts null columns to NaNs)
    for col in df.columns:
        df[col] = df[col].apply(lambda x: '' if isinstance(x, float) and np.isnan(x) else x)

    table_info['df'] = df
    return table_info

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

if __name__ == "__main__":
    denormalize_tables()
