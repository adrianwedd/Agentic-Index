import argparse
import json
import math
from pathlib import Path

from .agentic_index import (
    compute_recency_factor,
    compute_issue_health,
    license_freedom,
)


def enrich(path: Path) -> None:
    data = json.loads(path.read_text())
    for repo in data:
        stars = repo.get("stargazers_count", 0)
        repo["stars"] = stars
        repo["stars_log2"] = math.log2(stars + 1)
        repo["recency_factor"] = compute_recency_factor(repo.get("pushed_at", "1970-01-01T00:00:00Z"))
        repo["issue_health"] = compute_issue_health(repo.get("open_issues_count", 0), repo.get("closed_issues", 0))
        repo["doc_completeness"] = repo.get("doc_completeness", 0.0)
        repo["license_freedom"] = license_freedom((repo.get("license") or {}).get("spdx_id"))
        repo.setdefault("ecosystem_integration", 0.0)
    path.write_text(json.dumps(data, indent=2))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Enrich scraped repo data")
    parser.add_argument("json_path", nargs="?", default="data/repos.json")
    args = parser.parse_args(argv)
    enrich(Path(args.json_path))


if __name__ == "__main__":
    main()
