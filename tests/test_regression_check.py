import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scripts.regression_check as rc


def test_regression_allows_external_agentops(tmp_path):
    bad = "agentops" + "_cli"
    cfg = tmp_path / '.regression.yml'
    cfg.write_text(f'forbidden:\n  - {bad}\nallowed_regex:\n  - https://github\\.com/.*/agentops\\b\n')
    f = tmp_path / 'sample.txt'
    f.write_text('check https://github.com/foo/agentops for more')

    failures = rc.check_files([f], rc.load_config(cfg))
    assert not failures


def test_regression_blocks_internal(tmp_path):
    bad = "agentops" + "_cli"
    cfg = tmp_path / '.regression.yml'
    cfg.write_text(f'forbidden:\n  - {bad}\nallowed_regex: []\n')
    f = tmp_path / 'mod.py'
    f.write_text(f'import {bad}')

    failures = rc.check_files([f], rc.load_config(cfg))
    assert failures
