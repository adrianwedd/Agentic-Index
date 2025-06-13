"""AgentOps ranking and research utilities.

This module encapsulates the high-level research loop used for the AgentOps catalogue. The
process begins by seeding GitHub searches with a mix of hand curated queries and topic
filters. Each query fetches a batch of repositories through the GitHub API. Results are
stored and we capture repo metadata such as stars, forks, issue counts, commit history,
primary language, and license information. The crawler also pulls README excerpts so that
projects can be categorised and assessed for documentation quality.

After harvesting raw data we compute a composite score for each repository. The goal of the
score is to surface well maintained, permissively licensed projects that demonstrate strong
community traction. We normalise recency so that active projects are favoured, but we do not
penalise established libraries. Issue health looks at the ratio of open to closed issues to
spot abandoned repos. Documentation completeness checks for a reasonably detailed README
and inline code examples. License freedom considers whether a project uses a permissive or
viral license. Finally, ecosystem integration detects references to popular agent frameworks
or tooling within the README text and repository topics.

The research loop repeats until the top results stabilise across multiple iterations. This
helps smooth out one-off spikes in GitHub search results. Between iterations we also prune
repositories that fall below a minimum star threshold or that clearly lie outside the
framework or tooling categories. The output is a ranked CSV and Markdown table describing
the top repositories along with a simple changelog noting additions or removals since the
previous run.

This docstring acts as the canonical description of the research workflow so that
`docs/METHODOLOGY.md` can be auto-generated and kept in sync with the code. Running the
`gen_methodology.py` script extracts this text and combines it with the scoring formula from
the README to produce the full documentation.

The collected metrics are versioned with each run so that score trends can be analysed over time. We encourage community contributions via pull requests, which can add new search seeds or propose changes to the weighting scheme. Because everything is scripted, the entire pipeline can be executed locally for transparency. The methodology outlined here reflects our current best attempt at a fair ranking system, and feedback is always welcome. Our approach aims to remain lightweight and reproducible so other researchers can fork the pipeline, rerun it on new datasets, and compare results with minimal fuss.
"""

# dummy function to avoid unused module

def identity(x):
    """Return x without modification."""
    return x
=======
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
import sys
import urllib.request
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
    """Download an SVG badge, or write a tiny placeholder if offline."""
    try:
        with urllib.request.urlopen(url) as resp:
            dest.write_bytes(resp.read())
    except Exception:
        dest.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')

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
    repos     = json.loads(data_file.read_text())

    # score + categorise
    for repo in repos:
        repo["score"]    = compute_score(repo)
        repo["category"] = infer_category(repo)

    # sort & persist
    repos.sort(key=lambda r: r["score"], reverse=True)
    data_file.write_text(json.dumps(repos, indent=2))

    # top-50 table
    header = [
        "| Rank | Repo | Score | Category |",
        "|------|------|-------|----------|",
    ]
    rows = [
        f"| {i} | {repo['name']} | {repo['score']} | {repo['category']} |"
        for i, repo in enumerate(repos[:50], start=1)
    ]
    Path("data").mkdir(exist_ok=True)
    Path("data/top50.md").write_text("\n".join(header + rows) + "\n")

    # badges
    today_iso     = datetime.date.today().isoformat()
    top_repo_name = repos[0]["name"] if repos else "unknown"
    generate_badges(top_repo_name, today_iso)

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "data/repos.json"
    main(src)
