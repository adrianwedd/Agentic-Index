import json
from pathlib import Path
from unittest import mock

import agentic_index_cli.enricher as enricher
import agentic_index_cli.internal.rank as rank
import agentic_index_cli.internal.scrape as scrape


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
    resp.status_code = 200
    return resp


def test_refresh_flags(monkeypatch, tmp_path):
    monkeypatch.setattr(scrape.requests, "get", lambda *a, **kw: make_response(7))
    repos = scrape.scrape(min_stars=5, token=None)
    assert repos and all(r["stargazers_count"] >= 5 for r in repos)

    repo_file = tmp_path / "repos.json"
    repo_file.write_text(json.dumps(repos))
    enricher.enrich(repo_file)
    rank.main(str(repo_file))
    data = json.loads(repo_file.read_text())
    assert "AgenticIndexScore" in data["repos"][0]
