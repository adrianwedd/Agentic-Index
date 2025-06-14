import urllib.error
import urllib.request
from pathlib import Path
import io

from agentic_index_cli.internal.rank import fetch_badge


class DummyResp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        pass


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


def test_fetch_badge_urlerror(tmp_path, monkeypatch):
    dest = tmp_path / "badge.svg"

    def boom(url):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(urllib.request, "urlopen", boom)
    fetch_badge("http://example.com", dest)
    assert dest.exists()
    assert dest.read_text().startswith("<svg")


def test_fetch_badge_offline_env(tmp_path, monkeypatch):
    dest = tmp_path / "badge.svg"
    monkeypatch.setenv("CI_OFFLINE", "1")
    fetch_badge("http://example.com", dest)
    assert dest.exists()
    assert dest.read_text().startswith("<svg")


def test_fetch_badge_offline_no_overwrite(tmp_path, monkeypatch):
    dest = tmp_path / "badge.svg"
    dest.write_text("old")
    monkeypatch.setenv("CI_OFFLINE", "1")
    fetch_badge("http://example.com", dest)
    assert dest.read_text() == "old"


def test_fetch_badge_error_no_overwrite(tmp_path, monkeypatch):
    dest = tmp_path / "badge.svg"
    dest.write_text("old")

    def boom(url):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(urllib.request, "urlopen", boom)
    fetch_badge("http://example.com", dest)
    assert dest.read_text() == "old"
