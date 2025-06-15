import importlib

from fastapi.testclient import TestClient

import agentic_index_api.server as srv


def load_app(monkeypatch, key=None, ips=None):
    if key is not None:
        monkeypatch.setenv("API_KEY", key)
    else:
        monkeypatch.delenv("API_KEY", raising=False)
    if ips is not None:
        monkeypatch.setenv("IP_WHITELIST", ips)
    else:
        monkeypatch.delenv("IP_WHITELIST", raising=False)
    module = importlib.reload(srv)
    return module.app, module


def test_protected_requires_auth(monkeypatch):
    app, _ = load_app(monkeypatch, key="sekret")
    client = TestClient(app)
    for path in ["/sync", "/score", "/render", "/issue"]:
        resp = client.post(path)
        assert resp.status_code == 401


def test_api_key_header(monkeypatch, tmp_path):
    app, mod = load_app(monkeypatch, key="sekret")
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
        resp = client.post(path, headers={"X-API-KEY": "sekret"})
        assert resp.status_code == 200
    resp = client.post(
        "/issue", json={"repo": "o/r", "title": "t"}, headers={"X-API-KEY": "sekret"}
    )
    assert resp.status_code == 200


def test_ip_whitelist(monkeypatch):
    app, mod = load_app(monkeypatch, ips="testclient")
    monkeypatch.setattr(mod, "scrape", lambda *a, **k: [])
    monkeypatch.setattr(mod, "save_repos", lambda *a, **k: None)
    client = TestClient(app)
    resp = client.post("/sync")
    assert resp.status_code == 200


def test_docs(monkeypatch):
    app, _ = load_app(monkeypatch)
    client = TestClient(app)
    resp = client.get("/docs")
    assert resp.status_code == 200
    assert "<html" in resp.text.lower()
