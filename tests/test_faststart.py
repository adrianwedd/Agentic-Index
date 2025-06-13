import json
import subprocess
from pathlib import Path


def test_faststart(tmp_path):
    data = [
        {
            "full_name": "user1/repo1",
            "stars": 6000,
            "doc_completeness": 1,
            "AgentOpsScore": 90,
            "last_commit": "2024-01-01",
            "category": "A",
            "one_liner": "desc",
        },
        {
            "full_name": "user2/repo2",
            "stars": 8000,
            "doc_completeness": 1,
            "AgentOpsScore": 80,
            "last_commit": "2024-01-02",
            "category": "B",
            "one_liner": "desc",
        },
        {
            "full_name": "user3/repo3",
            "stars": 3000,
            "doc_completeness": 1,
            "AgentOpsScore": 85,
            "last_commit": "2024-01-03",
            "category": "C",
            "one_liner": "desc",
        },
    ]

    data_file = tmp_path / "repos.json"
    with data_file.open("w") as f:
        json.dump(data, f)

    script = Path(__file__).resolve().parents[1] / "scripts" / "faststart.py"

    subprocess.run(["python", str(script), "--top", "2", str(data_file)], check=True, cwd=tmp_path)

    output = tmp_path / "FAST_START.md"
    lines = [l for l in output.read_text().splitlines() if l.startswith("| ") and l[2].isdigit()]
    assert len(lines) == 2

    for line in lines:
        parts = [p.strip() for p in line.strip('|').split('|')]
        stars = parts[2]
        if stars.endswith('k'):
            value = float(stars[:-1]) * 1000
        else:
            value = float(stars)
        assert value >= 5000
