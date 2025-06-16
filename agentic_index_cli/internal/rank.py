# -*- coding: utf-8 -*-
"""Rank Agentic-AI repos and generate badges.

Usage:
    python extend_rank.py [data/repos.json]
"""

import datetime
import json
import math
import os
import shutil
import sys
import urllib.request
from pathlib import Path

import lib.quality_metrics  # ensure built-in metrics are registered
from agentic_index_cli.agentic_index import (
    compute_issue_health,
    compute_recency_factor,
    license_freedom,
)
from agentic_index_cli.config import load_config
from agentic_index_cli.validate import load_repos, save_repos
from lib.metrics_registry import get_metrics

# ─────────────────────────  Scoring & categorisation  ──────────────────────────

SCORE_KEY = "AgenticIndexScore"


def compute_score(repo: dict) -> float:
    """Return the Agentic Index score using registered metrics."""

    score = 0.0
    for metric in get_metrics():
        try:
            val = metric.score(repo)
        except Exception:
            val = 0.0
        score += metric.weight * val
    return round(score, 2)


def infer_category(repo: dict) -> str:
    """Derive a high-level category from repo metadata."""
    blob = (
        " ".join(repo.get("topics", []))
        + " "
        + repo.get("description", "")
        + " "
        + repo.get("name", "")
    )
    text = blob.lower()
    if "rag" in text:
        return "RAG-centric"
    if "multi-agent" in text or "multi agent" in text or "crew" in text:
        return "Multi-Agent Coordination"
    if "devtool" in text or "runtime" in text or "tool" in text:
        return "DevTools"
    if "experiment" in text or "research" in text:
        return "Experimental"
    return "General-purpose"


# ─────────────────────────────  Badge helpers  ─────────────────────────────────


def fetch_badge(url: str, dest: Path) -> None:
    """Download an SVG badge or create a local placeholder when offline."""
    if os.getenv("CI_OFFLINE") == "1":
        if dest.exists():
            return
        dest.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"></svg>')
        return
    try:
        resp = urllib.request.urlopen(url)
        try:
            content = resp.read().rstrip(b"\n")
            dest.write_bytes(content)
        finally:
            if hasattr(resp, "close"):
                resp.close()
    except Exception:
        if dest.exists():
            return
        dest.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"></svg>')


def generate_badges(top_repo: str, iso_date: str, repo_count: int) -> None:
    """Create Shields.io badges for the ranking results."""
    badges = Path("badges")
    badges.mkdir(exist_ok=True)

    sync_badge = (
        f"https://img.shields.io/static/v1?label=sync&message={iso_date}&color=blue"
    )
    top_badge = f"https://img.shields.io/static/v1?label=top&message={urllib.request.quote(top_repo)}&color=brightgreen"
    count_badge = f"https://img.shields.io/static/v1?label=repos&message={repo_count}&color=informational"

    fetch_badge(sync_badge, badges / "last_sync.svg")
    fetch_badge(top_badge, badges / "top_repo.svg")
    fetch_badge(count_badge, badges / "repo_count.svg")


# ───────────────────────────────  Main CLI  ────────────────────────────────────


def main(json_path: str = "data/repos.json", *, config: dict | None = None) -> None:
    """Rank repositories and write results back to disk."""
    cfg = config or load_config()
    top_n = cfg.get("ranking", {}).get("top_n", 100)
    delta_days = cfg.get("ranking", {}).get("delta_days", 7)
    data_file = Path(json_path)
    is_test = os.getenv("PYTEST_CURRENT_TEST") is not None
    repos = load_repos(data_file)

    data_dir = data_file.parent
    history_dir = data_dir / "history"
    history_dir.mkdir(exist_ok=True)
    last_snapshot_file = data_dir / "last_snapshot.txt"
    prev_map = {}
    if last_snapshot_file.exists():
        prev_path = Path(last_snapshot_file.read_text().strip())
        if not prev_path.is_absolute():
            prev_path = history_dir / prev_path.name
        if prev_path.exists():
            try:
                prev_repos = load_repos(prev_path)
                prev_map = {r.get("full_name", r.get("name")): r for r in prev_repos}
            except Exception:
                prev_map = {}
    # temporary shim for older data files
    for repo in repos:
        if "AgentOpsScore" in repo:
            repo[SCORE_KEY] = repo.pop("AgentOpsScore")

    # ensure essential fields exist; fall back to raw GitHub data when missing
    for repo in repos:
        repo.setdefault("stars", repo.get("stargazers_count", 0))
        if "recency_factor" not in repo and repo.get("pushed_at"):
            repo["recency_factor"] = compute_recency_factor(repo["pushed_at"])
        if "issue_health" not in repo:
            repo["issue_health"] = compute_issue_health(
                repo.get("open_issues_count", 0), repo.get("closed_issues", 0)
            )
        repo.setdefault("doc_completeness", 0.0)
        if "license_freedom" not in repo:
            lic = repo.get("license")
            if isinstance(lic, dict):
                lic = lic.get("spdx_id")
            repo["license_freedom"] = license_freedom(lic)
        repo.setdefault("ecosystem_integration", 0.0)
    # avoid mutating tracked repo files during tests
    skip_repo_write = (
        is_test and Path(json_path).resolve() == Path("data/repos.json").resolve()
    )
    skip_top_write = is_test

    # score + categorise
    for repo in repos:
        repo[SCORE_KEY] = compute_score(repo)
        repo["category"] = infer_category(repo)
        prev = prev_map.get(repo.get("full_name", repo.get("name")))
        if prev:
            repo["stars_delta"] = repo.get("stars", 0) - prev.get(
                "stars", prev.get("stargazers_count", 0)
            )
            repo["forks_delta"] = repo.get("forks_count", 0) - prev.get(
                "forks_count", 0
            )
            repo["issues_closed_delta"] = repo.get("closed_issues", 0) - prev.get(
                "closed_issues", 0
            )
            repo["score_delta"] = round(
                repo[SCORE_KEY] - float(prev.get(SCORE_KEY, 0)), 2
            )
        else:
            repo["stars_delta"] = "+new"
            repo["forks_delta"] = "+new"
            repo["issues_closed_delta"] = "+new"
            repo["score_delta"] = "+new"

    zero_scores = sum(1 for r in repos if r[SCORE_KEY] == 0)
    allowed_zero = max(1, int(len(repos) * 0.02))
    assert zero_scores <= allowed_zero, "too many repos scored 0.0"

    # sort & persist
    repos.sort(key=lambda r: r[SCORE_KEY], reverse=True)
    if not skip_repo_write:
        save_repos(data_file, repos)
        # persist snapshot
        today_iso = datetime.date.today().isoformat()
        snapshot_path = history_dir / f"{today_iso}.json"
        shutil.copy(data_file, snapshot_path)
        last_snapshot_file.write_text(str(snapshot_path))
        snapshots = sorted(history_dir.glob("*.json"))
        for old in snapshots[:-delta_days]:
            old.unlink()

        # write per-category lists
        by_cat = data_dir / "by_category"
        by_cat.mkdir(exist_ok=True)
        index: dict[str, str] = {}
        for cat in sorted({r.get("category") for r in repos if r.get("category")}):
            cat_repos = [r for r in repos if r.get("category") == cat]
            cat_repos.sort(key=lambda r: r[SCORE_KEY], reverse=True)
            fname = f"{cat}.json"
            save_repos(by_cat / fname, cat_repos)
            index[cat] = fname
        (by_cat / "index.json").write_text(json.dumps(index, indent=2) + "\n")

    # top-50 table
    header = [
        "| Rank | Repo | Score | ▲ StarsΔ | ▲ ScoreΔ | Category |",
        "|-----:|------|------:|-------:|--------:|----------|",
    ]

    def fmt(val):
        if isinstance(val, str):
            return val
        sign = "+" if val >= 0 else ""
        return f"{sign}{val}"

    rows = [
        "| {i} | {name} | {score:.2f} | {sd} | {qd} | {cat} |".format(
            i=i,
            name=repo["name"],
            score=repo[SCORE_KEY],
            sd=fmt(repo["stars_delta"]),
            qd=fmt(repo["score_delta"]),
            cat=repo["category"],
        )
        for i, repo in enumerate(repos[:top_n], start=1)
    ]
    if not skip_top_write:
        Path("data").mkdir(exist_ok=True)
        Path("data/top100.md").write_text("\n".join(header + rows) + "\n")

    # badges
    today_iso = datetime.date.today().isoformat()
    top_repo_name = repos[0]["name"] if repos else "unknown"
    generate_badges(top_repo_name, today_iso, len(repos))
