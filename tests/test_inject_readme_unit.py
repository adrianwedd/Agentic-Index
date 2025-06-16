import json
from pathlib import Path

import pytest

import agentic_index_cli.internal.inject_readme as inj


def _setup(tmp_path: Path, top_n: int = 50) -> Path:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "repos.json").write_text(
        json.dumps(
            {
                "schema_version": 2,
                "repos": [
                    {
                        "name": "x",
                        "full_name": "o/x",
                        "AgenticIndexScore": 1.0,
                        "stars_7d": 1,
                        "maintenance": 0.5,
                        "docs_score": 0.5,
                        "ecosystem": 0.3,
                        "last_release": None,
                        "license": "MIT",
                        "score_delta": 0,
                    }
                ],
            }
        )
    )
    (data_dir / "top100.md").write_text(
        '| Rank | <abbr title="Overall">📊</abbr> Overall | Repo | <abbr title="Stars gained in last 7 days">⭐ Δ7d</abbr> | <abbr title="Maintenance score">🔧 Maint</abbr> | <abbr title="Last release date">📅 Release</abbr> | <abbr title="Documentation score">📚 Docs</abbr> | <abbr title="Ecosystem fit">🧠 Fit</abbr> | <abbr title="License">⚖️ License</abbr> |\n|-----:|------:|------|-------:|-------:|-----------|-------:|-------:|---------|\n| 1 | 1.00 | x | 1 | 0.50 | - | 0.50 | 0.30 | MIT |\n'
    )
    (data_dir / "last_snapshot.json").write_text("[]")
    readme = tmp_path / "README.md"
    readme.write_text(
        f"start\n<!-- TOP{top_n}:START -->\nold\n<!-- TOP{top_n}:END -->\nend\n"
    )

    for name, val in {
        "README_PATH": readme,
        "DATA_PATH": data_dir / "top100.md",
        "REPOS_PATH": data_dir / "repos.json",
        "SNAPSHOT": data_dir / "last_snapshot.json",
    }.items():
        setattr(inj, name, val)
    return readme


def test_inject_and_check(tmp_path, monkeypatch):
    readme = _setup(tmp_path)

    assert inj.main(top_n=50) == 0
    text = readme.read_text()
    assert "| 1 | 1.00 | x |" in text

    assert inj.main(check=True, top_n=50) == 0


def test_check_fails_when_outdated(tmp_path, monkeypatch):
    readme = _setup(tmp_path)
    # write incorrect content
    readme.write_text("start\n<!-- TOP50:START -->\nfoo\n<!-- TOP50:END -->\nend\n")
    assert inj.main(check=True, top_n=50) == 1


@pytest.mark.parametrize(
    "field", ["name", "full_name", "AgenticIndexScore", "score_delta"]
)
def test_missing_required_key(tmp_path, monkeypatch, field):
    _setup(tmp_path)
    data = json.loads(inj.REPOS_PATH.read_text())
    del data["repos"][0][field]
    inj.REPOS_PATH.write_text(json.dumps(data))
    with pytest.raises(KeyError, match=field):
        inj.build_readme(top_n=50)


def test_missing_repos_file(tmp_path, monkeypatch):
    _setup(tmp_path)
    inj.REPOS_PATH.unlink()
    with pytest.raises(FileNotFoundError):
        inj.build_readme(top_n=50)
