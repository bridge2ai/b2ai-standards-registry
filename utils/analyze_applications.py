#!/usr/bin/env python3
"""
Analyze DataStandardOrTool.yaml to find entries with single applications
and their reference status.
"""

import re
from pathlib import Path


def analyze_applications(yaml_file):
    """Analyze applications in the YAML file by parsing line by line."""
    with open(yaml_file, 'r') as f:
        lines = f.readlines()

    single_app_entries = []
    current_entry = None
    in_application = False
    in_first_app = False
    app_count = 0
    app_id = None
    app_name = None
    ref_count = 0
    in_references = False

    for i, line in enumerate(lines):
        # Start of a new entry
        if line.startswith('- id: B2AI_STANDARD:'):
            # Save previous entry if it had exactly one application
            if current_entry and app_count == 1:
                single_app_entries.append({
                    'id': current_entry['id'],
                    'name': current_entry['name'],
                    'app_id': app_id,
                    'app_name': app_name,
                    'has_references': ref_count > 0,
                    'ref_count': ref_count
                })

            # Start new entry
            current_entry = {'id': line.split(
                'id:')[1].strip(), 'name': 'Unknown'}
            in_application = False
            in_first_app = False
            app_count = 0
            app_id = None
            app_name = None
            ref_count = 0
            in_references = False

        # Get the standard name
        elif current_entry and line.strip().startswith('name:') and not in_application:
            current_entry['name'] = line.split('name:', 1)[1].strip()

        # Start of has_application section
        elif line.strip() == 'has_application:':
            in_application = True

        # Count applications
        elif in_application and re.match(r'\s+- id: B2AI_APP:', line):
            app_count += 1
            if app_count == 1:
                in_first_app = True
                app_id = line.split('id:')[1].strip()
            elif app_count == 2:
                in_first_app = False
                in_references = False

        # Get application name (only for first app)
        elif in_first_app and line.strip().startswith('name:'):
            app_name = line.split('name:', 1)[1].strip()

        # Detect start of references section
        elif in_first_app and line.strip() == 'references:':
            in_references = True

        # Count references in first app
        elif in_first_app and in_references and re.match(r'\s+- ', line):
            ref_count += 1

        # End of has_application section (next top-level key starting at column 0)
        elif in_application and len(line) > 0 and line[0] not in [' ', '-', '\n']:
            in_application = False
            in_first_app = False
            in_references = False

    # Handle last entry
    if current_entry and app_count == 1:
        single_app_entries.append({
            'id': current_entry['id'],
            'name': current_entry['name'],
            'app_id': app_id,
            'app_name': app_name,
            'has_references': ref_count > 0,
            'ref_count': ref_count
        })

    # Separate into with and without references
    with_refs = [e for e in single_app_entries if e['has_references']]
    without_refs = [e for e in single_app_entries if not e['has_references']]

    return single_app_entries, with_refs, without_refs


def generate_markdown_table(entries, with_refs, without_refs):
    """Generate a Markdown table of the results."""
    md = "# Applications Analysis for DataStandardOrTool\n\n"

    md += f"## Summary\n\n"
    md += f"- **Total entries with single application**: {len(entries)}\n"
    md += f"- **With references**: {len(with_refs)}\n"
    md += f"- **Without references**: {len(without_refs)}\n\n"

    md += "## Entries with Single Application (No References)\n\n"
    md += "| Standard ID | Standard Name | Application ID | Application Name | References |\n"
    md += "|-------------|---------------|----------------|------------------|------------|\n"

    for entry in without_refs:
        app_name_display = entry['app_name'][:80] + \
            '...' if len(entry['app_name']) > 80 else entry['app_name']
        md += f"| {entry['id']} | {entry['name']} | {entry['app_id']} | {app_name_display} | {entry['ref_count']} |\n"

    md += f"\n**Count: {len(without_refs)} entries**\n\n"

    md += "## Entries with Single Application (With References)\n\n"
    md += "| Standard ID | Standard Name | Application ID | Application Name | References |\n"
    md += "|-------------|---------------|----------------|------------------|------------|\n"

    for entry in with_refs:
        app_name_display = entry['app_name'][:80] + \
            '...' if len(entry['app_name']) > 80 else entry['app_name']
        md += f"| {entry['id']} | {entry['name']} | {entry['app_id']} | {app_name_display} | {entry['ref_count']} |\n"

    md += f"\n**Count: {len(with_refs)} entries**\n"

    return md


if __name__ == '__main__':
    yaml_file = Path(__file__).parent / 'src' / \
        'data' / 'DataStandardOrTool.yaml'

    entries, with_refs, without_refs = analyze_applications(yaml_file)

    markdown = generate_markdown_table(entries, with_refs, without_refs)

    print(markdown)
