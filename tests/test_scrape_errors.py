import json
import time

import responses
from responses import matchers

import agentic_index_cli.internal.scrape as scrape


@responses.activate
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

    def cb(request):
        calls["n"] += 1
        if calls["n"] == 1:
            return (500, {}, "")
        return (
            200,
            {"X-RateLimit-Remaining": "1"},
            json.dumps({"items": [item]}),
        )

    responses.add_callback(
        responses.GET,
        "https://api.github.com/search/repositories",
        callback=cb,
        match=[
            matchers.query_param_matcher(
                {
                    "q": "q stars:>=0",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": "100",
                }
            )
        ],
    )
    monkeypatch.setattr(scrape.time, "sleep", lambda s: None)
    repos = scrape.scrape(0, token=None)
    assert calls["n"] >= 2
    assert repos[0]["full_name"] == "owner/repo"


@responses.activate
def test_scrape_rate_limit_sleep(monkeypatch):
    monkeypatch.setattr(scrape, "QUERIES", ["q"])
    sleeps = {"s": 0}

    def fake_sleep(sec):
        sleeps["s"] = sec

    monkeypatch.setattr(scrape.time, "sleep", fake_sleep)

    def cb(request):
        if sleeps["s"] == 0:
            return (
                403,
                {
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time()) + 1),
                },
                "",
            )
        return (
            200,
            {"X-RateLimit-Remaining": "1"},
            json.dumps({"items": []}),
        )

    responses.add_callback(
        responses.GET,
        "https://api.github.com/search/repositories",
        callback=cb,
        match=[
            matchers.query_param_matcher(
                {
                    "q": "q stars:>=0",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": "100",
                }
            )
        ],
    )

    scrape.scrape(0, token=None)
    assert sleeps["s"] > 0


@responses.activate
def test_scrape_bad_json(monkeypatch):
    monkeypatch.setattr(scrape, "QUERIES", ["q"])
    responses.add(
        responses.GET,
        "https://api.github.com/search/repositories",
        body="not-json",
        headers={"X-RateLimit-Remaining": "1"},
        status=200,
    )
    repos = scrape.scrape(0, token=None)
    assert repos == []
