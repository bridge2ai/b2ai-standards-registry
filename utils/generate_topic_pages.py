#!/usr/bin/env python3
"""Generate individual Data Topic pages and update overview diagram.

Steps:
1. Parse src/data/DataTopic.yaml for hierarchy.
2. Write per-topic markdown pages to docs/topics/NAME.markdown (using name with spaces removed).
3. Build Mermaid flowchart (LR) rooted at Data if present; use subclass_of edges.
4. Inject diagram into docs/DataTopic.markdown ahead of existing table (idempotent replacement between markers).
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, List, Set
import yaml

from id_linking import load_all_b2ai_data, convert_ids_to_links, convert_topic_links, slugify

REPO_ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = REPO_ROOT / 'src' / 'data' / 'DataTopic.yaml'
OUTPUT_DIR = REPO_ROOT / 'docs' / 'topics'
OVERVIEW_PATH = REPO_ROOT / 'docs' / 'DataTopic.markdown'
MARKER_START = '<!-- TOPIC_DIAGRAM_START -->'
MARKER_END = '<!-- TOPIC_DIAGRAM_END -->'


def load_data() -> List[Dict]:
    with open(YAML_PATH, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('data_topics_collection', [])


def build_index(topics: List[Dict]):
    by_id = {t['id']: t for t in topics if 'id' in t}
    children: Dict[str, List[str]] = {tid: [] for tid in by_id}
    roots: Set[str] = set(by_id.keys())
    for t in topics:
        tid = t.get('id')
        if not isinstance(tid, str):
            continue
        parents = t.get('subclass_of') or []
        if not isinstance(parents, list):
            continue
        for parent in parents:
            if isinstance(parent, str) and parent in by_id:
                children[parent].append(tid)
                roots.discard(tid)
    return by_id, children, roots


def write_pages(by_id: Dict[str, Dict], all_data: Dict[str, Dict]):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for tid, t in by_id.items():
        name = t.get('name', tid)
        # Topics use the exact name with spaces removed but capitalization preserved
        slug = name.replace(' ', '')
        path = OUTPUT_DIR / f"{slug}.markdown"
        lines = []
        lines.append(f"**id:** {tid}\n")

        # Basic contributor info
        for key in ['contributor_github_name', 'contributor_name', 'contributor_orcid']:
            if key in t:
                label = key.replace('_', ' ')
                lines.append(f"**{label}:** {t[key]}\n")

        # Description with ID linking
        if 'description' in t:
            description = convert_ids_to_links(
                str(t['description']), all_data, "..")
            lines.append(f"**description:** {description}\n")

        # External IDs
        for key in ['edam_id', 'mesh_id', 'ncit_id']:
            if key in t:
                label = key.replace('_', ' ')
                lines.append(f"**{label}:** {t[key]}\n")

        # Subclass relationships
        if 'subclass_of' in t:
            lines.append("**subclass of:**\n")
            topic_links = convert_topic_links(t['subclass_of'], all_data, "..")
            for link in topic_links:
                lines.append(f"- {link}\n")

        # Find what this topic is a parent of
        child_topic_ids = []
        for other_tid, other_t in by_id.items():
            if 'subclass_of' in other_t and tid in other_t['subclass_of']:
                child_topic_ids.append(other_tid)

        if child_topic_ids:
            lines.append("**parent of:**\n")
            # Sort by name for consistent output
            child_topic_ids.sort(key=lambda x: by_id.get(x, {}).get('name', x))
            child_links = convert_topic_links(child_topic_ids, all_data, "..")
            for link in child_links:
                lines.append(f"- {link}\n")

        with open(path, 'w') as f:
            f.write('\n'.join(lines))


def build_mermaid(by_id: Dict[str, Dict], children: Dict[str, List[str]], roots: Set[str]) -> str:
    # Try to find a good root - look for "Data" topic first
    ordered_roots = []
    data_topic = None
    for tid, t in by_id.items():
        if t.get('name', '').lower() == 'data':
            data_topic = tid
            break

    if data_topic:
        ordered_roots = [data_topic] + \
            [r for r in sorted(roots) if r != data_topic]
    else:
        ordered_roots = sorted(roots)

    lines = ["```mermaid", "flowchart LR"]

    # Define nodes
    for tid, t in by_id.items():
        label = t.get('name', tid)
        slug = label.replace(' ', '')
        lines.append(f"    {tid.replace(':', '_')}[{label}]")

    # Edges
    for parent, kids in children.items():
        for kid in kids:
            lines.append(
                f"    {parent.replace(':', '_')} --> {kid.replace(':', '_')}")

    # Clicks
    lines.append("")
    for tid, t in by_id.items():
        label = t.get('name', tid)
        slug = label.replace(' ', '')
        # Use double quotes per Mermaid spec; escape any internal double quotes in label.
        safe_label = label.replace('"', '\\"')
        lines.append(
            f'    click {tid.replace(":", "_")} "topics/{slug}/" "{safe_label}"')

    lines.append("```")
    return '\n'.join(lines)


def inject_overview(diagram: str):
    if OVERVIEW_PATH.exists():
        with open(OVERVIEW_PATH, 'r') as f:
            content = f.read()
    else:
        content = ''

    block = f"{MARKER_START}\n{diagram}\n{MARKER_END}"
    if MARKER_START in content and MARKER_END in content:
        content = re.sub(f"{MARKER_START}.*?{MARKER_END}",
                         block, content, flags=re.DOTALL)
    else:
        # Prepend block with heading if missing
        content = f"# Data Topics\n\n{block}\n\n" + content

    with open(OVERVIEW_PATH, 'w') as f:
        f.write(content)


def main():
    # Load all data for ID linking
    all_data = load_all_b2ai_data()

    topics = load_data()
    by_id, children, roots = build_index(topics)
    write_pages(by_id, all_data)
    diagram = build_mermaid(by_id, children, roots)
    inject_overview(diagram)
    print(
        f"Generated {len(by_id)} topic pages with ID linking and updated overview diagram.")


if __name__ == '__main__':
    main()
