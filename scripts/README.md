# Project Scripts

This directory contains manually executed scripts used for managing and interacting with the project's data standards and tools. These scripts are not meant to be run as part of automated updates (such as GitHub Actions) but can be executed locally when needed.

## Overview

The scripts in this folder are designed to:

- Define and manage Synapse table schemas.
- Perform one-time or occasional tasks related to database setup and maintenance.

**Note:** These scripts are intended to be run manually and are not part of the project's automated CI/CD pipeline.

## Setup

1. **Install Dependencies**

   In your terminal, navigate to the project root and install the requirements with:

   ```bash
   poetry install --all-extras
   ```

   **Essential:** Be sure to include the `--all-extras` option because the scripts require addtional dependencies.

2. **Synapse Authentication**

   Ensure you have the necessary authentication set up for Synapse access. Personal Access Token documentation is
   [here](https://help.synapse.org/docs/Managing-Your-Account.2055405596.html#ManagingYourAccount-PersonalAccessTokens).
   The direct link to create a token is [here](https://accounts.synapse.org/authenticated/personalaccesstokens).

   Once you have your access token, create or modify `~/.synapseConfig` file in your home directory.
   A `.synapseConfig` file template can be found [here](https://help.synapse.org/docs/Client-Configuration.1985446156.html).
   At minimum, it should contain:

   ```shell
   [authentication]
   # username = <username> (authtoken alone is enough to log you in, but you can optionally uncommment this line and enter your username in order to confirm the authenticated username matches)
   authtoken = <authtoken>
   ```

## Usage

Each script is intended to be run individually. Here’s how to use them:

### Example Script: analyze_and_update_synapse_tables.py

**Description:** Uploads tables from registry .json files to Synapse. Synapse table
schemas will be based on the data uploaded.

**Run:**

You should run all functions with a poetry run command at the start as such:

```bash
poetry run {command here}
```

For instance, to upload the Organization and DataTopic tables, run
```bash
poetry run python -m scripts.analyze_and_update_synapse_tables -t Organization DataTopic
```

To see command-line options for this script:
```bash
poetry run python -m scripts.analyze_and_update_synapse_tables -h
```

**When updates are made to data or schemas on this repository, `analyze_and_update_synapse_tables`
should be run automatically for the updated tables.**

Bugs appearing in this script during development (and hopefully fixed now) sometimes result in records being
uploaded to the destination Synapse table without deleting existing rows, resulting in data sometimes being
doubled or tripled. We should be on the lookout. This can lead (for instance) to the header card appearing
twice on the standards details page. [Issue 315](https://github.com/bridge2ai/b2ai-standards-registry/issues/315)
may help with this if it continues to be a problem.

### Updating Front End
*Written 2025-05-15. Will need updating soon*

Most of the current front-end functionality is driven by the [DST_denormalized](https://www.synapse.org/Synapse:syn65676531/tables/)
table, which itself depends on [DataStandardOrTool](https://www.synapse.org/Synapse:syn63096833/tables/),
[Organization](https://www.synapse.org/Synapse:syn63096836/tables/), and [DataTopic](https://www.synapse.org/Synapse:syn63096835/tables/).
When source tables change, DST_denormalized (and soon another table or two) will need to be updated. (That
update uses data from the Synapse tables, though if I were writing the update script today, I would probably
base it on data straight from this repo.) When source tables have been updated appropiately (it's woth checking
on Synapse), `create_denormalized_tables` must be run:

```bash
poetry run python -m scripts.create_denormalized_tables
```
Default is to generate all destination tables (so far, DST_denormalized and GCDataSet), but can specify
which to generate by listing them on the command line like
```bash
poetry run python -m scripts.create_denormalized_tables GCDataSet
```

### Script: format_yaml.py

**Description:** Custom formatter that formats .yaml/.yml files in the `src/data` folder arranging data with `id` key placed first and other keys arragned alphabetically.

**Run:**

```bash
poetry run python scripts/format_yaml.py
```

#### Requirements

This script requires Synapse authentication (replace `auth_token` in the script with your actual token or set it as an environment variable).

**Note:** Ensure you have a Synapse account with appropriate permissions before running this script.
