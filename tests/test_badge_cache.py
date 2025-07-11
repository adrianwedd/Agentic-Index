import importlib.util
import urllib.error
import urllib.request
from pathlib import Path

import pytest

pytestmark = pytest.mark.network

import agentic_index_cli.internal.badges as rank_mod

generate_badges = rank_mod.generate_badges


def test_badge_generation_uses_cache(tmp_path, monkeypatch):
    badges = tmp_path / "badges"
    badges.mkdir()
    for name in ["last_sync.svg", "top_repo.svg", "repo_count.svg"]:
        (badges / name).write_text("cached")
    monkeypatch.chdir(tmp_path)

    def fail(*args, **kwargs):
        raise urllib.error.HTTPError(args[0], 503, "err", None, None)

    monkeypatch.setattr(urllib.request, "urlopen", fail)
    generate_badges("repo", "2024-01-01", 5)

    for name in ["last_sync.svg", "top_repo.svg", "repo_count.svg"]:
        assert (badges / name).read_text() == "cached"
