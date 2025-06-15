import agentic_index_cli.agentic_index as ai


def test_search_and_harvest_pagination(monkeypatch):
    calls = []

    def fake_github_search(query, page):
        calls.append(page)
        return [{"full_name": f"repo{page}"}]

    def fake_harvest_repo(name):
        return {"name": name, ai.SCORE_KEY: 1}

    monkeypatch.setattr(ai, "SEARCH_TERMS", ["term"])
    monkeypatch.setattr(ai, "TOPIC_FILTERS", [])
    monkeypatch.setattr(ai, "github_search", fake_github_search)
    monkeypatch.setattr(ai, "harvest_repo", fake_harvest_repo)

    repos = ai.search_and_harvest(min_stars=0, max_pages=3)
    assert [r["name"] for r in repos] == ["repo1", "repo2", "repo3"]
    assert calls == [1, 2, 3]
