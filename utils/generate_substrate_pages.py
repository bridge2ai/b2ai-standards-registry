#!/usr/bin/env python3
"""Generate individual Data Substrate pages and update overview diagram.

Steps:
1. Parse src/data/DataSubstrate.yaml for hierarchy.
2. Write per-substrate markdown pages to docs/substrates/ID_NAME.markdown (slugified name).
3. Build Mermaid flowchart (LR) rooted at Data (B2AI_SUBSTRATE:7) if present; use subclass_of edges.
4. Inject diagram into docs/DataSubstrate.markdown ahead of existing table (idempotent replacement between markers).
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, List, Set
import yaml

from id_linking import load_all_b2ai_data, convert_ids_to_links, convert_substrate_links, slugify as shared_slugify

REPO_ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = REPO_ROOT / 'src' / 'data' / 'DataSubstrate.yaml'
OUTPUT_DIR = REPO_ROOT / 'docs' / 'substrates'
OVERVIEW_PATH = REPO_ROOT / 'docs' / 'DataSubstrate.markdown'
MARKER_START = '<!-- SUBSTRATE_DIAGRAM_START -->'
MARKER_END = '<!-- SUBSTRATE_DIAGRAM_END -->'


# Use shared slugify function
slugify = shared_slugify


def load_data() -> List[Dict]:
    with open(YAML_PATH, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('data_substrates_collection', [])


def build_index(substrates: List[Dict]):
    by_id = {s['id']: s for s in substrates if 'id' in s}
    children: Dict[str, List[str]] = {sid: [] for sid in by_id}
    roots: Set[str] = set(by_id.keys())
    for s in substrates:
        sid = s.get('id')
        if not isinstance(sid, str):
            continue
        parents = s.get('subclass_of') or []
        if not isinstance(parents, list):
            continue
        for parent in parents:
            if isinstance(parent, str) and parent in by_id:
                children[parent].append(sid)
                roots.discard(sid)
    return by_id, children, roots


def write_pages(by_id: Dict[str, Dict], all_data: Dict[str, Dict]):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for sid, s in by_id.items():
        name = s.get('name', sid)
        slug = slugify(name)
        path = OUTPUT_DIR / f"{slug}.markdown"
        lines = []
        lines.append(f"**id:** {sid}\n")
        for key in ['name', 'description', 'edam_id', 'mesh_id', 'ncit_id']:
            if key in s:
                label = key.replace('_', ' ')
                # Apply ID linking to description and other text fields
                value = convert_ids_to_links(str(s[key]), all_data, "..")
                lines.append(f"**{label}:** {value}\n")
        if 'file_extensions' in s:
            lines.append(
                f"**file extensions:** {' '.join(s['file_extensions'])}\n")
        if 'limitations' in s:
            lines.append("**limitations:**\n")
            for lim in s['limitations']:
                lines.append(
                    f"- {convert_ids_to_links(str(lim), all_data, '..')}\n")
        if 'subclass_of' in s:
            lines.append("**subclass of:**\n")
            substrate_links = convert_substrate_links(
                s['subclass_of'], all_data, "..")
            for link in substrate_links:
                lines.append(f"- {link}\n")
        with open(path, 'w') as f:
            f.write('\n'.join(lines))


def build_mermaid(by_id: Dict[str, Dict], children: Dict[str, List[str]], roots: Set[str]) -> str:
    # Prefer Data (B2AI_SUBSTRATE:7) as root if present
    ordered_roots = ['B2AI_SUBSTRATE:7'] + \
        [r for r in sorted(roots) if r != 'B2AI_SUBSTRATE:7']
    lines = ["```mermaid", "flowchart LR"]
    # Define nodes
    for sid, s in by_id.items():
        label = s.get('name', sid)
        slug = slugify(label)
        lines.append(f"    {sid.replace(':', '_')}[{label}]")
    # Edges
    for parent, kids in children.items():
        for kid in kids:
            lines.append(
                f"    {parent.replace(':', '_')} --> {kid.replace(':', '_')}")
    # Clicks
    lines.append("")
    for sid, s in by_id.items():
        label = s.get('name', sid)
        slug = slugify(label)
        # Use double quotes per Mermaid spec; escape any internal double quotes in label.
        # Link pattern: substrates/{slug}/ to mirror topics/ pattern (pretty URLs)
        safe_label = label.replace('"', '\\"')
        lines.append(
            f"    click {sid.replace(':', '_')} \"substrates/{slug}/\" \"{safe_label}\"")
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
        content = f"# Data Substrates\n\n{block}\n\n" + content
    with open(OVERVIEW_PATH, 'w') as f:
        f.write(content)


def main():
    # Load all data for ID linking
    all_data = load_all_b2ai_data()

    substrates = load_data()
    by_id, children, roots = build_index(substrates)
    write_pages(by_id, all_data)
    diagram = build_mermaid(by_id, children, roots)
    inject_overview(diagram)
    print(
        f"Generated {len(by_id)} substrate pages with ID linking and updated overview diagram.")


if __name__ == '__main__':
    main()
