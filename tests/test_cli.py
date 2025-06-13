import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_cli_help(tmp_path):
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', str(ROOT)], check=True)
    result = subprocess.run(['agentops', '--help'], capture_output=True, text=True)
    assert result.returncode == 0
    assert 'scrape' in result.stdout
    assert 'faststart' in result.stdout
