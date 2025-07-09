import importlib

import pytest
from fastapi.testclient import TestClient


def load_app(monkeypatch, key="k", ips=""):
    """Reload the server with the given environment variables."""
    monkeypatch.setenv("API_KEY", key)
    monkeypatch.setenv("IP_WHITELIST", ips)
    import agentic_index_api.server as srv

    module = importlib.reload(srv)
    return module.app, module


def test_protected_requires_auth(monkeypatch):
    app, _ = load_app(monkeypatch, key="sekret")
    client = TestClient(app)
    for path in ["/sync", "/score", "/render", "/issue"]:
        resp = client.post(path)
        assert resp.status_code == 401
        assert resp.json() == {"detail": "unauthorized"}


@pytest.mark.parametrize("mode", ["header", "ip"])
def test_auth_valid(monkeypatch, tmp_path, mode):
    if mode == "header":
        app, mod = load_app(monkeypatch, key="sekret")
        headers = {"X-API-KEY": "sekret"}
    else:
        app, mod = load_app(monkeypatch, ips="testclient")
        headers = {}
    monkeypatch.setattr(mod, "scrape", lambda *a, **k: [])
    monkeypatch.setattr(mod, "save_repos", lambda *a, **k: None)
    sync = tmp_path / "sync.json"
    sync.write_text("[]")
    monkeypatch.setattr(mod, "SYNC_DATA_PATH", sync)
    import sys
    import types

    dummy = types.SimpleNamespace(main=lambda *a, **k: None)
    monkeypatch.setitem(sys.modules, "agentic_index_cli.generate_outputs", dummy)
    monkeypatch.setattr(mod.issue_logger, "create_issue", lambda *a, **k: {})
    client = TestClient(app)
    for path in ["/sync", "/score", "/render"]:
        resp = client.post(path, headers=headers)
        assert resp.status_code == 200
    resp = client.post("/issue", json={"repo": "o/r", "title": "t"}, headers=headers)
    assert resp.status_code == 200


def test_invalid_api_key(monkeypatch):
    app, _ = load_app(monkeypatch, key="sekret")
    client = TestClient(app)
    resp = client.post("/sync", headers={"X-API-KEY": "wrong"})
    assert resp.status_code == 401
    assert resp.json() == {"detail": "unauthorized"}


def test_docs(monkeypatch):
    app, _ = load_app(monkeypatch)
    client = TestClient(app)
    resp = client.get("/docs")
    assert resp.status_code == 200
    assert "<html" in resp.text.lower()
