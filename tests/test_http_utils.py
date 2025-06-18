import asyncio
from types import SimpleNamespace
from unittest import mock

import aiohttp
import pytest

from agentic_index_cli.internal import http_utils


class DummyResponse:
    def __init__(self, status=200, headers=None, text="ok"):
        self.status = status
        self.headers = headers or {}
        self._text = text

    async def text(self):
        return self._text


class DummySession:
    def __init__(self, responses):
        self.responses = iter(responses)

    def get(self, *a, **k):
        resp = next(self.responses)

        class CM:
            async def __aenter__(self_inner):
                if isinstance(resp, Exception):
                    raise resp
                return resp

            async def __aexit__(self_inner, exc_type, exc, tb):
                pass

        return CM()


def run_async(coro):
    return asyncio.run(coro)


def test_async_get_success(monkeypatch):
    resp = DummyResponse(status=200, headers={"X": "Y"}, text="data")
    session = DummySession([resp])
    result = run_async(http_utils.async_get("http://x", session=session, retries=1))
    assert result.status_code == 200
    assert result.headers["X"] == "Y"
    assert result.text == "data"


def test_rate_limit_retry(monkeypatch):
    resp1 = DummyResponse(
        status=403,
        headers={"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "10"},
    )
    resp2 = DummyResponse(status=200)
    session = DummySession([resp1, resp2])
    sleep_calls = []

    async def fake_sleep(t):
        sleep_calls.append(t)

    monkeypatch.setattr(http_utils.asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(http_utils.time, "time", lambda: 5)
    result = run_async(http_utils.async_get("http://x", session=session, retries=2))
    assert result.status_code == 200
    assert sleep_calls == [5]


def test_server_error_retry(monkeypatch):
    resp1 = DummyResponse(status=500)
    resp2 = DummyResponse(status=200)
    session = DummySession([resp1, resp2])
    sleep_calls = []

    async def fake_sleep(t):
        sleep_calls.append(t)

    monkeypatch.setattr(http_utils.asyncio, "sleep", fake_sleep)
    result = run_async(http_utils.async_get("http://x", session=session, retries=2))
    assert result.status_code == 200
    assert sleep_calls == [1]


def test_client_error(monkeypatch):
    session = DummySession([aiohttp.ClientError("boom")])
    with pytest.raises(http_utils.APIError):
        run_async(http_utils.async_get("http://x", session=session, retries=1))


def test_sync_get(monkeypatch):
    async def fake_async_get(url, *, session, **kw):
        return http_utils.Response(201, {"A": "B"}, '{"v": 1}')

    monkeypatch.setattr(http_utils, "async_get", fake_async_get)

    class CS:
        async def __aenter__(self):
            return object()

        async def __aexit__(self, exc_type, exc, tb):
            pass

    monkeypatch.setattr(aiohttp, "ClientSession", CS)
    resp = http_utils.sync_get("http://x")
    assert resp.status_code == 201
    assert resp.headers["A"] == "B"
    assert resp.json() == {"v": 1}
