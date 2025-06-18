#!/usr/bin/env python3
"""Migrate repos.json from schema v2 to v3."""
import json
import sys
from pathlib import Path

NEW_FIELDS = {
    "stars": 0,
    "stars_delta": 0,
    "score_delta": 0.0,
    "recency_factor": 0.0,
    "issue_health": 0.0,
    "doc_completeness": 0.0,
    "license_freedom": 0.0,
    "ecosystem_integration": 0.0,
    "stars_log2": 0.0,
    "category": "",
    "topics": [],
}


def migrate(path: Path, dest: Path | None = None) -> None:
    data = json.loads(path.read_text())
    data["schema_version"] = 3
    for repo in data.get("repos", []):
        if "docs_score" in repo:
            repo["docs_quality"] = repo.pop("docs_score")
        if "ecosystem" in repo:
            repo["ecosystem_fit"] = repo.pop("ecosystem")
        if isinstance(repo.get("license"), dict):
            repo["license"] = repo["license"].get("spdx_id")
        for key, val in NEW_FIELDS.items():
            repo.setdefault(key, val)
    output = dest or path
    output.write_text(json.dumps(data, indent=2) + "\n")


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    src = Path(argv[0] if argv else "data/repos.json")
    dest = Path(argv[1]) if len(argv) > 1 else None
    migrate(src, dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
