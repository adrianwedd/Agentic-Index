#!/usr/bin/env python
"""Validate Codex queue entries against open issues."""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Set

import requests
import yaml

from agentic_index_cli import issue_logger

API_URL = issue_logger.API_URL


def load_queue(path: Path) -> List[str]:
    data = yaml.safe_load(path.read_text()) or {}
    return list(data.get("queue", []))


def fetch_open_tasks(repo: str, token: str | None) -> Set[str]:
    params = {"state": "open", "labels": "source/codex"}
    resp = requests.get(
        f"{API_URL}/repos/{repo}/issues",
        params=params,
        headers=issue_logger._headers(token),
        timeout=10,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"GitHub API error: {resp.status_code} {resp.text}")
    ids: Set[str] = set()
    for item in resp.json():
        m = re.search(r"^Task:\s*(\S+)", item.get("body", ""), re.MULTILINE)
        if m:
            ids.add(m.group(1))
    return ids


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check Codex queue sync")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--file", default=".codex/queue.yml")
    args = parser.parse_args(argv)

    queue_path = Path(args.file)
    if not queue_path.exists():
        print(f"Queue file not found: {queue_path}", file=sys.stderr)
        return 1

    token = issue_logger.get_token()
    queue_ids = set(load_queue(queue_path))
    issue_ids = fetch_open_tasks(args.repo, token)

    to_add = issue_ids - queue_ids
    to_remove = queue_ids - issue_ids

    if to_add:
        print("Add missing tasks:", ", ".join(sorted(to_add)))
    if to_remove:
        print("Remove stale tasks:", ", ".join(sorted(to_remove)))

    return 1 if to_add or to_remove else 0


if __name__ == "__main__":
    sys.exit(main())
