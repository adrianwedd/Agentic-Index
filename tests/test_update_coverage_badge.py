import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "update_coverage_badge.py"


def _write_xml(tmp_path: Path, rate: float) -> Path:
    p = tmp_path / "coverage.xml"
    p.write_text(f'<coverage line-rate="{rate}"></coverage>')
    return p


def test_update_badge(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(
        "![coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)"
    )
    xml = _write_xml(tmp_path, 0.86)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    subprocess.run(
        ["python", str(SCRIPT), str(xml), str(readme)],
        check=True,
        cwd=str(ROOT),
        env=env,
    )
    text = readme.read_text()
    assert "coverage-86%25-" in text


def test_update_badge_add_exclamation(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("[coverage](https://img.shields.io/badge/coverage-70%25-red)")
    xml = _write_xml(tmp_path, 0.95)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    subprocess.run(
        ["python", str(SCRIPT), str(xml), str(readme)],
        check=True,
        cwd=str(ROOT),
        env=env,
    )
    text = readme.read_text()
    assert text.startswith("![coverage]")
    assert "coverage-95%25-" in text
