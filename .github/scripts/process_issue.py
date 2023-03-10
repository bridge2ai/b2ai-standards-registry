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
import pystow
import requests
import yaml

logger = logging.getLogger(__name__)

MAPPING = {
    "Name": "name",
    "Description": "description",
    "Subclass_Of": "subclass_of",
    "Related_To": "related_to",
    "Contributor ORCID": "contributor_orcid",
    "Contributor Name": "contributor_name",
    "Contributor GitHub": "contributor_github",
    "Contributor Email": "contributor_email",
}

DATA_DIR = "src/data/"

# TODO: Include enough detail in issues to identify which dataset we should update

# DATA_PATHS = [
#     DATA_DIR / "DataStandardOrTool.yaml",
#     DATA_DIR / "DataSubstrate.yaml",
#     DATA_DIR / "DataTopic.yaml",
#     DATA_DIR / "Organization.yaml",
#     DATA_DIR / "UseCase.yaml",
# ]

# Just do one file for now
DATA_PATH = DATA_DIR + "DataStandardOrTool.yaml"

ORCID_HTTP_PREFIX = "http://orcid.org/"
ORCID_HTTPS_PREFIX = "https://orcid.org/"

MAIN_BRANCH = "main"


def has_token() -> bool:
    """Check if there is a github token available."""
    return pystow.get_config("github", "token") is not None


def get_issues_with_pr(
    issue_ids: Iterable[int], token: Optional[str] = None
) -> Set[int]:
    """Get the set of issues that are already closed by a pull request."""
    pulls = list_pulls(owner="bridge2ai", repo="b2ai-standards-registry", token=token)
    return {
        issue_id
        for pull, issue_id in itt.product(pulls, issue_ids)
        if f"Closes #{issue_id}" in (pull.get("body") or "")
    }


def get_headers(token: Optional[str] = None):
    """Get GitHub headers."""
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    token = pystow.get_config("github", "token", passthrough=token)
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def requests_get(
    path: str, token: Optional[str] = None, params: Optional[Mapping[str, Any]] = None
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
    token: Optional[str] = None,
):
    """List pull requests.
    :param owner: The name of the owner/organization for the repository.
    :param repo: The name of the repository.
    :param token: The GitHub OAuth token. Not required, but if given, will let
        you make many more queries before getting rate limited.
    :returns: JSON response from GitHub
    """
    return requests_get(f"repos/{owner}/{repo}/pulls", token=token)


def open_b2ai_standards_registry_pull_request(
    *,
    title: str,
    head: str,
    body: Optional[str] = None,
    token: Optional[str] = None,
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
    token: Optional[str] = None,
):
    """Open a pull request.
    :param owner: The name of the owner/organization for the repository.
    :param repo: The name of the repository.
    :param title: name of the PR
    :param head: name of the source branch
    :param base: name of the target branch
    :param body: body of the PR (optional)
    :param token: The GitHub OAuth token. Not required, but if given, will let
        you make many more queries before getting rate limited.
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
    token: Optional[str] = None,
    remapping: Optional[Mapping[str, str]] = None,
) -> Mapping[int, Dict[str, str]]:
    """Get parsed form data from issues on b2ai_standards_registry matching the given labels via :func:get_form_data`.
    :param labels: Labels to match
    :param token: The GitHub OAuth token. Not required, but if given, will let
        you make many more queries before getting rate limited.
    :param remapping: A dictionary for mapping the headers of the form into new values. This is useful since
        the headers themselves will be human readable text, and not nice keys for JSON data
    :return: A mapping from GitHub issue issue data
    """
    return get_form_data(
        owner="bridge2ai",
        repo="b2ai-standards-registry",
        labels=labels,
        token=token,
        remapping=remapping,
    )


def get_form_data(
    owner: str,
    repo: str,
    labels: Iterable[str],
    token: Optional[str] = None,
    remapping: Optional[Mapping[str, str]] = None,
) -> Mapping[int, Dict[str, str]]:
    """Get parsed form data from issues matching the given labels.
    :param owner: The name of the owner/organization for the repository.
    :param repo: The name of the repository.
    :param labels: Labels to match
    :param token: The GitHub OAuth token. Not required, but if given, will let
        you make many more queries before getting rate limited.
    :param remapping: A dictionary for mapping the headers of the form into new values. This is useful since
        the headers themselves will be human readable text, and not nice keys for JSON data
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
    if remapping:
        rv = {issue: remap(body_data, remapping) for issue, body_data in rv.items()}
    return rv


def remap(data: Dict[str, Any], mapping: Mapping[str, str]) -> Dict[str, Any]:
    """Map the keys in dictionary ``d`` based on dictionary ``m``."""
    try:
        return {mapping[key]: value for key, value in data.items()}
    except KeyError:
        logger.warning("Original dict: %s", data)
        logger.warning("Mapping dict: %s", mapping)
        mapping = {}
        return mapping


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


def commit(message: str, *args: str) -> Optional[str]:
    """Make a commit with the following message."""
    return _git("commit", *args, "-m", message)


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


def get_new_request_issues(token: Optional[str] = None) -> Mapping[int, dict]:
    """Get new entity request issues from the GitHub API.

    This is done by filtering on issues containing the "New" label.
    For issues with the label but not containing the expected data,
    
    :param token: The GitHub OAuth token. Not required, but if given, will let
    you make many more queries before getting rate limited.
    :returns: A mapping of issue identifiers to a dict
    that has been parsed out of the issue form.
    """
    data = get_b2ai_standards_registry_form_data(
        ["New"], remapping=MAPPING, token=token
    )
    rv: Dict[int, dict] = {}
    for issue_id, resource_data in data.items():
        try:
            name = resource_data.pop("name")
            desc = resource_data.pop("description")
            contributor = {
                "name": resource_data.pop("contributor_name"),
                "orcid": _pop_orcid(resource_data),
                "email": resource_data.pop("contributor_email", None),
                "github": resource_data.pop("contributor_github"),
            }
        except KeyError:
            logger.warning(f"Issue {issue_id} is missing one or more required fields.")
            continue

        mappings: Optional[Mapping]

        rv[issue_id] = {
            "name": name,
            "decription": desc,
            "contributor": contributor,
            "github_request_issue": issue_id,
            #"mappings": mappings,
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


def _join(x: Iterable[int], sep=", ") -> str:
    return sep.join(map(str, sorted(x)))


def make_title(prefixes: Sequence[str]) -> str:
    """Make a title for the PR."""
    if len(prefixes) == 0:
        raise ValueError
    if len(prefixes) == 1:
        return f"Add prefix: {prefixes[0]}"
    elif len(prefixes) == 2:
        return f"Add prefixes: {prefixes[0]} and {prefixes[1]}"
    else:
        return f'Add prefixes: {", ".join(prefixes[:-1])}, and {prefixes[-1]}'


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

    if not has_token():
        click.secho(
            "No GitHub access token is available through GITHUB_TOKEN", fg="red"
        )
        sys.exit(1)

    issue_to_resource = get_new_request_issues()
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

    pulled_issues = get_issues_with_pr(issue_to_resource)
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
        # TODO: write to a specific file based on the issue
        with open(DATA_PATH, "r") as yamlfile:
            this_yaml = yaml.safe_load(yamlfile)
            # TODO: the collection name will also vary depending on the file,
            # so we need to provide a map like what the project.Makefile uses
            this_yaml["data_standardortools_collection"].append({"id":"PLACEHOLDER",
                                                                 "name":resource["name"]})
        if this_yaml:
            with open(DATA_PATH, "w") as yamlfile:
                yaml.safe_dump(this_yaml, yamlfile, sort_keys=False)

    title = make_title(
        sorted(resource["name"]for resource in issue_to_resource.values())
    )
    body = ", ".join(f"Closes #{issue}" for issue in issue_to_resource)
    message = f"{title}\n\n{body}"
    branch_name = str(uuid4())[:8]

    if github:
        click.echo(
            f"""
          ::set-output name=BR_BODY::{body}
          ::set-output name=BR_TITLE::{title}
        """
        )
        return sys.exit(0)
    elif dry:
        click.secho(
            f"Skipping making branch {branch_name}, committing, pushing, and PRing",
            fg="yellow",
        )
        return sys.exit(0)

    click.secho("Creating and switching to branch", fg="green")
    click.echo(branch(branch_name))
    click.secho("Committing", fg="green")
    click.echo(commit(message, DATA_PATH))
    click.secho("Pushing", fg="green")
    click.echo(push("origin", branch_name))
    click.secho(f"Opening PR from {branch_name} to {MAIN_BRANCH}", fg="green")
    time.sleep(2)  # avoid race condition?
    rv = open_b2ai_standards_registry_pull_request(
        title=title,
        head=branch_name,
        body=body,
    )
    if "url" in rv:
        click.secho(f'PR at {rv["url"]}')
    else:  # probably an error
        click.secho(rv, fg="red")

    click.secho(f"Switching back to {MAIN_BRANCH} branch", fg="green")
    click.echo(home())


if __name__ == "__main__":
    main()
