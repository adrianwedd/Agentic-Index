from pathlib import Path

import agentic_index_cli.internal.regression_check as rc


def test_allowlist_respected(tmp_path):
    cfg = tmp_path / ".regression.yml"
    cfg.write_text("forbidden:\n  - BadWord\nallowed_regex: []\n")
    allow = tmp_path / "regression_allowlist.yml"
    allow.write_text("allow:\n  - '^Allowed line$'\n")

    f1 = tmp_path / "README1.md"
    f1.write_text("This contains BadWord")
    f2 = tmp_path / "README2.md"
    f2.write_text("Allowed line")

    config = rc.load_config(cfg)
    config["allowlist"] = rc.load_allowlist(allow)
    fails = rc.check_files([f1, f2], config)
    assert str(f1) + ":1: BadWord" in fails
    assert all(str(f2) not in fail for fail in fails)
