from pathlib import Path
import agentic_index_cli.internal.inject_readme as inj


def test_missing_markers(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "top50.md").write_text(
        "| Rank | <abbr title=\"Overall\">📊</abbr> Overall | Repo | <abbr title=\"Stars gained in last 30 days\">⭐ Δ30d</abbr> | <abbr title=\"Maintenance score\">🔧 Maint</abbr> | <abbr title=\"Last release date\">📅 Release</abbr> | <abbr title=\"Documentation score\">📚 Docs</abbr> | <abbr title=\"Ecosystem fit\">🧠 Fit</abbr> | <abbr title=\"License\">⚖️ License</abbr> |\n|-----:|------:|------|-------:|-------:|-----------|-------:|-------:|---------|\n"
    )
    readme.write_text("no table here")

    monkeypatch.setattr(inj, "README_PATH", readme)
    monkeypatch.setattr(inj, "DATA_PATH", data_dir / "top50.md")
    assert inj.main() == 1
