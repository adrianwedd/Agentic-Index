import subprocess
from pathlib import Path

from _utils import parse_delta

ROOT = Path(__file__).resolve().parents[1]
INJECT = ROOT / "scripts" / "inject_readme.py"


def test_readme_synced():
    subprocess.run(["python", str(INJECT), "--check"], check=True)

    text = (ROOT / "README.md").read_text()
    start = text.index("<!-- TOP50:START -->")
    end = text.index("<!-- TOP50:END -->", start)
    lines = [l for l in text[start:end].splitlines() if l.startswith("|")]
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 6:
            sd = parse_delta(cells[3])
            qd = parse_delta(cells[4])
            assert sd == "new" or isinstance(sd, (int, float))
            assert qd == "new" or isinstance(qd, (int, float))


def test_inject_idempotent(tmp_path):
    subprocess.run(["python", str(INJECT)], check=True)
    first = (ROOT / "README.md").read_text()
    subprocess.run(["python", str(INJECT)], check=True)
    assert (ROOT / "README.md").read_text() == first
