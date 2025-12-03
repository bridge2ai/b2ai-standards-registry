#!/usr/bin/env python3

import csv
import ast
import logging
from pathlib import Path
from ruamel.yaml import YAML
from io import StringIO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def sort_keys(data):
    """
    Recursively sorts keys in a dictionary, placing 'id' first if present.
    This follows the repository's YAML formatting style.

    :param data: .yml/.yaml data to sort. Can be: dict, list or scalar.
    :return: The sorted data structure with 'id' placed first and other keys in alphabetical order.
    """
    if isinstance(data, dict):
        sorted_dict = {}
        keys = list(data.keys())
        if "id" in keys:
            sorted_dict["id"] = sort_keys(data["id"])
        for key in sorted((k for k in keys if k != "id"), key=lambda x: str(x)):
            sorted_dict[key] = sort_keys(data[key])
        return sorted_dict
    elif isinstance(data, list):
        return [sort_keys(item) for item in data]
    else:
        return data


def main():
    """
    Main function that reads datatypes.csv and updates DataStandardOrTool.yaml with
    has_relevant_data_substrate values.
    """
    repo_path = Path('/home/harry/b2ai-standards-registry')
    csv_path = repo_path / 'datatypes.csv'
    yaml_path = repo_path / 'src' / 'data' / 'DataStandardOrTool.yaml'

    # Initialize YAML with proper formatting settings
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True
    yaml.width = 4096

    # Read datatypes.csv
    substrate_mappings = {}
    try:
        with open(csv_path, 'r') as f:
            csv_reader = csv.reader(f)
            header = next(csv_reader)  # Skip header
            for row in csv_reader:
                if len(row) >= 2:
                    standard_id = row[0]
                    # Safely evaluate the list string
                    substrate_values = ast.literal_eval(row[1])
                    substrate_mappings[standard_id] = substrate_values

        logging.info(
            f"Read {len(substrate_mappings)} mappings from {csv_path}")
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        return

    # Read DataStandardOrTool.yaml
    try:
        with open(yaml_path, 'r') as f:
            standards_data = yaml.load(f)

        logging.info(f"Loaded standards data from {yaml_path}")
    except Exception as e:
        logging.error(f"Error reading YAML file: {e}")
        return

    # Update standards with substrate information
    standards_collection = standards_data.get(
        'data_standardortools_collection', [])
    update_count = 0

    for standard in standards_collection:
        standard_id = standard.get('id')
        if standard_id in substrate_mappings:
            # Add or update has_relevant_data_substrate
            standard['has_relevant_data_substrate'] = substrate_values = substrate_mappings[standard_id]
            update_count += 1

    logging.info(
        f"Updated {update_count} standards with substrate information")

    # Sort the data according to repository's style
    standards_data = sort_keys(standards_data)

    # Write updated YAML back to file
    try:
        with open(yaml_path, 'w') as f:
            yaml.dump(standards_data, f)

        logging.info(f"Successfully wrote updated data to {yaml_path}")
    except Exception as e:
        logging.error(f"Error writing YAML file: {e}")
        return


if __name__ == "__main__":
    main()
