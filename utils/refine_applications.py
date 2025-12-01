#!/usr/bin/env python3
"""Refine Application objects for used_in_bridge2ai=true standards."""

import yaml
import requests
from time import sleep


def check_url(url):
    """Check if a URL resolves successfully."""
    try:
        if url.startswith('https://doi.org/'):
            # For DOIs, use HEAD request
            response = requests.head(url, allow_redirects=True, timeout=10)
            return response.status_code < 400
        else:
            # For other URLs, use GET request
            response = requests.get(url, timeout=10, allow_redirects=True)
            return response.status_code < 400
    except Exception as e:
        print(f"  ⚠️  Error checking {url}: {e}")
        return False


def remove_redundant_urls(app, parent_urls):
    """Remove URLs from app references that are redundant with parent."""
    if 'references' not in app or not app['references']:
        return False

    original_refs = app['references'].copy()
    app['references'] = [ref for ref in app['references'] if ref not in parent_urls]

    return len(app['references']) != len(original_refs)


def main():
    print("Loading data...")
    with open('src/data/DataStandardOrTool.yaml', 'r') as f:
        data = yaml.safe_load(f)

    standards = data['data_standardortools_collection']
    bridge2ai_standards = [
        s for s in standards if s.get('used_in_bridge2ai') == True]

    print(
        f"Found {len(bridge2ai_standards)} standards with used_in_bridge2ai=true\n")

    changes_made = []

    for std in bridge2ai_standards:
        if 'has_application' not in std or not std['has_application']:
            continue

        # Collect parent URLs
        parent_urls = set()
        if 'url' in std and std['url']:
            parent_urls.add(std['url'])
        if 'formal_specification' in std and std['formal_specification']:
            parent_urls.add(std['formal_specification'])

        std_id = std['id']
        std_name = std['name']

        for app in std['has_application']:
            app_id = app['id']
            app_name = app['name']

            print(f"\n{std_id} ({std_name})")
            print(f"  {app_id}: {app_name}")

            # Check for redundant URLs
            if remove_redundant_urls(app, parent_urls):
                print(f"  ✓ Removed redundant URLs")
                changes_made.append(
                    f"{std_id} / {app_id}: Removed redundant URLs")

            # Check URL validity
            if 'references' in app and app['references']:
                print(f"  Checking {len(app['references'])} references...")
                for ref in app['references']:
                    print(f"    - {ref}")
                    is_valid = check_url(ref)
                    if not is_valid:
                        print(f"      ❌ BROKEN")
                        changes_made.append(
                            f"{std_id} / {app_id}: Broken URL: {ref}")
                    else:
                        print(f"      ✓ OK")
                    sleep(0.5)  # Be nice to servers

            # Ensure at least 2 references remain
            if 'references' not in app or len(app['references']) < 2:
                print(
                    f"  ⚠️  Only {len(app.get('references', []))} references - needs more")
                changes_made.append(
                    f"{std_id} / {app_id}: Insufficient references ({len(app.get('references', []))})")

    # Save changes
    if changes_made:
        print("\n" + "="*60)
        print("CHANGES TO MAKE:")
        print("="*60)
        for change in changes_made:
            print(f"- {change}")

        print("\nSaving updated data...")
        with open('src/data/DataStandardOrTool.yaml', 'w') as f:
            yaml.dump(data, f, default_flow_style=False,
                      sort_keys=False, allow_unicode=True)
        print("✓ Saved")
    else:
        print("\nNo automatic changes needed.")


if __name__ == '__main__':
    main()
