#!/usr/bin/env python3
"""Generate Markdown table from Manifest.yaml for documentation.

This script reads the Manifest.yaml file and creates a formatted Markdown table
showing all data parts grouped by their parent B2AI_MANIFEST ID, with linked
identifiers for standards, substrates, topics, and anatomy terms.
"""
from __future__ import annotations
from id_linking import load_all_b2ai_data, convert_ids_to_links, convert_anatomy_links
import sys
from pathlib import Path
import yaml

# Add the utils directory to the path to import id_linking
sys.path.insert(0, str(Path(__file__).parent))


def load_manifest(manifest_path: Path) -> list:
    """Load the Manifest.yaml file."""
    with open(manifest_path, 'r') as f:
        data = yaml.safe_load(f)
        return data.get('manifest_collection', [])


def load_organizations(org_path: Path) -> dict:
    """Load organization data."""
    with open(org_path, 'r') as f:
        data = yaml.safe_load(f)
        orgs = data.get('organizations', [])
        return {org['id']: org for org in orgs}


def format_list_with_links(items: list | None, all_data: dict, prefix: str = "") -> str:
    """Format a list of IDs with their names and links."""
    if not items:
        return ""

    formatted = []
    for item in items:
        item_str = str(item)
        # Convert the ID to a link
        linked = convert_ids_to_links(
            item_str, all_data, relative_path_prefix=".")
        formatted.append(linked)

    return f"{prefix}{', '.join(formatted)}" if formatted else ""


def format_anatomy_list(anatomy_items: list | None) -> str:
    """Format anatomy terms (UBERON, CLO, etc.) with OBO Library links."""
    if not anatomy_items:
        return ""

    # Convert to OBO Library PURL links
    linked_anatomy = convert_anatomy_links(anatomy_items)
    return ", ".join(linked_anatomy)


def generate_manifest_table(manifest_path: Path, output_path: Path):
    """Generate the manifest table and write to output file."""
    repo_root = manifest_path.parent.parent.parent

    # Load all necessary data
    manifests = load_manifest(manifest_path)
    all_data = load_all_b2ai_data()
    organizations = load_organizations(
        repo_root / 'src' / 'data' / 'Organization.yaml')

    # Start building the markdown content
    lines = []
    lines.append("# Bridge2AI Data Manifest\n")
    lines.append("This page provides a comprehensive manifest of all data subsets, standards, substrates, topics, and relevant anatomy used across the Bridge2AI consortium.\n")
    lines.append(
        "Each data part is listed with its associated metadata and standards.\n")

    # Process each manifest entry
    for manifest in manifests:
        manifest_id = manifest.get('id', 'Unknown')

        # Get organization info
        org_ids = manifest.get('organization', [])
        org_names = []
        for org_id in org_ids:
            if org_id in organizations:
                org_names.append(organizations[org_id].get('name', org_id))
            else:
                org_names.append(org_id)
        org_str = ", ".join(org_names) if org_names else "Unknown"

        # Add section header for each Grand Challenge
        lines.append(f"\n## {manifest_id}: {org_str}\n")

        # Create table header for this manifest
        lines.append("\n| Data Part | Description | Standards & Tools | Substrates | Topics | Anatomy |")
        lines.append("|-----------|-------------|-------------------|------------|--------|---------|")

        # Process data parts
        data_parts = manifest.get('data_parts', [])
        if data_parts:
            for part in data_parts:
                name = part.get('data_part_name', 'Unnamed')
                description = part.get('data_part_description', '')

                # Format standards and tools
                standards = part.get('standards_and_tools', [])
                standards_str = format_list_with_links(standards, all_data)

                # Format substrates
                substrates = part.get('uses_data_substrates', [])
                substrates_str = format_list_with_links(substrates, all_data)

                # Format topics
                topics = part.get('concerns_data_topics', [])
                topics_str = format_list_with_links(topics, all_data)

                # Format anatomy
                anatomy = part.get('anatomy', [])
                anatomy_str = format_anatomy_list(anatomy)

                # Escape pipe characters in text
                name = name.replace('|', '\\|')
                description = description.replace('|', '\\|')

                lines.append(
                    f"| {name} | {description} | {standards_str} | {substrates_str} | {topics_str} | {anatomy_str} |")
        
        lines.append("")  # Add blank line after each table

    # Write to output file
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"Manifest table generated successfully at {output_path}")


def main():
    """Main entry point."""
    repo_root = Path(__file__).resolve().parent.parent
    manifest_path = repo_root / 'src' / 'data' / 'Manifest.yaml'
    output_path = repo_root / 'docs' / 'manifest.md'

    if not manifest_path.exists():
        print(f"Error: Manifest file not found at {manifest_path}")
        sys.exit(1)

    generate_manifest_table(manifest_path, output_path)


if __name__ == '__main__':
    main()
