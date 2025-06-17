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
            "stars": 0,
            "stars_delta": 0,
            "score_delta": 0,
            "recency_factor": 0.0,
            "issue_health": 0.1,
            "doc_completeness": 0.0,
            "license_freedom": 0.0,
            "ecosystem_integration": 0.0,
            "stars_log2": 0.0,
            "category": "Test",
        },
        {
            "name": "b",
            "full_name": "o/b",
            "AgenticIndexScore": 2.0,
            "stars": 0,
            "stars_delta": 0,
            "score_delta": 0,
            "recency_factor": 0.5,
            "issue_health": 0.6,
            "doc_completeness": 0.0,
            "license_freedom": 0.0,
            "ecosystem_integration": 0.2,
            "stars_log2": 0.0,
            "category": "Test",
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
    return readme


def test_no_all_zero_rows(tmp_path):
    _setup(tmp_path)
    _, repos = inj._load_rows(return_repos=True)
    for repo in repos:
        metrics = (
            repo.get("recency_factor", 0),
            repo.get("issue_health", 0),
            repo.get("doc_completeness", 0),
            repo.get("license_freedom", 0),
            repo.get("ecosystem_integration", 0),
        )
        if all(float(m) == 0 for m in metrics):
            raise AssertionError("row shows all zero metrics")
