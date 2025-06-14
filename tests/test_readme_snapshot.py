from pathlib import Path
from _utils import assert_readme_diff

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / "tests" / "snapshots" / "README.md"


def test_readme_snapshot():
    current = (ROOT / "README.md").read_text()
    expected = SNAP.read_text()
    assert_readme_diff(expected, current)
