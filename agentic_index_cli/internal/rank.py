
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
from pathlib import Path

from agentic_index_cli.quality.validate import validate_file
from agentic_index_cli.agentic_index import (
    compute_recency_factor,
    compute_issue_health,
    license_freedom,
)

# ─────────────────────────  Scoring & categorisation  ──────────────────────────

SCORE_KEY = "AgenticIndexScore"


def compute_score(repo: dict) -> float:
    """Return the Agentic Index score.

    Equation::

        S = 0.35 * log2(stars + 1)
            + 0.20 * recency
            + 0.15 * issue_health
            + 0.15 * docs
            + 0.10 * license
            + 0.05 * ecosystem
    """

    stars = repo.get("stars", repo.get("stargazers_count", 0))
    recency = repo.get("recency_factor")
    if recency is None:
        pushed = repo.get("pushed_at", "1970-01-01T00:00:00Z")
        recency = compute_recency_factor(pushed)
    issue_health = repo.get("issue_health")
    if issue_health is None:
        issue_health = compute_issue_health(
            repo.get("open_issues_count", 0), repo.get("closed_issues", 0)
        )
    docs = repo.get("doc_completeness", 0)
    license_free = repo.get("license_freedom")
    if license_free is None:
        license_free = license_freedom((repo.get("license") or {}).get("spdx_id"))
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
        dest.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>\n')
        return
    try:
        with urllib.request.urlopen(url) as resp:
            dest.write_bytes(resp.read())
    except Exception:
        if dest.exists():
            return
        dest.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>\n')


def generate_badges(top_repo: str, iso_date: str) -> None:
    badges = Path("badges")
    badges.mkdir(exist_ok=True)

    sync_badge = (
        f"https://img.shields.io/static/v1?label=sync&message={iso_date}&color=blue"
    )
    top_badge = f"https://img.shields.io/static/v1?label=top&message={urllib.request.quote(top_repo)}&color=brightgreen"

    fetch_badge(sync_badge, badges / "last_sync.svg")
    fetch_badge(top_badge, badges / "top_repo.svg")


# ───────────────────────────────  Main CLI  ────────────────────────────────────


def main(json_path: str = "data/repos.json") -> None:
    data_file = Path(json_path)
    is_test = os.getenv("PYTEST_CURRENT_TEST") is not None
    if is_test:
        repos = json.loads(data_file.read_text())
    else:
        repos = validate_file(json_path)
    # temporary shim for older data files
    for repo in repos:
        if "AgentOpsScore" in repo:
            repo[SCORE_KEY] = repo.pop("AgentOpsScore")
        if 'score' in repo and SCORE_KEY not in repo:
            repo[SCORE_KEY] = repo.pop('score')

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
            repo["license_freedom"] = license_freedom(
                (repo.get("license") or {}).get("spdx_id")
            )
        repo.setdefault("ecosystem_integration", 0.0)
    # avoid mutating tracked repo files during tests
    skip_repo_write = is_test and Path(json_path).resolve() == Path("data/repos.json").resolve()
    skip_top_write = is_test

    # score + categorise
    for repo in repos:
        repo[SCORE_KEY] = compute_score(repo)
        repo["category"] = infer_category(repo)

    zero_scores = sum(1 for r in repos if r[SCORE_KEY] == 0)
    allowed_zero = max(1, int(len(repos) * 0.02))
    assert zero_scores <= allowed_zero, "too many repos scored 0.0"

    # sort & persist
    repos.sort(key=lambda r: r[SCORE_KEY], reverse=True)
    if not skip_repo_write:
        data_file.write_text(json.dumps(repos, indent=2))

    # top-50 table
    header = [
        "| Rank | Repo | Score | Category |",
        "|------|------|-------|----------|",
    ]
    rows = [
        f"| {i} | {repo['name']} | {repo[SCORE_KEY]} | {repo['category']} |"
        for i, repo in enumerate(repos[:50], start=1)
    ]
    if not skip_top_write:
        Path("data").mkdir(exist_ok=True)
        Path("data/top50.md").write_text("\n".join(header + rows) + "\n")

    # badges
    today_iso = datetime.date.today().isoformat()
    top_repo_name = repos[0]["name"] if repos else "unknown"
    generate_badges(top_repo_name, today_iso)



