import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import agentic_index_cli.internal.inject_readme as inj


def _setup(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    repos = [
        {
            "name": "a",
            "full_name": "o/a",
            "AgenticIndexScore": 1.0,
            "stars_7d": 0,
            "license": "MIT",
        },
        {
            "name": "b",
            "full_name": "o/b",
            "AgenticIndexScore": 2.0,
            "stars_7d": 0,
            "maintenance": 0.5,
            "docs_score": 0.5,
            "ecosystem": 0.2,
            "license": "MIT",
        },
    ]
    (data_dir / "repos.json").write_text(
        json.dumps({"schema_version": 2, "repos": repos})
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
    return readme


def test_no_all_zero_rows(tmp_path):
    _setup(tmp_path)
    text = inj.build_readme()
    lines = [l for l in text.splitlines() if l.startswith("|")][2:]
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        maint, docs, eco = parts[5], parts[7], parts[8]
        if maint == docs == eco == "0.00":
            raise AssertionError("row shows all zero metrics")
