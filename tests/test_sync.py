import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_synced():
    subprocess.run([str(ROOT / 'scripts' / 'inject_readme.py')], check=True)
    subprocess.run(['git', 'diff', '--exit-code'], cwd=ROOT, check=True)
