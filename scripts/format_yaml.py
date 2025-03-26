#!/usr/bin/env python3

import os
import sys
from ruamel.yaml import YAML
from io import StringIO

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

def format_yaml_file(filepath, check=False):
    with open(filepath, "r") as f:
        try:
            original = f.read()
            data = yaml.load(original)
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return False

    data = sort_keys(data)

    out = StringIO()
    yaml.dump(data, out)
    formatted = out.getvalue()

    if formatted != original:
        if check:
            print(f"{filepath} - would be reformatted")
        else:
            with open(filepath, "w") as f:
                f.write(formatted)
            print(f"Formatted: {filepath}")
        return True

    return False

def find_yaml_files(root_dir="."):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith((".yaml", ".yml")):
                yield os.path.join(dirpath, filename)

def main():
    args = sys.argv[1:]
    check_mode = "--check" in args
    files = [arg for arg in args if not arg.startswith("-")]

    if not files:
        files = list(find_yaml_files("."))

    any_changed = False
    for filepath in files:
        if filepath.endswith((".yaml", ".yml")):
            changed = format_yaml_file(filepath, check=check_mode)
            if changed:
                any_changed = True

    if check_mode and any_changed:
        print("\nSome files would be reformatted. Run without --check to apply changes.")
        sys.exit(1)

if __name__ == "__main__":
    main()
