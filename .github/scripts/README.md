# GitHub Actions Scripts

This directory contains scripts designed specifically for use with GitHub Actions workflows. These scripts are intended to be run automatically as part of the CI/CD pipeline and should not be run manually.

## Overview

The scripts in this directory automate various tasks related to testing, deployment, and maintenance within GitHub Actions. Each script is triggered by a corresponding YAML workflow file in `.github/workflows/`.

## Script List

### Example Script: `update_synapse_tables.py`

- **Description**: Updates Synapse tables based on recent changes. This script is triggered automatically by changes in specific files and is not intended for manual use.

- **Usage**: This script is called within a GitHub Actions workflow. See file `project_data_change.yml`.

- **Trigger Conditions**: This workflow runs when there’s a `push` to the `main` branch that includes changes to any `.tsv` files in the `project/data/` directory.

- **How it Works**:
  1. **Changed Files Check**: The workflow identifies changes in `.tsv` files within the `project/data/` directory using the associated `sha` of the `push`. This way, the action can be rerun manually and update the tables if it fails.
  2. **Run Conditions**: If relevant `.tsv` files are changed, the list of changed files is passed to the `update_synapse_tables.py` script. The files are passed as  paths (ex: `["project/data/DataStandardOrTool.tsv", "project/data/Organization.tsv"]`)
  3. **Script Execution**: The script processes these files to update the corresponding tables in Synapse, using the Synapse authentication token stored in GitHub Secrets (`SYNAPSE_AUTH_TOKEN`) for secure access. It establishes a connection to synapse, takes snapshots of the tables it is updating, deletes all of the rows for those tables, and repopulates them using the tsv.

  **Note:** This script processes the tsv files and turns the rows into a list of entries to add to the database. It assumes the first line of the tsv is the header file, so that gets ignored. Please make sure to update this script if the header line is ever removed.

  **Important note:** This script will not work if the schema has changed. This includes added columns, deleted columns, or if columns have changed order. If the schema has changed, update and run the `scripts/modify_synapse_schema.py` script to update the table schemas in Synapse.
