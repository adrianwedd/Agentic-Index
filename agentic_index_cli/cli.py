"""Command line interface for the ranking workflow."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List

from rich.progress import track

from .network import search_and_harvest
from .render import changelog, load_previous, save_changelog, save_csv, save_markdown
from .scoring import SCORE_KEY


def sort_and_select(repos: List[Dict], limit: int = 100) -> List[Dict]:
    """Return the top ``limit`` repos sorted by score."""
    repos.sort(key=lambda x: x[SCORE_KEY], reverse=True)
    return repos[:limit]


def run_index(
    min_stars: int = 0, iterations: int = 1, output: Path = Path("data")
) -> None:
    """Run the full indexing workflow."""
    is_test = os.getenv("PYTEST_CURRENT_TEST") is not None
    output.mkdir(parents=True, exist_ok=True)
    prev_csv = output / "top100.csv"
    prev_repos = load_previous(prev_csv)

    final_repos = None
    last_top = None
    for _ in track(
        range(iterations), description="ranking", disable=not sys.stderr.isatty()
    ):
        repos = search_and_harvest(min_stars)
        top = sort_and_select(repos, 100)
        names = [r["name"] for r in top]
        if names == last_top:
            break
        last_top = names
        final_repos = top
    if final_repos is None:
        final_repos = top

    if not is_test or output != Path("data"):
        save_csv(final_repos, output / "top100.csv")
        save_markdown(final_repos, output / "top100.md")
        changes = changelog(prev_repos, [r["name"] for r in final_repos])
        save_changelog(changes, output / "CHANGELOG.md")


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Agentic Index Repo Indexer")
    parser.add_argument("--min-stars", type=int, default=0)
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--output", type=Path, default=Path("data"))
    args = parser.parse_args()

    run_index(args.min_stars, args.iterations, args.output)


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
