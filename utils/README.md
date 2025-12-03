# Bridge2AI Standards Registry - Utility Scripts

This directory contains utility scripts for the Bridge2AI Standards Registry project.

## B2AI Documentation Generation Scripts

The documentation generation scripts create individual pages for B2AI resources with intelligent cross-reference linking.

### Shared ID Linking Module (`id_linking.py`)

Provides shared functionality for converting B2AI IDs in text to appropriate markdown links across different resource types.

#### Key Functions

- `load_all_b2ai_data()`: Loads all B2AI data files and creates ID-to-info mappings
- `convert_ids_to_links(text, all_data, relative_path_prefix)`: Converts B2AI IDs in text to markdown links
- `convert_substrate_links(list, all_data, relative_path_prefix)`: Converts substrate ID lists to links
- `convert_topic_links(list, all_data, relative_path_prefix)`: Converts topic ID lists to links
- `slugify(value)`: Converts strings to URL-friendly slugs

#### Supported ID Types

- `B2AI_STANDARD:*` - Links to Standards Explorer external site
- `B2AI_USECASE:*` - Links to use case pages in `../usecases/`
- `B2AI_SUBSTRATE:*` - Links to substrate pages in `../substrates/`
- `B2AI_TOPIC:*` - Links to topic pages in `../topics/`
- `B2AI_DATA:*` - Currently returns ID as-is (no individual dataset pages yet)

### Generation Scripts

#### Use Cases: `generate_usecase_pages.py`
- Individual markdown pages in `docs/usecases/`
- Dual overview diagrams: main workflow and standalone use cases
- Category-based color coding
- Comprehensive cross-reference linking

#### Substrates: `generate_substrate_pages.py`
- Individual markdown pages in `docs/substrates/`
- Hierarchical Mermaid diagram showing subclass relationships
- ID linking in descriptions and limitations

#### Topics: `generate_topic_pages.py`
- Individual markdown pages in `docs/topics/`
- Hierarchical Mermaid diagram showing topic relationships
- Parent/child relationship display

#### Manifest Table: `generate_manifest_table.py`
- Generates comprehensive manifest table in `docs/manifest.md`
- Groups data parts by their parent B2AI_MANIFEST ID
- Shows organization, datasets, and all metadata for each data part
- Includes linked identifiers for standards, substrates, topics, and anatomy terms
- Uses `id_linking.py` for consistent cross-referencing

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
