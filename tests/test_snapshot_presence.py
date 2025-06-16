import json
import shutil
from pathlib import Path

import agentic_index_cli.internal.inject_readme as inj

ROOT = Path(__file__).resolve().parents[1]


def test_injector_handles_missing_snapshot(tmp_path, capsys, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    shutil.copy(ROOT / "data" / "top100.md", data_dir / "top100.md")
    data = json.loads((ROOT / "data" / "repos.json").read_text())
    for repo in data.get("repos", []):
        repo.setdefault("stars_7d", 0)
    (data_dir / "repos.json").write_text(json.dumps(data))
    # intentionally do not provide last_snapshot.json

    readme = tmp_path / "README.md"
    readme.write_text((ROOT / "README.md").read_text())

    monkeypatch.setattr(inj, "README_PATH", readme)
    monkeypatch.setattr(inj, "DATA_PATH", data_dir / "top100.md")
    monkeypatch.setattr(inj, "REPOS_PATH", data_dir / "repos.json")
    monkeypatch.setattr(inj, "SNAPSHOT", data_dir / "last_snapshot.json")

    ret = inj.main(check=True, top_n=50)
    captured = capsys.readouterr()
    assert ret == 0
    assert "missing snapshot" in captured.err
