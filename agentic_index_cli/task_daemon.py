"""Monitor codex_tasks.md and create GitHub issues."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional

from . import issue_logger

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
    return hashlib.sha1((task["title"] + task["body"]).encode()).hexdigest()


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
        try:
            issue_logger.post_worklog_comment(url, data)
        except issue_logger.APIError as exc:
            print(f"Failed to post worklog {f}: {exc}")
            continue
        f.rename(f.with_suffix(".posted"))


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Process Codex tasks")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--file", default="codex_tasks.md")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--task-id")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--interval", type=int, default=30)
    args = parser.parse_args(argv)

    path = Path(args.file)
    if args.watch:
        while True:
            process_tasks(
                path,
                args.repo,
                dry_run=args.dry_run,
                task_id=args.task_id,
                all_tasks=args.all,
            )
            process_worklogs()
            time.sleep(args.interval)
    else:
        process_tasks(
            path,
            args.repo,
            dry_run=args.dry_run,
            task_id=args.task_id,
            all_tasks=args.all,
        )
        process_worklogs()


if __name__ == "__main__":
    main()
