from pathlib import Path

import agentic_index_cli.internal.inject_readme as inj


def test_inject_readme(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    table = "| Rank | Repo | Score | ▲ StarsΔ | ▲ ScoreΔ | Category |\n|-----:|------|------:|-------:|--------:|----------|\n| 1 | x | 1.00 | +1 | +0.1 | cat |\n"
    (data_dir / "top50.md").write_text(table)
    (data_dir / "repos.json").write_text(
        '{"schema_version":1,"repos":[{"name":"x","full_name":"o/x","AgenticIndexScore":1.0,"category":"cat","stars":1}]}'
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
    assert "| 1 | x | 1.00 |" in content
    assert content.count("<!-- TOP50:START -->") == 1
