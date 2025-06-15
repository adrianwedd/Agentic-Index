import os

import pytest
import responses

import agentic_index_cli.issue_logger as il


def test_token_fallback(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("GITHUB_TOKEN_ISSUES", "tok")
    assert il.get_token() == "tok"


def test_cli_create_issue(monkeypatch):
    called = {}

    def fake_create(title, body, repo):
        called["args"] = (title, body, repo)
        return "x"

    monkeypatch.setattr(il, "create_issue", fake_create)
    il.main(["--new-issue", "--repo", "o/r", "--title", "t", "--body", "b"])
    assert called["args"] == ("t", "b", "o/r")


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
