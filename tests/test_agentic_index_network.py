import base64
import types

import agentic_index_cli.network as ai
import agentic_index_cli.render as rn
import agentic_index_cli.scoring as sc


class DummyResp:
    def __init__(self, data, status=200):
        self._data = data
        self.status_code = status
        self.text = ""

    def json(self):
        return self._data


def test_github_search(monkeypatch):
    captured = {}

    def fake_get(url, params=None, headers=None, **_):
        captured["params"] = params
        return DummyResp({"items": ["ok"]})

    monkeypatch.setattr(
        ai,
        "time",
        types.SimpleNamespace(
            sleep=lambda x: None, time=lambda: 0, perf_counter=lambda: 0
        ),
    )
    monkeypatch.setattr(ai, "github_get", lambda url, **kw: fake_get(url, **kw))
    res = ai.github_search("query", page=3)
    assert res == ["ok"]
    assert captured["params"]["page"] == 3


def test_fetch_repo_and_readme(monkeypatch):
    def fake_get_repo(url, headers=None):
        return DummyResp({"id": 123})

    encoded = base64.b64encode(b"hello").decode()

    def fake_get_readme(url, headers=None):
        return DummyResp({"content": encoded})

    monkeypatch.setattr(
        ai,
        "time",
        types.SimpleNamespace(
            sleep=lambda x: None, time=lambda: 0, perf_counter=lambda: 0
        ),
    )
    monkeypatch.setattr(ai, "github_get", lambda url, **kw: fake_get_repo(url))
    repo = ai.fetch_repo("owner/name")
    assert repo == {"id": 123}

    monkeypatch.setattr(ai, "github_get", lambda url, **kw: fake_get_readme(url))
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
    monkeypatch.setattr(sc, "compute_score", lambda r, rd: 1.0)
    monkeypatch.setattr(sc, "categorize", lambda desc, t: "General")
    res = ai.harvest_repo("owner/name")
    assert res["name"] == "owner/name"
    assert sc.SCORE_KEY in res


def test_error_branches(monkeypatch):
    monkeypatch.setattr(ai, "time", types.SimpleNamespace(sleep=lambda x: None))

    def bad_get(url, params=None, headers=None):
        return DummyResp({}, status=500)

    monkeypatch.setattr(ai, "github_get", lambda url, **kw: bad_get(url))
    assert ai.github_search("q") == []

    assert ai.fetch_repo("name") is None

    assert ai.fetch_readme("name") == ""

    def ok_get(url, params=None, headers=None):
        return DummyResp({}, status=200)

    monkeypatch.setattr(ai, "github_get", lambda url, **kw: ok_get(url))
    assert ai.fetch_readme("name") == ""


def test_harvest_repo_none(monkeypatch):
    monkeypatch.setattr(ai, "fetch_repo", lambda name: None)
    assert ai.harvest_repo("name") is None


def test_search_topics_duplicate(monkeypatch):
    monkeypatch.setattr(
        ai,
        "time",
        types.SimpleNamespace(
            sleep=lambda x: None, time=lambda: 0, perf_counter=lambda: 0
        ),
    )
    calls = []

    def fake_search(query, page):
        calls.append(page)
        return [{"full_name": "dupe"}]

    monkeypatch.setattr(ai, "SEARCH_TERMS", [])
    monkeypatch.setattr(ai, "TOPIC_FILTERS", ["topic"])

    async def fake_async_search(min_stars=0, max_pages=1):
        return [{"name": "dupe"}]

    monkeypatch.setattr(ai, "async_search_and_harvest", fake_async_search)

    repos = ai.search_and_harvest(max_pages=2)
    assert len(repos) == 1
    assert calls == []


def test_changelog_and_save(tmp_path):
    changes = rn.changelog(["a", "b"], ["b", "c"])
    path = tmp_path / "changelog.md"
    rn.save_changelog(changes, path)
    assert path.exists()

    empty = rn.changelog(["a"], ["a"])
    path2 = tmp_path / "none.md"
    rn.save_changelog(empty, path2)
    assert not path2.exists()
