#!/usr/bin/env python3
"""Propagate closed PR tasks into codex queue and task log."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Dict, List

import requests
import yaml

from agentic_index_cli import issue_logger

TASK_PATTERN = re.compile(r"(CR-[A-Z]+-\d+|GH-[A-Z]+-[\w\d-]+)")
QUEUE_FILE = Path(".codex/queue.yml")
TASKS_FILE = Path("codex_tasks.yml")


def load_yaml(path: Path) -> Dict[str, Any]:
    if path.exists():
        try:
            return yaml.safe_load(path.read_text()) or {}
        except Exception:
            return {}
    return {}


def save_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False))


def fetch_closed_prs(repo: str, token: str, limit: int) -> List[Dict[str, Any]]:
    url = f"{issue_logger.API_URL}/repos/{repo}/pulls"
    params = {"state": "closed", "per_page": limit}
    resp = requests.get(
        url, params=params, headers=issue_logger._headers(token), timeout=10
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"GitHub API error: {resp.status_code} {resp.text}")
    return resp.json()


def fetch_commits(pr: Dict[str, Any], token: str) -> List[Dict[str, Any]]:
    resp = requests.get(
        pr.get("commits_url"), headers=issue_logger._headers(token), timeout=10
    )
    if resp.status_code >= 400:
        return []
    return resp.json()


def update_tasks(
    tasks: Dict[str, Any], tid: str, pr_number: int, messages: List[str]
) -> None:
    entries = tasks.setdefault("tasks", [])
    for entry in entries:
        if entry.get("id") == tid:
            entry.setdefault("prs", []).append(pr_number)
            entry.setdefault("commits", []).extend(messages)
            entry["status"] = "done"
            return
    entries.append(
        {"id": tid, "prs": [pr_number], "commits": messages, "status": "done"}
    )


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Propagate closed PR tasks")
    parser.add_argument("--repo", required=True, help="GitHub repo, e.g. owner/name")
    parser.add_argument("--limit", type=int, default=20, help="Number of PRs to scan")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    token = issue_logger.get_token()
    if not token:
        raise SystemExit("GITHUB_TOKEN required")

    queue = load_yaml(QUEUE_FILE)
    queue_ids: List[str] = list(queue.get("queue", []))
    tasks = load_yaml(TASKS_FILE)

    prs = fetch_closed_prs(args.repo, token, args.limit)
    queue_modified = False
    tasks_modified = False

    for pr in prs:
        if not pr.get("merged_at"):
            continue
        pr_number = pr.get("number")
        commits = fetch_commits(pr, token)
        messages = [c.get("commit", {}).get("message", "") for c in commits]
        body = pr.get("body") or ""
        text = "\n".join([body] + messages)
        ids = sorted(set(TASK_PATTERN.findall(text)))
        if not ids:
            continue
        added = []
        removed = []
        for tid in ids:
            if tid in queue_ids:
                queue_ids.remove(tid)
                removed.append(tid)
                queue_modified = True
            else:
                added.append(tid)
            update_tasks(tasks, tid, pr_number, messages)
            tasks_modified = True
        if added:
            queue_ids.extend(added)
            queue_modified = True

        summary_lines = [f"Propagated tasks: {', '.join(ids)}"]
        if removed:
            summary_lines.append(
                f"Marked done and removed from queue: {', '.join(removed)}"
            )
        if added:
            summary_lines.append(f"Added to queue: {', '.join(added)}")
        summary = "\n".join(summary_lines)
        if not args.dry_run:
            issue_url = pr.get("issue_url") or pr.get("url")
            try:
                issue_logger.post_comment(issue_url, summary)
            except issue_logger.APIError:
                pass
        else:
            print(f"PR #{pr_number}:\n{summary}\n")

    if queue_modified and not args.dry_run:
        queue["queue"] = queue_ids
        save_yaml(QUEUE_FILE, queue)
    if tasks_modified and not args.dry_run:
        save_yaml(TASKS_FILE, tasks)


if __name__ == "__main__":
    main()
