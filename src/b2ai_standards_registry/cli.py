"""Command line interface for b2ai-standards-registry"""

import click
import logging

from scripts.publishing.publish_to_synapse import publish_to_synapse


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
@click.option("--dry-run", is_flag=True, help="Build and compare, but change nothing on Synapse")
@click.option("--force", is_flag=True, help="Publish every table even if its content hash is unchanged")
@click.option("--create-views", is_flag=True, help="Create any missing mv_* materialized views")
def publish_synapse(dry_run, force, create_views):
    """Publish changed tables to Synapse and point the portal's materialized views at them.

    See scripts/publishing/publish_to_synapse.py.
    """
    publish_to_synapse(force=force, dry_run=dry_run, create_views=create_views)


if __name__ == "__main__":
    main()
