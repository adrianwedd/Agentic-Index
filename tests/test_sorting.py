import json
from pathlib import Path
import agentic_index_cli.internal.inject_readme as inj
import pytest


def _setup(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    repos = [
        {
            "name": "A",
            "full_name": "o/A",
            "AgenticIndexScore": 1.0,
            "stars_30d": 10,
            "maintenance": 0.5,
            "docs_score": 0.0,
            "ecosystem": 0.0,
            "last_release": "2025-06-01T00:00:00Z",
            "license": "MIT",
        },
        {
            "name": "B",
            "full_name": "o/B",
            "AgenticIndexScore": 2.0,
            "stars_30d": 5,
            "maintenance": 0.9,
            "docs_score": 0.0,
            "ecosystem": 0.0,
            "last_release": "2025-05-01T00:00:00Z",
            "license": "MIT",
        },
    ]
    (data_dir / "repos.json").write_text(json.dumps({"schema_version": 2, "repos": repos}))
    (data_dir / "top50.md").write_text("")
    (data_dir / "last_snapshot.json").write_text("[]")
    readme = tmp_path / "README.md"
    readme.write_text("x\n<!-- TOP50:START -->\nold\n<!-- TOP50:END -->\n")

    for name, val in {
        "README_PATH": readme,
        "DATA_PATH": data_dir / "top50.md",
        "REPOS_PATH": data_dir / "repos.json",
        "SNAPSHOT": data_dir / "last_snapshot.json",
    }.items():
        setattr(inj, name, val)
    return readme


@pytest.mark.parametrize(
    "field,first",
    [
        ("score", "B"),
        ("stars_30d", "A"),
        ("maintenance", "B"),
        ("last_release", "A"),
    ],
)
def test_sort_order(tmp_path, field, first):
    _setup(tmp_path)
    text = inj.build_readme(sort_by=field)
    lines = [l for l in text.splitlines() if l.startswith("|")][2:]
    assert lines[0].split("|")[3].strip() == first


def test_stable_between_runs(tmp_path):
    _setup(tmp_path)
    first = inj.build_readme(sort_by="stars_30d")
    second = inj.build_readme(sort_by="stars_30d")
    assert first == second
