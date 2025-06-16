import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INJECT = ROOT / "scripts" / "inject_readme.py"


def test_readme_synced():
    subprocess.run(["python", str(INJECT), "--check", "--top-n", "50"], check=True)

    text = (ROOT / "README.md").read_text()
    start = text.index("<!-- TOP50:START -->")
    end = text.index("<!-- TOP50:END -->", start)
    lines = [l for l in text[start:end].splitlines() if l.startswith("|")]
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        assert len(cells) >= 13
        int(cells[0])
        float(cells[2])
        int(cells[3])
        if cells[4] and cells[4] != "+new":
            int(cells[4].replace("+", ""))
        if cells[5] and cells[5] != "+new":
            float(cells[5].replace("+", ""))
        if cells[6] != "-":
            float(cells[6])


def test_inject_idempotent(tmp_path):
    subprocess.run(["python", str(INJECT), "--top-n", "50"], check=True)
    first = (ROOT / "README.md").read_text()
    subprocess.run(["python", str(INJECT), "--top-n", "50"], check=True)
    assert (ROOT / "README.md").read_text() == first
