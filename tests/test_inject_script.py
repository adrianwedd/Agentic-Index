from pathlib import Path

import agentic_index_cli.internal.inject_readme as inj


def test_inject_readme(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    table = "| Rank | Repo | Score | Stars | Δ Stars | Δ Score | Recency | Issue Health | Doc Complete | License Freedom | Ecosystem | log₂(Stars) | Category |\n|-----:|------|------:|------:|--------:|--------:|-------:|-------------:|-------------:|---------------:|---------:|------------:|----------|\n| 1 | x | 1.00 | 10 | +1 |  | 1.00 | 0.50 | 0.50 | 0.90 | 0.30 | 3.32 | Test |\n"
    (data_dir / "top100.md").write_text(table)
    (data_dir / "repos.json").write_text(
        '{"schema_version":3,"repos":[{"name":"x","full_name":"o/x","AgenticIndexScore":1.0,"stars":10,"stars_delta":1,"score_delta":0,"recency_factor":1.0,"issue_health":0.5,"doc_completeness":0.5,"license_freedom":0.9,"ecosystem_integration":0.3,"stars_log2":3.32,"category":"Test"}]}'
    )

    monkeypatch.setattr(inj, "REPOS_PATH", data_dir / "repos.json")
    monkeypatch.setattr(inj, "SNAPSHOT", data_dir / "last_snapshot.json")

    readme.write_text("start\n<!-- TOP50:START -->\nold\n<!-- TOP50:END -->\nend\n")

    monkeypatch.setattr(inj, "README_PATH", readme)
    monkeypatch.setattr(inj, "DATA_PATH", data_dir / "top100.md")

    assert inj.main(top_n=50) == 0
    content = readme.read_text()
    assert "| 1 | x | 1.00 |" in content
    assert content.count("<!-- TOP50:START -->") == 1
