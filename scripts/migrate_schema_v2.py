#!/usr/bin/env python3
"""Migrate repos.json from schema v1 to v2."""
import json
import sys
from pathlib import Path

NEW_FIELDS = {
    "stars_7d": 0,
    "maintenance": 0.0,
    "docs_score": 0.0,
    "ecosystem": 0.0,
    "last_release": None,
}


def migrate(path: Path, dest: Path | None = None) -> None:
    data = json.loads(path.read_text())
    data["schema_version"] = 2
    for repo in data.get("repos", []):
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
