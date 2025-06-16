import json
from pathlib import Path

import agentic_index_cli.internal.inject_readme as inj


def _prepare(tmp_path: Path, top_n: int, repo_count: int) -> Path:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    repos = []
    for i in range(repo_count):
        repos.append(
            {
                "name": f"r{i}",
                "full_name": f"o/r{i}",
                "AgenticIndexScore": 1.0 + i,
                "stars_7d": i,
                "maintenance": 0.5,
                "docs_score": 0.5,
                "ecosystem": 0.3,
                "last_release": None,
                "license": "MIT",
                "score_delta": 0,
            }
        )
    (data_dir / "repos.json").write_text(
        json.dumps({"schema_version": 2, "repos": repos})
    )
    (data_dir / "last_snapshot.json").write_text("[]")
    readme = tmp_path / "README.md"
    readme.write_text(f"start\n<!-- TOP{top_n}:START -->\n<!-- TOP{top_n}:END -->\n")
    for name, val in {
        "README_PATH": readme,
        "REPOS_PATH": data_dir / "repos.json",
        "SNAPSHOT": data_dir / "last_snapshot.json",
    }.items():
        setattr(inj, name, val)
    return readme


def test_top_n_row_count(tmp_path):
    top_n = 3
    readme = _prepare(tmp_path, top_n, 5)
    assert inj.main(top_n=top_n) == 0
    lines = [l for l in readme.read_text().splitlines() if l.startswith("|")]
    # header + separator + rows
    assert len(lines) == 2 + top_n
