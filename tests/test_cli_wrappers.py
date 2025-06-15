import sys
from pathlib import Path

# ensure project root for importing "scripts" package
sys.path.append(str(Path(__file__).resolve().parents[1]))

import agentic_index_cli.generate_outputs as gen
import agentic_index_cli.inject as inject
import agentic_index_cli.ranker as ranker
import agentic_index_cli.scraper as scraper


def test_scraper_cli(monkeypatch):
    called = {}

    def fake_main():
        called["scrape"] = True

    monkeypatch.setattr(scraper, "main", fake_main)
    scraper.cli([])
    assert called.get("scrape")


def test_ranker_cli(monkeypatch, tmp_path):
    called = {}

    def fake_main(path):
        called["path"] = path

    monkeypatch.setattr(ranker, "main", fake_main)
    ranker.cli([str(tmp_path / "repos.json")])
    assert called["path"].endswith("repos.json")


def test_inject_cli(monkeypatch):
    called = {}

    def fake_main(force=False):
        called["force"] = force

    monkeypatch.setattr(inject, "main", fake_main)
    inject.cli(["--force"])
    assert called["force"] is True


def test_generate_outputs(monkeypatch):
    called = {}

    def fake_inject(force=False):
        called["force"] = force

    monkeypatch.setattr(gen, "inject", fake_inject)
    gen.main(["--force"])
    assert called["force"] is True
