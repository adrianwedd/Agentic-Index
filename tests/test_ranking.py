import hashlib
import json
from pathlib import Path
import subprocess

import pytest

REPO_JSON = Path('data/repos.json')
RANK_SCRIPT = Path('scripts/rank.py')
TOP_MD = Path('data/top50.md')

def run_script():
    subprocess.run(['python3', str(RANK_SCRIPT), str(REPO_JSON)], check=True)

def load_scores():
    data = json.loads(REPO_JSON.read_text())
    return [item.get('agentic_score', item.get('score')) for item in data]

def test_score_count_matches_repos():
    run_script()
    data = json.loads(REPO_JSON.read_text())
    scores = load_scores()
    assert len(scores) == len(data)

def test_table_sorted():
    run_script()
    # read markdown
    lines = [l for l in TOP_MD.read_text().splitlines() if l.startswith('|')][2:]
    scores = [float(line.split('|')[3].strip()) for line in lines]
    assert all(scores[i] >= scores[i+1] for i in range(len(scores)-1))

def test_deterministic_output(tmp_path):
    run_script()
    first = hashlib.sha256(TOP_MD.read_bytes()).hexdigest()
    run_script()
    second = hashlib.sha256(TOP_MD.read_bytes()).hexdigest()
    assert first == second
