import agentic_index_cli.internal.regression_check as rc


def test_regression_allows_snapshot_mentions(tmp_path):
    cfg = tmp_path / '.regression.yml'
    cfg.write_text('forbidden:\n  - agentops\nallowed_regex: []\n')
    allow = tmp_path / 'regression_allowlist.yml'
    allow.write_text("allow:\n  - '^agentops$'\n  - '\"score\"\\s*:'\n")

    f = tmp_path / 'data' / 'snap.json'
    f.parent.mkdir()
    f.write_text('agentops')

    config = rc.load_config(cfg)
    config['allowlist'] = rc.load_allowlist(allow)
    failures = rc.check_files([f], config)
    assert not failures


def test_regression_blocks_internal(tmp_path):
    cfg = tmp_path / '.regression.yml'
    cfg.write_text('forbidden:\n  - agentops\nallowed_regex: []\n')
    allow = tmp_path / 'regression_allowlist.yml'
    allow.write_text("allow:\n  - '^agentops$'\n  - '\"score\"\\s*:'\n")

    f = tmp_path / 'mod.py'
    f.write_text('import agentops')

    config = rc.load_config(cfg)
    config['allowlist'] = rc.load_allowlist(allow)
    failures = rc.check_files([f], config)
    assert failures
