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

import itertools as itt
import logging
import os
import sys
import time
from subprocess import CalledProcessError, check_output
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence, Set
from uuid import uuid4

import click
import more_itertools
import requests
import yaml

logger = logging.getLogger(__name__)

DATA_DIR = "src/data/"
COLLECTION_NAMES = {
    "Data Standard or Tool":"data_standardortools_collection",
    "Data Substrate":"data_substrates_collection",
    "Data Topic":"data_topics_collection",
    "Organization":"organizations",
    "Use Case":"use_cases",
}

ORCID_HTTP_PREFIX = "http://orcid.org/"
ORCID_HTTPS_PREFIX = "https://orcid.org/"

MAIN_BRANCH = "main"


def get_issues_with_pr(
    issue_ids: Iterable[int], token: str
) -> Set[int]:
    """Get the set of issues that are already closed by a pull request."""
    pulls = list_pulls(owner="bridge2ai", repo="b2ai-standards-registry", token=token)
    return {
        issue_id
        for pull, issue_id in itt.product(pulls, issue_ids)
        if f"Closes #{issue_id}" in (pull.get("body") or "")
    }


def get_headers(token: str):
    """Get GitHub headers."""
    return {"Authorization": f"token {token}"}


def requests_get(
    path: str, token: str, params: Optional[Mapping[str, Any]] = None
):
    """Send a get request to the GitHub API."""
    path = path.lstrip("/")
    return requests.get(
        f"https://api.github.com/{path}",
        headers=get_headers(token=token),
        params=params,
    ).json()


def list_pulls(
    *,
    owner: str,
    repo: str,
    token: str,
):
    """List pull requests.
    :param owner: The name of the owner/organization for the repository.
    :param repo: The name of the repository.
    :param token: The GitHub OAuth token
    :returns: JSON response from GitHub
    """
    return requests_get(f"repos/{owner}/{repo}/pulls", token=token)


def open_b2ai_standards_registry_pull_request(
    *,
    title: str,
    head: str,
    body: Optional[str] = None,
    token: str,
):
    """Open a pull request to b2ai-standards-registry via :func:`open_pull_request`."""
    return open_pull_request(
        owner="bridge2ai",
        repo="b2ai-standards-registry",
        base=MAIN_BRANCH,
        title=title,
        head=head,
        body=body,
        token=token,
    )


def open_pull_request(
    *,
    owner: str,
    repo: str,
    title: str,
    head: str,
    base: str,
    body: Optional[str] = None,
    token: str,
):
    """Open a pull request.
    :param owner: The name of the owner/organization for the repository.
    :param repo: The name of the repository.
    :param title: name of the PR
    :param head: name of the source branch
    :param base: name of the target branch
    :param body: body of the PR (optional)
    :param token: The GitHub OAuth token
    :returns: JSON response from GitHub
    """
    data = {
        "title": title,
        "head": head,
        "base": base,
    }
    if body:
        data["body"] = body
    return requests.post(
        f"https://api.github.com/repos/{owner}/{repo}/pulls",
        headers=get_headers(token=token),
        json=data,
    ).json()


def get_b2ai_standards_registry_form_data(
    labels: Iterable[str],
    token: str,
) -> Mapping[int, Dict[str, str]]:
    """Get parsed form data from issues on b2ai_standards_registry matching the given labels via :func:get_form_data`.
    :param labels: Labels to match
    :param token: The GitHub OAuth token
    :return: A mapping from GitHub issue issue data
    """
    return get_form_data(
        owner="bridge2ai",
        repo="b2ai-standards-registry",
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
    :param token: The GitHub OAuth token
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
    """Map the keys in dictionary."""
    return {key.lower().replace(" ", "_"): value for key, value in data.items()}


def parse_body(body: str) -> Dict[str, Any]:
    """Parse the body string from a GitHub issue (via the API).
    :param body: The body string from a GitHub issue (via the API) that corresponds to a form
    :returns: A dictionary of keys (headers) to values
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
    """Return if the current directory has any uncommitted stuff."""
    return _git("status", "--porcelain")


def push(*args) -> Optional[str]:
    """Push the Git repo."""
    return _git("push", *args)


def branch(name: str) -> Optional[str]:
    """Create a new branch and switch to it.
    :param name: The name of the new branch
    :returns: The message from the command
    .. seealso:: https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
    """
    return _git("checkout", "-b", name)


def home() -> Optional[str]:
    """Return to the main branch.
    :returns: The message from the command
    """
    return _git("checkout", MAIN_BRANCH)


def commit_all(message: str) -> Optional[str]:
    """Make a commit with the following message.
    :param message: The message to go with the commit.
    :returns: The message from the command
    .. note:: ``-a`` means "commit all files"
    """
    return _git("commit", "-m", message, "-a")


def _git(*args: str) -> Optional[str]:
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


def get_new_request_issues(token: str) -> Mapping[int, dict]:
    """Get new entity request issues from the GitHub API.

    This is done by filtering on issues containing the "New" label.
    For issues with the label but not containing the expected data,

    :param token: The GitHub OAuth token
    :returns: A mapping of issue identifiers to a dict
    that has been parsed out of the issue form.
    """
    data = get_b2ai_standards_registry_form_data(
        ["New"], token=token
    )
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
    return rv


def _pop_orcid(data: Dict[str, str]) -> str:
    orcid = data.pop("contributor_orcid")
    return _trim_orcid(orcid)


def _trim_orcid(orcid: str) -> str:
    if orcid.startswith(ORCID_HTTP_PREFIX):
        return orcid[len(ORCID_HTTP_PREFIX) :]
    if orcid.startswith(ORCID_HTTPS_PREFIX):
        return orcid[len(ORCID_HTTPS_PREFIX) :]
    return orcid


def make_title(names: Sequence[str]) -> str:
    """Make a title for the PR."""
    if len(names) == 0:
        raise ValueError
    if len(names) == 1:
        return f"Add entity {names[0]}"
    elif len(names) == 2:
        return f"Add entities {names[0]} and {names[1]}"
    else:
        return f'Add entity {", ".join(names[:-1])}, and {names[-1]}'


@click.command()
@click.option("--dry", is_flag=True, help="Dry run - do not create any PRs")
@click.option(
    "--github", is_flag=True, help="Use this flag in a GHA setting to set run variables"
)
@click.option(
    "--force", is_flag=True, help="Force processing script to run even if working dir is dirty"
)
def main(dry: bool, github: bool, force: bool):
    """Run the automatic curator."""
    status_porcelain_result = status_porcelain()
    if status_porcelain_result and not force and not dry:
        click.secho(
            f"The working directory is dirty:\n\n{status_porcelain_result}", fg="red"
        )
        sys.exit(1)

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logging.error("Missing `GITHUB_TOKEN` environment variable.")
        return sys.exit(0)

    issue_to_resource = get_new_request_issues(token)
    if issue_to_resource:
        click.echo(f"Found {len(issue_to_resource)} new request issues:")
        for issue_number in sorted(issue_to_resource, reverse=True):
            link = click.style(
                f"https://github.com/bridge2ai/b2ai-standards-registry/issues/{issue_number}",
                fg="cyan",
            )
            click.echo(f" - {link}")
    else:
        click.echo("Found no applicable issues.")

    pulled_issues = get_issues_with_pr(issue_to_resource, token)
    if pulled_issues:
        click.echo(f"Found PRs covering {len(pulled_issues)} new request issues:")
        for pr_number in sorted(pulled_issues, reverse=True):
            link = click.style(
                f"https://github.com/bridge2ai/b2ai-standards-registry/pulls/{pr_number}",
                fg="cyan",
            )
            click.echo(f" - {link}")
    else:
        click.echo("Found no PRs covering new request issues.")

    # filter out issues that already have an associated pull request
    issue_to_resource = {
        issue_id: value
        for issue_id, value in issue_to_resource.items()
        if issue_id not in pulled_issues
    }

    if issue_to_resource:
        click.echo(f"Adding {len(issue_to_resource)} issues after filter")
    else:
        click.secho("No issues without PRs to worry about. Exiting.")
        sys.exit(0)

    for issue_number, resource in issue_to_resource.items():
        click.echo(f'🚀 Adding {resource["name"]} (#{issue_number})')
        data_path = f"{DATA_DIR}{''.join(resource['entity_type'].title().split())}.yaml"
        with open(data_path, "r") as yamlfile:
            this_yaml = yaml.safe_load(yamlfile)
            collection_name = COLLECTION_NAMES[resource["entity_type"]]
            # TODO: instead of PLACEHOLDER, find the id of the
            # previous entity and +1
            entity = {
                "id":"PLACEHOLDER",
                "category":resource["category"],
                "name":resource["name"],
                "description":resource["description"],
                "contributor_name":resource["contributor"]["name"],
                "contributor_github_name":resource["contributor"]["github"],
                "contributor_orcid":resource["contributor"]["orcid"]
            }
            purpose_detail = resource.get("purpose_detail")
            if purpose_detail:
                entity["purpose_detail"] = purpose_detail
            this_yaml[collection_name].append(entity)
        if this_yaml:
            with open(data_path, "w") as yamlfile:
                yaml.safe_dump(this_yaml, yamlfile, sort_keys=False)

    title = make_title(
        sorted(resource["name"] for resource in issue_to_resource.values())
    )
    body = ", ".join(f"Closes #{issue}" for issue in issue_to_resource)
    message = f"{title}\n\n{body}"
    branch_name = str(uuid4())[:8]

    if github:
        click.echo(
            f"""
          ::set-output name=PR_BODY::{body}
          ::set-output name=PR_TITLE::{title}
        """
        )
        return sys.exit(0)
    elif dry:
        print("New branch would have been:")
        print(f"title: {title}")
        print(f"body: {body}")
        print(f"branch_name: {branch_name}")
        click.secho(
            f"Skipping making branch {branch_name}, committing, pushing, and PRing",
            fg="yellow",
        )
        return sys.exit(0)

    click.secho("Creating and switching to branch", fg="green")
    click.echo(branch(branch_name))

    click.secho("Committing", fg="green")
    commit_msg = commit_all(message)
    click.echo(commit_msg)
    if not commit_msg:
        return sys.exit(0)

    click.secho("Pushing", fg="green")
    click.echo(push("origin", branch_name))

    click.secho(f"Opening PR from {branch_name} to {MAIN_BRANCH}", fg="green")
    time.sleep(2)  # avoid race condition?
    rv = open_b2ai_standards_registry_pull_request(
        title=title,
        head=branch_name,
        body=body,
        token=token
    )
    if "url" in rv:
        click.secho(f'PR at {rv["url"]}')
    else:  # probably an error
        click.secho(rv, fg="red")

    click.secho(f"Switching back to {MAIN_BRANCH} branch", fg="green")
    click.echo(home())


if __name__ == "__main__":
    main()
