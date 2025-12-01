#!/usr/bin/env python3
"""Fix overlapping organization roles in DataStandardOrTool.yaml.

For each B2AI_STANDARD entry, if an organization ID appears in both
`responsible_organization` and `has_relevant_organization`, remove it from
`has_relevant_organization` (the more specific role wins).

Usage:
  - Dry run (default): shows what would change
      poetry run python utils/fix_org_roles.py

  - Write cleaned file in place:
      poetry run python utils/fix_org_roles.py --write

  - Write to a separate output path:
      poetry run python utils/fix_org_roles.py --output tmp/DataStandardOrTool.cleaned.yaml
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple
import sys

import yaml


def load_yaml(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def dump_yaml(data: Dict[str, Any], path: Path) -> None:
    # Use safe_dump with explicit start for cleanliness and preserve key order
    with open(path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def unique_preserve_order(seq: List[Any]) -> List[Any]:
    seen = set()
    out: List[Any] = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def fix_overlaps(standards: List[Dict[str, Any]]) -> Tuple[int, List[Dict[str, Any]]]:
    """Remove overlaps from has_relevant_organization for each standard.

    Returns a tuple of (changed_count, change_details) where change_details is a list of
    dicts with keys: id, removed, before, after.
    """
    changed = 0
    details: List[Dict[str, Any]] = []

    for item in standards:
        std_id = item.get("id", "<unknown>")
        relevant = item.get("has_relevant_organization")
        responsible = item.get("responsible_organization")

        if not relevant or not responsible:
            # Nothing to fix for this item (missing either list)
            continue

        # Normalize to lists of strings
        relevant_list = [str(x) for x in relevant]
        responsible_set = {str(x) for x in responsible}

        before = list(relevant_list)
        # Remove any org appearing in responsible
        filtered = [x for x in relevant_list if x not in responsible_set]
        # De-dup while preserving order
        filtered = unique_preserve_order(filtered)

        if filtered != relevant_list:
            changed += 1
            removed = [x for x in relevant_list if x not in filtered]
            # If empty, drop the key; otherwise, update
            if filtered:
                item["has_relevant_organization"] = filtered
            else:
                item.pop("has_relevant_organization", None)

            details.append({
                "id": std_id,
                "removed": removed,
                "before": before,
                "after": item.get("has_relevant_organization", []),
            })

    return changed, details


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    repo_root = Path(__file__).resolve().parent.parent
    default_input = repo_root / "src" / "data" / "DataStandardOrTool.yaml"

    parser.add_argument(
        "--input",
        type=Path,
        default=default_input,
        help=f"Path to DataStandardOrTool.yaml (default: {default_input})",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write changes back to the input file (in place).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output path to write the cleaned YAML (overrides --write).",
    )

    args = parser.parse_args()

    data = load_yaml(args.input)
    collection_key = "data_standardortools_collection"
    standards = data.get(collection_key)
    if not isinstance(standards, list):
        print(f"ERROR: Could not find list at key '{collection_key}' in {args.input}", file=sys.stderr)
        return 2

    changed_count, changes = fix_overlaps(standards)

    if changed_count == 0:
        print("No overlaps found. Nothing to change.")
    else:
        print(f"Found {changed_count} entr{'y' if changed_count == 1 else 'ies'} with overlaps.\n")
        for c in changes:
            print(f"- {c['id']}: removed from has_relevant_organization -> {c['removed']}")

    # Decide on output
    if args.output:
        dump_yaml(data, args.output)
        print(f"\nWrote cleaned file to: {args.output}")
    elif args.write:
        dump_yaml(data, args.input)
        print(f"\nUpdated file in place: {args.input}")
    else:
        print("\nDry run only (no files written). Use --write to update in place or --output to write to a new file.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
