#!/usr/bin/env python3
"""Print tasks sorted by priority."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from validate_tasks import validate_tasks


def rank_tasks(path: str) -> list[dict]:
    tasks = validate_tasks(path)
    return sorted(tasks, key=lambda t: (t.get("priority", 0), str(t.get("id"))))


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    path = argv[0] if argv else "tasks.yml"
    for task in rank_tasks(path):
        pid = task.get("priority")
        tid = task.get("id")
        desc = task.get("description", "")
        print(f"{pid:>2} {tid}: {desc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
