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
- Transforming values between source and destination tables

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
import sys
from typing import Any, Dict, List, Optional
from synapseclient import Synapse, Column
import pandas as pd
import numpy as np
import re
import json

from scripts.generate_tables_config import DEST_TABLES, TABLE_IDS
from scripts.utils import PROJECT_ID, clear_populate_snapshot_table, initialize_synapse

special_capitalization = {
    'has_ai_application': 'Has AI Application',
    'obofoundry': 'OBO Foundry',
}
manual_title_case_mappings = {
    'scrnaseqanalysis': 'scrna_seq_analysis',
    'machinelearningframework': 'machine_learning_framework',
    'datavisualization': 'data_visualization',
    'notebookplatform': 'notebook_platform',
    'audiovisual': 'audio_visual',
    'ontologyregistry': 'ontology_registry',
    'proteindata': 'protein_data',
    'codesystem': 'code_system',
    'cloudplatform': 'cloud_platform',
    'cloudservice': 'cloud_service',
    'speechdata': 'speech_data',
    'modelcards': 'model_cards',
    'eyedata': 'eye_data',
    'standardsregistry': 'standards_registry',
    'diagnosticinstrument': 'diagnostic_instrument',
    'markuplanguage': 'markup_language',
    'datamodel': 'data_model',
    'workflowlanguage': 'workflow_language',
    'referencegenome': 'reference_genome',
    'minimuminformationschema': 'minimum_information_schema',
    'clinicaldata': 'clinical_data',
    'drugdata': 'drug_data',
    'softwareregistry': 'software_registry',
    'dataregistry': 'data_registry',
    'graphdataplatform': 'graph_data_platform',
    'fileformat': 'file_format',
}
lowercase_words = {'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'in', 'nor', 'of', 'on', 'or', 'so', 'the', 'to', 'up', 'yet'}

def category_to_title_case(text: str) -> str:
    """
    Categories look like 'B2AI_STANDARD:BiomedicalStandard' or 'B2AI_STANDARD:DataStandardOrTool'.
    This removes the part before the colon and converts to title case.
    'B2AI_STANDARD:DataStandardOrTool' becomes 'Data Standard or Tool'
    """
    text = re.sub(r'^B2AI_[A-Z]+:', '', text)

    # Split on capital letters, but keep consecutive capitals together
    words = re.findall(r'[A-Z]+(?=[A-Z][a-z]|\b)|[A-Z][a-z]*|\d+', text)

    result_words = []
    for i, word in enumerate(words):
        word_lower = word.lower()
        if i == 0 or word_lower not in lowercase_words:
            result_words.append(word.capitalize())
        else:
            result_words.append(word_lower)

    return ' '.join(result_words)

def collections_to_title_case(lst: list[str]) -> str:
    return [collection_to_title_case(s) for s in lst]


def collection_to_title_case(s: str) -> str:
    if s in special_capitalization:
        return special_capitalization[s]
    s = manual_title_case_mappings.get(s, s)
    return snake_to_title_case(s)

def snake_to_title_case(s: str) -> str:
    words = [w.capitalize() if w not in lowercase_words else w for w in s.split('_')]
    words[0] = words[0].capitalize()
    words[-1] = words[-1].capitalize()
    return ' '.join(words)


def get_transform_function(transform_spec):
    """
    Get a transform function from either a string identifier or a callable.

    :param transform_spec: Either a string identifier for predefined transforms
                          or a callable function
    :return: Transform function
    """
    if callable(transform_spec):
        return transform_spec

    # Predefined transform functions
    predefined_transforms = {
        'category_to_title_case': category_to_title_case,
        'collections_to_title_case': collections_to_title_case,
        'bool_to_yes_no': lambda b: 'Yes' if b else 'No',
        'collections_to_has_ai_app': lambda col: 'Yes' if 'has_ai_application' in col else 'No',
        'collections_to_is_mature': lambda col: 'Is Mature' if 'standards_process_maturity_final' in col or 'implementation_maturity_production' in col else 'Is Not Mature',

        'create_org_link': lambda id_val, name_val: f"[{name_val}](/Explore/Organization/OrganizationDetailsPage?id={id_val})",
        'create_topic_link': lambda id_val, name_val: f"[{name_val}](/Explore/DataTopic/DataTopicDetailsPage?id={id_val})",
        'create_substrate_link': lambda id_val, name_val: f"[{name_val}](/Explore/DataSubstrate/DataSubstrateDetailsPage?id={id_val})",
    }

    if transform_spec in predefined_transforms:
        return predefined_transforms[transform_spec]

    raise ValueError(f"Unknown transform: {transform_spec}")

def col_transform(col: pd.Series, transform_name: str, df: pd.DataFrame) -> pd.Series:
    """
    All transforms now passing through this function for further special handling
    """
    transform = get_transform_function(transform_name) # purposely set to raise error if transform_name is wrong
    col_data = col.apply(transform)
    return col_data

def denormalize_tables(specific_tables: Optional[List[str]] = None) -> None:
    """
    Create and upload tables from definitions in ./generate_tables_config.py

    :param specific_tables: Optional list of tables to create; defaults to creating all
    """
    syn = initialize_synapse()
    src_tables = {}

    if specific_tables:
        dest_table_defs = [DEST_TABLES[t] for t in specific_tables]
    else:
        dest_table_defs = DEST_TABLES.values()

    for dest_table in dest_table_defs:
        base_tbl_name = dest_table['base_table']
        base_table_info = get_src_table(syn, TABLE_IDS[base_tbl_name])
        base_df = base_table_info['df']
        if base_df.empty:
            print(f"Skipping '{dest_table['dest_table_name']}' — base table '{base_tbl_name}' has no data.")
            continue

        # SRC_TABLE_NAMES is all source tables, src_table_names is just the ones for this dest table
        src_table_names = set([base_tbl_name] + [j['join_tbl'] for j in dest_table['join_columns']])
        for table_name in src_table_names:
            table_info = TABLE_IDS[table_name]
            table_info = get_src_table(syn, table_info)
            src_tables[table_name] = table_info

        make_dest_table(syn, dest_table, src_tables)


def make_dest_table(syn: Synapse, dest_table: Dict[str, Any], src_tables: Dict[str, Dict[str, Any]]) -> None:
    """
    Create and upload a Synapse table by joining a base table with related tables.

    TODO: If this ever needs to be refactored, it would be better to get source column information from
          registry json files (see ./analyze_and_update_synapse_tables.py) rather than from downloading
          and extracting schema info from Synapse versions of those tables.

    :param syn: Authenticated Synapse client used to query and store tables
    :param dest_table: Dictionary defining the destination table configuration. Includes:
        - 'base_table': str, name of the source table to use as the base
        - 'dest_table_name': str, name for the resulting Synapse table
        - 'columns': list of base columns to be used in the destination table. Includes:
            - 'faceted': boolean whether destination column should be faceted
            - 'name': source column name
            - 'alias': destination column name
            - 'transform': key for function in TRANSFORMS dict above
            ' 'columnType': destination column type; defaults to source column type, but transform could change it
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
                    col_data = col_transform(col_data, col_def['transform'], base_df)
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

        # TODO: Clean up all these nearly-same var names
        for join_config in dest_table.get('join_columns', []):
            join_tbl = join_config['join_tbl']
            join_table = src_tables[join_tbl]
            join_df = join_table['df']

            join_config['join_table_name'] = join_table['name']
            join_config['join_table_id'] = join_table['id']

            base_tbl_col = join_config['base_tbl_col']
            join_tbl_col = join_config['join_tbl_col']

            for dest_col in join_config['dest_cols']:
                faceted = dest_col.get('faceted', False)

                col_def = create_join_column(base_table_name, base_df, join_df, base_tbl_col, join_tbl_col, join_config, dest_col)

                if col_def:
                    col_def['faceted'] = faceted
                    join_columns.append(col_def)

        return join_columns

    def configure_column_metadata(columns: List[Dict[str, Any]], df: pd.DataFrame) -> List[Column]:
        """
        Set metadata on each column definition, including list sizes and faceting.
        TODO: If ever refactoring, this could be combined into a shared function with
              ./analyze_and_update_synapse_tables.py:get_col_defs

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
                col['maximumListLength'] = max(max_items, 2) # 2 is minimum allowed
                col['maximumSize'] = max_item_length
            elif col['columnType'] == 'INTEGER_LIST':
                values = df[col['name']]
                max_items = max(len(items) for items in values)
                col['maximumListLength'] = max(max_items, 2) # 2 is minimum allowed

        return [Column(**col_def['col']) for col_def in columns]

    # Step 1: Build all columns and their data
    base_columns = build_base_columns()
    join_columns = build_join_columns()
    all_columns = base_columns + join_columns

    # Step 2: Construct the full data frame
    data_dict = {col['alias']: col['data'] for col in all_columns if 'data' in col}
    final_df = pd.DataFrame(data_dict).reset_index(drop=True)

    # Step 3: Configure column metadata
    schema_cols = configure_column_metadata(all_columns, final_df)

    # Step 4: Clear, populate, snapshot dest table
    table_name = dest_table['dest_table_name']
    table_id = TABLE_IDS[table_name]['id'] if table_name in TABLE_IDS else None
    clear_populate_snapshot_table(syn, table_name, schema_cols, final_df, table_id)


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
    col = dest_col['col']
    col['name'] = dest_col_name

    if 'columnType' in dest_col:
        ctype = dest_col['columnType']
        col['columnType'] = ctype
        if not ctype.endswith('LIST') and 'maximumListLength' in col:
            del col['maximumListLength']

    return dest_col


def create_join_column(
  base_table_name: str,
  base_df: pd.DataFrame,
  join_df: pd.DataFrame,
  base_tbl_col: str,
  join_tbl_col: str,
  join_config: Dict[str, Any],
  dest_col: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a column containing lists of values or JSON objects from a join table.

    Supports:
    - Normal/reverse lookups (configured at join_config level)
    - Single/multi-field extraction
    - Optional transforms
    - JSON object creation

    TODO: update old docstring:
    For each row in the base DataFrame, this function looks up related entries in the join table
    and extracts a list of values for a specified field (e.g., names or labels) that correspond
    to a column of IDs in the base table.

    Clarification: For columns like topic and relevant org, which, in the base table appear as string lists of topic or org ids,
    this function fetches data (e.g., name, acronym) from the topic or org table for inclusion in the
    destination table

    :param base_table_name: The base table name, for error message if needed
    :param base_df: The source base table DataFrame containing the rows to enrich (e.g., main entities)
    :param join_df: The join table DataFrame containing additional values (e.g., names for IDs)
    :param base_tbl_col: Column in base_df that contains one or more IDs (list or scalar) to match
    :param join_tbl_col: Column in join_df that should match the IDs from `from_col`
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

    TODO: combine in the old create_json_column docstring:
    For each row in the base table, this function gathers related entries from the join table
    (based on matching IDs), extracts a subset of fields, and formats them as a list of
    dictionaries (JSON-like structure). This list is stored as the row's value in the output column.

    Expected configuration for destination table definition would look like the following:
        'join_columns': [
            {'join_tbl': 'DataTopic', 'from': 'concerns_data_topic', 'to': 'id',
             'dest_cols': [
                  {'faceted': False, 'name': 'topics_json', 'alias': 'Topics',
                   'fields': [{ 'name': 'name', 'alias': 'Topic'},
                              { 'name': 'description', 'alias': 'Description'}, ]},
            ]},
        ]
    OR
        'join_columns': [
            {'join_tbl': 'DataTopic', 'from': 'concerns_data_topic', 'to': 'id',
             'dest_cols': [
                  {'faceted': False, 'name': 'topics_json', 'alias': 'topics_json', 'whole_record': True,}
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
                     - 'whole_records': if true, will put whole matching records into a list of json objects
                     - So far join columns have all come from list fields. There may be a need
                       to generate a column with a single json record from a non-list column,
                       but we'll implement that when the need arises.
   :return: Dictionary containing metadata and data for the new column, including:
             - 'src': join table name
             - 'name': join table key
             - 'alias': output column name
             - 'col': Synapse Column definition (type JSON)
             - 'data': list of JSON-like structures (one per base row)
    """
    column_name = dest_col['alias']
    reverse_lookup = join_config.get('reverse_lookup', False)  # <- Moved here!

    # Determine if this is a JSON column
    is_json_column = 'fields' in dest_col or dest_col.get('whole_records', False)

    # Determine source columns
    if is_json_column:
        if dest_col.get('whole_records'):
            source_fields = None  # Will use all fields
        else:
            source_fields = [field['name'] for field in dest_col['fields']]
        is_multi_field = True  # JSON always treated as multi-field
    else:
        source_fields = dest_col.get('source_cols', [dest_col.get('name')])
        is_multi_field = len(source_fields) > 1

    # Get transform function (or no-op)
    if 'transform' in dest_col:
        transform_func = get_transform_function(dest_col['transform'])
    else:
        transform_func = lambda *args: args[0] if args else None

    def create_json_objects(matching_rows):
        """Helper to create JSON objects from matching rows"""
        json_objects = []
        for _, row in matching_rows.iterrows():
            if dest_col.get('whole_records'):
                obj = row.to_dict()
            else:
                obj = {}
                for field in dest_col['fields']:
                    field_name = field['name']
                    field_alias = field.get('alias', field_name)
                    obj[field_alias] = row[field_name]
            json_objects.append(obj)
        return json_objects

    def xcreate_json_objects(matching_rows):
        """Helper to create JSON objects from matching rows"""
        json_objects = []
        for _, row in matching_rows.iterrows():
            if dest_col.get('whole_records'):
                obj = row.to_dict()
            else:
                obj = {}
                for field in dest_col['fields']:
                    field_name = field['name']
                    field_alias = field.get('alias', field_name)
                    obj[field_alias] = row[field_name]
            json_objects.append(json.dumps(obj))
        return json_objects

    if reverse_lookup:
        # Reverse lookup: join table has lists pointing to base table IDs
        def process_ids(base_id):
            def base_id_matches(join_col_val):
                if isinstance(join_col_val, pd.Series):
                    join_col_val = list(join_col_val)
                if isinstance(join_col_val, list):
                    return base_id in join_col_val
                return join_col_val == base_id
            # Find join table rows where join_tbl_col list contains this base_id
            matching_rows = join_df[join_df[join_tbl_col].apply(base_id_matches)]

            if matching_rows.empty:
                return []

            if is_json_column:
                return create_json_objects(matching_rows)
            elif is_multi_field:
                return [
                    transform_func(*[row[field] for field in source_fields])
                    for _, row in matching_rows.iterrows()
                ]
            else:
                return matching_rows[source_fields[0]].apply(transform_func).tolist()

        # use lambda so process_ids doesn't receives a value, not a series
        result = base_df[base_tbl_col].apply(lambda x: process_ids(x)).tolist()

    else:
        # Normal lookup: base table has lists of IDs, join table has matching records
        if not is_json_column:  # JSON columns can work with scalar IDs too
            sample_val = base_df[base_tbl_col].dropna().iloc[0] if not base_df[base_tbl_col].dropna().empty else []
            if not isinstance(sample_val, list):
                raise ValueError(f"Expected list column from '{base_table_name}.{base_tbl_col}', but got scalar.")

        join_lookup = join_df.set_index(join_tbl_col)

        def process_ids(ids):
            if not ids:
                return []

            # Handle both list and scalar IDs
            if not isinstance(ids, list):
                ids = [ids]

            matching_rows = join_lookup.loc[join_lookup.index.intersection(ids)].reset_index()

            if matching_rows.empty:
                return []

            if is_json_column:
                return create_json_objects(matching_rows)
            elif is_multi_field:
                return [
                    transform_func(*[row[field] for field in source_fields])
                    for _, row in matching_rows.iterrows()
                ]
            else:
                return matching_rows[source_fields[0]].apply(transform_func).tolist()

        result = base_df[base_tbl_col].apply(lambda x: process_ids(x)).tolist()

    # Determine column type
    if is_json_column:
        columnType = 'JSON'
    else:
        # Type detection for regular columns
        sample_values = [val for sublist in result[:10] for val in sublist]
        if sample_values:
            datatype = type(sample_values[0])
            columnType = 'STRING_LIST' if datatype == str else 'INTEGER_LIST'
        else:
            columnType = 'STRING_LIST'

    return {
        'src': join_config['join_table_name'],
        'name': dest_col.get('name', 'json_fields') if not is_json_column else 'json_objects',
        'alias': column_name,
        'col': Column(name=column_name, columnType=columnType),
        'data': result
    }

def get_src_table(syn: Synapse, table_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve and validate a source table from Synapse, capture its column metadata and a cleaned DataFrame.
    If the table is empty:
        - If a version number has been specified, raise an exception and quit execution.
        - Otherwise, find the last non-empty version and use that
            - Ideally,

    This function:
    - Retrieves the Synapse table and confirms its name matches the expected one
    - Extracts column metadata
    - Queries the full table contents into a DataFrame
    - Cleans NaNs from the DataFrame (replacing them with empty strings)
    - Stores the DataFrame, table object, and column info in the returned dictionary

    :param syn: Authenticated Synapse client
    :param table_info: Dictionary with keys:
             - 'id': Synapse table ID
             - 'name': expected name of the table
    :return: Dictionary with keys:
             - 'id': Synapse table ID
             - 'name': expected name of the table
             - 'syn_table': the retrieved Synapse table object
             - 'columns': dict of Synapse column metadata keyed by column name
             - 'df': cleaned DataFrame of table contents
    :raises ValueError: if the retrieved Synapse table has a different name than expected
    """
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

if __name__ == "__main__":
    denormalize_tables(sys.argv[1:])
