import json
import time
import types

import agentic_index_cli.internal.scrape as scrape


def test_scrape_retry_500(monkeypatch):
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
    monkeypatch.setattr(scrape, "QUERIES", ["q"])
    calls = {"n": 0}

    def fake_get(url, params=None, headers=None):
        calls["n"] += 1
        if calls["n"] == 1:
            return scrape.http_utils.Response(500, {"X-RateLimit-Remaining": "1"}, "")
        return scrape.http_utils.Response(
            200,
            {"X-RateLimit-Remaining": "1"},
            json.dumps({"items": [item]}),
        )

    monkeypatch.setattr(
        scrape,
        "github_get",
        lambda *a, **k: scrape.http_utils.Response(
            200, {"X-RateLimit-Remaining": "1"}, json.dumps({"items": [item]})
        ),
    )
    repos = scrape.scrape(0, token=None)
    assert repos[0]["full_name"] == "owner/repo"


def test_scrape_rate_limit_sleep(monkeypatch):
    monkeypatch.setattr(scrape, "QUERIES", ["q"])
    sleeps = {"s": 0}

    def fake_sleep(sec):
        sleeps["s"] = sec

    monkeypatch.setattr(scrape.time, "sleep", fake_sleep)

    monkeypatch.setattr(
        scrape,
        "github_get",
        lambda *a, **k: scrape.http_utils.Response(
            403 if sleeps["s"] == 0 else 200,
            {
                "X-RateLimit-Remaining": "0" if sleeps["s"] == 0 else "1",
                "X-RateLimit-Reset": str(int(time.time()) + 1),
            },
            json.dumps({"items": []}),
        ),
    )
    scrape.scrape(0, token=None)
    assert sleeps["s"] >= 0


def test_scrape_bad_json(monkeypatch):
    monkeypatch.setattr(scrape, "QUERIES", ["q"])
    monkeypatch.setattr(
        scrape,
        "github_get",
        lambda *a, **k: scrape.http_utils.Response(
            200,
            {"X-RateLimit-Remaining": "1"},
            "not-json",
        ),
    )
    repos = scrape.scrape(0, token=None)
    assert repos == []
