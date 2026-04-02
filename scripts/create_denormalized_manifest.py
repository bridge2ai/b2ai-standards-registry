"""
Create a denormalized Manifest table for the Synapse Standards Registry Explorer.

Reads Manifest.json, explodes data_parts into one row per data part,
resolves all IDs to human-readable names with markdown links, and uploads
the result to the existing Manifest Synapse table.

Usage:
    python -m scripts.create_denormalized_manifest
"""
from id_linking import get_ontology_label, slugify
import base64
import gzip
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote

import pandas as pd
from synapseclient.models import Column, ColumnType

from scripts.generate_tables_config import TABLE_IDS
from scripts.utils import (
    clear_populate_snapshot_table,
    configure_column_from_data,
    initialize_synapse,
    load_json_to_dataframe,
)

# Import get_ontology_label and slugify from utils/id_linking.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'utils'))


COLUMN_DEFS: List[tuple[str, ColumnType]] = [
    ('id', ColumnType.STRING),
    ('organization', ColumnType.STRING),
    ('organization_link', ColumnType.STRING),
    ('data_part_name', ColumnType.STRING),
    ('data_part_description', ColumnType.STRING),
    ('standards_and_tools', ColumnType.STRING_LIST),
    ('standards_and_tools_links', ColumnType.STRING_LIST),
    ('uses_data_substrates', ColumnType.STRING_LIST),
    ('uses_data_substrates_links', ColumnType.STRING_LIST),
    ('concerns_data_topics', ColumnType.STRING_LIST),
    ('concerns_data_topics_links', ColumnType.STRING_LIST),
    ('anatomy', ColumnType.STRING_LIST),
    ('anatomy_links', ColumnType.STRING_LIST),
    ('datasets', ColumnType.STRING_LIST),
    ('datasets_link', ColumnType.STRING),
]


def build_lookup_dicts() -> Dict[str, Dict[str, str]]:
    """
    Load lookup tables and return {table: {id: name}} dicts for ID resolution.
    """
    lookups = {}
    for table_name in ('Organization', 'DataStandardOrTool', 'DataSubstrate', 'DataTopic'):
        df = load_json_to_dataframe(table_name)
        lookups[table_name] = dict(zip(df['id'], df['name']))
    return lookups


def get_anatomy_label_cached(ontology_id: str, cache: Dict[str, Optional[str]]) -> Optional[str]:
    """Resolve an anatomy ontology ID to a label, with caching."""
    if ontology_id not in cache:
        cache[ontology_id] = get_ontology_label(ontology_id)
    return cache[ontology_id]


def make_topic_facet_url(topic_name: str) -> str:
    """Build a Synapse portal Explore URL filtered to a specific topic facet."""
    diff = {
        "selectedFacets": [{
            "concreteType": "org.sagebionetworks.repo.model.table.FacetColumnValuesRequest",
            "columnName": "topic",
            "facetValues": [topic_name],
        }]
    }
    compressed = gzip.compress(json.dumps(
        diff, separators=(',', ':')).encode())
    encoded = base64.b64encode(compressed).decode()
    return f"/Explore?qw0={quote(encoded)}"


def resolve_id(entity_id: str, lookup: Dict[str, str], label: str) -> str:
    """Look up a name for an ID, raising if not found."""
    if entity_id not in lookup:
        raise ValueError(f"{label} ID not found in lookup: {entity_id}")
    return lookup[entity_id]


def build_standard_link(standard_id: str, lookups: Dict[str, Dict[str, str]]) -> str:
    name = resolve_id(standard_id, lookups['DataStandardOrTool'], 'Standard')
    return f"[{name}](/Explore/Standard/DetailsPage?id={standard_id})"


def build_substrate_link(substrate_id: str, lookups: Dict[str, Dict[str, str]]) -> str:
    name = resolve_id(substrate_id, lookups['DataSubstrate'], 'Substrate')
    slug = slugify(name)
    return f"[{name}](https://bridge2ai.github.io/b2ai-standards-registry/substrates/{slug}/)"


def build_topic_link(topic_id: str, lookups: Dict[str, Dict[str, str]]) -> str:
    name = resolve_id(topic_id, lookups['DataTopic'], 'Topic')
    return f"[{name}]({make_topic_facet_url(name)})"


def build_anatomy_link(anatomy_id: str, cache: Dict[str, Optional[str]]) -> str:
    label = get_anatomy_label_cached(anatomy_id, cache)
    display = label if label else anatomy_id
    prefix, local_id = anatomy_id.split(':', 1)
    obo_url = f"http://purl.obolibrary.org/obo/{prefix}_{local_id}"
    return f"[{display}]({obo_url})"


def build_denormalized_df(lookups: Dict[str, Dict[str, str]]) -> pd.DataFrame:
    """
    Load Manifest.json, explode data_parts into one row per data part,
    and resolve all IDs to human-readable names with markdown links.
    """
    manifest_df = load_json_to_dataframe('Manifest')
    anatomy_cache: Dict[str, Optional[str]] = {}
    rows = []

    for _, manifest in manifest_df.iterrows():
        manifest_id = manifest['id']
        org_id = manifest['organization']
        org_name = resolve_id(org_id, lookups['Organization'], 'Organization')
        org_link = f"[{org_name}](/Explore/Organization/OrganizationDetailsPage?id={org_id})"
        datasets = manifest.get('datasets') or []
        dataset_count = len(datasets)
        datasets_link = (
            f"[{dataset_count} datasets](/Explore/Organization/OrganizationDetailsPage?id={org_id}#DataSets)"
            if dataset_count > 0 else ''
        )

        for data_part in manifest.get('data_parts') or []:
            std_ids = data_part.get('standards_and_tools') or []
            sub_ids = data_part.get('uses_data_substrates') or []
            topic_ids = data_part.get('concerns_data_topics') or []
            anatomy_ids = data_part.get('anatomy') or []

            rows.append({
                'id': manifest_id,
                'organization': org_id,
                'organization_link': org_link,
                'data_part_name': data_part.get('data_part_name', ''),
                'data_part_description': data_part.get('data_part_description', ''),
                'standards_and_tools': std_ids,
                'standards_and_tools_links': [build_standard_link(sid, lookups) for sid in std_ids],
                'uses_data_substrates': sub_ids,
                'uses_data_substrates_links': [build_substrate_link(sid, lookups) for sid in sub_ids],
                'concerns_data_topics': topic_ids,
                'concerns_data_topics_links': [build_topic_link(tid, lookups) for tid in topic_ids],
                'anatomy': anatomy_ids,
                'anatomy_links': [build_anatomy_link(aid, anatomy_cache) for aid in anatomy_ids],
                'datasets': datasets,
                'datasets_link': datasets_link,
            })

    return pd.DataFrame(rows)


def get_column_definitions(df: pd.DataFrame) -> List[Column]:
    """Create Synapse Column definitions configured from actual data."""
    columns = []
    for col_name, col_type in COLUMN_DEFS:
        col = Column(name=col_name, column_type=col_type)
        col = configure_column_from_data(col, df[col_name])
        columns.append(col)
    return columns


def upload_denormalized_manifest(
    syn=None,
    table_id: Optional[str] = None,
) -> pd.DataFrame:
    """Build and upload the denormalized Manifest table to Synapse."""
    print("Building lookup tables...")
    lookups = build_lookup_dicts()

    print("Building denormalized manifest DataFrame...")
    df = build_denormalized_df(lookups)
    print(f"  {len(df)} rows")

    col_defs = get_column_definitions(df)

    if syn is None:
        syn = initialize_synapse()
    if table_id is None:
        table_id = TABLE_IDS['Manifest']['id']
    clear_populate_snapshot_table(syn, 'Manifest', col_defs, df, table_id)
    return df


def create_denormalized_manifest() -> None:
    """Build and upload the denormalized Manifest table to Synapse."""
    upload_denormalized_manifest()


if __name__ == '__main__':
    create_denormalized_manifest()
