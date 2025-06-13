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
    "language",
    "pushed_at",
    "owner",
]

def test_repos_schema():
    path = Path(__file__).resolve().parent.parent / "data" / "repos.json"
    assert path.exists(), f"Missing {path}"
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    for item in data:
        for key in REQUIRED_KEYS:
            assert key in item
        assert "spdx_id" in (item["license"] or {})
        assert "login" in (item["owner"] or {})
