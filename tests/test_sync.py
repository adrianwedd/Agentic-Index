import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INJECT = ROOT / "scripts" / "inject_readme.py"


def test_readme_synced():
    subprocess.run(["python", str(INJECT), "--check"], check=True)


def test_inject_idempotent(tmp_path):
    orig = (ROOT / "README.md").read_text()
    subprocess.run(["python", str(INJECT)], check=True)
    subprocess.run(["python", str(INJECT)], check=True)
    assert (ROOT / "README.md").read_text() == orig
