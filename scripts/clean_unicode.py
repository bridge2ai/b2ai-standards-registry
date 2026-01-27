#!/usr/bin/env python3
"""
Normalize typographic Unicode punctuation to ASCII for data files.
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import sys
import unicodedata
from typing import Counter, Dict, List

# Map of characters we want to normalize to ASCII-friendly forms.
REPLACEMENTS: Dict[str, str] = {
    "\u2013": "-",   # en dash
    "\u2014": "--",  # em dash
    "\u2018": "'",   # left single quote
    "\u2019": "'",   # right single quote
    "\u201c": '"',   # left double quote
    "\u201d": '"',   # right double quote
    "\u2212": "-",   # minus sign
    "\u00a0": " ",  # non-breaking space
}


def normalize_text(text: str) -> tuple[str, Counter[str]]:
    """Return normalized text and a counter of replaced characters."""
    replaced: Counter[str] = collections.Counter()
    for source, target in REPLACEMENTS.items():
        hits = text.count(source)
        if hits:
            replaced[source] = hits
            text = text.replace(source, target)
    return text, replaced


def collect_non_ascii(text: str) -> Counter[str]:
    """Return counts of remaining non-ASCII characters."""
    return collections.Counter(ch for ch in text if ord(ch) > 127)


def describe_char(ch: str) -> str:
    """Return a readable description for a character."""
    codepoint = f"U+{ord(ch):04X}"
    name = unicodedata.name(ch, "<unknown>")
    display = ch if ch.isprintable() and ch not in {
        " ", "\t", "\n", "\r"} else repr(ch)
    return f"{display} ({codepoint}, {name})"


def process_path(path: pathlib.Path, dry_run: bool) -> dict:
    original = path.read_text(encoding="utf-8")
    normalized, replaced = normalize_text(original)
    remaining = collect_non_ascii(normalized)
    changed = normalized != original
    if changed and not dry_run:
        path.write_text(normalized, encoding="utf-8")
    return {
        "path": path,
        "changed": changed,
        "replaced": replaced,
        "remaining": remaining,
    }


def print_report(report: dict, limit: int) -> None:
    path = report["path"]
    replaced = report["replaced"]
    remaining = report["remaining"]
    total_replaced = sum(replaced.values())
    status = "modified" if report["changed"] else "unchanged"
    print(f"{path}: {status}; replaced {total_replaced} characters")
    if replaced:
        details = ", ".join(
            f"{describe_char(ch)} x{count}" for ch, count in replaced.most_common()
        )
        print(f"  Applied replacements: {details}")
    if remaining:
        unique_count = len(remaining)
        print(f"  Remaining non-ASCII characters ({unique_count} unique):")
        for ch, count in remaining.most_common(limit):
            print(f"    {describe_char(ch)} x{count}")
        if unique_count > limit:
            print(f"    ... {unique_count - limit} more unique characters")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize typographic Unicode punctuation to ASCII for YAML data files."
    )
    parser.add_argument("paths", nargs="+",
                        type=pathlib.Path, help="Files to clean.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report changes without writing files.",
    )
    parser.add_argument(
        "--fail-on-remaining",
        action="store_true",
        help="Exit with code 1 if any non-ASCII characters remain after normalization.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of distinct remaining characters to display (default: 20).",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    reports = [process_path(path, dry_run=args.dry_run) for path in args.paths]

    exit_code = 0
    for report in reports:
        print_report(report, args.limit)
        if args.fail_on_remaining and report["remaining"]:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
