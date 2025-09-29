#!/usr/bin/env python3
"""Generate individual Use Case pages and update overview diagram.

Steps:
1. Parse src/data/UseCase.yaml for hierarchy.
2. Write per-usecase markdown pages to docs/usecases/ID_NAME.markdown (slugified name).
3. Build Mermaid flowchart (LR) using enables relationships to show workflow.
4. Inject diagram into docs/UseCase.markdown ahead of existing table (idempotent replacement between markers).
"""
from __future__ import annotations
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Set
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = REPO_ROOT / 'src' / 'data' / 'UseCase.yaml'
OUTPUT_DIR = REPO_ROOT / 'docs' / 'usecases'
OVERVIEW_PATH = REPO_ROOT / 'docs' / 'UseCase.markdown'
MARKER_START = '<!-- USECASE_DIAGRAM_START -->'
MARKER_END = '<!-- USECASE_DIAGRAM_END -->'


def slugify(value: str) -> str:
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-zA-Z0-9]+', '-', value).strip('-').lower()
    return value or 'usecase'


def load_data() -> List[Dict]:
    with open(YAML_PATH, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('use_cases', [])


def build_index(usecases: List[Dict]):
    by_id = {s['id']: s for s in usecases if 'id' in s}
    enabled_by: Dict[str, List[str]] = {sid: [] for sid in by_id}
    roots: Set[str] = set(by_id.keys())
    
    for s in usecases:
        sid = s.get('id')
        if not isinstance(sid, str):
            continue
        enables = s.get('enables') or []
        if not isinstance(enables, list):
            continue
        for enabled in enables:
            if isinstance(enabled, str) and enabled in by_id:
                enabled_by[enabled].append(sid)
                roots.discard(enabled)
    
    return by_id, enabled_by, roots


def write_pages(by_id: Dict[str, Dict]):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for sid, s in by_id.items():
        name = s.get('name', sid)
        slug = slugify(name)
        path = OUTPUT_DIR / f"{slug}.markdown"
        lines = []
        
        # Basic info
        lines.append(f"**ID:** {sid}\n")
        if 'name' in s:
            lines.append(f"**Name:** {s['name']}\n")
        if 'description' in s:
            lines.append(f"**Description:** {s['description']}\n")
        
        # Category and involvement flags
        if 'use_case_category' in s:
            categories = s['use_case_category']
            if isinstance(categories, list):
                lines.append(f"**Category:** {', '.join(categories)}\n")
            else:
                lines.append(f"**Category:** {categories}\n")
        
        involvement_flags = []
        if s.get('involved_in_experimental_design'):
            involvement_flags.append('Experimental Design')
        if s.get('involved_in_metadata_management'):
            involvement_flags.append('Metadata Management')
        if s.get('involved_in_quality_control'):
            involvement_flags.append('Quality Control')
        if involvement_flags:
            lines.append(f"**Involved in:** {', '.join(involvement_flags)}\n")
        
        # Data topics
        if 'data_topics' in s:
            lines.append("**Data Topics:**\n")
            for topic in s['data_topics']:
                lines.append(f"- {topic}\n")
        
        # Relationships
        if 'enables' in s:
            lines.append("**Enables:**\n")
            for enabled in s['enables']:
                enabled_name = by_id.get(enabled, {}).get('name', enabled)
                lines.append(f"- {enabled} ({enabled_name})\n")
        
        # Find what enables this use case
        enablers = []
        for other_sid, other_s in by_id.items():
            if 'enables' in other_s and sid in other_s['enables']:
                enablers.append((other_sid, other_s.get('name', other_sid)))
        if enablers:
            lines.append("**Enabled by:**\n")
            for enabler_id, enabler_name in enablers:
                lines.append(f"- {enabler_id} ({enabler_name})\n")
        
        # Relevant GCs
        if 'relevant_to_gcs' in s:
            lines.append("**Relevant to GCs:**\n")
            for gc in s['relevant_to_gcs']:
                lines.append(f"- {gc}\n")
        
        # Standards and tools
        if 'standards_and_tools_for_gc_use' in s:
            lines.append("**Standards and Tools:**\n")
            for standard in s['standards_and_tools_for_gc_use']:
                lines.append(f"- {standard}\n")
        
        if 'alternative_standards_and_tools' in s:
            lines.append("**Alternative Standards and Tools:**\n")
            for standard in s['alternative_standards_and_tools']:
                lines.append(f"- {standard}\n")
        
        # External references
        if 'xref' in s:
            lines.append("**External References:**\n")
            for xref in s['xref']:
                lines.append(f"- {xref}\n")
        
        # Contributor info
        if 'contributor_name' in s:
            lines.append(f"**Contributor:** {s['contributor_name']}")
            if 'contributor_orcid' in s:
                lines.append(f" ({s['contributor_orcid']})")
            lines.append("\n")
        
        with open(path, 'w') as f:
            f.write('\n'.join(lines))


def build_mermaid_diagrams(by_id: Dict[str, Dict], enabled_by: Dict[str, List[str]], roots: Set[str]) -> tuple[str, str]:
    # Group by category for better visual organization
    categories = {}
    for sid, s in by_id.items():
        cat = s.get('use_case_category', ['other'])
        if isinstance(cat, list):
            cat = cat[0] if cat else 'other'
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(sid)
    
    # Define nodes with category-based styling
    category_colors = {
        'acquisition': 'fill:#e1f5fe',
        'integration': 'fill:#f3e5f5', 
        'standardization': 'fill:#e8f5e8',
        'modeling': 'fill:#fff3e0',
        'other': 'fill:#f5f5f5'
    }
    
    # Identify connected and unconnected nodes
    connected_nodes = set()
    for sid, s in by_id.items():
        enables = s.get('enables', [])
        if enables:
            connected_nodes.add(sid)
            for enabled in enables:
                if enabled in by_id:
                    connected_nodes.add(enabled)
    
    unconnected_nodes = [sid for sid in by_id.keys() if sid not in connected_nodes]
    
    # Build main workflow diagram
    main_lines = ["```mermaid", "flowchart LR"]
    
    # Create connected nodes
    for sid, s in by_id.items():
        if sid in connected_nodes:
            label = s.get('name', sid)
            if len(label) > 50:
                label = label[:47] + "..."
            label = label.replace('"', '\\"').replace('[', '&#91;').replace(']', '&#93;')
            main_lines.append(f"    {sid.replace(':', '_')}[\"{label}\"]")
    
    # Add workflow relationships
    main_lines.append("")
    main_lines.append("    %% Workflow relationships")
    for sid, s in by_id.items():
        enables = s.get('enables', [])
        for enabled in enables:
            if enabled in by_id:
                main_lines.append(f"    {sid.replace(':', '_')} --> {enabled.replace(':', '_')}")
    
    # Add styling for main diagram
    main_lines.append("")
    for cat, color in category_colors.items():
        if cat in categories:
            for sid in categories[cat]:
                if sid in connected_nodes:
                    main_lines.append(f"    style {sid.replace(':', '_')} {color}")
    
    # Add click events for main diagram
    main_lines.append("")
    for sid, s in by_id.items():
        if sid in connected_nodes:
            label = s.get('name', sid)
            slug = slugify(label)
            safe_label = label.replace('"', '\\"')
            main_lines.append(f"    click {sid.replace(':', '_')} \"../usecases/{slug}/\" \"{safe_label}\"")
    
    main_lines.append("```")
    main_diagram = '\n'.join(main_lines)
    
    # Build standalone diagram
    standalone_lines = ["```mermaid", "flowchart LR"]
    
    if unconnected_nodes:
        # Group unconnected nodes by category
        unconnected_by_category = {}
        for sid in unconnected_nodes:
            s = by_id[sid]
            cat = s.get('use_case_category', ['other'])
            if isinstance(cat, list):
                cat = cat[0] if cat else 'other'
            if cat not in unconnected_by_category:
                unconnected_by_category[cat] = []
            unconnected_by_category[cat].append(sid)
        
        # Create subgraphs for each category
        for cat, cat_nodes in unconnected_by_category.items():
            if len(cat_nodes) > 1:
                cat_title = cat.replace('_', ' ').title()
                standalone_lines.append(f"    subgraph {cat}_standalone [\"{cat_title}\"]")
                standalone_lines.append("        direction LR")
                
                for sid in cat_nodes:
                    s = by_id[sid]
                    label = s.get('name', sid)
                    if len(label) > 50:
                        label = label[:47] + "..."
                    label = label.replace('"', '\\"').replace('[', '&#91;').replace(']', '&#93;')
                    standalone_lines.append(f"        {sid.replace(':', '_')}[\"{label}\"]")
                standalone_lines.append("    end")
            else:
                for sid in cat_nodes:
                    s = by_id[sid]
                    label = s.get('name', sid)
                    if len(label) > 50:
                        label = label[:47] + "..."
                    label = label.replace('"', '\\"').replace('[', '&#91;').replace(']', '&#93;')
                    standalone_lines.append(f"    {sid.replace(':', '_')}[\"{label}\"]")
        
        # Add styling for standalone diagram
        standalone_lines.append("")
        for cat, color in category_colors.items():
            if cat in categories:
                for sid in categories[cat]:
                    if sid in unconnected_nodes:
                        standalone_lines.append(f"    style {sid.replace(':', '_')} {color}")
        
        # Add click events for standalone diagram
        standalone_lines.append("")
        for sid in unconnected_nodes:
            s = by_id[sid]
            label = s.get('name', sid)
            slug = slugify(label)
            safe_label = label.replace('"', '\\"')
            standalone_lines.append(f"    click {sid.replace(':', '_')} \"../usecases/{slug}/\" \"{safe_label}\"")
    
    standalone_lines.append("```")
    standalone_diagram = '\n'.join(standalone_lines)
    
    return main_diagram, standalone_diagram


def inject_overview(main_diagram: str, standalone_diagram: str):
    # Define markers for both diagrams
    main_marker_start = "<!-- USECASE_MAIN_DIAGRAM_START -->"
    main_marker_end = "<!-- USECASE_MAIN_DIAGRAM_END -->"
    standalone_marker_start = "<!-- USECASE_STANDALONE_DIAGRAM_START -->"
    standalone_marker_end = "<!-- USECASE_STANDALONE_DIAGRAM_END -->"
    
    if OVERVIEW_PATH.exists():
        with open(OVERVIEW_PATH, 'r') as f:
            content = f.read()
    else:
        content = ''
    
    main_block = f"{main_marker_start}\n{main_diagram}\n{main_marker_end}"
    standalone_block = f"{standalone_marker_start}\n{standalone_diagram}\n{standalone_marker_end}"
    
    # Handle existing content with markers
    if main_marker_start in content and main_marker_end in content:
        content = re.sub(f"{main_marker_start}.*?{main_marker_end}", main_block, content, flags=re.DOTALL)
        if standalone_marker_start in content and standalone_marker_end in content:
            content = re.sub(f"{standalone_marker_start}.*?{standalone_marker_end}", standalone_block, content, flags=re.DOTALL)
        else:
            # Add standalone diagram after main diagram
            content = content.replace(main_marker_end, f"{main_marker_end}\n\n## Standalone Use Cases\n\nThe following use cases operate independently without direct dependencies on other use cases:\n\n{standalone_block}")
    else:
        # Create new content with both diagrams
        new_content = f"""# Use Cases in the Bridge2AI Standards Explorer

The Bridge2AI project defines various use cases that represent different stages and activities in biomedical data workflows. These use cases are organized into categories and show relationships through enabling dependencies.

## Use Case Categories

The colors in the diagrams below represent different categories of use cases:

<div style="display: flex; flex-wrap: wrap; gap: 20px; margin: 20px 0;">
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 20px; height: 20px; background-color: #e1f5fe; border: 1px solid #ccc; border-radius: 3px;"></div>
    <strong>Acquisition</strong>: Use cases focused on obtaining and collecting data from various sources
  </div>
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 20px; height: 20px; background-color: #f3e5f5; border: 1px solid #ccc; border-radius: 3px;"></div>
    <strong>Integration</strong>: Use cases that combine or link data from multiple sources
  </div>
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 20px; height: 20px; background-color: #e8f5e8; border: 1px solid #ccc; border-radius: 3px;"></div>
    <strong>Standardization</strong>: Use cases that establish consistent formats and quality standards
  </div>
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 20px; height: 20px; background-color: #fff3e0; border: 1px solid #ccc; border-radius: 3px;"></div>
    <strong>Modeling</strong>: Use cases that develop analytical or predictive models from data
  </div>
</div>

## Main Use Cases

{main_block}

## Standalone Use Cases

{standalone_block}

"""
        content = new_content
    
    with open(OVERVIEW_PATH, 'w') as f:
        f.write(content)


def main():
    usecases = load_data()
    by_id, enabled_by, roots = build_index(usecases)
    write_pages(by_id)
    main_diagram, standalone_diagram = build_mermaid_diagrams(by_id, enabled_by, roots)
    inject_overview(main_diagram, standalone_diagram)
    print(f"Generated {len(by_id)} use case pages and updated overview with two diagrams.")


if __name__ == '__main__':
    main()