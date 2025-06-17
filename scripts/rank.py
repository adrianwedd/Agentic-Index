#!/usr/bin/env python3
"""CLI wrapper for ranking repositories."""

import argparse
import sys
from pathlib import Path

# ensure agentic_index_cli is importable when executed via `python scripts/rank.py`
sys.path.append(str(Path(__file__).resolve().parents[1]))

from agentic_index_cli.config import load_config
from agentic_index_cli.internal.rank import generate_badges, main


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rank repositories")
    parser.add_argument("path", nargs="?", default="data/repos.json")
    parser.add_argument("--config")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    cfg = load_config(args.config) if args.config else None
    if cfg is None:
        main(args.path)
    else:
        main(args.path, config=cfg)
