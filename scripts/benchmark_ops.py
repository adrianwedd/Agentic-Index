#!/usr/bin/env python
"""Benchmark sort and diff operations."""
from __future__ import annotations

import sys
import time
from pathlib import Path

REPOS_PATH = Path("data/repos.json")
BASELINE_SORT = 0.5
BASELINE_DIFF = 0.2
BASELINE_DELTA = 0.1
THRESHOLD = 1.5


def bench_sort() -> float:
    from agentic_index_cli.validate import load_repos

    repos = load_repos(REPOS_PATH, use_cache=True, use_stream=False)
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

    new_text = build_readme(top_n=50)
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


def bench_stars_delta() -> float:
    """Benchmark star delta calculations."""
    from agentic_index_cli.validate import load_repos

    repos = load_repos(REPOS_PATH, use_cache=True, use_stream=False)
    snapshot_path = Path("data/last_snapshot.txt")
    prev_map: dict[str, dict] = {}
    if snapshot_path.exists():
        prev_path = Path(snapshot_path.read_text().strip())
        if not prev_path.is_absolute():
            prev_path = Path("data/history") / prev_path.name
        if prev_path.exists():
            prev_repos = load_repos(prev_path, use_cache=True, use_stream=False)
            prev_map = {r.get("full_name", r.get("name")): r for r in prev_repos}

    start = time.perf_counter()
    for repo in repos:
        prev = prev_map.get(repo.get("full_name", repo.get("name")))
        if prev:
            repo["stars_delta"] = repo.get("stars", 0) - prev.get(
                "stars", prev.get("stargazers_count", 0)
            )
        else:
            repo["stars_delta"] = "+new"
    dur = time.perf_counter() - start
    if dur > BASELINE_DELTA * THRESHOLD:
        print(
            f"WARNING: star delta calc took {dur:.3f}s, baseline {BASELINE_DELTA:.3f}s",
            file=sys.stderr,
        )
    else:
        print(f"stars_delta {dur:.3f}s")
    return dur


if __name__ == "__main__":
    bench_sort()
    bench_diff()
    bench_stars_delta()
