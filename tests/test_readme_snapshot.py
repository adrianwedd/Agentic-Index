import re
from pathlib import Path

from _utils import assert_readme_diff

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / "tests" / "snapshots" / "README.md"


def test_readme_snapshot():
    current = (ROOT / "README.md").read_text()
    expected = SNAP.read_text()
    assert_readme_diff(expected, current)


def test_badge_block_formatting():
    markdown = (ROOT / "README.md").read_text()
    pattern = r"!\[[^\]]+\]\([^)]+\)"
    matches = list(re.finditer(pattern, markdown))

    assert matches, "no badges found"

    for m in re.finditer(r"!\[", markdown):
        if not re.match(pattern, markdown[m.start() :]):
            raise AssertionError(f"malformed badge near index {m.start()}")

    seen = set()
    for m in matches:
        alt, url = re.match(r"!\[([^]]+)\]\(([^)]+)\)", m.group()).groups()

        key = (alt.strip(), url.strip())
        assert key not in seen, f"duplicate badge {alt}"
        seen.add(key)

    for line in markdown.splitlines():

        line_matches = re.findall(pattern, line)
        if len(line_matches) > 1:
            assert line.strip() == " ".join(
                line_matches
            ), f"badge spacing error: {line}"
