"""CLI helpers for posting GitHub issues or comments."""

from __future__ import annotations

import argparse
import os
from typing import Any, Dict, List

import requests

from .exceptions import APIError

API_URL = "https://api.github.com"


def _headers(token: str | None) -> Dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def get_token() -> str | None:
    """Return GitHub token from environment if available."""
    return os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_TOKEN_ISSUES")


def create_issue(
    title: str, body: str, repo: str, labels: List[str] | None = None, *, token: str | None = None
) -> str:
    """Create a new issue and return the HTML URL."""
    token = token or get_token()
    if not token:
        raise APIError(
            "Missing GITHUB_TOKEN. Set GITHUB_TOKEN or GITHUB_TOKEN_ISSUES to enable issue logging."
        )
    payload: Dict[str, Any] = {"title": title, "body": body}
    if labels:
        payload["labels"] = labels
    resp = requests.post(
        f"{API_URL}/repos/{repo}/issues",
        json=payload,
        headers=_headers(token),
        timeout=10,
    )
    if resp.status_code >= 400:
        raise APIError(f"{resp.status_code} {resp.text}")
    return resp.json().get("html_url", "")


def _parse_issue_url(issue_url: str) -> tuple[str, int]:
    """Return ``repo`` and ``issue_number`` extracted from ``issue_url``."""
    import re

    api_match = re.search(r"repos/([^/]+/[^/]+)/issues/(\d+)", issue_url)
    html_match = re.search(r"github.com/([^/]+/[^/]+)/issues/(\d+)", issue_url)
    match = api_match or html_match
    if not match:
        raise ValueError(f"Invalid issue URL: {issue_url}")
    repo, num = match.groups()
    return repo, int(num)


def post_comment(issue_url: str, body: str, *, token: str | None = None) -> str:
    """Post a comment to ``issue_url`` and return the comment HTML URL."""
    token = token or get_token()
    if not token:
        raise APIError(
            "Missing GITHUB_TOKEN. Set GITHUB_TOKEN or GITHUB_TOKEN_ISSUES to enable issue logging."
        )
    repo, issue_number = _parse_issue_url(issue_url)
    resp = requests.post(
        f"{API_URL}/repos/{repo}/issues/{issue_number}/comments",
        json={"body": body},
        headers=_headers(token),
        timeout=10,
    )
    if resp.status_code >= 400:
        raise APIError(f"{resp.status_code} {resp.text}")
    return resp.json().get("html_url", "")


def main(argv: list[str] | None = None) -> None:
    """Entry point for issue/comment logging."""
    parser = argparse.ArgumentParser(description="Post GitHub issues or comments")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--new-issue", action="store_true", help="create a new issue")
    mode.add_argument("--comment", action="store_true", help="comment on an issue")
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--title")
    parser.add_argument("--body", default="")
    parser.add_argument("--issue-number", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    if args.new_issue:
        if not args.title:
            parser.error("--title required for --new-issue")
        if args.dry_run:
            if args.verbose:
                print(f"DRY RUN: would create issue in {args.repo}")
            return
        url = create_issue(args.title, args.body, args.repo)
        if args.verbose:
            print(url)
    else:
        if args.issue_number is None:
            parser.error("--issue-number required for --comment")
        if args.dry_run:
            if args.verbose:
                print(f"DRY RUN: would comment on issue {args.issue_number} in {args.repo}")
            return
        issue_url = f"https://api.github.com/repos/{args.repo}/issues/{args.issue_number}"
        url = post_comment(issue_url, args.body)
        if args.verbose:
            print(url)


AGENT_ACTIONS = {
    "create_issue": create_issue,
    "post_comment": post_comment,
}


if __name__ == "__main__":
    main()
