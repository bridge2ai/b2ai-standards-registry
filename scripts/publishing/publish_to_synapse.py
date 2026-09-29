"""
Publish registry data to Synapse and point the portal's materialized views at it.

Every run builds all tables locally: source tables from project/data/*.json,
the denormalized Manifest, and the DEST_TABLES in generate_tables_config. Then,
for each table:
  - compare a hash of its schema and rows with the hash annotated on the
    Synapse table at its last publish, and skip it if they match
  - otherwise clear, repopulate and snapshot it, and check that the snapshot's
    row count matches what was uploaded
  - annotate the table with the hash and the verified snapshot version

Finally, each materialized view named mv_<table> in the project is pointed at
its table's verified snapshot (`SELECT * FROM synX.N`). The portal queries the
views, so it picks up new data without a code change. A table built elsewhere
(D4D_content) has no published-version annotation, so its view follows the
table's latest snapshot.

Because change detection is by content hash, there's no need to track which
inputs feed which denormalized tables: a table is re-uploaded exactly when what
we'd upload differs from what's there.

Usage:
    python -m scripts.publishing.publish_to_synapse [--dry-run] [--force] [--create-views]
"""
import hashlib
import json
import os
import sys
from argparse import ArgumentParser
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
from synapseclient import Synapse
from synapseclient.models import Column, MaterializedView, Table

from scripts.publishing.analyze_and_update_synapse_tables import PATHS_TO_IDS, build_source_table, file_path_to_table_name
from scripts.publishing.create_denormalized_manifest import build_denormalized_manifest
from scripts.publishing.create_denormalized_tables import build_dest_tables
from scripts.publishing.generate_tables_config import TABLE_IDS
from scripts.publishing.utils import DATA_PATH, PROJECT_ID, clear_populate_snapshot_table, initialize_synapse

HASH_ANNOTATION = 'b2ai_content_hash'
VERSION_ANNOTATION = 'b2ai_published_version'
VIEW_PREFIX = 'mv_'

# Tables the portal (synapse-web-monorepo b2ai.standards resources.ts) reads,
# each through a materialized view named VIEW_PREFIX + table name
PORTAL_TABLES = [
    'DST_denormalized',
    'DataSet_denormalized',
    'DataSubstrate',
    'DataTopic_denormalized',
    'Organization_denormalized',
    'D4D_content',
    'Manifest',
]

Built = Tuple[List[Column], pd.DataFrame]


class PublishError(Exception):
    pass


def build_all_tables(syn: Synapse) -> Dict[str, Built]:
    """Build every table we publish, keyed by table name."""
    tables: Dict[str, Built] = {}
    for path in PATHS_TO_IDS:
        name = file_path_to_table_name(path)
        if name == 'Manifest':
            continue
        built = build_source_table(os.path.join(DATA_PATH, os.path.basename(path)))
        if built is None:
            raise PublishError(f"No list of records in {path}")
        tables[name] = built

    tables['Manifest'] = build_denormalized_manifest()
    src_tables = {'Manifest_denormalized': {
        **TABLE_IDS['Manifest_denormalized'], 'df': tables['Manifest'][1]}}
    for name, col_defs, df in build_dest_tables(syn, src_tables=src_tables):
        tables[name] = (col_defs, df)
    return tables


def content_hash(col_defs: List[Column], df: pd.DataFrame) -> str:
    """Hash of everything an upload would send: column definitions and rows."""
    schema = [(c.name, str(c.column_type), c.maximum_size, c.maximum_list_length, str(c.facet_type))
              for c in col_defs]
    rows = df.to_json(orient='split', default_handler=str)
    return hashlib.sha256((json.dumps(schema) + rows).encode()).hexdigest()


def get_annotation(syn: Synapse, entity_id: str, key: str) -> Optional[str]:
    annotation = syn.restGET(f'/entity/{entity_id}/annotations2')['annotations'].get(key)
    return annotation['value'][0] if annotation else None


def set_annotations(syn: Synapse, entity_id: str, values: Dict[str, Union[str, int]]) -> None:
    annotations = syn.restGET(f'/entity/{entity_id}/annotations2')
    for key, value in values.items():
        annotations['annotations'][key] = {
            'type': 'LONG' if isinstance(value, int) else 'STRING', 'value': [str(value)]}
    syn.restPUT(f'/entity/{entity_id}/annotations2', json.dumps(annotations))


def row_count(table_id: str, version: int) -> int:
    return int(Table.query(query=f"SELECT COUNT(*) FROM {table_id}.{version}").iloc[0, 0])


def publish_table(syn: Synapse, name: str, col_defs: List[Column], df: pd.DataFrame,
                  force: bool = False, dry_run: bool = False) -> None:
    """Upload, snapshot and verify one table, unless its content is unchanged."""
    table_id = TABLE_IDS[name]['id']
    if df.empty:
        raise PublishError(f"{name} built with no rows; not uploading")

    digest = content_hash(col_defs, df)
    if not force and get_annotation(syn, table_id, HASH_ANNOTATION) == digest:
        print(f"{name}: unchanged")
        return
    if dry_run:
        print(f"{name}: changed, would publish {len(df)} rows")
        return

    _, version = clear_populate_snapshot_table(
        syn, name, col_defs, df, table_id, snapshot_comment=f"content hash {digest}")
    count = row_count(table_id, version)
    if count != len(df):
        raise PublishError(
            f"{name}: snapshot {table_id}.{version} has {count} rows, uploaded {len(df)}")
    set_annotations(syn, table_id, {HASH_ANNOTATION: digest, VERSION_ANNOTATION: version})
    print(f"{name}: published and verified {table_id}.{version} ({count} rows)")


def latest_snapshot_version(syn: Synapse, table_id: str) -> int:
    # Newest first; the unsnapshotted in-progress version isn't listed
    return syn.restGET(f'/entity/{table_id}/version?offset=0&limit=1')['results'][0]['versionNumber']


def update_views(syn: Synapse, create_missing: bool = False, dry_run: bool = False) -> None:
    """Point each portal table's materialized view at its verified snapshot."""
    views = {v['name']: v['id'] for v in syn.getChildren(PROJECT_ID, includeTypes=['materializedview'])}
    for name in PORTAL_TABLES:
        table_id = TABLE_IDS[name]['id']
        version = get_annotation(syn, table_id, VERSION_ANNOTATION) or latest_snapshot_version(syn, table_id)
        sql = f"SELECT * FROM {table_id}.{version}"
        view_name = VIEW_PREFIX + name
        view = MaterializedView(id=views[view_name]).get() if view_name in views else None

        if view is None and not create_missing:
            print(f"{view_name}: no such view (run with --create-views)")
            continue
        if view is not None and view.defining_sql == sql:
            print(f"{view_name} ({view.id}): already {sql}")
            continue
        if dry_run:
            print(f"{view_name}: would set to {sql}")
            continue
        if row_count(table_id, int(version)) == 0:
            raise PublishError(f"{table_id}.{version} is empty; not pointing {view_name} at it")

        if view is None:
            view = MaterializedView(name=view_name, parent_id=PROJECT_ID, defining_sql=sql).store()
            print(f"{view_name}: created {view.id} as {sql}")
        else:
            view.defining_sql = sql
            view.store()
            print(f"{view_name} ({view.id}): set to {sql}")


def publish_to_synapse(force: bool = False, dry_run: bool = False, create_views: bool = False) -> None:
    syn = initialize_synapse()
    tables = build_all_tables(syn)

    # Keep going past a failed table: every view points only at verified
    # snapshots, so the others can still be published safely
    failures = []
    for name, (col_defs, df) in tables.items():
        try:
            publish_table(syn, name, col_defs, df, force=force, dry_run=dry_run)
        except Exception as e:
            print(f"FAILED {name}: {e}")
            failures.append(name)

    update_views(syn, create_missing=create_views, dry_run=dry_run)

    if failures:
        raise PublishError(f"Failed to publish: {', '.join(failures)}")


def cli():
    parser = ArgumentParser(description=__doc__.split('\n\n')[0].strip())
    parser.add_argument('--dry-run', action='store_true',
                        help='Build and compare, but change nothing on Synapse')
    parser.add_argument('--force', action='store_true',
                        help='Publish every table even if its content hash is unchanged')
    parser.add_argument('--create-views', action='store_true',
                        help='Create any missing mv_* materialized views')
    args = parser.parse_args()
    try:
        publish_to_synapse(force=args.force, dry_run=args.dry_run, create_views=args.create_views)
    except PublishError as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    cli()
