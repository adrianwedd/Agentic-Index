import io
import json
import os
import sys

import pytest
import responses

import agentic_index_cli.issue_logger as il


def test_token_fallback(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("GITHUB_TOKEN_ISSUES", "tok")
    assert il.get_token() == "tok"


def test_cli_create_issue(monkeypatch):
    called = {}

    def fake_create(
        title, body, repo, labels=None, milestone=None, *, token=None, debug=False
    ):
        called["args"] = (title, body, repo, labels, milestone, debug)
        return "x"

    monkeypatch.setattr(il, "create_issue", fake_create)
    il.main(
        [
            "--new-issue",
            "--repo",
            "o/r",
            "--title",
            "t",
            "--body",
            "b",
            "--label",
            "l1",
            "--milestone",
            "3",
            "--debug",
        ]
    )
    assert called["args"] == ("t", "b", "o/r", ["l1"], 3, True)


@responses.activate
def test_post_comment_error(monkeypatch):
    responses.add(
        responses.POST,
        "https://api.github.com/repos/o/r/issues/1/comments",
        json={"message": "bad"},
        status=401,
    )
    with pytest.raises(il.APIError):
        il.post_comment("https://api.github.com/repos/o/r/issues/1", "msg", token="bad")


@responses.activate
def test_post_worklog_new(monkeypatch):
    responses.add(
        responses.GET,
        "https://api.github.com/repos/o/r/issues/1/comments",
        json=[],
        status=200,
    )
    responses.add(
        responses.POST,
        "https://api.github.com/repos/o/r/issues/1/comments",
        json={"html_url": "u", "id": 2},
        status=201,
    )
    data = {
        "task": "T",
        "agent_id": "A",
        "files": ["f.py"],
        "started": "s",
        "finished": "e",
    }
    url = il.post_worklog_comment(
        "https://api.github.com/repos/o/r/issues/1", data, token="t"
    )
    assert url == "u"
    assert "<!-- codex-log -->" in responses.calls[1].request.body.decode()


@responses.activate
def test_post_worklog_update(monkeypatch):
    responses.add(
        responses.GET,
        "https://api.github.com/repos/o/r/issues/1/comments",
        json=[{"id": 9, "body": "<!-- codex-log --> old"}],
        status=200,
    )
    responses.add(
        responses.PATCH,
        "https://api.github.com/repos/o/r/issues/comments/9",
        json={"html_url": "u"},
        status=200,
    )
    data = {"task": "T", "agent_id": "A"}
    url = il.post_worklog_comment(
        "https://api.github.com/repos/o/r/issues/1", data, token="t"
    )
    assert url == "u"
    assert responses.calls[1].request.method == "PATCH"


def test_post_worklog_fallback(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN_ISSUES", raising=False)
    data = {"task": "T"}
    with pytest.raises(il.APIError):
        il.post_worklog_comment("https://api.github.com/repos/o/r/issues/1", data)
    pending = tmp_path / "state" / "worklog_pending.json"
    assert pending.exists()


@responses.activate
def test_update_issue(monkeypatch):
    responses.add(
        responses.PATCH,
        "https://api.github.com/repos/o/r/issues/1",
        json={"html_url": "u"},
        status=200,
    )
    url = il.update_issue(
        "https://api.github.com/repos/o/r/issues/1",
        body="b",
        assignees=["a"],
        token="t",
    )
    assert url == "u"
    body = responses.calls[0].request.body.decode()
    assert "assignees" in body


def test_cli_update(monkeypatch):
    called = {}

    def fake_update(issue_url, **kw):
        called.update({"url": issue_url, **kw})
        return "u"

    monkeypatch.setattr(il, "update_issue", fake_update)
    il.main(
        [
            "--update",
            "--repo",
            "o/r",
            "--issue-number",
            "1",
            "--body",
            "b",
            "--assign",
            "a",
        ]
    )
    assert called["url"].endswith("issues/1")
    assert called["body"] == "b"


def test_cli_body_stdin(monkeypatch):
    called = {}

    def fake_comment(issue_url, body, debug=False):
        called["url"] = issue_url
        called["body"] = body
        return "u"

    monkeypatch.setattr(il, "post_comment", fake_comment)
    monkeypatch.setattr(il, "get_token", lambda: "t")
    monkeypatch.setattr(sys, "stdin", io.StringIO("line1\nline2\n"))
    il.main(
        [
            "--comment",
            "--repo",
            "o/r",
            "--issue-number",
            "1",
            "--body",
            "-",
        ]
    )
    assert called["body"] == "line1\nline2\n"


def test_cli_worklog(monkeypatch, tmp_path):
    data = {"task": "T"}
    p = tmp_path / "wl.json"
    p.write_text(json.dumps(data))
    called = {}

    def fake_post(url, d, debug=False):
        called["url"] = url
        called["data"] = d
        return "u"

    monkeypatch.setattr(il, "post_worklog_comment", fake_post)
    il.main(
        [
            "--worklog",
            str(p),
            "--issue-url",
            "https://api.github.com/repos/o/r/issues/1",
        ]
    )
    assert called["url"].endswith("/1")
    assert called["data"] == data


@responses.activate
def test_worklog_targets(monkeypatch):
    responses.add(
        responses.GET,
        "https://api.github.com/repos/o/r/issues/1/comments",
        json=[],
        status=200,
    )
    responses.add(
        responses.POST,
        "https://api.github.com/repos/o/r/issues/1/comments",
        json={"html_url": "u"},
        status=201,
    )
    data = {"task": "T", "pr_url": "https://api.github.com/repos/o/r/issues/1"}
    url = il.post_worklog_comment(
        "https://api.github.com/repos/o/r/issues/1",
        data,
        token="t",
        targets=["pr", "issue"],
    )
    assert url == "u"
