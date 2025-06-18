#!/usr/bin/env python3
"""Regenerate dynamic badges without running the full ranking pipeline."""
import argparse
import datetime
import json
from pathlib import Path

from agentic_index_cli.helpers.once_per_day import once_per_day
from agentic_index_cli.internal.badges import generate_badges


def main(json_path: str = "data/repos.json", *, force: bool = False) -> None:
    if not force and not once_per_day("generate_badges"):
        print("Badges already generated today", flush=True)
        return

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
    parser = argparse.ArgumentParser(description="Regenerate dynamic badges")
    parser.add_argument("json", nargs="?", default="data/repos.json")
    parser.add_argument(
        "--force", action="store_true", help="ignore once-per-day guard"
    )
    args = parser.parse_args()
    main(args.json, force=args.force)
