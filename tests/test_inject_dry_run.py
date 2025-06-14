import shutil
from pathlib import Path

import agentic_index_cli.internal.inject_readme as inj
from _utils import parse_delta


def assert_diff_numeric_tolerant(old: str, new: str, *, delta: float = 0.01) -> None:
    """Assert tables ``old`` and ``new`` differ only within a numeric tolerance."""
    old_lines = [l for l in old.splitlines() if l.startswith("|")]
    new_lines = [l for l in new.splitlines() if l.startswith("|")]
    assert len(old_lines) == len(new_lines)
    for i, (ol, nl) in enumerate(zip(old_lines, new_lines)):
        if i < 2:
            assert ol.strip() == nl.strip()
            continue
        ocells = [c.strip() for c in ol.strip().strip("|").split("|")]
        ncells = [c.strip() for c in nl.strip().strip("|").split("|")]
        assert ocells[0] == ncells[0]  # rank
        assert ocells[1] == ncells[1]  # repo name
        if ocells[2] and ncells[2]:
            assert abs(float(ocells[2]) - float(ncells[2])) <= delta
        osd = parse_delta(ocells[3])
        nsd = parse_delta(ncells[3])
        if isinstance(osd, (int, float)) and isinstance(nsd, (int, float)):
            assert abs(osd - nsd) <= delta
        else:
            assert osd == nsd
        oqd = parse_delta(ocells[4])
        nqd = parse_delta(ncells[4])
        if isinstance(oqd, (int, float)) and isinstance(nqd, (int, float)):
            assert abs(oqd - nqd) <= delta
        else:
            assert oqd == nqd
        assert ocells[5] == ncells[5]

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
    assert_diff_numeric_tolerant(readme.read_text().strip(), modified)

    assert inj.main(check=True) == 0
