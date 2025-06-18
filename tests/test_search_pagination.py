import agentic_index_cli.network as ai


def test_search_and_harvest_pagination(monkeypatch):
    def fake_harvest_repo(name):
        return {"name": name, ai.SCORE_KEY: 1}

    monkeypatch.setattr(ai, "SEARCH_TERMS", ["term"])
    monkeypatch.setattr(ai, "TOPIC_FILTERS", [])

    async def fake_async_search(min_stars=0, max_pages=1):
        return [fake_harvest_repo(f"repo{i}") for i in range(1, 4)]

    monkeypatch.setattr(ai, "async_search_and_harvest", fake_async_search)

    repos = ai.search_and_harvest(min_stars=0, max_pages=3)
    assert [r["name"] for r in repos] == ["repo1", "repo2", "repo3"]
