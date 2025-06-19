from pathlib import Path

import agentic_index_cli.__main__ as main
import agentic_index_cli.cli as ai
import agentic_index_cli.enricher as enricher
import agentic_index_cli.faststart as faststart
import agentic_index_cli.prune as prune


def test_main_scrape(monkeypatch, tmp_path):
    called = {}

    def fake_run_index(min_stars, iterations, output):
        called["args"] = (min_stars, iterations, output)

    monkeypatch.setattr(ai, "run_index", fake_run_index)
    main.main(
        ["scrape", "--min-stars", "1", "--iterations", "2", "--output", str(tmp_path)]
    )
    assert called["args"] == (1, 2, Path(tmp_path))


def _patch_common(monkeypatch):
    monkeypatch.setattr(main, "configure_logging", lambda *a, **k: None)
    monkeypatch.setattr(main, "configure_sentry", lambda *a, **k: None)


def test_main_enrich(monkeypatch):
    _patch_common(monkeypatch)
    called = {}

    def fake_enrich(args):
        called["args"] = args

    monkeypatch.setattr(enricher, "main", fake_enrich)
    main.main(["enrich", "repos.json"])

    assert called["args"] == ["repos.json"]


def test_main_faststart(monkeypatch):
    _patch_common(monkeypatch)
    called = {}

    def fake_run(top, path):
        called["args"] = (top, path)

    monkeypatch.setattr(faststart, "run", fake_run)
    main.main(["faststart-cmd", "--top", "3", "data.json"])

    assert called["args"] == (3, Path("data.json"))


def test_main_prune(monkeypatch):
    _patch_common(monkeypatch)
    called = {}

    def fake_prune(inactive, repos_path, changelog_path):
        called["args"] = (inactive, repos_path, changelog_path)

    monkeypatch.setattr(prune, "prune", fake_prune)
    main.main(
        [
            "prune-cmd",
            "--inactive",
            "30",
            "--repos-path",
            "r.json",
            "--changelog-path",
            "CHANGELOG.md",
        ]
    )

    assert called["args"] == (30, Path("r.json"), Path("CHANGELOG.md"))
