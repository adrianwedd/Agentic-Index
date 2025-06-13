from pathlib import Path

import agentic_index_cli.internal.inject_readme as inj


def test_inject_readme(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    table = "| h |\n|--|\n|1|x|\n"
    (data_dir / "top50.md").write_text(table)

    readme.write_text(
        "start\n<!-- TOP50:START -->\nold\n<!-- TOP50:END -->\nend\n"
    )

    monkeypatch.setattr(inj, "README_PATH", readme)
    monkeypatch.setattr(inj, "DATA_PATH", data_dir / "top50.md")

    assert inj.main() == 0
    content = readme.read_text()
    assert table.strip() in content
    assert content.count("<!-- TOP50:START -->") == 1
