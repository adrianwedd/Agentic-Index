import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INJECT = str(ROOT / "scripts" / "inject_readme.py")


def test_readme_synced():
    subprocess.run([INJECT], check=True)
    subprocess.run(["git", "diff", "--exit-code", "--", "README.md"], check=True)


def test_inject_idempotent(tmp_path):
    orig = (ROOT / "README.md").read_text()
    subprocess.run([INJECT], check=True)
    subprocess.run([INJECT], check=True)
    assert (ROOT / "README.md").read_text() == orig
