"""Helpers for enriching scraped repository data."""

import argparse
import json
import math
from pathlib import Path

from jsonschema import Draft7Validator

from .agentic_index import (
    categorize,
    compute_issue_health,
    compute_recency_factor,
    license_freedom,
)
from .validate import load_repos, save_repos


def _previous_map(data_file: Path) -> dict:
    """Return repo mapping from the last snapshot if available."""
    history_dir = data_file.parent / "history"
    last = data_file.parent / "last_snapshot.txt"
    if not last.exists():
        return {}
    prev_path = Path(last.read_text().strip())
    if not prev_path.is_absolute():
        prev_path = history_dir / prev_path.name
    if not prev_path.exists():
        return {}
    try:
        prev_repos = load_repos(prev_path)
    except Exception:
        return {}
    return {r.get("full_name", r.get("name")): r for r in prev_repos}


def enrich(path: Path) -> None:
    """Add derived fields to a repository JSON file."""
    data = load_repos(path)
    prev_map = _previous_map(path)
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
        if lic is not None:
            repo["license"] = {"spdx_id": lic}
        else:
            repo["license"] = None
        repo.setdefault("ecosystem_integration", 0.0)
        repo["category"] = categorize(
            repo.get("description", ""), repo.get("topics", [])
        )
        prev = prev_map.get(repo.get("full_name", repo.get("name")))
        if prev:
            repo["stars_delta"] = stars - prev.get(
                "stars", prev.get("stargazers_count", 0)
            )
            repo["score_delta"] = round(
                float(repo.get("AgenticIndexScore", 0))
                - float(prev.get("AgenticIndexScore", 0)),
                2,
            )
        else:
            repo["stars_delta"] = 0
            repo["score_delta"] = 0.0

    save_repos(path, data)

    schema_path = Path(__file__).resolve().parents[1] / "schemas" / "repo.schema.json"
    schema = json.loads(schema_path.read_text())
    validator = Draft7Validator(schema)
    saved = json.loads(path.read_text())
    repos = saved.get("repos", saved)
    for item in repos:
        lic = item.get("license")
        if isinstance(lic, str):
            item = dict(item)
            item["license"] = {"spdx_id": lic}
        validator.validate(item)


def main(argv=None):
    """Command-line interface for :func:`enrich`."""
    parser = argparse.ArgumentParser(description="Enrich scraped repo data")
    parser.add_argument("json_path", nargs="?", default="data/repos.json")
    args = parser.parse_args(argv)
    enrich(Path(args.json_path))


if __name__ == "__main__":
    main()
