import json
import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scripts.rank as rank
import scripts.scrape as scrape


def make_response(stars):
    item = {
        "name": f"repo{stars}",
        "full_name": f"owner/repo{stars}",
        "html_url": "https://example.com",
        "description": "",
        "stargazers_count": stars,
        "forks_count": 0,
        "open_issues_count": 0,
        "archived": False,
        "license": {"spdx_id": "MIT"},
        "language": "Python",
        "pushed_at": "2025-01-01T00:00:00Z",
        "owner": {"login": "owner"},
    }
    resp = mock.Mock()
    resp.json.return_value = {"items": [item]}
    resp.headers = {"X-RateLimit-Remaining": "100"}
    resp.links = {}
    resp.raise_for_status = mock.Mock()
    return resp


def test_refresh_flags(monkeypatch, tmp_path):
    monkeypatch.setattr(scrape.requests, "get", lambda *a, **kw: make_response(7))
    repos = scrape.scrape(min_stars=5, token=None)
    assert repos and all(r["stargazers_count"] >= 5 for r in repos)

    repo_file = tmp_path / "repos.json"
    repo_file.write_text(json.dumps(repos))

    rank.main(str(repo_file))
    data = json.loads(repo_file.read_text())
    assert "AgenticIndexScore" in data[0]
