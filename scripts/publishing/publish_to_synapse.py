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
table's latest snapshot; the denormalized tables that join it read that same
snapshot (utils.portal_version), so they agree with what the portal shows.

A table that fails to publish or verify keeps its last verified snapshot; the
rest still publish, and the run exits non-zero. The Manifest is held back this
way when an anatomy label lookup fails, so it's never published with bare IDs
where labels should be; the next run retries.

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
from typing import Dict, List, Tuple, Union

import pandas as pd
from synapseclient import Synapse
from synapseclient.models import Column, MaterializedView, Table

from scripts.publishing.denormalized_manifest import build_denormalized_manifest
from scripts.publishing.denormalized_tables import build_dest_tables
from scripts.publishing.generate_tables_config import TABLE_IDS
from scripts.publishing.source_tables import SOURCE_TABLES, build_source_table
from scripts.publishing.utils import (
    PROJECT_ID, VERSION_ANNOTATION, clear_populate_snapshot_table, get_annotation, initialize_synapse, portal_version)

HASH_ANNOTATION = 'b2ai_content_hash'
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


def status(state: str, name: str, detail: str = '') -> None:
    print(f"  {state:<10} {name:<29} {detail}".rstrip())


def build_all_tables(syn: Synapse) -> Tuple[Dict[str, Built], Dict[str, str]]:
    """
    Build every table we publish.

    :return: (tables keyed by name, reasons keyed by name for tables that built
        but mustn't be published)
    """
    tables: Dict[str, Built] = {name: build_source_table(name) for name in SOURCE_TABLES}
    held_back: Dict[str, str] = {}

    manifest_cols, manifest_df, lookup_failures = build_denormalized_manifest()
    tables['Manifest'] = (manifest_cols, manifest_df)
    if lookup_failures:
        held_back['Manifest'] = (
            f"EBI OLS anatomy label lookup failed for {', '.join(lookup_failures)}; "
            "keeping the last published Manifest")

    # DataTopic_denormalized joins only data part ids and names, not anatomy
    # labels, so it can use this Manifest even when the Manifest is held back
    src_tables = {'Manifest_denormalized': {**TABLE_IDS['Manifest_denormalized'], 'df': manifest_df}}
    for name, col_defs, df in build_dest_tables(syn, src_tables=src_tables):
        tables[name] = (col_defs, df)
    return tables, held_back


def content_hash(col_defs: List[Column], df: pd.DataFrame) -> str:
    """Hash of everything an upload would send: column definitions and rows."""
    schema = [(c.name, str(c.column_type), c.maximum_size, c.maximum_list_length, str(c.facet_type))
              for c in col_defs]
    rows = df.to_json(orient='split', default_handler=str)
    return hashlib.sha256((json.dumps(schema) + rows).encode()).hexdigest()


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
        status('unchanged', name)
        return
    if dry_run:
        status('CHANGED', name, f"would publish {len(df)} rows")
        return

    _, version = clear_populate_snapshot_table(
        syn, name, col_defs, df, table_id, snapshot_comment=f"content hash {digest}")
    count = row_count(table_id, version)
    if count != len(df):
        raise PublishError(
            f"{name}: snapshot {table_id}.{version} has {count} rows, uploaded {len(df)}")
    set_annotations(syn, table_id, {HASH_ANNOTATION: digest, VERSION_ANNOTATION: version})
    status('PUBLISHED', name, f"{table_id}.{version}, {count} rows verified")


def update_views(syn: Synapse, create_missing: bool = False, dry_run: bool = False) -> List[str]:
    """Point each portal table's materialized view at its verified snapshot; return views that failed."""
    children = syn.restPOST('/entity/children', json.dumps(
        {'parentId': PROJECT_ID, 'includeTypes': ['materializedview']}))['page']
    views = {v['name']: v['id'] for v in children}
    failures = []
    for name in PORTAL_TABLES:
        view_name = VIEW_PREFIX + name
        try:
            table_id = TABLE_IDS[name]['id']
            version = portal_version(syn, table_id)
            sql = f"SELECT * FROM {table_id}.{version}"
            view = MaterializedView(id=views[view_name]).get() if view_name in views else None

            if view is None and not create_missing:
                status('MISSING', view_name, "run with --create-views")
                continue
            if view is not None and view.defining_sql == sql:
                status('current', view_name, f"{table_id}.{version}")
                continue
            if dry_run:
                status('CHANGED', view_name, f"would point at {table_id}.{version}")
                continue
            if row_count(table_id, version) == 0:
                raise PublishError(f"{table_id}.{version} is empty; not pointing {view_name} at it")

            if view is None:
                view = MaterializedView(name=view_name, parent_id=PROJECT_ID, defining_sql=sql).store()
                status('CREATED', view_name, f"{view.id} -> {table_id}.{version}")
            else:
                view.defining_sql = sql
                view.store()
                status('UPDATED', view_name, f"-> {table_id}.{version}")
        except Exception as e:
            report_failure(view_name, e)
            failures.append(view_name)
    return failures


def publish_to_synapse(force: bool = False, dry_run: bool = False, create_views: bool = False) -> None:
    syn = initialize_synapse()
    print("Building tables")
    tables, held_back = build_all_tables(syn)

    print("\nTables")

    # Keep going past a failed table: every view points only at verified
    # snapshots, so the others can still be published safely
    failures = []
    for name, (col_defs, df) in tables.items():
        try:
            if name in held_back:
                raise PublishError(held_back[name])
            publish_table(syn, name, col_defs, df, force=force, dry_run=dry_run)
        except Exception as e:
            report_failure(name, e)
            failures.append(name)

    print("\nViews")
    failures += update_views(syn, create_missing=create_views, dry_run=dry_run)

    if failures:
        raise PublishError(f"Failed to publish: {', '.join(failures)}")


def report_failure(name: str, error: Exception) -> None:
    status('FAILED', name, str(error))
    if os.getenv('GITHUB_ACTIONS'):
        # Shows on the workflow run's summary page
        print(f"::error title=Synapse publish failed: {name}::{error}")


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
