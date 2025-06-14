from pathlib import Path

import agentic_index_cli.internal.inject_readme as inj


def test_inject_readme(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    table = (
        "| Rank | <abbr title=\"Score\">📊</abbr> Score | Repo | <abbr title=\"Stars gained in last 30 days\">⭐ Δ30d</abbr> | <abbr title=\"Maintenance score\">🔧 Maint</abbr> | <abbr title=\"Last release date\">📅 Release</abbr> | <abbr title=\"Documentation score\">📚 Docs</abbr> | <abbr title=\"Ecosystem fit\">🧠 Fit</abbr> | <abbr title=\"License\">⚖️ License</abbr> |\n|-----:|------:|------|-------:|-------:|-----------|-------:|-------:|---------|\n| 1 | 1.00 | x | 1 | 0.50 | - | 0.50 | 0.30 | MIT |\n"
    )
    (data_dir / "top50.md").write_text(table)
    (data_dir / "repos.json").write_text(
        '{"schema_version":2,"repos":[{"name":"x","full_name":"o/x","AgenticIndexScore":1.0,"stars_30d":1,"maintenance":0.5,"docs_score":0.5,"ecosystem":0.3,"last_release":null,"license":"MIT"}]}'
    )

    monkeypatch.setattr(inj, "REPOS_PATH", data_dir / "repos.json")
    monkeypatch.setattr(inj, "SNAPSHOT", data_dir / "last_snapshot.json")

    readme.write_text(
        "start\n<!-- TOP50:START -->\nold\n<!-- TOP50:END -->\nend\n"
    )

    monkeypatch.setattr(inj, "README_PATH", readme)
    monkeypatch.setattr(inj, "DATA_PATH", data_dir / "top50.md")

    assert inj.main() == 0
    content = readme.read_text()
    assert "| 1 | 1.00 | x |" in content
    assert content.count("<!-- TOP50:START -->") == 1
