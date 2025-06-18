from pathlib import Path

import pytest

import agentic_index_cli.internal.inject_readme as inj


def test_missing_markers(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "top100.md").write_text(
        "| Rank | Repo | Description | Score | Stars | Δ Stars |\n"
        "|-----:|------|-------------|------:|------:|--------:|\n"
    )
    (data_dir / "repos.json").write_text('{"schema_version":3,"repos":[]}')
    (data_dir / "last_snapshot.json").write_text("[]")
    by_cat = data_dir / "by_category"
    by_cat.mkdir()
    (by_cat / "index.json").write_text("{}")
    readme.write_text("no table here")

    monkeypatch.setattr(inj, "README_PATH", readme)
    monkeypatch.setattr(inj, "DATA_PATH", data_dir / "top100.md")
    monkeypatch.setattr(inj, "REPOS_PATH", data_dir / "repos.json")
    monkeypatch.setattr(inj, "SNAPSHOT", data_dir / "last_snapshot.json")
    monkeypatch.setattr(inj, "BY_CAT_INDEX", by_cat / "index.json")
    assert inj.main(top_n=50) == 1


def test_marker_mismatch(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "repos.json").write_text('{"schema_version":2,"repos":[]}')
    (data_dir / "top100.md").write_text("")
    (data_dir / "last_snapshot.json").write_text("[]")
    by_cat = data_dir / "by_category"
    by_cat.mkdir()
    (by_cat / "index.json").write_text("{}")
    readme.write_text("start\n<!-- TOP50:START -->\n<!-- TOP50:END -->\n")

    for name, val in {
        "README_PATH": readme,
        "DATA_PATH": data_dir / "top100.md",
        "REPOS_PATH": data_dir / "repos.json",
        "SNAPSHOT": data_dir / "last_snapshot.json",
        "BY_CAT_INDEX": by_cat / "index.json",
    }.items():
        setattr(inj, name, val)

    with pytest.raises(ValueError, match="TOP100:START"):
        inj.build_readme(top_n=100)
