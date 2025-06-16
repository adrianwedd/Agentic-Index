import json
import os
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.network

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "update_security_badge.py"


def _write_json(tmp_path: Path, issues: int) -> Path:
    data = {"results": ["x"] * issues}
    p = tmp_path / "bandit.json"
    p.write_text(json.dumps(data))
    return p


def test_update_badge(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(
        "![security](https://img.shields.io/badge/security-0%20issues-brightgreen)"
    )
    report = _write_json(tmp_path, 3)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    subprocess.run(
        ["python", str(SCRIPT), str(report), str(readme)],
        check=True,
        cwd=str(ROOT),
        env=env,
    )
    text = readme.read_text()
    assert "security-3%20issues-" in text


def test_update_badge_add_exclamation(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(
        "[security](https://img.shields.io/badge/security-5%20issues-red)"
    )
    report = _write_json(tmp_path, 1)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    subprocess.run(
        ["python", str(SCRIPT), str(report), str(readme)],
        check=True,
        cwd=str(ROOT),
        env=env,
    )
    text = readme.read_text()
    assert text.startswith("![security]")
    assert "security-1%20issues-" in text
