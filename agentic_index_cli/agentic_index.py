"""GitHub scraping and ranking helpers used by the CLI."""

import argparse
import csv
import json
import math
import os
import sys
import time
from datetime import datetime, timedelta
from rich.progress import track
from pathlib import Path
from typing import Dict, List, Optional
import requests

SCORE_KEY = "AgenticIndexScore"

GITHUB_API = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
}
TOKEN = os.getenv("GITHUB_TOKEN")
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

SEARCH_TERMS = [
    "agent framework",
    "LLM agent",
]
TOPIC_FILTERS = [
    "agent",
]

PERMISSIVE_LICENSES = {
    "mit",
    "apache-2.0",
    "bsd-2-clause",
    "bsd-3-clause",
    "isc",
    "zlib",
    "mpl-2.0",
}
VIRAL_LICENSES = {
    "gpl-3.0",
    "gpl-2.0",
    "agpl-3.0",
    "agpl-2.0",
}


def github_search(query: str, page: int = 1) -> List[Dict]:
    """Return GitHub search results for ``query``."""
    time.sleep(1)  # rate limiting
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 5,
        "page": page,
    }
    resp = requests.get(f"{GITHUB_API}/search/repositories", params=params, headers=HEADERS)
    if resp.status_code != 200:
        print(f"GitHub search error {resp.status_code}: {resp.text}", file=sys.stderr)
        return []
    data = resp.json()
    return data.get("items", [])


def fetch_repo(full_name: str) -> Optional[Dict]:
    """Return repository metadata for ``full_name``."""
    time.sleep(1)
    resp = requests.get(f"{GITHUB_API}/repos/{full_name}", headers=HEADERS)
    if resp.status_code != 200:
        print(f"Repo fetch error {full_name} {resp.status_code}", file=sys.stderr)
        return None
    return resp.json()


def fetch_readme(full_name: str) -> str:
    """Return decoded README text for ``full_name``."""
    time.sleep(1)
    resp = requests.get(f"{GITHUB_API}/repos/{full_name}/readme", headers=HEADERS)
    if resp.status_code != 200:
        return ""
    data = resp.json()
    if "content" in data:
        import base64
        return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
    return ""


def compute_recency_factor(pushed_at: str) -> float:
    """Return a freshness score based on ``pushed_at`` timestamp."""
    pushed_date = datetime.strptime(pushed_at, "%Y-%m-%dT%H:%M:%SZ")
    days = (datetime.utcnow() - pushed_date).days
    if days <= 30:
        return 1.0
    if days >= 365:
        return 0.0
    return max(0.0, 1 - (days - 30) / 335)


def compute_issue_health(open_issues: int, closed_issues: int) -> float:
    """Return ratio of closed to total issues."""
    denom = open_issues + closed_issues + 1e-6
    return 1 - open_issues / denom


def readme_doc_completeness(readme: str) -> float:
    """Return 1.0 if README is long and contains code blocks."""
    words = len(readme.split())
    has_code = "```" in readme
    if words >= 300 and has_code:
        return 1.0
    return 0.0


def license_freedom(license_spdx: Optional[str]) -> float:
    """Score how permissive a license is."""
    if not license_spdx:
        return 0.0
    key = license_spdx.lower()
    if key in PERMISSIVE_LICENSES:
        return 1.0
    if key in VIRAL_LICENSES:
        return 0.5
    return 0.5


def ecosystem_integration(topics: List[str], readme: str) -> float:
    """Return 1.0 if popular ecosystem keywords are present."""
    text = " ".join(topics).lower() + " " + readme.lower()
    keywords = ["langchain", "plugin", "openai", "tool", "extension", "framework"]
    for k in keywords:
        if k in text:
            return 1.0
    return 0.0


def categorize(description: str, topics: List[str]) -> str:
    """Return a coarse category for a project."""
    text = (description or "").lower() + " " + " ".join(topics).lower()
    if "rag" in text or "retrieval" in text:
        return "RAG-centric"
    if "multi-agent" in text or "crew" in text or "team" in text:
        return "Multi-Agent"
    if "dev" in text or "tool" in text or "test" in text:
        return "DevTools"
    if any(domain in text for domain in ["video", "game", "finance", "security"]):
        return "Domain-Specific"
    if "experimental" in text or "research" in text:
        return "Experimental"
    return "General-purpose"


def compute_score(repo: Dict, readme: str) -> float:
    """Compute the Agentic Index score for ``repo``."""
    stars = repo.get("stargazers_count", 0)
    open_issues = repo.get("open_issues_count", 0)
    closed_issues = repo.get("closed_issues", 0)
    recency = compute_recency_factor(repo.get("pushed_at"))
    issue_health = compute_issue_health(open_issues, closed_issues)
    doc_comp = readme_doc_completeness(readme)
    lic = repo.get("license")
    if isinstance(lic, dict):
        lic = lic.get("spdx_id")
    license_free = license_freedom(lic)
    eco = ecosystem_integration(repo.get("topics", []), readme)
    score = (
        0.30 * math.log2(stars + 1)
        + 0.25 * recency
        + 0.20 * issue_health
        + 0.15 * doc_comp
        + 0.07 * license_free
        + 0.03 * eco
    )
    return round(score * 100 / 8, 2)  # normalized roughly to 0-100


def harvest_repo(full_name: str) -> Optional[Dict]:
    """Return normalized data for ``full_name``."""
    repo = fetch_repo(full_name)
    if not repo:
        return None
    readme = fetch_readme(full_name)
    score = compute_score(repo, readme)
    category = categorize(repo.get("description", ""), repo.get("topics", []))
    first_paragraph = readme.split("\n\n")[0][:200]
    return {
        "name": full_name,
        "description": repo.get("description", ""),
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "open_issues": repo.get("open_issues_count", 0),
        "closed_issues": repo.get("closed_issues", 0),
        "last_commit": repo.get("pushed_at", ""),
        "language": repo.get("language", ""),
        "license": (repo.get("license") if not isinstance(repo.get("license"), dict) else repo.get("license").get("spdx_id")),
        "maintainer": repo.get("owner", {}).get("login"),
        "topics": ",".join(repo.get("topics", [])),
        "readme_excerpt": first_paragraph,
        SCORE_KEY: score,
        "category": category,
    }


def search_and_harvest(min_stars: int = 0, max_pages: int = 1) -> List[Dict]:
    """Search GitHub and harvest repo metadata."""
    seen = set()
    results = []
    for term in SEARCH_TERMS:
        for page in track(
            range(1, max_pages + 1),
            description=f"{term}",
            disable=not sys.stderr.isatty(),
        ):
            query = f"{term} stars:>={min_stars}"
            repos = github_search(query, page)
            for repo in repos:
                full_name = repo["full_name"]
                if full_name in seen:
                    continue
                seen.add(full_name)
                meta = harvest_repo(full_name)
                if meta:
                    results.append(meta)
    # Topic filter
    for topic in TOPIC_FILTERS:
        for page in track(
            range(1, max_pages + 1),
            description=f"topic:{topic}",
            disable=not sys.stderr.isatty(),
        ):
            query = f"topic:{topic} stars:>={min_stars}"
            repos = github_search(query, page)
            for repo in repos:
                full_name = repo["full_name"]
                if full_name in seen:
                    continue
                seen.add(full_name)
                meta = harvest_repo(full_name)
                if meta:
                    results.append(meta)
    return results


def sort_and_select(repos: List[Dict], limit: int = 100) -> List[Dict]:
    """Return the top ``limit`` repos sorted by score."""
    repos.sort(key=lambda x: x[SCORE_KEY], reverse=True)
    return repos[:limit]


def save_csv(repos: List[Dict], path: Path):
    """Write ``repos`` to ``path`` as CSV."""
    keys = [
        "name",
        "stars",
        "last_commit",
        SCORE_KEY,
        "category",
        "description",
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in repos:
            writer.writerow({k: r[k] for k in keys})


def save_markdown(repos: List[Dict], path: Path):
    """Write a Markdown table of ``repos`` to ``path``."""
    with path.open("w") as f:
        f.write("| # | Repo | ★ | Last Commit | Score | Category | One-liner |\n")
        f.write("|---|------|----|------------|-------|----------|-----------|\n")
        for i, r in enumerate(repos, 1):
            date = r["last_commit"].split("T")[0]
            line = (
                f"| {i} | {r['name']} | {r['stars']} | {date} | {r[SCORE_KEY]} | {r['category']} | {r['description']} |\n"
            )
            f.write(line)


def load_previous(path: Path) -> List[str]:
    """Load previously ranked repository names from ``path``."""
    if not path.exists():
        return []
    with path.open() as f:
        reader = csv.DictReader(f)
        return [row["name"] for row in reader]


def changelog(old: List[str], new: List[str]) -> List[Dict]:
    """Return changelog entries comparing old and new repo lists."""
    old_set = set(old)
    new_set = set(new)
    changes = []
    for name in new_set - old_set:
        changes.append({"repo": name, "action": "Added"})
    for name in old_set - new_set:
        changes.append({"repo": name, "action": "Removed"})
    return changes


def save_changelog(changes: List[Dict], path: Path):
    """Write changelog entries to ``path``."""
    if not changes:
        return
    with path.open("w") as f:
        f.write("| Repo | Action |\n|------|--------|\n")
        for c in changes:
            f.write(f"| {c['repo']} | {c['action']} |\n")


def run_index(min_stars: int = 0, iterations: int = 1, output: Path = Path("data")) -> None:
    is_test = os.getenv("PYTEST_CURRENT_TEST") is not None

    """Run the full indexing workflow."""

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
        save_csv(final_repos, output / "top50.csv")
        save_markdown(final_repos, output / "top50.md")
        changes = changelog(prev_repos, [r["name"] for r in final_repos])
        save_changelog(changes, output / "CHANGELOG.md")


def main():
    """CLI for running :func:`run_index`."""
    parser = argparse.ArgumentParser(description="Agentic Index Repo Indexer")
    parser.add_argument("--min-stars", type=int, default=0)
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--output", type=Path, default=Path("data"))
    args = parser.parse_args()

    run_index(args.min_stars, args.iterations, args.output)


if __name__ == "__main__":
    main()
