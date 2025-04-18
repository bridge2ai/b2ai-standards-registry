"""
Processes GitHub issues to new pull requests for the Bridge2AI Standards Registry.

This script does *not* check if a requested entity is already present in the registry.
It parses an issue,
makes proposed changes on the appropriate document,
and creates a PR for the proposed changes.

Some portions of this code originally developed by Charles Tapley Hoyt (@cthoyt)
for Bioregistry and used under MIT License (see below).
Sources:
https://github.com/biopragmatics/bioregistry/blob/main/.github/workflows/new_prefix_pr.yml
https://github.com/biopragmatics/bioregistry/blob/main/src/bioregistry/gh/new_prefix.py
https://github.com/biopragmatics/bioregistry/blob/main/src/bioregistry/gh/github_client.py

Scripts were modified to refer to this project (b2ai-standards-registry) and its data types.
Code from multiple Python modules were also merged into a single file; function references
were updated accordingly.
---
MIT License

Copyright (c) 2020-2021 Charles Tapley Hoyt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
---
"""

from enum import Enum, IntEnum
import itertools as itt
import logging
import os
import re
import subprocess
import sys
import time
from subprocess import CalledProcessError, check_output
from types import MappingProxyType
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence, Set
from uuid import uuid4

import click
import more_itertools
import requests
import yaml

logger = logging.getLogger(__name__)

DATA_DIR = "src/data/"
COLLECTION_NAMES = MappingProxyType(
    {
        "Data Standard or Tool": "data_standardortools_collection",
        "Data Substrate": "data_substrates_collection",
        "Data Topic": "data_topics_collection",
        "Organization": "organizations",
        "Use Case": "use_cases",
    }
)
ORC_ID_PREFIXES = ("http://orcid.org/", "https://orcid.org/")


class Prefix(str, Enum):
    """Define constraints for expected prefixes"""

    B2AI_STANDARD = "B2AI_STANDARD"
    B2AI_SUBSTRATE = "B2AI_SUBSTRATE"
    B2AI_TOPIC = "B2AI_TOPIC"
    B2AI_ORG = "B2AI_ORG"
    B2AI_USECASE = "B2AI_USECASE"


class GitHub(str, Enum):
    """Define constraints for GitHub values"""

    BRANCH = "main"
    OWNER = "bridge2ai"
    REPO = "b2ai-standards-registry"


class ExitCode(IntEnum):
    """Exit status codes"""

    SUCCESS = 0
    ERROR = 1


def exit_with_msg(
    msg: Optional[str] = None,
    fg: Optional[str] = None,
    exit_status_code: ExitCode = ExitCode.ERROR,
) -> None:
    """Exit with message

    :param msg: Message to log and display
    :param fg: Foreground color of the text
    :param exit_status_code: Exit status code
    """
    if msg:
        logging.error(msg) if exit_status_code == ExitCode.ERROR else logging.info(msg)
        click.echo(msg) if fg is None else click.secho(msg, fg=fg)

    sys.exit(exit_status_code)


def get_issues_with_pr(issue_ids: Iterable[int], token: str) -> Set[int]:
    """Get the set of issues that are already closed by a pull request.

    :param issue_ids: GitHub Issue IDs
    :param token: GitHub authentication token
    :return: Issue IDs that are closed by a PR
    """

    def _display_msg(pulled_issues: Dict[int, dict]) -> None:
        """Display messages regarding issues with PR

        :param pulled_issues: Issue IDs that are closed by a PR
        """
        if pulled_issues:
            click.echo(f"Found PRs covering {len(pulled_issues)} new request issues:")
            for pr_number in sorted(pulled_issues, reverse=True):
                link = click.style(
                    f"https://github.com/{GitHub.OWNER.value}/{GitHub.REPO.value}/pulls/{pr_number}",
                    fg="cyan",
                )
                click.echo(f" - {link}")
        else:
            click.echo("Found no PRs covering new request issues.")

    pulls = list_pulls(owner=GitHub.OWNER.value, repo=GitHub.REPO.value, token=token)
    pulled_issues = {
        issue_id
        for pull, issue_id in itt.product(pulls, issue_ids)
        if f"Closes #{issue_id}" in (pull.get("body") or "")
    }
    _display_msg(pulled_issues)
    return pulled_issues


def get_headers(token: str) -> Dict[str, str]:
    """Get GitHub headers.

    :param token: GitHub authentication token
    :return: Headers with authorization
    """
    return {"Authorization": f"token {token}"}


def requests_get(
    path: str, token: str, params: Optional[Mapping[str, Any]] = None
) -> Dict[str, Any]:
    """Send a get request to the GitHub API.

    :param path: API endpoint
    :param token: GitHub authentication token
    :param params: Query string parameters
    :return: JSON response from request
    """
    path = path.lstrip("/")
    return requests.get(
        f"https://api.github.com/{path}",
        headers=get_headers(token=token),
        params=params,
    ).json()


def list_pulls(
    owner: str,
    repo: str,
    token: str,
):
    """List pull requests.

    :param owner: The name of the owner/organization for the repository
    :param repo: The name of the repository
    :param token: The GitHub Authentication token
    :return: JSON response from GitHub
    """
    return requests_get(f"repos/{owner}/{repo}/pulls", token=token)


def open_b2ai_standards_registry_pull_request(
    title: str,
    head: str,
    token: str,
    body: Optional[str] = None,
):
    """Open a pull request to b2ai-standards-registry via :func:`open_pull_request`.

    :param title: Name of the PR
    :param head: Name of the source branch
    :param token: GitHub authentication token
    :param body: Body of the PR
    """
    return open_pull_request(
        owner=GitHub.OWNER.value,
        repo=GitHub.REPO.value,
        base=GitHub.BRANCH.value,
        title=title,
        head=head,
        body=body,
        token=token,
    )


def open_pull_request(
    owner: str,
    repo: str,
    title: str,
    head: str,
    base: str,
    token: str,
    body: Optional[str] = None,
):
    """Open a pull request.

    :param owner: The name of the owner/organization for the repository
    :param repo: The name of the repository
    :param title: Name of the PR
    :param head: Name of the source branch
    :param base: Name of the target branch
    :param token: The GitHub Authentication token
    :param body: Body of the PR
    :return: JSON response from GitHub
    """
    data = {"title": title, "head": head, "base": base, "body": body}
    return requests.post(
        f"https://api.github.com/repos/{owner}/{repo}/pulls",
        headers=get_headers(token=token),
        json=data,
    ).json()



def get_b2ai_standards_registry_form_data(
    labels: Iterable[str],
    token: str,
) -> Mapping[int, Dict[str, str]]:
    """Get parsed form data from issues on b2ai_standards_registry matching the given
    labels via :func:`get_form_data`.

    :param labels: Labels to match
    :param token: The GitHub Authentication token
    :return: A mapping from GitHub issue issue data
    """
    return get_form_data(
        owner=GitHub.OWNER.value,
        repo=GitHub.REPO.value,
        labels=labels,
        token=token,
    )


def get_form_data(
    owner: str,
    repo: str,
    labels: Iterable[str],
    token: str,
) -> Mapping[int, Dict[str, str]]:
    """Get parsed form data from issues matching the given labels.

    :param owner: The name of the owner/organization for the repository.
    :param repo: The name of the repository.
    :param labels: Labels to match
    :param token: The GitHub Authentication token
    :return: A mapping from github issue to issue data
    """
    labels = labels if isinstance(labels, str) else ",".join(labels)
    res_json = requests_get(
        f"repos/{owner}/{repo}/issues",
        token=token,
        params={
            "labels": labels,
            "state": "open",
        },
    )

    rv = {
        issue["number"]: parse_body(issue["body"])
        for issue in res_json
        if "pull_request" not in issue
    }
    rv = {issue: remap(body_data) for issue, body_data in rv.items()}
    return rv


def remap(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remap dictionary keys to lowercase with underscore and convert ``related_to``
    value to a list

    :param data: Input dictionary
    :return: Mutated ``data`` with transformed keys
    """
    remapped = {key.lower().replace(" ", "_"): value for key, value in data.items()}
    if remapped.get("related_to"):
        remapped["related_to"] = re.split(r"\s+", remapped["related_to"])
    return remapped


def parse_body(body: str) -> Dict[str, Any]:
    """Parse the body string from a GitHub issue (via the API).

    :param body: The body string from a GitHub issue (via the API) that corresponds to a form
    :return: A dictionary of keys (headers) to values
    """
    rv = {}
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    for group in more_itertools.split_before(
        lines, lambda line: line.startswith("### ")
    ):
        header, *rest = group
        header = header.lstrip("#").lstrip()
        rest = " ".join(x.strip() for x in rest)
        if rest == "_No response_" or not rest:
            continue
        rv[header] = rest
    return rv


def status_porcelain() -> Optional[str]:
    """Return if the current directory has any uncommitted stuff.

    :return: The message from the command
    """
    return _git("status", "--porcelain")


def push(*args) -> Optional[str]:
    """Push changes to the Git repo.

    :return: The message from the command
    """
    return _git("push", *args)


def branch(name: str) -> Optional[str]:
    """Create a new branch and switch to it.

    :param name: The name of the new branch
    :return: The message from the command
    .. seealso:: https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
    """
    return _git("checkout", "-b", name)


def home() -> Optional[str]:
    """Return to the main branch.

    :return: The message from the command
    """
    return _git("checkout", GitHub.BRANCH.value)


def commit_all(message: str) -> Optional[str]:
    """Make a commit with the following message.

    :param message: The message to go with the commit.
    :return: The message from the command
    .. note:: ``-a`` means "commit all files"
    """
    return _git("commit", "-m", message, "-a")


def _git(*args: str) -> Optional[str]:
    """Run a git command

    :return: The message from the command, if successful.
    """
    with open(os.devnull, "w") as devnull:
        try:
            ret = check_output(  # noqa: S603,S607
                ["git", *args],
                cwd=os.path.dirname(__file__),
                stderr=devnull,
            )
        except CalledProcessError as e:
            logger.warning(f"error in _git:\n{e}")
            return None
        else:
            return ret.strip().decode("utf-8")


def get_new_request_issues(token: str) -> Dict[int, dict]:
    """Get new entity request issues from the GitHub API.

    This is done by filtering on issues containing the "New" label.
    For issues with the label but not containing the expected data,

    :param token: The GitHub Authentication token
    :return: A dictionary of issue identifiers to a dict that has been parsed out of the
        issue form
    """

    def _display_msg(issue_to_resource: Dict[int, dict]) -> None:
        """Display messages regarding issues to resources

        :param issue_to_resource: A dictionary of issue identifiers to a dict that has been
            parsed out of the issue form
        """
        if issue_to_resource:
            click.echo(f"Found {len(issue_to_resource)} new request issues:")
            for issue_number in sorted(issue_to_resource, reverse=True):
                link = click.style(
                    f"https://github.com/{GitHub.OWNER.value}/{GitHub.REPO.value}/issues/{issue_number}",
                    fg="cyan",
                )
                click.echo(f" - {link}")
        else:
            click.echo("Found no applicable issues.")

    data = get_b2ai_standards_registry_form_data(["New"], token=token)
    rv: Dict[int, dict] = {}
    for issue_id, resource_data in data.items():
        try:
            category = resource_data.pop("category")
            name = resource_data.pop("name")
            desc = resource_data.pop("description")
            entity_type = resource_data.pop("entity_type")
            contributor = {
                "name": resource_data.pop("contributor_name"),
                "orcid": _pop_orcid(resource_data),
                "email": resource_data.pop("contributor_email", None),
                "github": resource_data.pop("contributor_github"),
            }
        except KeyError:
            logger.warning(f"Issue {issue_id} is missing one or more required fields.")
            continue

        rv[issue_id] = {
            "name": name,
            "category": category,
            "description": desc,
            "contributor": contributor,
            "github_request_issue": issue_id,
            "entity_type": entity_type,
            **resource_data,
        }
    _display_msg(rv)
    return rv


def _pop_orcid(data: Dict[str, str]) -> str:
    """Remove ``contributor_orcid`` from ``data``

    :param data: GitHub issue data. If ``contributor_orcid`` is exists, this will
        be removed.
    :return: ORC ID
    """
    orcid = data.pop("contributor_orcid", "")

    for orc_id_prefix in ORC_ID_PREFIXES:
        if orcid.startswith(orc_id_prefix):
            return orcid[len(orc_id_prefix) :]

    return orcid


def make_title(names: Sequence[str]) -> str:
    """Make a title for the PR.

    :param names: Names of entities that are being included in the PR
    :return: PR title
    """
    conventional_commit_prefix = "feat:"
    if len(names) == 0:
        raise ValueError
    if len(names) == 1:
        return f"{conventional_commit_prefix} add entity {names[0]}"
    elif len(names) == 2:
        return f"{conventional_commit_prefix} add entities {names[0]} and {names[1]}"
    else:
        return f"{conventional_commit_prefix} add entity {', '.join(names[:-1])}, and {names[-1]}"


def _update_yaml(issue_to_resource: Dict[int, dict]) -> None:
    """Update source YAML file with new entities

    :param issue_to_resource: A dictionary of issue identifiers to a dict that has been
        parsed out of the issue form
    """
    for issue_number, resource in issue_to_resource.items():
        click.echo(f"🚀 Adding {resource['name']} (#{issue_number})")
        data_path = f"{DATA_DIR}{''.join(resource['entity_type'].title().split())}.yaml"

        with open(data_path, "r") as yaml_file:
            this_yaml = yaml.safe_load(yaml_file)
            collection_name = COLLECTION_NAMES[resource["entity_type"]]

            prev_curie = this_yaml[collection_name][-1]["id"]
            prev_id_prefix, prev_id = prev_curie.split(":")

            try:
                Prefix(prev_id_prefix)
            except ValueError as e:
                exit_with_msg(msg=str(e), fg="red", exit_status_code=ExitCode.ERROR)

            category = resource["category"]
            if not category.startswith(f"{prev_id_prefix}:"):
                category = f"{prev_id_prefix}:{category}"

            entity = {
                "id": f"{prev_id_prefix}:{int(prev_id) + 1}",
                "category": category,
                "name": resource["name"],
                "description": resource["description"],
                "contributor_name": resource["contributor"]["name"],
                "contributor_github_name": resource["contributor"]["github"],
                "contributor_orcid": resource["contributor"]["orcid"],
            }

            for _field in ("purpose_detail", "related_to"):
                _val = resource.get(_field)
                if _val:
                    entity[_field] = _val

            this_yaml[collection_name].append(entity)

        if this_yaml:
            with open(data_path, "w") as yamlfile:
                yaml.safe_dump(this_yaml, yamlfile, sort_keys=False)


def entity_exists_in_file(entity_name: str, file_path: str) -> bool:
    """
    Check if an entity exists in a YAML file.

    :param entity_name: The entity name to search for
    :param file_path: Full path to the YAML file to check
    :return: True if the entity exists, False otherwise
    """
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            content = yaml.safe_load(f)
            if not isinstance(content, dict):
                return False
            for collection in content.values():
                if isinstance(collection, list):
                    for item in collection:
                        if isinstance(item, dict) and item.get("name") == entity_name:
                            return True
        except yaml.YAMLError as e:
            print(f"Error reading {file_path}: {e}")
    return False


@click.command()
@click.option("--dry", is_flag=True, help="Dry run - do not create any PRs")
@click.option(
    "--github",
    is_flag=True,
    help="Use this flag in a GitHub Action setting to set run variables",
)
@click.option(
    "--force",
    is_flag=True,
    help="Force processing script to run even if working dir is dirty",
)
def main(dry: bool, github: bool, force: bool) -> None:
    """Run the automatic curator."""
    status_porcelain_result = status_porcelain()
    if status_porcelain_result and not force and not dry:
        exit_with_msg(
            msg=f"The working directory is dirty:\n\n{status_porcelain_result}",
            fg="red",
            exit_status_code=ExitCode.ERROR,
        )

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        exit_with_msg(
            msg="Missing `GITHUB_TOKEN` environment variable.",
            exit_status_code=ExitCode.ERROR,
        )

    issue_to_resource = get_new_request_issues(token)
    pulled_issues = get_issues_with_pr(issue_to_resource, token)

    # filter out issues that already have an associated pull request
    issue_to_resource = {
        issue_id: value
        for issue_id, value in issue_to_resource.items()
        if issue_id not in pulled_issues
    }

    # filter out issues that already exist in the yaml files
    filtered = {}
    for issue_id, value in issue_to_resource.items():
        filename = f"{''.join(value['entity_type'].title().split())}.yaml"
        filepath = os.path.join(DATA_DIR, filename)
        if entity_exists_in_file(value["name"], filepath):
            click.secho(f"Skipping issue #{issue_id}: '{value['name']}' already exists in {filename}", fg="yellow")
        else:
            filtered[issue_id] = value

    issue_to_resource = filtered


    if issue_to_resource:
        click.echo(f"Adding {len(issue_to_resource)} issues after filter")
    else:
        exit_with_msg(
            msg="No issues without PRs to worry about. Exiting.",
            exit_status_code=ExitCode.SUCCESS,
        )

    _update_yaml(issue_to_resource)

    try:
        click.secho("Running `make site`", fg="green")
        subprocess.run(["make", "site"], check=True)
    except subprocess.CalledProcessError as e:
        exit_with_msg(
            msg=f"An error occurred while running `make site`: {e}",
            fg="red",
            exit_status_code=ExitCode.ERROR,
        )

    title = make_title(
        sorted(resource["name"] for resource in issue_to_resource.values())
    )
    body = ", ".join(f"Closes #{issue}" for issue in issue_to_resource)
    message = f"{title}\n\n{body}"
    branch_name = str(uuid4())[:8]

    if github:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            click.echo(f"PR_BODY={body}", file=f)
            click.echo(f"PR_TITLE={title}", file=f)
        exit_with_msg(exit_status_code=ExitCode.SUCCESS)
    elif dry:
        click.echo("New branch would have been:")
        click.echo(f"title: {title}")
        click.echo(f"body: {body}")
        click.echo(f"branch_name: {branch_name}")
        exit_with_msg(
            msg=f"Skipping making branch {branch_name}, committing, pushing, and PRing",
            fg="yellow",
            exit_status_code=ExitCode.SUCCESS,
        )

    click.secho("Creating and switching to branch", fg="green")
    click.echo(branch(branch_name))

    click.secho("Committing", fg="green")
    commit_msg = commit_all(message)
    click.echo(commit_msg)
    if not commit_msg:
        exit_with_msg(exit_status_code=ExitCode.ERROR)

    click.secho("Pushing", fg="green")
    click.echo(push("origin", branch_name))

    click.secho(f"Opening PR from {branch_name} to {GitHub.BRANCH.value}", fg="green")
    time.sleep(2)  # avoid race condition?
    rv = open_b2ai_standards_registry_pull_request(
        title=title, head=branch_name, body=body, token=token
    )
    if "url" in rv:
        click.secho(f"PR at {rv['url']}")
    else:  # probably an error
        click.secho(rv, fg="red")

    click.secho(f"Switching back to {GitHub.BRANCH.value} branch", fg="green")
    click.echo(home())


if __name__ == "__main__":
    main()
