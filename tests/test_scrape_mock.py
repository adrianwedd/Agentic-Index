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


import requests


@responses.activate
def test_scrape_timeout_retry(monkeypatch):
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

    def fake_get(url, headers=None, params=None):
        calls["n"] += 1
        if calls["n"] < 3:
            raise requests.Timeout("timeout")
        resp = mock.Mock()
        resp.status_code = 200
        resp.json.return_value = {"items": [item]}
        resp.headers = {"X-RateLimit-Remaining": "1"}
        return resp

    monkeypatch.setattr(scrape.requests, "get", fake_get)
    monkeypatch.setattr(scrape.time, "sleep", lambda s: None)
    repos = scrape.scrape(min_stars=0, token=None)
    assert calls["n"] >= 3
    assert repos[0]["full_name"] == "owner/repo"


@responses.activate
def test_scrape_timeout_fail(monkeypatch):
    monkeypatch.setattr(scrape, "QUERIES", ["q"])

    def fail_get(*a, **k):
        raise requests.Timeout("boom")

    monkeypatch.setattr(scrape.requests, "get", fail_get)
    monkeypatch.setattr(scrape.time, "sleep", lambda s: None)
    with pytest.raises(scrape.APIError):
        scrape.scrape(min_stars=0, token=None)


@responses.activate
def test_scrape_rate_limit_retry(monkeypatch):
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

    def rate_limit_get(url, headers=None, params=None):
        calls["n"] += 1
        resp = mock.Mock()
        if calls["n"] == 1:
            resp.status_code = 403
            resp.headers = {
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int(time.time())),
            }
            return resp
        resp.status_code = 200
        resp.json.return_value = {"items": [item]}
        resp.headers = {"X-RateLimit-Remaining": "1"}
        return resp

    monkeypatch.setattr(scrape.requests, "get", rate_limit_get)
    monkeypatch.setattr(scrape.time, "sleep", lambda s: None)
    repos = scrape.scrape(min_stars=0, token=None)
    assert calls["n"] >= 2
    assert repos[0]["full_name"] == "owner/repo"
