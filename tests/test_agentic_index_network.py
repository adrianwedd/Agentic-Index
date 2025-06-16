import base64
import types

import agentic_index_cli.agentic_index as ai


class DummyResp:
    def __init__(self, data, status=200):
        self._data = data
        self.status_code = status
        self.text = ""

    def json(self):
        return self._data


def test_github_search(monkeypatch):
    captured = {}

    def fake_get(url, params=None, headers=None):
        captured["params"] = params
        return DummyResp({"items": ["ok"]})

    monkeypatch.setattr(ai, "time", types.SimpleNamespace(sleep=lambda x: None))
    monkeypatch.setattr(ai.requests, "get", fake_get)
    res = ai.github_search("query", page=3)
    assert res == ["ok"]
    assert captured["params"]["page"] == 3


def test_fetch_repo_and_readme(monkeypatch):
    def fake_get_repo(url, headers=None):
        return DummyResp({"id": 123})

    encoded = base64.b64encode(b"hello").decode()

    def fake_get_readme(url, headers=None):
        return DummyResp({"content": encoded})

    monkeypatch.setattr(ai, "time", types.SimpleNamespace(sleep=lambda x: None))
    monkeypatch.setattr(ai.requests, "get", fake_get_repo)
    repo = ai.fetch_repo("owner/name")
    assert repo == {"id": 123}

    monkeypatch.setattr(ai.requests, "get", fake_get_readme)
    text = ai.fetch_readme("owner/name")
    assert text == "hello"


def test_harvest_repo(monkeypatch):
    meta = {
        "description": "d",
        "stargazers_count": 1,
        "forks_count": 1,
        "open_issues_count": 0,
        "closed_issues": 1,
        "pushed_at": "2025-01-01T00:00:00Z",
        "language": "Python",
        "license": {"spdx_id": "MIT"},
        "owner": {"login": "me"},
        "topics": ["tool"],
    }
    monkeypatch.setattr(ai, "fetch_repo", lambda name: meta)
    monkeypatch.setattr(ai, "fetch_readme", lambda name: "README")
    monkeypatch.setattr(ai, "compute_score", lambda r, rd: 1.0)
    monkeypatch.setattr(ai, "categorize", lambda desc, t: "General")
    res = ai.harvest_repo("owner/name")
    assert res["name"] == "owner/name"
    assert ai.SCORE_KEY in res


def test_error_branches(monkeypatch):
    monkeypatch.setattr(ai, "time", types.SimpleNamespace(sleep=lambda x: None))

    def bad_get(url, params=None, headers=None):
        return DummyResp({}, status=500)

    monkeypatch.setattr(ai.requests, "get", bad_get)
    assert ai.github_search("q") == []

    assert ai.fetch_repo("name") is None

    assert ai.fetch_readme("name") == ""

    def ok_get(url, params=None, headers=None):
        return DummyResp({}, status=200)

    monkeypatch.setattr(ai.requests, "get", ok_get)
    assert ai.fetch_readme("name") == ""


def test_harvest_repo_none(monkeypatch):
    monkeypatch.setattr(ai, "fetch_repo", lambda name: None)
    assert ai.harvest_repo("name") is None


def test_search_topics_duplicate(monkeypatch):
    monkeypatch.setattr(ai, "time", types.SimpleNamespace(sleep=lambda x: None))
    calls = []

    def fake_search(query, page):
        calls.append(page)
        return [{"full_name": "dupe"}]

    monkeypatch.setattr(ai, "SEARCH_TERMS", [])
    monkeypatch.setattr(ai, "TOPIC_FILTERS", ["topic"])
    monkeypatch.setattr(ai, "github_search", fake_search)
    monkeypatch.setattr(ai, "harvest_repo", lambda name: {"name": name})

    repos = ai.search_and_harvest(max_pages=2)
    assert len(repos) == 1
    assert calls == [1, 2]


def test_changelog_and_save(tmp_path):
    changes = ai.changelog(["a", "b"], ["b", "c"])
    path = tmp_path / "changelog.md"
    ai.save_changelog(changes, path)
    assert path.exists()

    empty = ai.changelog(["a"], ["a"])
    path2 = tmp_path / "none.md"
    ai.save_changelog(empty, path2)
    assert not path2.exists()
