from pathlib import Path

import agentic_index_cli.internal.inject_readme as inj


def test_inject_readme(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    table = (
        "| Rank | Repo | Description | Score | Stars | Δ Stars |\n"
        "|-----:|------|-------------|------:|------:|--------:|\n"
        "| 1 | [x](https://github.com/o/x) | test repo | 1.00 | 10 | +1 |\n"
    )
    (data_dir / "top100.md").write_text(table)
    (data_dir / "repos.json").write_text(
        '{"schema_version":3,"repos":[{"name":"x","full_name":"o/x","html_url":"https://github.com/o/x","description":"test repo","AgenticIndexScore":1.0,"stars":10,"stars_delta":1,"score_delta":0,"recency_factor":1.0,"issue_health":0.5,"doc_completeness":0.5,"license_freedom":0.9,"ecosystem_integration":0.3,"stars_log2":3.32,"category":"Test"}]}'
    )
    (data_dir / "last_snapshot.json").write_text("[]")
    by_cat = data_dir / "by_category"
    by_cat.mkdir()
    (by_cat / "index.json").write_text("{}")

    monkeypatch.setattr(inj, "REPOS_PATH", data_dir / "repos.json")
    monkeypatch.setattr(inj, "SNAPSHOT", data_dir / "last_snapshot.json")

    readme.write_text("start\n<!-- TOP50:START -->\nold\n<!-- TOP50:END -->\nend\n")

    monkeypatch.setattr(inj, "README_PATH", readme)
    monkeypatch.setattr(inj, "DATA_PATH", data_dir / "top100.md")
    monkeypatch.setattr(inj, "BY_CAT_INDEX", by_cat / "index.json")

    assert inj.main(top_n=50) == 0
    content = readme.read_text()
    assert "| 1 | [x](https://github.com/o/x) | test repo | 1.00 | 10 | +1 |" in content
    assert content.count("<!-- TOP50:START -->") == 1
