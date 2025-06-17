import json

import agentic_index_cli.internal.scrape as scrape


def test_scrape_mock(monkeypatch):
    import warnings

    warnings.filterwarnings("ignore", category=DeprecationWarning, module="responses")
    item = {
        "name": "repo",
        "full_name": "owner/repo",
        "html_url": "https://example.com/repo",
        "description": "test repo",
        "stargazers_count": 1,
        "forks_count": 0,
        "open_issues_count": 0,
        "archived": False,
        "license": {"spdx_id": "MIT"},
        "language": "Python",
        "pushed_at": "2025-01-01T00:00:00Z",
        "owner": {"login": "owner"},
    }

    def fake_get(url, params=None, headers=None):
        return scrape.http_utils.Response(
            200,
            {"X-RateLimit-Remaining": "99"},
            json.dumps({"items": [item]}),
        )

    monkeypatch.setattr(scrape.http_utils, "sync_get", fake_get)
    repos = scrape.scrape(min_stars=0, token=None)
    assert repos and repos[0]["full_name"] == "owner/repo"
