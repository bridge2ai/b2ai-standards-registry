"""A script to get all entries in the registry."""

import os
import yaml
import csv

# Directory containing YAML files
directory = './src/data/'

# Output TSV file
output_file = 'all_ids.tsv'

# List to store the combined data
combined_data = []

# Iterate through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.yaml') or filename.endswith('.yml'):
        with open(os.path.join(directory, filename), 'r') as file:
            data = yaml.safe_load(file)
            # Get the first (and only) value which is the container class
            container_class = next(iter(data.values()))
            for item in container_class:
                item_id = item.get('id')
                item_name = item.get('name')

                # Manifest entries do not have a native name field, so use the
                # owning organization identifier in the exported name column.
                if item_id and item_id.startswith('B2AI_MANIFEST:') and not item_name:
                    item_name = item.get('organization')

                combined_data.append([item_id, item_name])

# Write the combined data to a TSV file
with open(output_file, 'w', newline='') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
    writer.writerow(['id', 'name'])  # Write header
    writer.writerows(combined_data)
