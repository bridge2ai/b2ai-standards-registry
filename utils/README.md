# Bridge2AI Standards Registry - Utility Scripts

This directory contains utility scripts for the Bridge2AI Standards Registry project.

## Documentation Generation Scripts

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

### Page Generation Scripts

#### `generate_usecase_pages.py`
Generates individual markdown pages for B2AI use cases in `docs/usecases/`:
- Dual overview diagrams: main workflow and standalone use cases
- Category-based color coding
- Comprehensive cross-reference linking with standards, substrates, and topics

#### `generate_substrate_pages.py`
Generates individual markdown pages for data substrates in `docs/substrates/`:
- Hierarchical Mermaid diagram showing subclass relationships
- ID linking in descriptions and limitations
- Standards that use each substrate

#### `generate_topic_pages.py`
Generates individual markdown pages for data topics in `docs/topics/`:
- Hierarchical Mermaid diagram showing topic relationships
- Parent/child relationship display
- Standards related to each topic

#### `generate_manifest_table.py`
Generates comprehensive manifest table in `docs/manifest.md`:
- Groups data parts by their parent B2AI_MANIFEST ID
- Shows organization, datasets, and all metadata for each data part
- Includes linked identifiers for standards, substrates, topics, and anatomy terms
- Uses `id_linking.py` for consistent cross-referencing

#### `convert_entries_to_pages.py`
General-purpose script to convert YAML data entries to individual markdown pages:
- Converts all entries from a YAML file to markdown format
- Creates files in a specified output directory
- Handles nested structures and cross-references

## Data Management and Transformation Scripts

### `add_b2ai_usage.py`
Sets the `used_in_bridge2ai` flag to `true` for standards associated with specific Bridge2AI organizations (B2AI_ORG:114-117).

### `add_default_topic.py`
Adds the default `concerns_data_topic` (B2AI_TOPIC:5) to standards that don't already have a data topic specified.

### `add_relevant_data_substrate.py`
Adds relevant data substrate associations to standards based on CSV mapping data:
- Reads substrate mappings from a CSV file
- Updates `relevant_data_substrate` field for matching standards
- Maintains proper YAML formatting with sorted keys

### `add_second_refs.py`
Adds secondary references to application objects that only have one reference:
- Ensures all applications have at least two references for better citation support
- Uses a pool of general references for specific domains (e.g., DICOM AI applications)

### `combine_data.py`
Exports all registry entries to a TSV file (`all_ids.tsv`):
- Iterates through all YAML files in the data directory
- Extracts `id` and `name` fields from all entries
- Creates a comprehensive tab-separated values file for easy searching and analysis

## Data Quality and Analysis Scripts

### `analyze_applications.py`
Analyzes DataStandardOrTool.yaml to identify entries with single applications and their reference status:
- Finds standards with exactly one application
- Reports on application IDs, names, and reference counts
- Helps identify applications that need additional documentation

### `analyze_purpose_details.py`
Analyzes purpose_detail fields to find entries with short descriptions:
- Counts sentences in each purpose_detail field
- Identifies entries that need more comprehensive descriptions
- Generates reports with word counts and sentence counts

### `check_urls.py`
Validates URLs in all YAML files to detect broken links and problematic pages:
- Checks HTTP response status codes
- Validates content length (detects empty/minimal pages)
- Parallelized URL checking for faster processing
- Detailed reporting of issues

**Usage:**
```bash
python check_urls.py [--directory PATH] [--timeout SECONDS] [--min-content-length BYTES] [--verbose]
```

**Options:**
- `--directory`: Path to the directory containing YAML files (default: ../src/data)
- `--timeout`: Timeout for URL requests in seconds (default: 10)
- `--min-content-length`: Minimum content length in bytes to consider valid (default: 500)
- `--verbose`: Show more detailed output

## Data Cleanup and Fixing Scripts

### `fix_applications.py`
Fixes various issues in Application objects:
- Removes redundant references (URLs that duplicate parent standard URLs)
- Sets `used_in_bridge2ai` to false by default for all applications
- Removes bad/invalid reference URLs

### `fix_org_roles.py`
Resolves overlapping organization roles in DataStandardOrTool.yaml:
- Removes organizations from `has_relevant_organization` if they also appear in `responsible_organization`
- Ensures the more specific role (responsible) takes precedence
- Supports dry-run mode to preview changes before applying

**Usage:**
```bash
# Dry run (preview changes)
python utils/fix_org_roles.py

# Apply changes to file
python utils/fix_org_roles.py --write

# Write to separate output file
python utils/fix_org_roles.py --output path/to/output.yaml
```

### `refine_applications.py`
Refines Application objects for standards marked with `used_in_bridge2ai=true`:
- Removes redundant URLs from application references
- Validates all reference URLs
- Checks for proper description content
- Ensures minimum of 2 valid references per application

### `update_ai_applications.py`
Updates DataStandardOrTool.yaml entries to use the new Application inline structure:
- Migrates from deprecated `has_ai_application` tag to `has_application` slot
- Creates properly formatted Application objects with unique IDs (B2AI_APP:XXX)
- Generates placeholder descriptions referencing the parent standard
- Sets default values for new application fields

### `fetch_reference_metadata.py`
Looks up publication metadata (CrossRef for DOIs, arXiv API for arXiv links/IDs, GitHub API for repo URLs) and formats it as Reference objects:
- Fetch a single DOI/URL and print a Reference object in YAML or JSON
- Enriches DataStandardOrTool.yaml so publication and application references include titles, authors, journal, and year
- Supports optional rate limiting, custom CrossRef contact email, and GitHub token via `GITHUB_TOKEN`

## Shell Scripts

### `get-value.sh`
Shell utility for extracting specific field values from YAML files using simple path expressions.
