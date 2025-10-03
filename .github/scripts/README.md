# GitHub Actions Scripts

This directory contains scripts designed specifically for use with GitHub Actions workflows. These scripts are intended to be run automatically as part of the CI/CD pipeline and should not be run manually.

## Overview

The scripts in this directory automate various tasks related to testing, deployment, and maintenance within GitHub Actions. Each script is triggered by a corresponding YAML workflow file in `.github/workflows/`.

## Script List

### Process Issue: `process_issue.py`

- **Description**: Creates a PR when a new issue is created with the label `New`,
  indicating wanting to add a new entity.

- **Usage**: This script is called within a GitHub Actions workflow. See [new_entity_pr.yml](../workflows/new_entity_pr.yml).

- **Trigger Conditions**: This workflow runs when there’s a new issue created with the
  `New` label.

  **Important note:** This script assumes that the
  [New Entity Issue Template](../ISSUE_TEMPLATE/newEntity.yml) was used.
