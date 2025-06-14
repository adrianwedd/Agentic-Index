import sys
import shutil
from pathlib import Path

import re
import pytest

# ensure project root is on the path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import agentic_index_cli.internal.inject_readme as inj
from helpers import assert_readme_equivalent



ROOT = Path(__file__).resolve().parents[1]


def _setup(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    shutil.copy(ROOT / "data" / "top50.md", data_dir / "top50.md")
    shutil.copy(ROOT / "data" / "repos.json", data_dir / "repos.json")
    try:
        shutil.copy(ROOT / "data" / "last_snapshot.json", data_dir / "last_snapshot.json")
    except FileNotFoundError:
        (data_dir / "last_snapshot.json").write_text("{}")

    readme = tmp_path / "README.md"
    readme.write_text((ROOT / "README.md").read_text())

    monkeypatch.setattr(inj, "README_PATH", readme)
    monkeypatch.setattr(inj, "DATA_PATH", data_dir / "top50.md")
    monkeypatch.setattr(inj, "REPOS_PATH", data_dir / "repos.json")
    monkeypatch.setattr(inj, "SNAPSHOT", data_dir / "last_snapshot.json")

    modified = inj.build_readme().strip()
    return readme, modified


def test_inject_readme_check(tmp_path, monkeypatch):
    readme, modified = _setup(tmp_path, monkeypatch)
    assert_readme_equivalent(readme.read_text().strip(), modified, {"score": 0.005})
    assert inj.main(check=True) == 0


def _bump_score(text: str, delta: float) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("| 1 |"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            cells[1] = f"{float(cells[1]) + delta:.2f}"
            lines[i] = "| " + " | ".join(cells) + " |"
            break
    return "\n".join(lines)


def _change_cell(text: str, col: int, value: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("| 1 |"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            cells[col] = value
            lines[i] = "| " + " | ".join(cells) + " |"
            break
    return "\n".join(lines)


@pytest.mark.parametrize(
    "modifier,should_pass",
    [
        (lambda txt: _bump_score(txt, 0.015), True),
        (lambda txt: _bump_score(txt, 0.05), False),
        (lambda txt: _change_cell(txt, 8, "MIT"), False),
        (lambda txt: _change_cell(txt, 0, "2"), False),
    ],
)
def test_readme_tolerances(tmp_path, monkeypatch, modifier, should_pass):
    readme, modified = _setup(tmp_path, monkeypatch)
    modified = modifier(modified)
    if should_pass:
        assert_readme_equivalent(readme.read_text().strip(), modified, {"score": 0.005})
    else:
        with pytest.raises(AssertionError):
            assert_readme_equivalent(readme.read_text().strip(), modified, {"score": 0.005})
