from pathlib import Path
import agentic_index_cli.internal.inject_readme as inj


def test_missing_markers(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "top50.md").write_text("| Rank | Repo | Score | Category |\n|------|------|-------|----------|\n")
    readme.write_text("no table here")

    monkeypatch.setattr(inj, "README_PATH", readme)
    monkeypatch.setattr(inj, "DATA_PATH", data_dir / "top50.md")
    assert inj.main() == 1
