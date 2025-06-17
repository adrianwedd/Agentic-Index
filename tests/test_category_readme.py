import json
from pathlib import Path

import agentic_index_cli.internal.inject_readme as inj


def _setup(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    repos = [
        {
            "name": "a",
            "full_name": "o/a",
            "html_url": "https://github.com/o/a",
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
            "category": "CatA",
            "topics": ["ai-agent", "autonomous"],
        },
        {
            "name": "b",
            "full_name": "o/b",
            "html_url": "https://github.com/o/b",
            "AgenticIndexScore": 2.0,
            "stars": 5,
            "stars_delta": 0,
            "score_delta": 0,
            "recency_factor": 1.0,
            "issue_health": 0.5,
            "doc_completeness": 0.5,
            "license_freedom": 0.9,
            "ecosystem_integration": 0.3,
            "stars_log2": 2.32,
            "category": "CatB",
            "topics": ["llm"],
        },
    ]
    (data_dir / "repos.json").write_text(
        json.dumps({"schema_version": 3, "repos": repos})
    )
    (data_dir / "top100.md").write_text("")
    (data_dir / "last_snapshot.json").write_text("[]")
    for name, val in {
        "ROOT": tmp_path,
        "README_PATH": tmp_path / "README.md",
        "DATA_PATH": data_dir / "top100.md",
        "REPOS_PATH": data_dir / "repos.json",
        "SNAPSHOT": data_dir / "last_snapshot.json",
    }.items():
        setattr(inj, name, val)
    return tmp_path


def test_write_category_readme(tmp_path):
    _setup(tmp_path)
    ret = inj.write_category_readme("CatA", force=True)
    assert ret == 0
    text = (tmp_path / "README_CatA.md").read_text()
    assert "Top Agentic-AI Repositories: CatA" in text
    assert "`ai-agent`" in text
    assert "| 1 | [a](https://github.com/o/a) |" in text


def test_write_all_categories(tmp_path):
    _setup(tmp_path)
    ret = inj.write_all_categories(force=True)
    assert ret == 0
    assert (tmp_path / "README_CatA.md").exists()
    assert (tmp_path / "README_CatB.md").exists()
