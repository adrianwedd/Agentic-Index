import json

from fastapi.testclient import TestClient

from agentic_index_cli.internal.rank import compute_score

from .test_api_auth import load_app


def make_client(monkeypatch, tmp_path, data=None):
    if data is not None:
        path = tmp_path / "sync.json"
        path.write_text(json.dumps(data))
    else:
        path = tmp_path / "missing.json"
    app, mod = load_app(monkeypatch, key="k")
    monkeypatch.setattr(mod, "SYNC_DATA_PATH", path)
    return TestClient(app), {"X-API-KEY": "k"}


def test_score_endpoint_calculates_scores(tmp_path, monkeypatch):
    data = [
        {
            "name": "B",
            "stargazers_count": 20,
            "open_issues_count": 0,
            "closed_issues": 20,
            "pushed_at": "2025-06-10T00:00:00Z",
            "license": {"spdx_id": "MIT"},
            "doc_completeness": 0.8,
            "ecosystem_integration": 1.0,
        },
        {
            "name": "A",
            "stargazers_count": 10,
            "open_issues_count": 0,
            "closed_issues": 10,
            "pushed_at": "2025-06-01T00:00:00Z",
            "license": {"spdx_id": "MIT"},
            "doc_completeness": 0.5,
            "ecosystem_integration": 0.0,
        },
    ]
    client, headers = make_client(monkeypatch, tmp_path, data)
    resp = client.post("/score", json={}, headers=headers)
    assert resp.status_code == 200
    returned = resp.json()["top_scores"]

    expected = []
    for repo in data:
        expected.append({"name": repo["name"], "score": compute_score(repo)})
    expected.sort(key=lambda r: r["score"], reverse=True)

    assert returned == expected[:5]


def test_score_missing_file(tmp_path, monkeypatch):
    client, headers = make_client(monkeypatch, tmp_path)
    resp = client.post("/score", json={}, headers=headers)
    assert resp.status_code == 400


def test_score_invalid_file(tmp_path, monkeypatch):
    bad = tmp_path / "bad.json"
    bad.write_text("{}")
    app, mod = load_app(monkeypatch, key="k")
    monkeypatch.setattr(mod, "SYNC_DATA_PATH", bad)
    client = TestClient(app)
    resp = client.post("/score", json={}, headers={"X-API-KEY": "k"})
    assert resp.status_code == 400
