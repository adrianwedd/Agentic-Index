import json
import subprocess
from pathlib import Path

from jsonschema import Draft7Validator


def test_enrich_schema(tmp_path):
    sample = [
        {
            "name": "repo",
            "full_name": "owner/repo",
            "html_url": "https://example.com",
            "description": "",
            "stargazers_count": 10,
            "forks_count": 0,
            "open_issues_count": 0,
            "archived": False,
            "license": {"spdx_id": "MIT"},
            "language": "Python",
            "pushed_at": "2025-01-01T00:00:00Z",
            "owner": {"login": "owner"},
        }
    ]
    path = tmp_path / "repos.json"
    path.write_text(json.dumps({"schema_version": 1, "repos": sample}))
    subprocess.run(
        ["python", "-m", "agentic_index_cli.enricher", str(path)], check=True
    )
    data = json.loads(path.read_text())
    repo = data["repos"][0]
    for key in [
        "stars_log2",
        "recency_factor",
        "issue_health",
        "doc_completeness",
        "license_freedom",
        "ecosystem_integration",
        "stars",
        "stars_delta",
        "score_delta",
        "category",
    ]:
        assert key in repo

    schema_path = Path(__file__).resolve().parents[1] / "schemas" / "repo.schema.json"
    schema = json.loads(schema_path.read_text())
    lic = repo.get("license")
    if isinstance(lic, str):
        repo = dict(repo)
        repo["license"] = {"spdx_id": lic}
    Draft7Validator(schema).validate(repo)


import pytest


def test_enrich_schema_error(tmp_path):
    repo = {
        "full_name": "owner/repo",
        "stargazers_count": 1,
        "forks_count": 0,
        "open_issues_count": 0,
        "license": {"spdx_id": "MIT"},
        "owner": {"login": "owner"},
    }
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"schema_version": 1, "repos": [repo]}))
    with pytest.raises(Exception):
        enricher.enrich(path)
