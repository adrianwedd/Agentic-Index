import json
from fastapi.testclient import TestClient
import importlib
import agentic_index_api.server as srv
from tests.test_api_auth import load_app


def make_client(monkeypatch, tmp_path, data=None):
    if data is not None:
        path = tmp_path / "sync.json"
        path.write_text(json.dumps(data))
    else:
        path = tmp_path / "missing.json"
    app, mod = load_app(monkeypatch, key="k")
    monkeypatch.setattr(mod, "SYNC_DATA_PATH", path)
    return TestClient(app), {"X-API-KEY": "k"}


def test_score_endpoint_loads_data(tmp_path, monkeypatch):
    client, headers = make_client(monkeypatch, tmp_path, [{"name": "repo1"}, {"full_name": "a/b"}])
    resp = client.post("/score", json={}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["top_scores"] == ["repo1", "a/b"]


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
