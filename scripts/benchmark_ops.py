#!/usr/bin/env python
"""Benchmark sort, diff and star-delta operations."""
from __future__ import annotations

import sys
import time
from pathlib import Path

REPOS_PATH = Path("data/repos.json")
BASELINE_SORT = 0.5
BASELINE_DIFF = 0.2
BASELINE_STAR_DELTA = 0.3
THRESHOLD = 1.5


def bench_sort() -> float:
    from agentic_index_cli.validate import load_repos

    repos = load_repos(REPOS_PATH, cache=True, stream=False)
    start = time.perf_counter()
    repos.sort(key=lambda r: r.get("AgenticIndexScore", 0), reverse=True)
    dur = time.perf_counter() - start
    if dur > BASELINE_SORT * THRESHOLD:
        print(
            f"WARNING: sorting took {dur:.3f}s, baseline {BASELINE_SORT:.3f}s",
            file=sys.stderr,
        )
    else:
        print(f"sort {dur:.3f}s")
    return dur


def bench_diff() -> float:
    from agentic_index_cli.internal.inject_readme import build_readme, diff

    new_text = build_readme(end_newline=True)
    start = time.perf_counter()
    _ = diff(new_text)
    dur = time.perf_counter() - start
    if dur > BASELINE_DIFF * THRESHOLD:
        print(
            f"WARNING: diff took {dur:.3f}s, baseline {BASELINE_DIFF:.3f}s",
            file=sys.stderr,
        )
    else:
        print(f"diff {dur:.3f}s")
    return dur


def bench_star_delta() -> float:
    """Benchmark star-delta calculations."""
    from agentic_index_cli.validate import load_repos

    history_file = Path("data/last_snapshot.txt")
    last_path = (
        Path(history_file.read_text().strip()) if history_file.exists() else None
    )
    prev_map = {}
    if last_path and last_path.exists():
        prev_repos = load_repos(last_path)
        prev_map = {r.get("full_name", r.get("name")): r for r in prev_repos}

    repos = load_repos(REPOS_PATH, cache=True, stream=False)
    start = time.perf_counter()
    for repo in repos:
        prev = prev_map.get(repo.get("full_name", repo.get("name")))
        if prev:
            _ = repo.get("stars", repo.get("stargazers_count", 0)) - prev.get(
                "stars",
                prev.get("stargazers_count", 0),
            )
        else:
            _ = 0
    dur = time.perf_counter() - start
    if dur > BASELINE_STAR_DELTA * THRESHOLD:
        print(
            f"WARNING: star-delta took {dur:.3f}s, baseline {BASELINE_STAR_DELTA:.3f}s",
            file=sys.stderr,
        )
    else:
        print(f"star-delta {dur:.3f}s")
    return dur


if __name__ == "__main__":
    bench_sort()
    bench_diff()
    bench_star_delta()
