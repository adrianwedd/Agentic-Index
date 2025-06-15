"""Helpers for enriching scraped repository data."""

import argparse
import math
from pathlib import Path

from .agentic_index import (compute_issue_health, compute_recency_factor,
                            license_freedom)
from .validate import load_repos, save_repos


def enrich(path: Path) -> None:
    """Add derived fields to a repository JSON file."""
    data = load_repos(path)
    for repo in data:
        stars = repo.get("stargazers_count", 0)
        repo["stars"] = stars
        repo["stars_log2"] = math.log2(stars + 1)
        repo["recency_factor"] = compute_recency_factor(
            repo.get("pushed_at", "1970-01-01T00:00:00Z")
        )
        repo["issue_health"] = compute_issue_health(
            repo.get("open_issues_count", 0), repo.get("closed_issues", 0)
        )
        repo["doc_completeness"] = repo.get("doc_completeness", 0.0)
        lic = repo.get("license")
        if isinstance(lic, dict):
            lic = lic.get("spdx_id")
        repo["license_freedom"] = license_freedom(lic)
        repo.setdefault("ecosystem_integration", 0.0)
    save_repos(path, data)


def main(argv=None):
    """Command-line interface for :func:`enrich`."""
    parser = argparse.ArgumentParser(description="Enrich scraped repo data")
    parser.add_argument("json_path", nargs="?", default="data/repos.json")
    args = parser.parse_args(argv)
    enrich(Path(args.json_path))


if __name__ == "__main__":
    main()
