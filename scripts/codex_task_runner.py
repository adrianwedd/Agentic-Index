#!/usr/bin/env python3
"""Simple Codex queue runner."""

from pathlib import Path
import yaml


def load_queue(path: Path = Path('.codex/queue.yml')) -> dict:
    """Return queue definition from YAML file."""
    with path.open('r', encoding='utf-8') as fh:
        return yaml.safe_load(fh)


def run_queue(queue: dict) -> None:
    """Print each task ID in sequence."""
    tasks = queue.get('queue', [])
    for idx, task in enumerate(tasks, 1):
        print(f"[Task {idx}] {task}")
        # In a real implementation this would hand off to Codex CLI


def main() -> None:
    queue = load_queue()
    run_queue(queue)


if __name__ == '__main__':
    main()
