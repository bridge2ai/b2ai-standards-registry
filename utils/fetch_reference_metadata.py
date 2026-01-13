#!/usr/bin/env python3
"""Lookup reference metadata from CrossRef, arXiv, and GitHub.

This helper script fetches publication metadata for DOIs (CrossRef),
arXiv links/IDs, and GitHub repositories, formatting them as Reference
objects defined in the standards schema. It can:

- Fetch a single DOI/URL and print the Reference object
- Update src/data/DataStandardOrTool.yaml in-place (or to a new file)
    so publication and application references use full Reference objects

Examples:
    # Print metadata for a single DOI
    python utils/fetch_reference_metadata.py --doi 10.1093/bioinformatics/btq391

    # Print metadata for an arXiv link
    python utils/fetch_reference_metadata.py --doi https://arxiv.org/abs/1904.03323

    # Print metadata for a GitHub repo link
    python utils/fetch_reference_metadata.py --doi https://github.com/NVIDIA/Megatron-LM

    # Print metadata for a generic web page (title-only fallback)
    python utils/fetch_reference_metadata.py --doi https://ceur-ws.org/Vol-2849/paper-21.pdf

    # Update the registry data file in-place (default) with a short delay
    python utils/fetch_reference_metadata.py --write --delay 0.2

    # Dry-run: show stats only (default behavior without --write)
    python utils/fetch_reference_metadata.py --verbose
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import quote

import requests
import yaml

CROSSREF_WORKS_URL = "https://api.crossref.org/works/"
ARXIV_API_URL = "https://export.arxiv.org/api/query?id_list="
GITHUB_API_URL = "https://api.github.com/repos/"
DOI_PATTERN = re.compile(r"10\.\d{4,9}/\S+", re.IGNORECASE)
ARXIV_PATTERN = re.compile(
    r"arxiv\.org/(abs|pdf)/([A-Za-z0-9._-]+)", re.IGNORECASE)
GITHUB_REPO_PATTERN = re.compile(r"github\.com/([^/]+)/([^/#?]+)")
TITLE_PATTERN = re.compile(
    r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def build_user_agent(mailto: Optional[str]) -> str:
    base = "b2ai-standards-registry/metadata-enricher"
    if mailto:
        return f"{base} (mailto:{mailto})"
    return base


def extract_doi(raw: str) -> Optional[str]:
    """Normalize a DOI or DOI URL to bare DOI form."""
    if not raw:
        return None

    value = str(raw).strip().strip(" .")
    value = re.sub(r"^doi:", "", value, flags=re.IGNORECASE)
    prefixes = (
        "https://doi.org/",
        "http://doi.org/",
        "http://dx.doi.org/",
    )
    for prefix in prefixes:
        if value.lower().startswith(prefix):
            value = value[len(prefix):]
            break

    if DOI_PATTERN.match(value):
        return value
    return None


def extract_arxiv_id(ref_url: str) -> Optional[str]:
    match = ARXIV_PATTERN.search(ref_url)
    if match:
        return match.group(2)
    return None


def extract_github_repo(ref_url: str) -> Optional[str]:
    match = GITHUB_REPO_PATTERN.search(ref_url)
    if match:
        owner, repo = match.group(1), match.group(2).rstrip(".git")
        return f"{owner}/{repo}"
    return None


def normalize_reference(raw: Any) -> Tuple[str, Optional[str]]:
    """Return (normalized_url, doi) for a reference value."""
    if raw is None:
        return "", None

    if isinstance(raw, dict) and "ref_url" in raw:
        # Already a Reference object
        return str(raw.get("ref_url", "")), extract_doi(raw.get("ref_url", ""))

    text = str(raw).strip()
    doi = extract_doi(text)
    if doi:
        return f"https://doi.org/{doi}", doi
    return text, None


def year_from_date_parts(parts: Any) -> Optional[int]:
    if not parts:
        return None
    date_parts = parts.get("date-parts") if isinstance(parts, dict) else None
    if not date_parts or not isinstance(date_parts, list) or not date_parts[0]:
        return None
    first = date_parts[0]
    if isinstance(first, (list, tuple)) and first:
        year = first[0]
        if isinstance(year, int):
            return year
    return None


def extract_year(message: Dict[str, Any]) -> Optional[int]:
    for key in ("published-print", "published-online", "issued"):
        year = year_from_date_parts(message.get(key))
        if year:
            return year
    return None


def extract_journal(message: Dict[str, Any]) -> Optional[str]:
    for key in ("short-container-title", "container-title"):
        titles = message.get(key) or []
        if isinstance(titles, list) and titles:
            return str(titles[0])
    return None


def format_authors(authors: Iterable[Dict[str, Any]]) -> List[str]:
    formatted: List[str] = []
    for author in authors or []:
        family = author.get("family")
        given = author.get("given")
        if not family and not given:
            continue
        if family and given:
            initials = "".join(part[0]
                               for part in re.split(r"[ \-]", given) if part)
            formatted.append(f"{family} {initials}")
        elif family:
            formatted.append(str(family))
        else:
            formatted.append(str(given))
    return formatted


def fetch_arxiv_metadata(arxiv_id: str, session: requests.Session, delay: float, verbose: bool) -> Optional[Dict[str, Any]]:
    url = f"{ARXIV_API_URL}{quote(arxiv_id)}"
    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        if verbose:
            print(
                f"[warn] arXiv request failed for {arxiv_id}: {exc}", file=sys.stderr)
        time.sleep(delay)
        return None

    try:
        root = ET.fromstring(response.text)
    except ET.ParseError as exc:
        if verbose:
            print(
                f"[warn] arXiv XML parse failed for {arxiv_id}: {exc}", file=sys.stderr)
        return None

    # arXiv Atom feed namespace handling
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entry = root.find("atom:entry", ns)
    if entry is None:
        return None

    def text_or_none(elem_name: str) -> Optional[str]:
        elem = entry.find(elem_name, ns)
        if elem is not None and elem.text:
            return elem.text.strip()
        return None

    title = text_or_none("atom:title")
    summary = text_or_none("atom:summary")
    published = text_or_none("atom:published")
    authors = [a.find("atom:name", ns).text.strip() for a in entry.findall(
        "atom:author", ns) if a.find("atom:name", ns) is not None and a.find("atom:name", ns).text]

    year = None
    if published and len(published) >= 4 and published[:4].isdigit():
        year = int(published[:4])

    return {
        "ref_title": title,
        "ref_authors": authors or None,
        "ref_publication_year": year,
        "ref_journal": "arXiv",
        "ref_summary": summary,
    }


def fetch_github_metadata(repo: str, session: requests.Session, token: Optional[str], delay: float, verbose: bool) -> Optional[Dict[str, Any]]:
    url = f"{GITHUB_API_URL}{repo}"
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = session.get(url, headers=headers, timeout=15)
    except requests.RequestException as exc:
        if verbose:
            print(
                f"[warn] GitHub request failed for {repo}: {exc}", file=sys.stderr)
        time.sleep(delay)
        return None

    if response.status_code == 404:
        if verbose:
            print(f"[warn] GitHub repo not found: {repo}", file=sys.stderr)
        return None
    if response.status_code in (429, 503):
        if verbose:
            print(
                f"[info] GitHub rate limit for {repo}; status {response.status_code}", file=sys.stderr)
        time.sleep(delay)
        return None

    try:
        response.raise_for_status()
        data = response.json()
    except (requests.HTTPError, ValueError) as exc:
        if verbose:
            print(
                f"[warn] GitHub parse failed for {repo}: {exc}", file=sys.stderr)
        return None

    title = data.get("full_name") or data.get("name")
    desc = data.get("description")
    updated = data.get("updated_at")
    year = None
    if updated and len(updated) >= 4 and updated[:4].isdigit():
        year = int(updated[:4])

    metadata: Dict[str, Any] = {
        "ref_title": title,
    }
    if desc:
        metadata["ref_journal"] = "GitHub"
        metadata["ref_authors"] = [data.get("owner", {}).get(
            "login")] if data.get("owner", {}).get("login") else None
        metadata["ref_publication_year"] = year
    return metadata


def fetch_page_title(ref_url: str, session: requests.Session, delay: float, verbose: bool) -> Optional[Dict[str, Any]]:
    """Fetch page title from a generic HTML page. Returns None if not HTML or on error."""

    headers = {"User-Agent": build_user_agent(os.getenv("CROSSREF_MAILTO"))}
    try:
        response = session.get(ref_url, headers=headers,
                               timeout=10, allow_redirects=True)
    except requests.RequestException as exc:
        if verbose:
            print(
                f"[warn] page request failed for {ref_url}: {exc}", file=sys.stderr)
        time.sleep(delay)
        return None

    content_type = (response.headers.get("content-type") or "").lower()
    if "text/html" not in content_type:
        return None

    # Limit read to avoid huge pages
    raw = response.content[:100000]
    try:
        text = raw.decode(response.encoding or "utf-8", errors="ignore")
    except Exception:
        text = raw.decode("utf-8", errors="ignore")

    match = TITLE_PATTERN.search(text)
    if not match:
        return None

    title = html.unescape(match.group(1)).strip()
    title = re.sub(r"\s+", " ", title)
    if not title:
        return None

    return {"ref_title": title, "ref_journal": None, "ref_authors": None, "ref_publication_year": None}


def fetch_crossref_message(
    doi: str,
    session: requests.Session,
    mailto: Optional[str],
    delay: float,
    retries: int = 3,
    timeout: int = 15,
    verbose: bool = False,
) -> Optional[Dict[str, Any]]:
    url = f"{CROSSREF_WORKS_URL}{quote(doi)}"
    headers = {"User-Agent": build_user_agent(mailto)}

    for attempt in range(retries):
        try:
            response = session.get(url, headers=headers, timeout=timeout)
        except requests.RequestException as exc:  # network/timeout errors
            if verbose:
                print(
                    f"[warn] request failed for {doi}: {exc}", file=sys.stderr)
            time.sleep(delay)
            continue

        if response.status_code == 404:
            if verbose:
                print(f"[warn] DOI not found: {doi}", file=sys.stderr)
            return None

        if response.status_code in (429, 503):
            # Too many requests or service unavailable: back off
            sleep_for = delay * (attempt + 1)
            if verbose:
                print(
                    f"[info] rate limited ({response.status_code}) for {doi}; retrying after {sleep_for:.2f}s",
                    file=sys.stderr,
                )
            time.sleep(sleep_for)
            continue

        if response.status_code >= 500:
            sleep_for = delay * (attempt + 1)
            if verbose:
                print(
                    f"[info] server error {response.status_code} for {doi}; retrying after {sleep_for:.2f}s",
                    file=sys.stderr,
                )
            time.sleep(sleep_for)
            continue

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            if verbose:
                print(f"[warn] HTTP error for {doi}: {exc}", file=sys.stderr)
            return None

        try:
            payload = response.json()
        except ValueError as exc:
            if verbose:
                print(
                    f"[warn] JSON decode failed for {doi}: {exc}", file=sys.stderr)
            return None

        return payload.get("message")

    if verbose:
        print(f"[warn] exhausted retries for {doi}", file=sys.stderr)
    return None


def build_reference_object(ref_url: str, message: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    reference: Dict[str, Any] = {"ref_url": ref_url}
    if not message:
        return reference

    # CrossRef-like payload
    if "title" in message or "author" in message:
        titles = message.get("title") or []
        if isinstance(titles, list) and titles:
            reference["ref_title"] = str(titles[0])

        authors = format_authors(message.get("author", []))
        if authors:
            reference["ref_authors"] = authors

        year = extract_year(message)
        if year:
            reference["ref_publication_year"] = year

        journal = extract_journal(message)
        if journal:
            reference["ref_journal"] = journal
        return reference

    # arXiv/GitHub/page metadata shape already matches Reference keys
    for key in ("ref_title", "ref_authors", "ref_publication_year", "ref_journal"):
        if key in message and message[key]:
            reference[key] = message[key]
    return reference


def enrich_value(
    value: Any,
    session: requests.Session,
    cache: Dict[str, Optional[Dict[str, Any]]],
    mailto: Optional[str],
    delay: float,
    verbose: bool,
) -> Tuple[Dict[str, Any], bool, Dict[str, int]]:
    """Return (reference_object, changed, api_stats)."""
    if isinstance(value, dict) and "ref_url" in value:
        return value, False, {"crossref": 0, "arxiv": 0, "github": 0, "web": 0}

    ref_url, doi = normalize_reference(value)
    api_stats = {"crossref": 0, "arxiv": 0, "github": 0, "web": 0}

    message: Optional[Dict[str, Any]] = None
    if doi:
        api_stats["crossref"] = 1
        if doi not in cache:
            cache[doi] = fetch_crossref_message(
                doi, session, mailto, delay, verbose=verbose)
        message = cache[doi]
    else:
        arxiv_id = extract_arxiv_id(ref_url)
        if arxiv_id:
            api_stats["arxiv"] = 1
            cache_key = f"arxiv:{arxiv_id}"
            if cache_key not in cache:
                cache[cache_key] = fetch_arxiv_metadata(
                    arxiv_id, session, delay, verbose)
            message = cache.get(cache_key)
        else:
            gh_repo = extract_github_repo(ref_url)
            if gh_repo:
                api_stats["github"] = 1
                cache_key = f"github:{gh_repo}"
                if cache_key not in cache:
                    cache[cache_key] = fetch_github_metadata(
                        gh_repo,
                        session,
                        token=os.getenv("GITHUB_TOKEN"),
                        delay=delay,
                        verbose=verbose,
                    )
                message = cache.get(cache_key)
            else:
                # Generic web page fallback to extract <title>
                cache_key = f"web:{ref_url}"
                api_stats["web"] = 1
                if cache_key not in cache:
                    cache[cache_key] = fetch_page_title(
                        ref_url, session, delay, verbose)
                message = cache.get(cache_key)
    reference = build_reference_object(ref_url, message)
    return reference, True, api_stats


def enrich_references_list(
    values: List[Any],
    session: requests.Session,
    cache: Dict[str, Optional[Dict[str, Any]]],
    mailto: Optional[str],
    delay: float,
    verbose: bool,
    max_to_process: Optional[int] = None,
    counters: Optional[Dict[str, int]] = None,
) -> List[Any]:
    updated: List[Any] = []
    for idx, value in enumerate(values):
        if max_to_process is not None and idx >= max_to_process:
            updated.append(value)
            continue

        ref_obj, changed, api_stats = enrich_value(
            value, session, cache, mailto, delay, verbose)
        updated.append(ref_obj)

        if counters is not None:
            counters["references_total"] += 1
            if changed:
                counters["references_changed"] += 1
            counters["api_crossref"] += api_stats.get("crossref", 0)
            counters["api_arxiv"] += api_stats.get("arxiv", 0)
            counters["api_github"] += api_stats.get("github", 0)
            counters["api_web"] += api_stats.get("web", 0)
    return updated


def process_data_file(
    input_path: str,
    output_path: str,
    mailto: Optional[str],
    delay: float,
    max_references: Optional[int],
    verbose: bool,
    write: bool,
) -> Dict[str, int]:
    with open(input_path, "r") as handle:
        data = yaml.safe_load(handle)

    counters = {
        "standards_with_publication": 0,
        "publications_enriched": 0,
        "applications_enriched": 0,
        "references_total": 0,
        "references_changed": 0,
        "api_crossref": 0,
        "api_arxiv": 0,
        "api_github": 0,
        "api_web": 0,
    }

    cache: Dict[str, Optional[Dict[str, Any]]] = {}
    session = requests.Session()

    for std in data.get("data_standardortools_collection", []):
        publication = std.get("publication")
        if publication:
            counters["standards_with_publication"] += 1
            ref_obj, changed, api_stats = enrich_value(
                publication, session, cache, mailto, delay, verbose
            )
            if changed:
                std["publication"] = ref_obj
                counters["publications_enriched"] += 1
            counters["api_crossref"] += api_stats.get("crossref", 0)
            counters["api_arxiv"] += api_stats.get("arxiv", 0)
            counters["api_github"] += api_stats.get("github", 0)
            counters["api_web"] += api_stats.get("web", 0)

        if not std.get("has_application"):
            continue

        for app in std["has_application"]:
            refs = app.get("references")
            if not refs:
                continue
            app["references"] = enrich_references_list(
                refs,
                session,
                cache,
                mailto,
                delay,
                verbose,
                max_to_process=max_references,
                counters=counters,
            )
            counters["applications_enriched"] += 1

    if write:
        with open(output_path, "w") as handle:
            yaml.dump(data, handle, default_flow_style=False,
                      sort_keys=False, allow_unicode=True)

    return counters


def print_reference(reference: Dict[str, Any], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(reference, indent=2, ensure_ascii=False))
    else:
        yaml.dump(reference, sys.stdout, default_flow_style=False,
                  sort_keys=False, allow_unicode=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--doi", help="Fetch a single DOI/URL and print the Reference object")
    parser.add_argument(
        "--input",
        default="src/data/DataStandardOrTool.yaml",
        help="Path to the DataStandardOrTool YAML file",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output path. Defaults to the input path when --write is used.",
    )
    parser.add_argument(
        "--mailto",
        default=os.getenv("CROSSREF_MAILTO"),
        help="Contact email for CrossRef User-Agent (env CROSSREF_MAILTO also supported)",
    )
    parser.add_argument("--delay", type=float, default=0.2,
                        help="Delay (seconds) between retries")
    parser.add_argument(
        "--max-references",
        type=int,
        default=None,
        help="Limit number of references processed per list (for testing)",
    )
    parser.add_argument("--verbose", action="store_true",
                        help="Print debug information")
    parser.add_argument("--write", action="store_true",
                        help="Write changes to file")
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=["yaml", "json"],
        default="yaml",
        help="Output format when using --doi",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.doi:
        session = requests.Session()
        reference, _, _ = enrich_value(
            args.doi,
            session=session,
            cache={},
            mailto=args.mailto,
            delay=args.delay,
            verbose=args.verbose,
        )
        print_reference(reference, args.output_format)
        return

    output_path = args.output or args.input
    counters = process_data_file(
        input_path=args.input,
        output_path=output_path,
        mailto=args.mailto,
        delay=args.delay,
        max_references=args.max_references,
        verbose=args.verbose,
        write=args.write,
    )

    print("Reference enrichment summary")
    print(
        f"  Standards with publication: {counters['standards_with_publication']}")
    print(f"  Publications enriched:      {counters['publications_enriched']}")
    print(f"  Applications enriched:      {counters['applications_enriched']}")
    print(f"  References processed:       {counters['references_total']}")
    print(f"  References changed:         {counters['references_changed']}")
    print(f"  CrossRef API calls:         {counters['api_crossref']}")
    print(f"  arXiv API calls:            {counters['api_arxiv']}")
    print(f"  GitHub API calls:           {counters['api_github']}")
    print(f"  Web page fetches:           {counters['api_web']}")

    if args.write:
        print(f"\n✓ Updated {output_path}")
    else:
        print("\n(No files were written; rerun with --write to apply changes.)")


if __name__ == "__main__":
    main()
