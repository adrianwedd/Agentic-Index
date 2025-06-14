from pathlib import Path
import json
import agentic_index_cli.internal.inject_readme as inj


def _setup(tmp_path: Path) -> Path:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "repos.json").write_text(
        json.dumps({"schema_version": 1, "repos": [{"name": "x", "full_name": "o/x", "AgenticIndexScore": 1.0, "stars": 1, "category": "cat"}]})
    )
    (data_dir / "top50.md").write_text(
        "| Rank | Repo | Score | ▲ StarsΔ | ▲ ScoreΔ | Category |\n|-----:|------|------:|-------:|--------:|----------|\n| 1 | x | 1.00 | +0 | +0 | cat |\n"
    )
    (data_dir / "last_snapshot.json").write_text('[{"name":"x","AgenticIndexScore":1.0,"stars":1}]')
    readme = tmp_path / "README.md"
    readme.write_text("start\n<!-- TOP50:START -->\nold\n<!-- TOP50:END -->\nend\n")

    for name, val in {
        "README_PATH": readme,
        "DATA_PATH": data_dir / "top50.md",
        "REPOS_PATH": data_dir / "repos.json",
        "SNAPSHOT": data_dir / "last_snapshot.json",
    }.items():
        setattr(inj, name, val)
    return readme


def test_inject_and_check(tmp_path, monkeypatch):
    readme = _setup(tmp_path)

    assert inj.main() == 0
    text = readme.read_text()
    assert "| 1 | x | 1.00 |" in text

    assert inj.main(check=True) == 0


def test_check_fails_when_outdated(tmp_path, monkeypatch):
    readme = _setup(tmp_path)
    # write incorrect content
    readme.write_text("start\n<!-- TOP50:START -->\nfoo\n<!-- TOP50:END -->\nend\n")
    assert inj.main(check=True) == 1
