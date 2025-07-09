from fastapi.testclient import TestClient

from .test_api_auth import load_app


def test_status(monkeypatch):
    app, _ = load_app(monkeypatch)
    client = TestClient(app)
    resp = client.get("/status")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_healthz(monkeypatch):
    app, _ = load_app(monkeypatch)
    client = TestClient(app)
    resp = client.get("/healthz")
    assert resp.status_code == 200
