"""Monitor codex_tasks.md and create GitHub issues."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional

import requests
import yaml

from . import issue_logger
from .internal import issue_logger as internal_issue_logger

TASK_RE = re.compile(r"^###\s+(GH-[^\s]+)\s*\u2022?\s*(.*)")
STATE_PATH = Path("state/codex_state.json")


class Task(dict):
    """Simple task container."""

    id: str
    title: str
    body: str


def load_state() -> Dict[str, Dict[str, str]]:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            return {}
    return {}


def save_state(state: Dict[str, Dict[str, str]]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))


def parse_tasks(path: Path) -> List[Task]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    tasks: List[Task] = []
    i = 0
    while i < len(lines):
        m = TASK_RE.match(lines[i])
        if m:
            task_id = m.group(1).strip()
            title = m.group(2).strip()
            body_lines = []
            i += 1
            while i < len(lines) and not TASK_RE.match(lines[i]):
                body_lines.append(lines[i])
                i += 1
            body = "\n".join(body_lines).strip()
            tasks.append(Task(id=task_id, title=title, body=body))
        else:
            i += 1
    return tasks


def task_hash(task: Task) -> str:
    return hashlib.sha1(
        (task["title"] + task["body"]).encode(), usedforsecurity=False
    ).hexdigest()


def load_queue(path: Path) -> List[str]:
    data = yaml.safe_load(path.read_text()) or {}
    return list(data.get("queue", []))


def find_issue_url(repo: str, task_id: str, token: str | None) -> str | None:
    resp = requests.get(
        f"{issue_logger.API_URL}/repos/{repo}/issues",
        params={"state": "open", "labels": "source/codex"},
        headers=issue_logger._headers(token),
        timeout=10,
    )
    if resp.status_code >= 400:
        return None
    for item in resp.json():
        if f"Task: {task_id}" in item.get("body", ""):
            return item.get("url") or item.get("html_url")
    return None


def process_tasks(
    path: Path,
    repo: str,
    *,
    dry_run: bool = False,
    task_id: Optional[str] = None,
    all_tasks: bool = False,
) -> None:
    state = load_state()
    tasks = parse_tasks(path)
    for task in tasks:
        if task_id and task["id"] != task_id:
            continue
        h = task_hash(task)
        info = state.get(task["id"], {})
        if not all_tasks and info.get("hash") == h:
            continue
        body = f"{task['body']}\n\nTask: {task['id']}"
        if dry_run:
            print(f"DRY RUN: would create issue for {task['id']}")
            continue
        try:
            url = issue_logger.create_issue(
                task["title"], body, repo, labels=["type/task", "source/codex"]
            )
        except issue_logger.APIError as exc:
            print(f"Failed to create issue for {task['id']}: {exc}")
            continue
        state[task["id"]] = {"hash": h, "url": url}
        print(f"Created issue {url} for {task['id']}")
    save_state(state)


def process_queue(path: Path, repo: str) -> None:
    state = load_state()
    token = issue_logger.get_token()
    queue_ids = load_queue(path)
    for tid in queue_ids:
        info = state.get(tid, {})
        if info.get("started"):
            continue
        url = info.get("url")
        if not url:
            url = find_issue_url(repo, tid, token)
            if not url:
                continue
            info["url"] = url
        try:
            internal_issue_logger.post_agent_log(url, f"Starting task {tid}")
        except issue_logger.APIError as exc:
            print(f"Failed to post start log for {tid}: {exc}")
            continue
        info["started"] = True
        state[tid] = info
    save_state(state)


def process_worklogs() -> None:
    wl_dir = Path("worklog")
    if not wl_dir.is_dir():
        return
    state = load_state()
    for f in wl_dir.glob("*.json"):
        try:
            data = json.loads(f.read_text())
        except Exception:
            continue
        tid = data.get("task_id")
        if not tid:
            continue
        info = state.get(tid)
        if not info:
            continue
        url = info.get("url")
        if not url:
            continue
        event = data.get("event")
        try:
            if event == "start":
                internal_issue_logger.post_agent_log(
                    url, data.get("cr", ""), data.get("steps")
                )
                info["started"] = True
            else:
                issue_logger.post_worklog_comment(url, data, targets=["issue", "pr"])
                info["completed"] = True
                f.rename(f.with_suffix(".posted"))
        except issue_logger.APIError as exc:
            print(f"Failed to post worklog {f}: {exc}")
            continue
    save_state(state)


def sync_pr(event_json: str) -> None:
    """Handle PR open/ready/closed events."""
    event = json.loads(event_json)
    action = event.get("action")
    if action in {"opened", "ready_for_review"}:
        try:
            issue_logger.create_issue_for_pr(event)
        except issue_logger.APIError as exc:
            print(f"Failed to create tracking issue: {exc}")
    elif action == "closed" and event.get("pull_request", {}).get("merged"):
        try:
            issue_logger.close_issue_for_pr(event)
        except issue_logger.APIError as exc:
            print(f"Failed to close tracking issue: {exc}")


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Codex automation utilities")
    sub = parser.add_subparsers(dest="cmd")

    run_p = sub.add_parser("run", help="Process Codex tasks")
    run_p.add_argument("--repo", required=True)
    run_p.add_argument("--file", default="codex_tasks.md")
    run_p.add_argument("--dry-run", action="store_true")
    run_p.add_argument("--task-id")
    run_p.add_argument("--all", action="store_true")
    run_p.add_argument("--watch", action="store_true")
    run_p.add_argument("--interval", type=int, default=30)

    pr_p = sub.add_parser("sync-pr", help="Sync PR issue")
    pr_p.add_argument("event")

    args = parser.parse_args(argv)

    if args.cmd == "sync-pr":
        sync_pr(args.event)
        return

    # default to run tasks if no subcommand given
    repo = getattr(args, "repo", None)
    if not repo:
        parser.error("--repo required")

    path = Path(args.file)
    if args.watch:
        while True:
            process_tasks(
                path,
                repo,
                dry_run=args.dry_run,
                task_id=args.task_id,
                all_tasks=args.all,
            )
            process_queue(Path(".codex/queue.yml"), repo)
            process_worklogs()
            time.sleep(args.interval)
    else:
        process_tasks(
            path,
            repo,
            dry_run=args.dry_run,
            task_id=args.task_id,
            all_tasks=args.all,
        )
        process_queue(Path(".codex/queue.yml"), repo)
        process_worklogs()


if __name__ == "__main__":
    main()
