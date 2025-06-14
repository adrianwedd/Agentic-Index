import urllib.error
import urllib.request
from pathlib import Path

from agentic_index_cli.internal.rank import fetch_badge


class DummyResp:
    def __init__(self, data: bytes):
        self.data = data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def read(self) -> bytes:
        return self.data


def test_fetch_badge_success(tmp_path, monkeypatch):
    dest = tmp_path / "badge.svg"
    monkeypatch.setattr(urllib.request, "urlopen", lambda url: DummyResp(b"<svg>ok</svg>"))
    fetch_badge("http://example.com", dest)
    assert dest.read_bytes() == b"<svg>ok</svg>"


def test_fetch_badge_404_creates_placeholder(tmp_path, monkeypatch):
    dest = tmp_path / "badge.svg"

    def fail(url):
        raise urllib.error.HTTPError(url, 404, "not found", None, None)

    monkeypatch.setattr(urllib.request, "urlopen", fail)
    fetch_badge("http://example.com", dest)
    assert dest.exists()
    assert "<svg" in dest.read_text()
