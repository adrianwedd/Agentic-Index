import json
import os
from pathlib import Path

REQUIRED_KEYS = [
    "name",
    "full_name",
    "html_url",
    "description",
    "stargazers_count",
    "forks_count",
    "open_issues_count",
    "archived",
    "license",
    "pushed_at",
    "owner",
]

def test_repos_schema():
    path = Path(__file__).resolve().parent.parent / "data" / "repos.json"
    assert path.exists(), f"Missing {path}"
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    assert data.get("schema_version") == 1
    repos = data["repos"]
    assert isinstance(repos, list)
    for item in repos:
        for key in REQUIRED_KEYS:
            assert key in item
        assert "login" in (item.get("owner") or {})
