import json
from pathlib import Path

import pytest

import agentic_index_cli.internal.inject_readme as inj


def _setup(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    repos = [
        {
            "name": "A",
            "full_name": "o/A",
            "AgenticIndexScore": 1.0,
            "stars": 10,
            "stars_delta": 5,
            "score_delta": 0.1,
            "recency_factor": 0.5,
            "issue_health": 0.8,
            "doc_completeness": 0.0,
            "license_freedom": 1.0,
            "ecosystem_integration": 0.0,
            "stars_log2": 3.32,
            "category": "A",
        },
        {
            "name": "B",
            "full_name": "o/B",
            "AgenticIndexScore": 2.0,
            "stars": 5,
            "stars_delta": 1,
            "score_delta": 0.2,
            "recency_factor": 0.9,
            "issue_health": 0.7,
            "doc_completeness": 0.0,
            "license_freedom": 1.0,
            "ecosystem_integration": 0.0,
            "stars_log2": 2.32,
            "category": "B",
        },
    ]
    (data_dir / "repos.json").write_text(
        json.dumps({"schema_version": 3, "repos": repos})
    )
    (data_dir / "top100.md").write_text("")
    (data_dir / "last_snapshot.json").write_text("[]")
    readme = tmp_path / "README.md"
    readme.write_text("x\n<!-- TOP50:START -->\nold\n<!-- TOP50:END -->\n")

    for name, val in {
        "README_PATH": readme,
        "DATA_PATH": data_dir / "top100.md",
        "REPOS_PATH": data_dir / "repos.json",
        "SNAPSHOT": data_dir / "last_snapshot.json",
    }.items():
        setattr(inj, name, val)
    inj.DATA_PATH = Path("nonexistent")
    return readme


@pytest.mark.parametrize(
    "field,first",
    [
        ("score", "B"),
        ("stars", "A"),
        ("recency", "B"),
    ],
)
def test_sort_order(tmp_path, field, first):
    _setup(tmp_path)
    text = inj.build_readme(sort_by=field, top_n=50)
    lines = [l for l in text.splitlines() if l.startswith("|")][2:]
    assert lines[0].split("|")[2].strip() == first


def test_stable_between_runs(tmp_path):
    _setup(tmp_path)
    first = inj.build_readme(sort_by="stars", top_n=50)
    second = inj.build_readme(sort_by="stars", top_n=50)
    assert first == second
