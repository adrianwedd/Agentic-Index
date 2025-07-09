import asyncio

from agentic_index_cli import github_client as gc
from agentic_index_cli.internal import http_utils


def run_async(coro):
    return asyncio.run(coro)


def test_get_combines_headers(monkeypatch):
    captured = {}

    def fake_sync_get(url, *, params=None, headers=None, **kwargs):
        captured["params"] = params
        captured["headers"] = headers
        return http_utils.Response(200, headers or {}, "{}")

    monkeypatch.setattr(gc.http_utils, "sync_get", fake_sync_get)
    resp = gc.get("http://x", params={"a": 1}, headers={"X": "Y"})
    assert resp.status_code == 200
    assert captured["params"] == {"a": 1}
    assert captured["headers"]["Accept"] == "application/vnd.github+json"
    assert captured["headers"]["X"] == "Y"


def test_async_get(monkeypatch):
    resp = http_utils.Response(200, {}, "ok")

    async def fake_async_get(*args, **kwargs):
        return resp

    monkeypatch.setattr(gc.http_utils, "async_get", fake_async_get)

    class DummySession:
        pass

    result = run_async(gc.async_get("http://x", session=DummySession()))
    assert result is resp
