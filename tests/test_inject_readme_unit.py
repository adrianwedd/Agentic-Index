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
                "schema_version": 3,
                "repos": [
                    {
                        "name": "x",
                        "full_name": "o/x",
                        "html_url": "https://github.com/o/x",
                        "description": "test repo",
                        "AgenticIndexScore": 1.0,
                        "stars": 10,
                        "stars_delta": 1,
                        "score_delta": 0,
                        "recency_factor": 1.0,
                        "issue_health": 0.5,
                        "doc_completeness": 0.5,
                        "license_freedom": 0.9,
                        "ecosystem_integration": 0.3,
                        "stars_log2": 3.32,
                        "category": "General",
                        "stars_7d": 1,
                        "maintenance": 0.5,
                        "docs_quality": 0.5,
                        "ecosystem_fit": 0.3,
                        "release_age": 1,
                        "license_score": 1.0,
                    }
                ],
            }
        )
    )
    (data_dir / "top100.md").write_text(
        "| Rank | Repo | Description | Score | Stars | Δ Stars |\n"
        "|-----:|------|-------------|------:|------:|--------:|\n"
        "| 1 | [x](https://github.com/o/x) | test repo | 1.00 | 10 | +1 |\n"
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
    assert "| 1 | [x](https://github.com/o/x) | test repo | 1.00 | 10 | +1 |" in text

    assert inj.main(check=True, top_n=50) == 0


def test_check_fails_when_outdated(tmp_path, monkeypatch):
    readme = _setup(tmp_path)
    # write incorrect content
    readme.write_text("start\n<!-- TOP50:START -->\nfoo\n<!-- TOP50:END -->\nend\n")
    assert inj.main(check=True, top_n=50) == 1


@pytest.mark.parametrize(
    "field",
    ["name", "full_name", "AgenticIndexScore", "stars"],
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
