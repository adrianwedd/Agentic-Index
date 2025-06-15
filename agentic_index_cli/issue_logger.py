"""CLI helpers for posting GitHub issues or comments."""

from __future__ import annotations

import argparse
import os
from typing import Any, Dict

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


def create_issue(repo: str, title: str, body: str, *, token: str | None = None) -> Dict[str, Any]:
    """Create a new issue on ``repo`` and return the JSON response."""
    token = token or get_token()
    resp = requests.post(
        f"{API_URL}/repos/{repo}/issues",
        json={"title": title, "body": body},
        headers=_headers(token),
        timeout=10,
    )
    if resp.status_code >= 400:
        raise APIError(f"{resp.status_code} {resp.text}")
    return resp.json()


def post_comment(repo: str, issue_number: int, body: str, *, token: str | None = None) -> Dict[str, Any]:
    """Post a comment to an existing issue and return the JSON response."""
    token = token or get_token()
    resp = requests.post(
        f"{API_URL}/repos/{repo}/issues/{issue_number}/comments",
        json={"body": body},
        headers=_headers(token),
        timeout=10,
    )
    if resp.status_code >= 400:
        raise APIError(f"{resp.status_code} {resp.text}")
    return resp.json()


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
        data = create_issue(args.repo, args.title, args.body)
        if args.verbose:
            print(data.get("html_url", ""))
    else:
        if args.issue_number is None:
            parser.error("--issue-number required for --comment")
        if args.dry_run:
            if args.verbose:
                print(f"DRY RUN: would comment on issue {args.issue_number} in {args.repo}")
            return
        data = post_comment(args.repo, args.issue_number, args.body)
        if args.verbose:
            print(data.get("html_url", ""))


if __name__ == "__main__":
    main()
