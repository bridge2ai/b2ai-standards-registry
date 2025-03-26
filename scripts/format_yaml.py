#!/usr/bin/env python3

import os
import sys
from ruamel.yaml import YAML

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.preserve_quotes = True
yaml.width = 4096

def sort_keys(data):
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

def format_yaml_file(filepath):
    with open(filepath, "r") as f:
        try:
            data = yaml.load(f)
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return

    data = sort_keys(data)

    with open(filepath, "w") as f:
        yaml.dump(data, f)
    print(f"Formatted: {filepath}")

def find_yaml_files(root_dir="."):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith((".yaml", ".yml")):
                yield os.path.join(dirpath, filename)

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    for filepath in find_yaml_files(root):
        format_yaml_file(filepath)

if __name__ == "__main__":
    main()
