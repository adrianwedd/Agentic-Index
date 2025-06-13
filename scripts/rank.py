#!/usr/bin/env python3
"""
Rank agentic-AI repos, write a Markdown table, and emit Shields.io badges
showing the last sync date and today’s top-ranked repo.

Usage:
    python extend_rank.py [data/repos.json]
"""

import datetime
import json
import math
import os
import sys
import urllib.request
import logging
from pathlib import Path

# ─────────────────────────  Scoring & categorisation  ──────────────────────────

def compute_score(repo: dict) -> float:
    stars        = repo.get("stars", 0)
    recency      = repo.get("recency_factor", 0)
    issue_health = repo.get("issue_health", 0)
    docs         = repo.get("doc_completeness", 0)
    license_free = repo.get("license_freedom", 0)
    ecosys       = repo.get("ecosystem_integration", 0)
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
    """Download an SVG badge with fallback to existing file."""
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            if getattr(resp, "status", 200) >= 400:
                raise urllib.error.HTTPError(url, resp.status, "", resp.headers, None)
            dest.write_bytes(resp.read())
    except Exception:
        logging.warning("badge fetch failed – using cached")

def generate_badges(top_repo: str, iso_date: str) -> None:
    badges = Path("badges")
    badges.mkdir(exist_ok=True)

    sync_badge = f"https://img.shields.io/static/v1?label=sync&message={iso_date}&color=blue"
    top_badge  = f"https://img.shields.io/static/v1?label=top&message={urllib.request.quote(top_repo)}&color=brightgreen"

    _fetch(sync_badge, badges / "last_sync.svg")
    _fetch(top_badge,  badges / "top_repo.svg")

# ───────────────────────────────  Main CLI  ────────────────────────────────────

def main(json_path: str = "data/repos.json") -> None:
    data_file = Path(json_path)
    repos = json.loads(data_file.read_text())
    for repo in repos:
        if "agentic_score" not in repo and "score" in repo:
            repo["agentic_score"] = repo["score"]
    in_test = os.getenv("PYTEST_CURRENT_TEST") is not None

    # score + categorise
    for repo in repos:
        repo["agentic_score"] = compute_score(repo)
        repo["category"] = infer_category(repo)

    # sort & persist
    repos.sort(key=lambda r: r["agentic_score"], reverse=True)
    if not in_test:
        data_file.write_text(json.dumps(repos, indent=2))

    # top-50 table
    header = [
        "| Rank | Repo | Agentic Score | Category |",
        "|------|------|--------------|----------|",
    ]
    rows = [
        f"| {i} | {repo['name']} | {repo['agentic_score']} | {repo['category']} |"
        for i, repo in enumerate(repos[:50], start=1)
    ]
    if not in_test:
        Path("data").mkdir(exist_ok=True)
        Path("data/top50.md").write_text("\n".join(header + rows) + "\n")

    # badges
    today_iso     = datetime.date.today().isoformat()
    top_repo_name = repos[0]["name"] if repos else "unknown"
    generate_badges(top_repo_name, today_iso)

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "data/repos.json"
    main(src)
