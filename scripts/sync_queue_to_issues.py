#!/usr/bin/env python3
"""Sync .codex/queue.yml entries to GitHub issues."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

from agentic_index_cli import issue_logger


def sync_queue(path: Path, repo: str) -> bool:
    data: Dict[str, Any] = yaml.safe_load(path.read_text()) or {}
    queue = data.get("queue", [])
    changed = False
    new_queue = []

    for item in queue:
        if isinstance(item, dict):
            task_id = item.get("task") or item.get("id")
            issue_id = item.get("issue_id")
            entry = dict(item)
        else:
            task_id = str(item)
            issue_id = None
            entry = {"task": task_id}

        if not issue_id:
            title = task_id
            body = f"Automated task for {task_id}"

            # Check if issue already exists to prevent duplicates
            existing_issues = issue_logger.search_issues(
                f'"{title}" in:title repo:{repo}'
            )
            if existing_issues:
                print(
                    f"Issue for {task_id} already exists: {existing_issues[0]['html_url']}"
                )
                # Extract issue number from existing issue
                entry["issue_id"] = existing_issues[0]["number"]
                changed = True
            else:
                url = issue_logger.create_issue(title, body, repo)
                _, num = issue_logger._parse_issue_url(url)
                entry["issue_id"] = num
                changed = True
        new_queue.append(entry)

    if changed:
        data["queue"] = new_queue
        path.write_text(yaml.safe_dump(data))
    return changed


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: sync_queue_to_issues.py <queue.yml>")
        sys.exit(1)
    queue_path = Path(argv[0])
    repo = os.getenv("GITHUB_REPOSITORY")
    if not repo:
        print("GITHUB_REPOSITORY not set", file=sys.stderr)
        sys.exit(1)
    sync_queue(queue_path, repo)


if __name__ == "__main__":
    main()
