import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cli_help(tmp_path):
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", str(ROOT)], check=True
    )
    result = subprocess.run(["agentic-index", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "--min-stars" in result.stdout
    assert "--iterations" in result.stdout


def test_python_m_entrypoint():
    result = subprocess.run(
        [sys.executable, "-m", "agentic_index_cli", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "scrape" in result.stdout
