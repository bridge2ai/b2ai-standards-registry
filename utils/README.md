# Bridge2AI Standards Registry - Utility Scripts

This directory contains utility scripts for the Bridge2AI Standards Registry project.

## URL Checker Script

The `check_urls.py` script is used to validate the URLs in all YAML files in the data directory. It checks for broken links and potentially invalid pages (like very short or empty pages).

### Features

- Checks all URLs in YAML files in the data directory
- Validates HTTP response status codes
- Checks if the content is too short (potentially invalid)
- Parallelized URL checking for faster processing
- Detailed reporting of issues found
- Uses only standard library modules and minimal dependencies

### Usage

```bash
python check_urls.py [--directory PATH] [--timeout SECONDS] [--min-content-length BYTES] [--verbose]
```

Options:
- `--directory`: Path to the directory containing YAML files (default: ../src/data)
- `--timeout`: Timeout for URL requests in seconds (default: 10)
- `--min-content-length`: Minimum content length in bytes to consider valid (default: 500)
- `--verbose`: Show more detailed output

### Example

```bash
# Run with default settings
python check_urls.py

# Check URLs with increased timeout and more detailed output
python check_urls.py --timeout 20 --verbose

# Check URLs in a different directory
python check_urls.py --directory /path/to/yaml/files
```

### Output

The script provides a summary report of:
- Total URLs checked
- Valid URLs
- URLs with warnings (e.g., content too short)
- Broken URLs (e.g., 404, timeout)
- Detailed information about each problematic URL
