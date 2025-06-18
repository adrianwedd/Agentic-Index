import subprocess
import sys
from pathlib import Path


def test_validate_repos_json():
    root = Path(__file__).resolve().parents[1]
    data_path = root / "data" / "repos.json"
    result = subprocess.run(
        [sys.executable, "-m", "agentic_index_cli.validate", str(data_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
