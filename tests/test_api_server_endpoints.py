"""Integration tests for agentic_index_api.server."""

import importlib
import sys
import types

from fastapi.testclient import TestClient

import agentic_index_api.server as srv


def load_app(monkeypatch):
    monkeypatch.setenv("API_KEY", "k")
    module = importlib.reload(srv)
    return TestClient(module.app), module


def test_sync_endpoint(monkeypatch, tmp_path):
    client, mod = load_app(monkeypatch)

    called = {}

    def fake_scrape(min_stars=0, token=None):
        called["min_stars"] = min_stars
        return [{"name": "r"}]

    def fake_save(path, repos):
        called["path"] = path
        called["repos"] = repos

    monkeypatch.setattr(mod, "scrape", fake_scrape)
    monkeypatch.setattr(mod, "save_repos", fake_save)

    resp = client.post("/sync", headers={"X-API-KEY": "k"}, json={"min_stars": 1})
    assert resp.status_code == 200
    assert resp.json() == {"repos": 1}
    assert called["min_stars"] == 1
    assert called["repos"] == [{"name": "r"}]


def test_render_endpoint(monkeypatch):
    client, mod = load_app(monkeypatch)

    called = {}
    dummy = types.SimpleNamespace(main=lambda: called.setdefault("ran", True))
    monkeypatch.setitem(sys.modules, "agentic_index_cli.generate_outputs", dummy)

    resp = client.post("/render", headers={"X-API-KEY": "k"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
    assert called.get("ran") is True
