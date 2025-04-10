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

    **Essential:** Be sure to include the `--all-extras` option.


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

### Example Script: modify_synapse_schema.py

**Description:** Sets up and manages table schemas in Synapse, defining the column structure for each table.

**Run:**

```bash
python scripts/modify_synapse_schema.py
```

#### Requirements

This script requires Synapse authentication (replace `auth_token` in the script with your actual token or set it as an environment variable).

**Note:** Ensure you have a Synapse account with appropriate permissions before running this script.
