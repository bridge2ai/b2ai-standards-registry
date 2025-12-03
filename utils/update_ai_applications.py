#!/usr/bin/env python3
"""
Script to update DataStandardOrTool.yaml entries with has_ai_application tag.

This script:
1. Finds all entries with 'has_ai_application' in their collection
2. Removes the 'has_ai_application' tag from the collection
3. Adds 'has_application' slot with inline Application objects
4. Each Application object contains:
   - id: Unique identifier (B2AI_APP:XXX)
   - category: B2AI:Application
   - name: Placeholder name
   - description: Placeholder description referencing the standard
   - used_in_bridge2ai: False (default)
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any


def load_yaml_file(filepath: Path) -> Dict[str, Any]:
    """Load YAML file preserving order and structure."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml_file(filepath: Path, data: Dict[str, Any]) -> None:
    """Save YAML file with proper formatting."""
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False,
                  allow_unicode=True, width=float("inf"))


def update_entries(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update entries that have has_ai_application tag.

    Returns:
        Updated data dictionary
    """
    entries = data.get('data_standardortools_collection', [])
    app_counter = 1
    updated_count = 0

    for entry in entries:
        collection = entry.get('collection', [])

        # Check if entry has has_ai_application tag
        if 'has_ai_application' in collection:
            print(f"Processing: {entry.get('id')} - {entry.get('name')}")

            # Remove has_ai_application from collection
            collection.remove('has_ai_application')

            # Remove collection slot if it's now empty
            if collection:
                entry['collection'] = collection
            elif 'collection' in entry:
                del entry['collection']

            # Create unique Application ID (without leading zeros)
            app_id = f"B2AI_APP:{app_counter}"

            # Create inline Application object with placeholder values
            application = {
                'id': app_id,
                'category': 'B2AI:Application',
                'name': f'Placeholder Application {app_counter}',
                'description': f'AI application for {entry.get("name", "unknown standard")} - needs detailed description',
                'used_in_bridge2ai': False
            }

            # Add has_application slot with inline Application object
            entry['has_application'] = [application]

            app_counter += 1
            updated_count += 1

    print(f"\nTotal entries updated: {updated_count}")

    return data


def main():
    """Main function to process the YAML file."""
    # Path to the data file
    data_file = Path(__file__).parent / 'src' / \
        'data' / 'DataStandardOrTool.yaml'

    print(f"Loading data from: {data_file}")

    # Load the YAML file
    data = load_yaml_file(data_file)

    # Update entries
    updated_data = update_entries(data)

    # Remove applications_collection if it exists (we're using inline now)
    if 'applications_collection' in updated_data:
        del updated_data['applications_collection']

    # Create backup
    backup_file = data_file.with_suffix('.yaml.backup')
    print(f"\nCreating backup at: {backup_file}")
    import shutil
    shutil.copy(data_file, backup_file)

    # Save updated data
    print(f"Saving updated data to: {data_file}")
    save_yaml_file(data_file, updated_data)

    print("\nUpdate complete!")
    print(f"Backup saved to: {backup_file}")


if __name__ == '__main__':
    main()
