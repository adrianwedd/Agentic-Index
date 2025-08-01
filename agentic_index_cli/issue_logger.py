"""CLI helpers for posting GitHub issues or comments."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


def _request(
    method: str,
    url: str,
    *,
    token: Optional[str],
    json: Optional[Dict[str, Any]] = None,
    debug: bool = False,
) -> requests.Response:
    """Perform a GitHub API request with standard headers."""
    headers = _headers(token)
    if debug:
        print(f"{method} {url}")
        if json:
            print(json)
    try:
        resp = requests.request(method, url, json=json, headers=headers, timeout=10)
    except Exception as exc:  # pragma: no cover - network issues
        raise APIError(str(exc)) from exc
    return resp


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
    title: str,
    body: str,
    repo: str,
    labels: List[str] | None = None,
    milestone: int | None = None,
    *,
    token: str | None = None,
    debug: bool = False,
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
    if milestone is not None:
        payload["milestone"] = milestone
    resp = _request(
        "POST",
        f"{API_URL}/repos/{repo}/issues",
        token=token,
        json=payload,
        debug=debug,
    )
    if resp.status_code >= 400:
        raise APIError(f"{resp.status_code} {resp.text}")
    return resp.json().get("html_url", "")


def update_issue(
    issue_url: str,
    *,
    body: str | None = None,
    state: str | None = None,
    assignees: List[str] | None = None,
    milestone: int | None = None,
    token: str | None = None,
    debug: bool = False,
) -> str:
    """Update fields on an existing issue."""
    token = token or get_token()
    if not token:
        raise APIError(
            "Missing GITHUB_TOKEN. Set GITHUB_TOKEN or GITHUB_TOKEN_ISSUES to enable issue logging."
        )
    repo, issue_number = _parse_issue_url(issue_url)
    payload: Dict[str, Any] = {}
    if body is not None:
        payload["body"] = body
    if state is not None:
        payload["state"] = state
    if assignees is not None:
        payload["assignees"] = assignees
    if milestone is not None:
        payload["milestone"] = milestone
    resp = _request(
        "PATCH",
        f"{API_URL}/repos/{repo}/issues/{issue_number}",
        token=token,
        json=payload,
        debug=debug,
    )
    if resp.status_code >= 400:
        raise APIError(f"{resp.status_code} {resp.text}")
    return resp.json().get("html_url", "")


def close_issue(
    issue_url: str, *, token: str | None = None, debug: bool = False
) -> str:
    """Close ``issue_url``."""
    return update_issue(issue_url, state="closed", token=token, debug=debug)


def search_issues(
    query: str, *, token: str | None = None, debug: bool = False
) -> List[Dict[str, Any]]:
    """Search for issues using GitHub's search API."""
    token = token or get_token()
    if not token:
        return []
    
    resp = _request(
        "GET",
        f"{API_URL}/search/issues?q={query}",
        token=token,
        debug=debug,
    )
    if resp.status_code >= 400:
        if debug:
            print(f"Search failed: {resp.status_code} {resp.text}")
        return []
    
    return resp.json().get("items", [])


def _parse_issue_url(issue_url: str) -> tuple[str, int]:
    """Return ``repo`` and ``issue_number`` extracted from ``issue_url``."""
    return _parse_issue_or_pr_url(issue_url)


def _parse_issue_or_pr_url(url: str) -> tuple[str, int]:
    """Return ``repo`` and ``number`` extracted from issue or PR ``url``."""
    import re

    api_match = re.search(r"repos/([^/]+/[^/]+)/(issues|pulls)/(\d+)", url)
    html_match = re.search(r"github.com/([^/]+/[^/]+)/(issues|pull)/(\d+)", url)
    match = api_match or html_match
    if not match:
        raise ValueError(f"Invalid issue or PR URL: {url}")
    repo, _, num = match.groups()
    return repo, int(num)


def _save_pending(url: str, data: Dict[str, Any]) -> None:
    """Append ``data`` to ``state/worklog_pending.json``."""
    path = Path("state/worklog_pending.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    entries: List[Dict[str, Any]] = []
    if path.exists():
        try:
            entries = json.loads(path.read_text())
        except Exception:
            entries = []
    entries.append({"url": url, "data": data})
    path.write_text(json.dumps(entries, indent=2))


def post_comment(
    issue_url: str, body: str, *, token: str | None = None, debug: bool = False
) -> str:
    """Post a comment to ``issue_url`` and return the comment HTML URL."""
    token = token or get_token()
    if not token:
        raise APIError(
            "Missing GITHUB_TOKEN. Set GITHUB_TOKEN or GITHUB_TOKEN_ISSUES to enable issue logging."
        )
    repo, issue_number = _parse_issue_url(issue_url)
    resp = _request(
        "POST",
        f"{API_URL}/repos/{repo}/issues/{issue_number}/comments",
        token=token,
        json={"body": body},
        debug=debug,
    )
    if resp.status_code >= 400:
        raise APIError(f"{resp.status_code} {resp.text}")
    return resp.json().get("html_url", "")


def _post_worklog_single(
    url: str, worklog_data: Dict[str, Any], *, token: str, debug: bool = False
) -> str:
    repo, number = _parse_issue_or_pr_url(url)
    comments_url = f"{API_URL}/repos/{repo}/issues/{number}/comments"

    body_lines = ["<!-- codex-log -->"]
    task = worklog_data.get("task") or worklog_data.get("task_name", "Task")
    body_lines.append(f"### {task}")

    table = [
        ("Agent", worklog_data.get("agent_id", "")),
        ("Started", worklog_data.get("started")),
        ("Finished", worklog_data.get("finished")),
        ("Commit", worklog_data.get("commit")),
    ]
    body_lines.append("| Key | Value |")
    body_lines.append("| --- | --- |")
    for k, v in table:
        if v:
            body_lines.append(f"| {k} | {v} |")

    files = worklog_data.get("files") or []
    if files:
        body_lines.append("\n<details><summary>Files Touched</summary>\n")
        for f in files:
            body_lines.append(f"- `{f}`")
        body_lines.append("</details>")

    summary = worklog_data.get("summary")
    if summary:
        body_lines.append("")
        body_lines.append(summary)

    body = "\n".join(body_lines)

    resp = requests.get(comments_url, headers=_headers(token), timeout=10)
    if resp.status_code >= 400:
        _save_pending(url, worklog_data)
        raise APIError(f"{resp.status_code} {resp.text}")
    existing = None
    for c in resp.json():
        if "<!-- codex-log -->" in c.get("body", ""):
            existing = c
            break

    if existing:
        cid = existing["id"]
        resp = requests.patch(
            f"{API_URL}/repos/{repo}/issues/comments/{cid}",
            json={"body": body},
            headers=_headers(token),
            timeout=10,
        )
    else:
        resp = requests.post(
            comments_url,
            json={"body": body},
            headers=_headers(token),
            timeout=10,
        )

    if resp.status_code >= 400:
        _save_pending(url, worklog_data)
        raise APIError(f"{resp.status_code} {resp.text}")

    return resp.json().get("html_url", "")


def post_worklog_comment(
    issue_or_pr_url: str,
    worklog_data: Dict[str, Any],
    *,
    token: str | None = None,
    targets: list[str] | None = None,
    debug: bool = False,
) -> str:
    """Post or update a structured Codex worklog comment."""
    token = token or get_token()
    if not token:
        _save_pending(issue_or_pr_url, worklog_data)
        raise APIError(
            "Missing GITHUB_TOKEN. Set GITHUB_TOKEN or GITHUB_TOKEN_ISSUES to enable issue logging."
        )
    if targets:
        last = ""
        for t in targets:
            url = issue_or_pr_url
            if t == "pr":
                url = worklog_data.get("pr_url", issue_or_pr_url)
            elif t == "issue":
                url = worklog_data.get("issue_url", issue_or_pr_url)
            last = _post_worklog_single(url, worklog_data, token=token, debug=debug)
        return last

    return _post_worklog_single(issue_or_pr_url, worklog_data, token=token, debug=debug)


def _find_tracking_issue(repo: str, pr_number: int, token: str | None) -> str | None:
    """Return issue API URL linked to PR ``pr_number`` if any."""
    resp = requests.get(
        f"{API_URL}/repos/{repo}/issues/{pr_number}/comments",
        headers=_headers(token),
        timeout=10,
    )
    if resp.status_code >= 400:
        return None
    for c in resp.json():
        m = re.search(r"tracking-issue:(\d+)", c.get("body", ""))
        if m:
            num = int(m.group(1))
            return f"{API_URL}/repos/{repo}/issues/{num}"
    return None


def create_issue_for_pr(event: Dict[str, Any], *, token: str | None = None) -> str:
    """Create a tracking issue for ``event`` if one does not exist."""
    token = token or get_token()
    pr = event.get("pull_request", {})
    repo = event.get("repository", {}).get("full_name")
    if not repo or not pr:
        raise APIError("Missing pull request data")
    pr_number = pr.get("number")
    issue_url = _find_tracking_issue(repo, pr_number, token)
    if issue_url:
        return issue_url

    title = pr.get("title", "")
    body_parts = []
    if pr.get("body"):
        body_parts.append(pr["body"])
    body_parts.append(f"PR: {pr.get('html_url')}")
    body = "\n\n".join(body_parts)

    issue_html = create_issue(title, body, repo, token=token)
    _, issue_number = _parse_issue_url(issue_html)
    pr_api_url = f"{API_URL}/repos/{repo}/issues/{pr_number}"
    comment = f"Created tracking issue #{issue_number}\n<!-- tracking-issue:{issue_number} -->"
    post_comment(pr_api_url, comment, token=token)
    return issue_html


def close_issue_for_pr(event: Dict[str, Any], *, token: str | None = None) -> None:
    """Close the tracking issue linked to ``event``."""
    token = token or get_token()
    pr = event.get("pull_request", {})
    repo = event.get("repository", {}).get("full_name")
    if not repo or not pr:
        return
    pr_number = pr.get("number")
    issue_url = _find_tracking_issue(repo, pr_number, token)
    if not issue_url:
        return
    post_comment(issue_url, f"PR #{pr_number} merged – closing issue.", token=token)
    close_issue(issue_url, token=token)


def main(argv: list[str] | None = None) -> None:
    """Entry point for issue/comment logging."""
    parser = argparse.ArgumentParser(description="Post GitHub issues or comments")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--new-issue", action="store_true", help="create a new issue")
    mode.add_argument("--comment", action="store_true", help="comment on an issue")
    mode.add_argument("--update", action="store_true", help="update issue fields")
    mode.add_argument("--close", action="store_true", help="close an issue")
    mode.add_argument(
        "--worklog", metavar="FILE", help="post a structured worklog JSON file"
    )
    parser.add_argument("--repo", help="owner/repo")
    parser.add_argument("--title")
    parser.add_argument("--body", default="")
    parser.add_argument("--body-file")
    parser.add_argument("--issue-number", type=int)
    parser.add_argument("--issue-url")
    parser.add_argument("--assign", action="append", default=[])
    parser.add_argument("--label", action="append", default=[])
    parser.add_argument("--milestone", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    if args.body_file:
        args.body = Path(args.body_file).read_text()
    elif args.body == "-":
        args.body = sys.stdin.read()

    if args.new_issue:
        if not args.title:
            parser.error("--title required for --new-issue")
        if args.dry_run:
            if args.verbose:
                print(f"DRY RUN: would create issue in {args.repo}")
            return
        url = create_issue(
            args.title,
            args.body,
            args.repo,
            labels=args.label or None,
            milestone=args.milestone,
            debug=args.debug,
        )
        if args.verbose:
            print(url)
        return

    if args.worklog:
        data = json.loads(Path(args.worklog).read_text())
        if args.issue_url:
            issue_url = args.issue_url
        elif args.issue_number:
            if not args.repo:
                parser.error("--repo required")
            issue_url = (
                f"https://api.github.com/repos/{args.repo}/issues/{args.issue_number}"
            )
        else:
            issue_url = data.get("issue_url") or data.get("url")
            if not issue_url:
                parser.error("--issue-url or --issue-number required")
        if args.dry_run:
            if args.verbose:
                print(f"DRY RUN: would post worklog to {issue_url}")
            return
        url = post_worklog_comment(issue_url, data, debug=args.debug)
        if args.verbose:
            print(url)
        return

    if not args.worklog and not args.issue_number and not args.issue_url:
        parser.error("--issue-number or --issue-url required")

    if args.issue_url:
        repo, num = _parse_issue_or_pr_url(args.issue_url)
        issue_url = f"https://api.github.com/repos/{repo}/issues/{num}"
        if not args.repo:
            args.repo = repo
    else:
        if not args.repo:
            parser.error("--repo required")
        issue_url = (
            f"https://api.github.com/repos/{args.repo}/issues/{args.issue_number}"
        )

    if args.dry_run:
        if args.verbose:
            action = "comment" if args.comment else "update"
            if args.close:
                action = "close"
            print(f"DRY RUN: would {action} issue {args.issue_number} in {args.repo}")
        return

    if args.comment:
        url = post_comment(issue_url, args.body, debug=args.debug)
    elif args.close:
        url = close_issue(issue_url, debug=args.debug)
    else:
        url = update_issue(
            issue_url,
            body=args.body if args.update else None,
            assignees=args.assign or None,
            milestone=args.milestone,
            debug=args.debug,
        )
    if args.verbose:
        print(url)


AGENT_ACTIONS = {
    "create_issue": create_issue,
    "post_comment": post_comment,
    "post_worklog_comment": post_worklog_comment,
    "create_issue_for_pr": create_issue_for_pr,
    "close_issue_for_pr": close_issue_for_pr,
    "update_issue": update_issue,
    "close_issue": close_issue,
}


if __name__ == "__main__":
    main()
