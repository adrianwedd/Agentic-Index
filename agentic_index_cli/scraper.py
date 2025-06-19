"""CLI entry point for scraping repositories."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import List, Optional

from .internal import scrape as scrape_mod


def main(argv: Optional[List[str]] = None) -> None:
    """Scrape GitHub repositories and write to a JSON file."""

    parser = argparse.ArgumentParser(description="Scrape repositories")
    parser.add_argument("--min-stars", type=int, default=0)
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("data/repos.json"),
        help="Output file path",
    )
    args = parser.parse_args(argv)

    token = os.getenv("GITHUB_TOKEN")
    repos = scrape_mod.scrape(min_stars=args.min_stars, token=token)
    path = args.output
    path.parent.mkdir(parents=True, exist_ok=True)
    scrape_mod.save_repos(path, repos)


def cli(argv: Optional[List[str]] = None) -> None:
    """Entry point for ``python -m agentic_index_cli.scraper``."""

    if argv:
        main(argv)
    else:
        main()


if __name__ == "__main__":
    cli()
