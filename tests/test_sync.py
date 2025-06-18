import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INJECT = ROOT / "scripts" / "inject_readme.py"


def test_readme_synced():
    by_cat = ROOT / "data" / "by_category"
    by_cat.mkdir(exist_ok=True)
    (by_cat / "index.json").write_text("{}")
    subprocess.run(["python", str(INJECT), "--check", "--top-n", "50"], check=True)

    text = (ROOT / "README.md").read_text()
    start = text.index("<!-- TOP50:START -->")
    end = text.index("<!-- TOP50:END -->", start)
    lines = [l for l in text[start:end].splitlines() if l.startswith("|")]
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        assert len(cells) == 6
        int(cells[0])
        float(cells[3])
        int(cells[4])
        if cells[5] and cells[5] != "+new":
            int(cells[5].replace("+", ""))


def test_inject_idempotent(tmp_path):
    by_cat = ROOT / "data" / "by_category"
    by_cat.mkdir(exist_ok=True)
    (by_cat / "index.json").write_text("{}")
    subprocess.run(["python", str(INJECT), "--top-n", "50"], check=True)
    first = (ROOT / "README.md").read_text()
    subprocess.run(["python", str(INJECT), "--top-n", "50"], check=True)
    assert (ROOT / "README.md").read_text() == first
