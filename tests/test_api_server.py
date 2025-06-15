from fastapi.testclient import TestClient

from agentic_index_api.server import app


def test_status():
    client = TestClient(app)
    resp = client.get("/status")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_healthz():
    client = TestClient(app)
    resp = client.get("/healthz")
    assert resp.status_code == 200
