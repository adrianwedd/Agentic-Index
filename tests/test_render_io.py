import datetime
import json
import types
from pathlib import Path

import agentic_index_cli.internal.badges as badges
import agentic_index_cli.internal.snapshot as snap
import agentic_index_cli.render as render
from agentic_index_cli.scoring import SCORE_KEY


def test_save_csv_and_load_previous(tmp_path):
    repos = [
        {
            "name": "repo",
            "stars": 1,
            "last_commit": "2025-01-01T00:00:00Z",
            SCORE_KEY: 1.0,
            "category": "General",
            "description": "d",
        }
    ]
    csv_path = tmp_path / "out.csv"
    render.save_csv(repos, csv_path)
    assert csv_path.exists()
    assert render.load_previous(csv_path) == ["repo"]


def test_markdown_snapshot(tmp_path):
    repos = [
        {
            "name": "owner/repo1",
            "stars": 100,
            "last_commit": "2025-01-01T00:00:00Z",
            SCORE_KEY: 10,
            "category": "General",
            "description": "desc1",
        },
        {
            "name": "owner/repo2",
            "stars": 50,
            "last_commit": "2025-01-02T00:00:00Z",
            SCORE_KEY: 8,
            "category": "General",
            "description": "desc2",
        },
    ]
    md_path = tmp_path / "table.md"
    render.save_markdown(repos, md_path)
    expected = Path(__file__).parent / "snapshots" / "markdown_table.md"
    assert md_path.read_text().strip() == expected.read_text().strip()


def test_generate_badges(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    calls = []

    def fake_fetch(url, dest):
        dest.write_text("svg")
        calls.append(dest)

    monkeypatch.setattr(badges, "fetch_badge", fake_fetch)
    badges.generate_badges("repo", "2025-01-01", 2)
    for name in ["last_sync.svg", "top_repo.svg", "repo_count.svg"]:
        assert (Path("badges") / name).read_text() == "svg"
    assert len(calls) == 3


def test_persist_history_and_write_by_category(tmp_path, monkeypatch):
    data_file = tmp_path / "repos.json"
    data_file.write_text(json.dumps([{"name": "x"}]))
    history = tmp_path / "history"
    history.mkdir()
    (history / "2025-01-01.json").write_text("[]")
    (history / "2025-01-02.json").write_text("[]")

    fake_today = datetime.date(2025, 1, 3)
    monkeypatch.setattr(
        snap,
        "datetime",
        types.SimpleNamespace(date=types.SimpleNamespace(today=lambda: fake_today)),
    )

    snap.persist_history(data_file, [{"name": "x"}], delta_days=2)
    new_file = history / "2025-01-03.json"
    assert new_file.exists()
    assert not (history / "2025-01-01.json").exists()
    last = (tmp_path / "last_snapshot.txt").read_text().strip()
    assert last.endswith("2025-01-03.json")

    repos = [
        {"name": "a", "category": "One", SCORE_KEY: 2.0},
        {"name": "b", "category": "Two", SCORE_KEY: 1.0},
        {"name": "c", "category": "One", SCORE_KEY: 1.0},
    ]
    snap.write_by_category(tmp_path, repos)
    by_cat = tmp_path / "by_category"
    idx = json.loads((by_cat / "index.json").read_text())
    assert idx == {"One": "One.json", "Two": "Two.json"}
    one = json.loads((by_cat / idx["One"]).read_text())["repos"]
    assert [r["name"] for r in one] == ["a", "c"]
