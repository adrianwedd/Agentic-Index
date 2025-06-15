#!/usr/bin/env python3
"""Parse and process tasks defined in ``codex_tasks.md``.

This script extracts code blocks fenced with ``codex-task`` from a markdown file,
parses the YAML metadata for each task and prints them in a structured format.

The intended task schema is roughly::

    ```codex-task
    id: TASK-001
    title: Example task
    priority: 1
    steps:
      - do one thing
    acceptance_criteria:
      - results logged
    ```

Tasks are sorted by ``priority`` and ``id``. Use ``--start-from`` to begin from a
specific task ID and ``--summary-only`` to only list IDs and titles.
"""
from __future__ import annotations

import argparse
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

from agentic_index_cli import issue_logger

import yaml

# Regex to extract fenced code blocks labelled "codex-task"
CODE_BLOCK_RE = re.compile(r"```codex-task\n(?P<code>.*?)\n```", re.DOTALL)


def parse_tasks(path: Path) -> List[Dict[str, Any]]:
    """Return a list of task dictionaries parsed from ``path``."""
    text = path.read_text(encoding="utf-8")
    tasks: List[Dict[str, Any]] = []
    seen_ids: set[str] = set()

    for block in CODE_BLOCK_RE.findall(text):
        try:
            data = yaml.safe_load(block) or {}
        except yaml.YAMLError as exc:  # malformed YAML
            logging.warning("YAML error while parsing task block: %s", exc)
            continue

        if not isinstance(data, dict):
            logging.warning("Skipping task block, expected mapping but got %r", data)
            continue

        task_id = data.get("id")
        if not task_id:
            logging.warning("Skipping task block with missing 'id'")
            continue
        if task_id in seen_ids:
            logging.warning("Duplicate task id %s skipped", task_id)
            continue

        try:
            data["priority"] = int(data.get("priority", 0))
        except (ValueError, TypeError):
            logging.warning("Invalid priority for task %s; defaulting to 0", task_id)
            data["priority"] = 0

        tasks.append(data)
        seen_ids.add(task_id)

    return tasks


def sort_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return tasks sorted by ``priority`` then ``id``."""
    return sorted(tasks, key=lambda t: (t.get("priority", 0), t.get("id", "")))


def format_task(task: Dict[str, Any]) -> str:
    lines = [f"ID: {task.get('id')}", f"Title: {task.get('title', '')}"]
    steps = task.get("steps") or []
    if steps:
        lines.append("Steps:")
        lines.extend(f" - {s}" for s in steps)
    ac = task.get("acceptance_criteria") or []
    if ac:
        lines.append("Acceptance Criteria:")
        lines.extend(f" - {c}" for c in ac)
    return "\n".join(lines)


def write_summary(summary: str) -> None:
    """If running in GitHub Actions, append ``summary`` to the step summary."""
    summary_file = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as fh:
            fh.write(summary + "\n")


def run_url() -> str:
    """Return GitHub Actions run URL if available."""
    server = os.getenv("GITHUB_SERVER_URL")
    repo = os.getenv("GITHUB_REPOSITORY")
    run_id = os.getenv("GITHUB_RUN_ID")
    if server and repo and run_id:
        return f"{server}/{repo}/actions/runs/{run_id}"
    return ""


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Process Codex tasks")
    parser.add_argument("--file", default="codex_tasks.md", help="Tasks markdown file")
    parser.add_argument("--start-from", metavar="ID", help="Start processing from this task ID")
    parser.add_argument("--summary-only", action="store_true", help="Only output IDs and titles")
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.exists():
        print(f"Error: tasks file not found: {path}", file=sys.stderr)
        return 1

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    tasks = sort_tasks(parse_tasks(path))
    if args.start_from:
        try:
            start_index = next(i for i, t in enumerate(tasks) if t.get("id") == args.start_from)
            tasks = tasks[start_index:]
        except StopIteration:
            logging.warning("start-from id %s not found", args.start_from)
            tasks = []

    output_lines = []
    if args.summary_only:
        for t in tasks:
            output_lines.append(f"{t.get('id')}: {t.get('title', '')}")
    else:
        run = run_url()
        for t in tasks:
            if t.get("create_issue"):
                repo = t.get("repo")
                if not repo:
                    logging.error("create_issue set but repo missing for %s", t.get("id"))
                else:
                    body = (t.get("body") or "") + f"\n\nTask ID: {t.get('id')}"
                    if run:
                        body += f"\nRun: {run}"
                    labels = t.get("labels") or []
                    try:
                        url = issue_logger.create_issue(t.get("title", ""), body, repo, labels=labels)
                        logging.info("Created issue %s", url)
                    except issue_logger.APIError as exc:
                        logging.error("Failed to create issue for %s: %s", t.get("id"), exc)
            output_lines.append(format_task(t))
            output_lines.append("")

    output = "\n".join(output_lines).rstrip()
    if output:
        print(output)
        write_summary(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
