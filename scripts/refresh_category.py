#!/usr/bin/env python3
"""Refresh data for a single category."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# allow running from repo root
sys.path.append(str(Path(__file__).resolve().parents[1]))

import agentic_index_cli.internal.inject_readme as inj
from agentic_index_api.sync_utils import sync
from agentic_index_cli.enricher import enrich
from agentic_index_cli.internal.rank_main import main as rank

TOPIC_MAP = {
    "Frameworks": ["framework"],
    "Multi-Agent Coordination": ["multi-agent", "crew"],
    "RAG-centric": ["rag"],
    "DevTools": ["devtool", "tool"],
    "Domain-Specific": ["video", "game", "finance", "security"],
    "Experimental": ["experiment", "research"],
}


def refresh(category: str, out_dir: Path) -> None:
    topics = TOPIC_MAP.get(category)
    if topics is None:
        raise SystemExit(f"Unknown category: {category}")

    repos = sync(topics=topics)
    out_dir.mkdir(parents=True, exist_ok=True)
    data_path = out_dir / "repos.json"
    data_path.write_text(json.dumps({"repos": repos}, indent=2) + "\n")

    enrich(data_path)
    rank(str(data_path))

    by_cat = out_dir / "by_category"
    inj.write_category_readme(category, force=True, repos_path=data_path)

    index_file = by_cat / "index.json"
    try:
        current = json.loads(index_file.read_text())
    except Exception:
        current = {}
    current[category] = f"{category}.json"
    index_file.write_text(json.dumps(current, indent=2) + "\n")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Refresh data for a category")
    parser.add_argument("category")
    parser.add_argument("--output", default="data")
    args = parser.parse_args(argv)

    refresh(args.category, Path(args.output))


if __name__ == "__main__":
    main()
