import shutil
from pathlib import Path

import agentic_index_cli.internal.inject_readme as inj

ROOT = Path(__file__).resolve().parents[1]


def test_inject_readme_check(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    shutil.copy(ROOT / "data" / "top50.md", data_dir / "top50.md")
    shutil.copy(ROOT / "data" / "repos.json", data_dir / "repos.json")
    shutil.copy(ROOT / "data" / "last_snapshot.json", data_dir / "last_snapshot.json")

    readme = tmp_path / "README.md"
    readme.write_text((ROOT / "README.md").read_text())

    monkeypatch.setattr(inj, "README_PATH", readme)
    monkeypatch.setattr(inj, "DATA_PATH", data_dir / "top50.md")
    monkeypatch.setattr(inj, "REPOS_PATH", data_dir / "repos.json")
    monkeypatch.setattr(inj, "SNAPSHOT", data_dir / "last_snapshot.json")

    modified = inj.build_readme().strip()
    assert modified == readme.read_text().strip()

    assert inj.main(check=True) == 0
