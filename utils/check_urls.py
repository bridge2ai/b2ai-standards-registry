"""
Script to check the validity of URLs in YAML files.

This script scans YAML files in the data directory and checks each URL for:
1. Validity (not broken, proper HTTP response)
2. Content quality (not too short or empty)

Usage:
    python check_urls.py [--directory PATH] [--timeout SECONDS] [--min-content-length BYTES] [--verbose]

Options:
    --directory          Path to the directory containing YAML files (default: ../src/data)
    --timeout            Timeout for URL requests in seconds (default: 10)
    --min-content-length Minimum content length in bytes to consider valid (default: 500)
    --verbose            Show more detailed output
"""

import argparse
import sys
import yaml
import requests
from urllib.parse import urlparse
import concurrent.futures
from pathlib import Path
import logging
import time
from typing import Dict, List, Tuple, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Set up User-Agent to avoid being blocked by some servers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}


def is_valid_url(url: str) -> bool:
    """Check if a URL has a valid format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def extract_urls_from_yaml(yaml_file: Path) -> Dict[str, List[str]]:
    """Extract URLs from a YAML file."""
    url_fields = ["url", "formal_specification", "ror_id", "wikidata_id"]
    urls_by_id = {}

    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # Find the root collection key (varies by file)
        root_key = None
        if isinstance(data, dict):
            for key in data:
                if isinstance(data[key], list) and len(data[key]) > 0 and isinstance(data[key][0], dict) and 'id' in data[key][0]:
                    root_key = key
                    break

        if not root_key:
            logger.warning(f"No valid collection found in {yaml_file}")
            return {}

        for item in data[root_key]:
            item_id = item.get('id', 'unknown_id')
            item_name = item.get('name', 'unknown_name')
            urls = []

            for field in url_fields:
                if field in item and item[field]:
                    value = item[field]
                    # Handle if the field is a string and looks like a URL
                    if isinstance(value, str) and is_valid_url(value):
                        urls.append((field, value))

            if urls:
                urls_by_id[f"{item_id} ({item_name})"] = urls

    except Exception as e:
        logger.error(f"Error processing {yaml_file}: {e}")
        return {}

    return urls_by_id


def check_url(url_info: Tuple[str, str, str], timeout: int, min_content_length: int) -> Dict[str, Any]:
    """
    Check a URL for validity and content quality.

    Args:
        url_info: Tuple containing (entity_id, field_name, url)
        timeout: Request timeout in seconds
        min_content_length: Minimum content length to consider valid

    Returns:
        Dictionary with check results
    """
    entity_id, field_name, url = url_info
    result = {
        'entity_id': entity_id,
        'field': field_name,
        'url': url,
        'status': 'unknown',
        'status_code': None,
        'error': None,
        'content_length': 0,
        'is_short_content': False,
    }

    # Skip URLs that are not HTTP/HTTPS
    if not url.startswith(('http://', 'https://')):
        if url.startswith(('ror:', 'wikidata:')):
            # Handle special cases like ROR and Wikidata IDs
            if url.startswith('ror:'):
                expanded_url = f"https://ror.org/{url[4:]}"
                result['url'] = expanded_url
                url = expanded_url
            elif url.startswith('wikidata:'):
                expanded_url = f"http://www.wikidata.org/wiki/{url[9:]}"
                result['url'] = expanded_url
                url = expanded_url
        else:
            result['status'] = 'skipped'
            result['error'] = 'Not an HTTP/HTTPS URL'
            return result

    try:
        # Send a HEAD request first to check status without downloading content
        head_response = requests.head(
            url, timeout=timeout, headers=HEADERS, allow_redirects=True)
        result['status_code'] = head_response.status_code

        # If HEAD request is successful, send a GET request for content check
        if 200 <= head_response.status_code < 400:
            get_response = requests.get(
                url, timeout=timeout, headers=HEADERS, allow_redirects=True)
            result['status_code'] = get_response.status_code

            if 200 <= get_response.status_code < 400:
                content_length = len(get_response.content)
                result['content_length'] = content_length
                result['is_short_content'] = content_length < min_content_length

                if result['is_short_content']:
                    result['status'] = 'warning'
                    result['error'] = f'Content length ({content_length} bytes) is less than minimum ({min_content_length} bytes)'
                else:
                    result['status'] = 'valid'
            else:
                result['status'] = 'error'
                result['error'] = f'GET request failed with status code {get_response.status_code}'
        else:
            result['status'] = 'error'
            result['error'] = f'HEAD request failed with status code {head_response.status_code}'

    except requests.exceptions.Timeout:
        result['status'] = 'error'
        result['error'] = f'Request timed out after {timeout} seconds'
    except requests.exceptions.ConnectionError as e:
        result['status'] = 'error'
        result['error'] = f'Connection error: {str(e)}'
    except requests.exceptions.RequestException as e:
        result['status'] = 'error'
        result['error'] = f'Request failed: {str(e)}'
    except Exception as e:
        result['status'] = 'error'
        result['error'] = f'Unexpected error: {str(e)}'

    return result


def check_urls_in_directory(directory: Path, timeout: int, min_content_length: int, verbose: bool) -> Dict[str, List[Dict[str, Any]]]:
    """Check all URLs in YAML files in the given directory."""
    yaml_files = list(directory.glob('*.yaml'))
    if not yaml_files:
        logger.error(f"No YAML files found in {directory}")
        return {}

    logger.info(f"Found {len(yaml_files)} YAML files in {directory}")

    all_results = {}
    all_urls_to_check = []

    # First, extract all URLs from all YAML files
    for yaml_file in yaml_files:
        logger.info(f"Extracting URLs from {yaml_file}")
        urls_by_id = extract_urls_from_yaml(yaml_file)

        for entity_id, urls in urls_by_id.items():
            for field, url in urls:
                all_urls_to_check.append((entity_id, field, url))

    logger.info(f"Found {len(all_urls_to_check)} URLs to check")

    # Then check all URLs in parallel
    results = []
    completed = 0
    total = len(all_urls_to_check)
    start_time = time.time()

    def print_progress():
        if not verbose:
            return
        elapsed = time.time() - start_time
        rate = completed / elapsed if elapsed > 0 else 0
        eta = (total - completed) / rate if rate > 0 else 0
        sys.stdout.write(f"\rChecking URLs: {completed}/{total} [{completed/total*100:.1f}%] "
                         f"(ETA: {eta:.1f}s){'.' * (completed % 4)}{'  ' * (4 - completed % 4)}")
        sys.stdout.flush()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {
            executor.submit(check_url, url_info, timeout, min_content_length): url_info
            for url_info in all_urls_to_check
        }

        for future in concurrent.futures.as_completed(future_to_url):
            url_info = future_to_url[future]
            try:
                result = future.result()
                results.append(result)

                # Update progress
                completed += 1
                print_progress()

                # Print verbose output if requested
                if verbose:
                    if result['status'] == 'valid':
                        logger.info(f"\n✓ {result['url']}")
                    elif result['status'] == 'warning':
                        logger.warning(
                            f"\n⚠ {result['url']} - {result['error']}")
                    elif result['status'] == 'error':
                        logger.error(
                            f"\n✗ {result['url']} - {result['error']}")
            except Exception as e:
                logger.error(f"\nError checking {url_info[2]}: {e}")
                completed += 1
                print_progress()

    # Print newline after progress indicator
    if verbose:
        sys.stdout.write("\n")

    # Group results by status
    all_results = {
        'valid': [r for r in results if r['status'] == 'valid'],
        'warnings': [r for r in results if r['status'] == 'warning'],
        'errors': [r for r in results if r['status'] == 'error'],
        'skipped': [r for r in results if r['status'] == 'skipped'],
    }

    return all_results


def generate_report(results: Dict[str, List[Dict[str, Any]]]) -> None:
    """Generate a report of URL checking results."""
    total_urls = sum(len(v) for v in results.values())
    valid_count = len(results['valid'])
    warning_count = len(results['warnings'])
    error_count = len(results['errors'])
    skipped_count = len(results['skipped'])

    logger.info("\n" + "="*80)
    logger.info(f"URL Check Summary - {total_urls} URLs checked")
    logger.info("="*80)
    logger.info(
        f"✓ Valid URLs: {valid_count} ({valid_count/total_urls*100:.1f}%)")
    logger.info(
        f"⚠ URLs with warnings: {warning_count} ({warning_count/total_urls*100:.1f}%)")
    logger.info(
        f"✗ Broken URLs: {error_count} ({error_count/total_urls*100:.1f}%)")
    logger.info(
        f"- Skipped URLs: {skipped_count} ({skipped_count/total_urls*100:.1f}%)")

    if error_count > 0:
        logger.info("\n" + "="*80)
        logger.info("Broken URLs:")
        logger.info("="*80)
        for result in results['errors']:
            logger.info(f"Entity: {result['entity_id']}")
            logger.info(f"Field: {result['field']}")
            logger.info(f"URL: {result['url']}")
            logger.info(f"Error: {result['error']}")
            logger.info("-"*80)

    if warning_count > 0:
        logger.info("\n" + "="*80)
        logger.info("URLs with warnings:")
        logger.info("="*80)
        for result in results['warnings']:
            logger.info(f"Entity: {result['entity_id']}")
            logger.info(f"Field: {result['field']}")
            logger.info(f"URL: {result['url']}")
            logger.info(f"Warning: {result['error']}")
            logger.info("-"*80)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Check URLs in YAML files')
    parser.add_argument('--directory', type=str, default='../src/data',
                        help='Path to the directory containing YAML files')
    parser.add_argument('--timeout', type=int, default=10,
                        help='Timeout for URL requests in seconds')
    parser.add_argument('--min-content-length', type=int, default=500,
                        help='Minimum content length in bytes to consider valid')
    parser.add_argument('--verbose', action='store_true',
                        help='Show more detailed output')

    args = parser.parse_args()

    # Convert relative path to absolute if needed
    directory = Path(args.directory)
    if not directory.is_absolute():
        # Get the directory of this script
        script_dir = Path(__file__).resolve().parent
        directory = (script_dir / directory).resolve()

    if not directory.exists() or not directory.is_dir():
        logger.error(f"Directory not found: {directory}")
        sys.exit(1)

    logger.info(f"Checking URLs in YAML files in {directory}")
    logger.info(f"Timeout: {args.timeout} seconds")
    logger.info(f"Minimum content length: {args.min_content_length} bytes")

    results = check_urls_in_directory(
        directory, args.timeout, args.min_content_length, args.verbose)
    generate_report(results)


if __name__ == "__main__":
    main()
