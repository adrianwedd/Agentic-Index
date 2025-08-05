import pytest
from fastapi.testclient import TestClient


def test_sync_endpoint(tmp_path, monkeypatch):
    try:
        from agentic_index_api import sync_utils as sync_module
        from agentic_index_api.simple_app import app
    except Exception as e:
        pytest.skip(f"Could not load API modules: {e}")

    def fake_search(min_stars=0, max_pages=1):
        return [{"maintainer": "openai", "topics": "llm,agents"}]

    monkeypatch.setattr(sync_module, "search_and_harvest", fake_search)
    monkeypatch.setattr(sync_module, "STATE_PATH", tmp_path / "sync.json")
    client = TestClient(app)
    resp = client.post("/sync", json={"org": "openai", "topics": ["llm"]})
    assert resp.status_code == 200
    assert resp.json() == {"synced": 1}
    assert (tmp_path / "sync.json").exists()
