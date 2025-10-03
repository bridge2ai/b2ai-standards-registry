"""Command line interface for b2ai-standards-registry"""

import click
import logging

from scripts.analyze_and_update_synapse_tables import analyze_and_update
from scripts.create_denormalized_tables import denormalize_tables


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
def main(verbose: int, quiet: bool):
    """CLI for b2ai-standards-registry.

    :param verbose: Verbosity while running.
    :param quiet: Boolean to be quiet or verbose.
    """
    logger = logging.getLogger()
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)
    logger.info(f"Logger {logger.name} set to level {logger.level}")


@main.command()
@click.argument("files", nargs=-1)
@click.option("--all", is_flag=True, help="Upload all files in PATHS_TO_IDS")
@click.option("--table-names", multiple=True, help="List of table names to upload")
def update_synapse(files, all, table_names):
    """Update Synapse tables from JSON files.

    :param files: List of file paths (relative or absolute)
    :param all: Boolean, whether to upload all files in PATHS_TO_IDS
    :param table_names: List of table names to upload
    """
    analyze_and_update(files, all, table_names)


@main.command()
@click.option("--specific-tables", multiple=True, help="List of specific denormalized tables to create")
def create_denormalized_tables(specific_tables=None):
    """Create denormalized tables.

    Create and upload tables from definitions in ./generate_tables_config.py

    :param specific_tables: Optional list of tables to create; defaults to creating all
    """
    denormalize_tables(specific_tables)


if __name__ == "__main__":
    main()
