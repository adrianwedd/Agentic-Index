#!/usr/bin/env python3
"""Rank repos and emit badges summarizing the results.

Usage:
    python extend_rank.py [data/repos.json]
"""

import datetime
import json
import math
import sys
import urllib.request
from pathlib import Path

# ─────────────────────────  Scoring & categorisation  ──────────────────────────

def compute_score(repo: dict) -> float:
    """Compute the ranking score for ``repo``."""

    stars = repo.get("stars", 0)
    recency = repo.get("recency_factor", 0)
    issue_health = repo.get("issue_health", 0)
    docs = repo.get("doc_completeness", 0)
    license_free = repo.get("license_freedom", 0)
    ecosys = repo.get("ecosystem_integration", 0)
    score = (
        0.35 * math.log2(stars + 1)
        + 0.20 * recency
        + 0.15 * issue_health
        + 0.15 * docs
        + 0.10 * license_free
        + 0.05 * ecosys
    )
    return round(score, 2)

def infer_category(repo: dict) -> str:
    """Derive a broad category from repository metadata."""

    blob = " ".join(repo.get("topics", [])) + " " + repo.get("description", "") + " " + repo.get("name", "")
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

def _fetch(url: str, dest: Path) -> None:
    """Download an SVG badge, or write a tiny placeholder if offline."""
    try:
        with urllib.request.urlopen(url) as resp:
            dest.write_bytes(resp.read())
    except Exception:
        dest.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')

def generate_badges(top_repo: str, iso_date: str) -> None:
    """Create SVG badges for badge consumers."""

    badges = Path("badges")
    badges.mkdir(exist_ok=True)

    sync_badge = f"https://img.shields.io/static/v1?label=sync&message={iso_date}&color=blue"
    top_badge  = f"https://img.shields.io/static/v1?label=top&message={urllib.request.quote(top_repo)}&color=brightgreen"

    _fetch(sync_badge, badges / "last_sync.svg")
    _fetch(top_badge,  badges / "top_repo.svg")

# ───────────────────────────────  Main CLI  ────────────────────────────────────

def main(json_path: str = "data/repos.json") -> None:
    """Process ``json_path`` and generate ranking outputs."""

    data_file = Path(json_path)
    repos = json.loads(data_file.read_text())

    # score + categorise
    for repo in repos:
        repo["score"]    = compute_score(repo)
        repo["category"] = infer_category(repo)

    # sort & persist
    repos.sort(key=lambda r: r["score"], reverse=True)
    data_file.write_text(json.dumps(repos, indent=2))

    # top-50 table using the full schema expected by docs
    header = [
        "| Rank | Repo (Click to Visit) | ★ Stars | Last Commit | "
        "Score | Category | One-Liner |",
        "|------|-----------------------|---------|-------------|"
        "-------|----------|-----------|",
    ]
    rows = []
    for i, repo in enumerate(repos[:50], start=1):
        link = f"[{repo['full_name']}](https://github.com/{repo['full_name']})"
        stars = repo.get('stars') or repo.get('stargazers_count', 0)
        stars_str = f"{stars/1000:.1f}k" if stars >= 1000 else str(stars)
        last_commit = repo.get('pushed_at', '')[:10]
        row = (
            f"| {i} | {link} | {stars_str} | {last_commit} | {repo['score']} | "
            f"{repo['category']} | {repo.get('description', '').splitlines()[0]} |"
        )
        rows.append(row)

    Path("data").mkdir(exist_ok=True)
    Path("data/top50.md").write_text("\n".join(header + rows) + "\n")

    # badges
    today_iso     = datetime.date.today().isoformat()
    top_repo_name = repos[0]["name"] if repos else "unknown"
    generate_badges(top_repo_name, today_iso)

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "data/repos.json"
    main(src)
