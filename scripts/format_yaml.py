#!/usr/bin/env python3

import sys
from ruamel.yaml import YAML
from io import StringIO
from typing import Any, Generator
from pathlib import Path

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.preserve_quotes = True
yaml.width = 4096

def sort_keys(data: Any) -> Any:
    """
    Recursively sorts keys in a dictionary, placing 'id' first if present.

    Args:
        data: .yml/.yaml data to sort. Can be: dict, list or scalar.

    Returns:
        The sorted data structure with 'id' placed first and other keys in alphabetical order.
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

def format_yaml_file(filepath: Path, check: bool = False) -> bool:
    """
    Formats a .yml/.yaml file by sorting its keys and writing the changes back to the original file.

    Args:
        filepath: Path to the .yaml file.
        check: If True, compares if the formatted file is different from the original.

    Returns:
        True if the file was changed or would be reformatted, False otherwise.
    """
    try:
        original = filepath.read_text()
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
            filepath.write_text(formatted)
            print(f"Formatted: {filepath}")
        return True

    return False

def find_yaml_files(root_dir: Path = Path(".")) -> Generator[Path, None, None]:
    """
    Recursively finds all .yaml and .yml files starting from the given directory.

    Args:
        root_dir: Root directory to search from as a Path object.

    Yields:
        Path objects pointing to .yaml files.
    """
    yield from root_dir.rglob("*.yml")
    yield from root_dir.rglob("*.yaml")

def main() -> None:
    args = sys.argv[1:]
    check_mode = "--check" in args
    files = [Path(arg) for arg in args if not arg.startswith("-")]

    if not files:
        files = list(find_yaml_files(Path(".")))

    any_changed = False
    for filepath in files:
        if not filepath.is_relative_to(Path("src/data")):
            continue
        if filepath.suffix in (".yaml", ".yml"):
            changed = format_yaml_file(filepath, check=check_mode)
            if changed:
                any_changed = True

    if check_mode and any_changed:
        print("\nSome files would be reformatted. Run without --check to apply changes.")
        sys.exit(1)

if __name__ == "__main__":
    main()