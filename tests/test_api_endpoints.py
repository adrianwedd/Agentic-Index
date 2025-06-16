from fastapi.testclient import TestClient

from agentic_index_api import main as api_main

api_main.REPOS[:] = [
    {
        "name": "repo1",
        "full_name": "repo1",
        "stargazers_count": 1,
        "AgenticIndexScore": 1.0,
    }
]
api_main.RANKED[:] = api_main.REPOS[:]
api_main.NAME_MAP.clear()
for r in api_main.REPOS:
    api_main.NAME_MAP[r["name"]] = r

client = TestClient(api_main.app)


def test_repo_endpoint():
    resp = client.get("/repo/repo1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"].lower() == "repo1"
    assert "rank" in data
    assert "score" in data
    assert "stars" in data


def test_history_endpoint():
    resp = client.get("/history/repo1")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data.get("history"), list)
    assert data["history"]
    assert all("score" in h and "date" in h for h in data["history"])
