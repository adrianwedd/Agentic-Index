#!/usr/bin/env python3
"""Regenerate dynamic badges without running the full ranking pipeline."""
import datetime
import json
from pathlib import Path

from agentic_index_cli.internal.rank import generate_badges


def main(json_path: str = "data/repos.json") -> None:
    path = Path(json_path)
    data = json.loads(path.read_text())
    repos = data.get("repos", data)
    repo_count = len(repos)
    top_repo = max(
        repos,
        key=lambda r: r.get("AgenticIndexScore", r.get("AgentOpsScore", 0)),
        default={},
    ).get("name", "unknown")
    today_iso = datetime.date.today().isoformat()
    generate_badges(top_repo, today_iso, repo_count)


if __name__ == "__main__":
    main()
