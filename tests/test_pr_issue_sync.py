import json
from pathlib import Path

import agentic_index_cli.issue_logger as il


def _event():
    return {
        "action": "opened",
        "repository": {"full_name": "o/r"},
        "pull_request": {
            "number": 1,
            "title": "T",
            "body": "b",
            "html_url": "https://github.com/o/r/pull/1",
        },
    }


def test_create_issue_for_pr(monkeypatch):
    event = _event()
    monkeypatch.setattr(
        il.requests,
        "get",
        lambda *a, **k: type("R", (), {"status_code": 200, "json": lambda self: []})(),
    )
    created = {}

    def fake_create(
        title, body, repo, token=None, labels=None, milestone=None, debug=False
    ):
        created["args"] = (title, body, repo)
        return "https://github.com/o/r/issues/2"

    posted = {}

    def fake_post(url, body, token=None, debug=False):
        posted["url"] = url
        posted["body"] = body
        return "c"

    monkeypatch.setattr(il, "create_issue", fake_create)
    monkeypatch.setattr(il, "post_comment", fake_post)
    url = il.create_issue_for_pr(event, token="t")
    assert url.endswith("/issues/2")
    assert created["args"][0] == "T"
    assert posted["url"].endswith("/issues/1")
    assert "tracking-issue" in posted["body"]


def test_create_issue_for_pr_existing(monkeypatch):
    event = _event()

    def fake_get(*a, **k):
        return type(
            "R",
            (),
            {
                "status_code": 200,
                "json": lambda self: [{"body": "<!-- tracking-issue:3 -->"}],
            },
        )()

    monkeypatch.setattr(il.requests, "get", fake_get)
    url = il.create_issue_for_pr(event, token="t")
    assert url.endswith("/issues/3")


def test_close_issue_for_pr(monkeypatch):
    event = _event()
    event["action"] = "closed"
    event["pull_request"]["merged"] = True

    def fake_get(*a, **k):
        return type(
            "R",
            (),
            {
                "status_code": 200,
                "json": lambda self: [{"body": "<!-- tracking-issue:4 -->"}],
            },
        )()

    called = {}

    def fake_post(url, body, token=None, debug=False):
        called.setdefault("post", []).append((url, body))
        return "c"

    def fake_close(url, token=None, debug=False):
        called["close"] = url
        return "u"

    monkeypatch.setattr(il.requests, "get", fake_get)
    monkeypatch.setattr(il, "post_comment", fake_post)
    monkeypatch.setattr(il, "close_issue", fake_close)

    il.close_issue_for_pr(event, token="t")
    assert called["close"].endswith("/issues/4")
    assert any("closing" in b for _, b in called["post"])
