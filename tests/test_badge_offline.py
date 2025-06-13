import os
from pathlib import Path
import subprocess


def test_badges_offline(monkeypatch, tmp_path):
    badges = Path('badges')
    for f in badges.glob('*.svg'):
        f.unlink()
    monkeypatch.setenv('CI_OFFLINE', '1')
    subprocess.run(['python', 'scripts/rank.py'], check=True)
    for name in ['last_sync.svg', 'top_repo.svg']:
        p = badges / name
        assert p.exists()
        assert '<svg' in p.read_text()
