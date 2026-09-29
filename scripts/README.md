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

### Publishing to Synapse: publishing/

The scripts in [publishing/](publishing/) upload registry data to Synapse for
the Standards Explorer portal. Use
[publish_to_synapse.py](publishing/publish_to_synapse.py):

```bash
poetry run python -m scripts.publishing.publish_to_synapse --dry-run
poetry run python -m scripts.publishing.publish_to_synapse
```

(or `poetry run b2aisr publish-synapse`). It:

1. builds every table locally: source tables from `project/data/*.json`, the
   denormalized Manifest, and the denormalized tables defined in
   [generate_tables_config.py](publishing/generate_tables_config.py).
   `D4D_content` comes from another repo and is read from Synapse.
2. skips any table whose content hash matches the `b2ai_content_hash`
   annotation on its Synapse table
3. clears, repopulates and snapshots the rest, checks each snapshot's row count
   against what was uploaded, and records the hash and snapshot version
   (`b2ai_published_version`) as annotations
4. points each materialized view `mv_<table>` at its table's verified snapshot
   (`SELECT * FROM synX.N`). `D4D_content`'s view follows its latest snapshot.

The portal (`apps/portals/b2ai.standards/src/config/resources.ts` in
synapse-web-monorepo) queries the `mv_*` views, so a publish needs no portal
change. `--create-views` creates any missing views; `--force` re-uploads
unchanged tables.

A table that fails to publish or verify is reported and the run exits non-zero,
but its view stays on the last verified snapshot and other tables still publish.

The older per-step scripts are still there and still used by the GitHub Action
([project_data_change.yml](../.github/workflows/project_data_change.yml)); they
don't update the views:

- [analyze_and_update_synapse_tables.py](publishing/analyze_and_update_synapse_tables.py):
  `poetry run python -m scripts.publishing.analyze_and_update_synapse_tables -t Organization DataTopic`
- [create_denormalized_tables.py](publishing/create_denormalized_tables.py):
  `poetry run python -m scripts.publishing.create_denormalized_tables [DST_denormalized ...]`
- [create_denormalized_manifest.py](publishing/create_denormalized_manifest.py)

Bugs in earlier versions sometimes uploaded records without deleting existing
rows, doubling or tripling data
([issue 315](https://github.com/bridge2ai/b2ai-standards-registry/issues/315)).
`publish_to_synapse` catches that with its row-count check.

### Script: format_yaml.py

**Description:** Custom formatter that formats .yaml/.yml files in the `src/data` folder arranging data with `id` key placed first and other keys arragned alphabetically.

**Run:**

```bash
poetry run python scripts/format_yaml.py
```

#### Requirements

This script requires Synapse authentication (replace `auth_token` in the script with your actual token or set it as an environment variable).

**Note:** Ensure you have a Synapse account with appropriate permissions before running this script.
