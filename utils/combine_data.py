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
            container_class = next(iter(data.values()))  # Get the first (and only) value which is the container class
            for item in container_class:
                combined_data.append([item.get('id'), item.get('name')])

# Write the combined data to a TSV file
with open(output_file, 'w', newline='') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    writer.writerow(['id', 'name'])  # Write header
    writer.writerows(combined_data)