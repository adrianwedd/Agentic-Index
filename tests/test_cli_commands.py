import io
import sys
from pathlib import Path

import agentic_index_cli.enricher as enricher
import agentic_index_cli.faststart as faststart
import agentic_index_cli.inject as inject_cli
import agentic_index_cli.internal.scrape as scrape_mod
import agentic_index_cli.prune as prune
import agentic_index_cli.scraper as scraper
from agentic_index_cli.internal import inject_readme


def test_scrape_cli(monkeypatch, tmp_path):
    called = {}

    def fake_scrape(min_stars=0, token=None):
        called["scrape"] = (min_stars, token)
        return [{"full_name": "owner/repo"}]

    def fake_save(path, repos):
        called["save"] = (path, repos)

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GITHUB_TOKEN", "tok")
    monkeypatch.setattr(scrape_mod, "scrape", fake_scrape)
    monkeypatch.setattr(scrape_mod, "save_repos", fake_save)

    sys.argv = ["scrape", "--min-stars", "5"]
    scraper.main()

    assert called["scrape"] == (5, "tok")
    assert called["save"][0] == Path("data/repos.json")
    assert called["save"][1][0]["full_name"] == "owner/repo"


def test_enrich_cli(monkeypatch):
    sample = [
        {
            "name": "repo",
            "full_name": "owner/repo",
            "stargazers_count": 1,
            "forks_count": 0,
            "open_issues_count": 0,
            "pushed_at": "2025-01-01T00:00:00Z",
            "owner": {"login": "owner"},
        }
    ]
    called = {}

    monkeypatch.setattr(enricher, "load_repos", lambda p: sample)
    monkeypatch.setattr(
        enricher, "save_repos", lambda p, d: called.setdefault("save", (p, d))
    )
    monkeypatch.setattr(enricher, "_previous_map", lambda p: {})
    monkeypatch.setattr(enricher, "categorize", lambda d, t: "cat")
    monkeypatch.setattr(enricher, "compute_recency_factor", lambda p: 0)
    monkeypatch.setattr(enricher, "compute_issue_health", lambda o, c: 0)
    monkeypatch.setattr(enricher, "license_freedom", lambda l: 1)
    monkeypatch.setattr(Path, "read_text", lambda self: '{"repos": []}')

    enricher.main(["data.json"])

    assert called["save"][0] == Path("data.json")
    assert called["save"][1][0]["category"] == "cat"


def test_inject_cli(monkeypatch):
    called = {}

    def fake_main(
        force=False, check=False, write=True, sort_by="score", top_n=100, limit=None
    ):
        called["args"] = force

    monkeypatch.setattr(inject_readme, "main", fake_main)
    monkeypatch.setattr(inject_cli, "main", fake_main)
    inject_cli.cli(["--force"])
    assert called["args"] is True


def test_faststart_cli(monkeypatch, tmp_path):
    sample = [
        {
            "full_name": "owner/repo",
            "stars": 6000,
            "doc_completeness": 1,
            "AgenticIndexScore": 10,
            "last_commit": "2025-01-01",
            "category": "A",
            "one_liner": "desc",
        }
    ]
    monkeypatch.setattr(faststart, "load_repos", lambda p: sample)

    written = {}

    class DummyFile(io.StringIO):
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            written["content"] = self.getvalue()

    def fake_open(self, mode="r", *args, **kwargs):
        assert "w" in mode
        written["path"] = self
        return DummyFile()

    monkeypatch.setattr(Path, "open", fake_open)
    monkeypatch.chdir(tmp_path)

    faststart.main(["--top", "1", "repos.json"])

    assert written["path"] == Path("FAST_START.md")
    assert "owner/repo" in written["content"]


import agentic_index_cli.plot_trends as plot_trends


def test_plot_trends_cli(capsys):
    plot_trends.main()
    captured = capsys.readouterr()
    assert "not yet implemented" in captured.out


def test_prune_cli(monkeypatch):
    called = {}

    def fake_prune(
        inactive, repos_path=Path("repos.json"), changelog_path=Path("CHANGELOG.md")
    ):
        called["args"] = (inactive, repos_path, changelog_path)

    monkeypatch.setattr(prune, "prune", fake_prune)
    prune.main(
        ["--inactive", "10", "--repos-path", "r.json", "--changelog-path", "c.md"]
    )

    assert called["args"] == (10, Path("r.json"), Path("c.md"))
