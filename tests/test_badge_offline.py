import os
from pathlib import Path
import subprocess


def test_badges_offline(monkeypatch, tmp_path):
    badges = Path('badges')
    orig_svgs = list(badges.glob('*.svg'))
    for f in orig_svgs:
        f.unlink()
    monkeypatch.setenv('CI_OFFLINE', '1')
    subprocess.run(['python', '-m', 'agentic_index_cli.enricher'], check=True)
    subprocess.run(['python', 'scripts/rank.py'], check=True)
    for name in ['last_sync.svg', 'top_repo.svg', 'repo_count.svg']:
        p = badges / name
        assert p.exists()
        assert '<svg' in p.read_text()
    subprocess.run(['git', 'checkout', '--', 'badges'], check=True)
