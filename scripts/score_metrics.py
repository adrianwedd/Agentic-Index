#!/usr/bin/env python3
"""Compute enrichment metrics for repos.json."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from jsonschema import Draft7Validator

from lib.quality_metrics import docs_score, maintenance_score


def _release_age(ts: str | None) -> int | None:
    if not ts:
        return None
    try:
        dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None
    return (datetime.now(timezone.utc) - dt.replace(tzinfo=timezone.utc)).days


def main(path: str = "data/repos.json") -> None:
    p = Path(path)
    data = json.loads(p.read_text())
    repos = data.get("repos", data)
    schema_path = Path(__file__).resolve().parents[1] / "schemas" / "repo.schema.json"
    schema = json.loads(schema_path.read_text())
    validator = Draft7Validator(schema)
    for repo in repos:
        # maintenance score from recency and issue ratio
        days_since_commit = 0.0
        if repo.get("pushed_at"):
            try:
                dt = datetime.strptime(repo["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")
                days_since_commit = (
                    datetime.now(timezone.utc) - dt.replace(tzinfo=timezone.utc)
                ).days
            except Exception:
                pass
        open_issues = repo.get("open_issues_count", 0)
        closed_issues = repo.get("closed_issues", 0)
        denom = open_issues + closed_issues
        ratio = 0.0 if denom == 0 else open_issues / denom
        repo["maintenance"] = maintenance_score(days_since_commit, ratio)

        # docs quality from doc_completeness
        repo["docs_score"] = round(float(repo.get("doc_completeness", 0.0)) * 10, 2)

        # ecosystem fit from ecosystem_integration
        repo["ecosystem"] = round(float(repo.get("ecosystem_integration", 0.0)) * 10, 2)

        repo["license_score"] = round(float(repo.get("license_freedom", 0.0)) * 10, 2)

        repo["release_age"] = _release_age(repo.get("last_release"))

        lic = repo.get("license")
        if isinstance(lic, str):
            check_item = dict(repo)
            check_item["license"] = {"spdx_id": lic}
        else:
            check_item = repo
        validator.validate(check_item)
    p.write_text(json.dumps({"schema_version": 2, "repos": repos}, indent=2) + "\n")

    saved = json.loads(p.read_text())
    for item in saved.get("repos", saved):
        lic = item.get("license")
        if isinstance(lic, str):
            item = dict(item)
            item["license"] = {"spdx_id": lic}
        validator.validate(item)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
