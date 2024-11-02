# Project Scripts

This directory contains manually executed scripts used for managing and interacting with the project's data standards and tools. These scripts are not meant to be run as part of automated updates (such as GitHub Actions) but can be executed locally when needed.

## Overview

The scripts in this folder are designed to:

- Define and manage Synapse table schemas.
- Perform one-time or occasional tasks related to database setup and maintenance.

**Note:** These scripts are intended to be run manually and are not part of the project's automated CI/CD pipeline.

## Setup

To run these scripts, you’ll need to install the required dependencies. This can be done by installing the dependencies listed in the requirements-scripts.txt file.

1. **Install Dependencies**

    In your terminal, navigate to the project root and install the requirements with:

    ```shell
    pip install -r scripts/requirements-scripts.txt
    ```

2. **Environment Variables**

    Ensure you have the necessary authentication set up for Synapse access. You can set up your Personal Access Token following the documentation [here](https://help.synapse.org/docs/Managing-Your-Account.2055405596.html#ManagingYourAccount-PersonalAccessTokens).

    Once you have your access token, export it like below:

    ```shell
    export SYNAPSE_AUTH_TOKEN=paste_your_token_here
    ```

## Usage

Each script is intended to be run individually. Here’s how to use them:

### Example Script: table_schema_setup.py

**Description:** Sets up and manages table schemas in Synapse, defining the column structure for each table.

**Run:**

```bash
python scripts/table_schema_setup.py
```

#### Requirements

This script requires Synapse authentication (replace `auth_token` in the script with your actual token or set it as an environment variable).

**Note:** Ensure you have a Synapse account with appropriate permissions before running this script.
