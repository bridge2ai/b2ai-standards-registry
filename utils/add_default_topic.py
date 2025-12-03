#!/usr/bin/env python3

import yaml
import os

# Path to the YAML file
file_path = os.path.join('src', 'data', 'DataStandardOrTool.yaml')

# Read the YAML file
with open(file_path, 'r') as file:
    data = yaml.safe_load(file)

# Count entries before modification
count_modified = 0

# Process each entry in the collection
for entry in data['data_standardortools_collection']:
    # Check if the entry doesn't have concerns_data_topic
    if 'concerns_data_topic' not in entry:
        # Add the default concerns_data_topic
        entry['concerns_data_topic'] = ['B2AI_TOPIC:5']
        count_modified += 1

# Save the modified data back to the file
with open(file_path, 'w') as file:
    yaml.dump(data, file, sort_keys=False)

print(
    f"Modified {count_modified} entries, adding default concerns_data_topic: B2AI_TOPIC:5")
