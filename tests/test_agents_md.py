import re
from pathlib import Path


def test_agents_table_and_paths():
    md = Path("agents.md").read_text(encoding="utf-8").splitlines()
    header = "| Agent Name | Trigger | Code Location | Main Function | Outputs |"
    assert header in md
    start = md.index(header)
    assert md[start + 1].startswith("|---")
    rows = []
    for line in md[start + 2 :]:
        if not line.startswith("|"):
            break
        rows.append(line)
    assert len(rows) >= 6
    cols = [c.strip() for c in header.split("|")[1:-1]]
    for row in rows:
        values = [c.strip() for c in row.split("|")[1:-1]]
        assert len(values) == len(cols)
        path_str = values[2].strip("`")
        assert Path(path_str).exists(), f"Missing {path_str}"
