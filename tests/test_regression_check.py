from pathlib import Path

import agentic_index_cli.internal.regression_check as rc


def test_regression_allows_snapshot_mentions(tmp_path):
    cfg = tmp_path / ".regression.yml"
    cfg.write_text("forbidden:\n  - agentops\nallowed_regex: []\n")
    allow = tmp_path / "regression_allowlist.yml"
    allow.write_text("allow:\n  - '^agentops$'\n  - '\"score\"\\s*:'\n")

    f = tmp_path / "data" / "snap.json"
    f.parent.mkdir()
    f.write_text("agentops")

    config = rc.load_config(cfg)
    config["allowlist"] = rc.load_allowlist(allow)
    failures = rc.check_files([f], config)
    assert not failures


def test_regression_blocks_internal(tmp_path):
    cfg = tmp_path / ".regression.yml"
    cfg.write_text("forbidden:\n  - agentops\nallowed_regex: []\n")
    allow = tmp_path / "regression_allowlist.yml"
    allow.write_text("allow:\n  - '^agentops$'\n  - '\"score\"\\s*:'\n")

    f = tmp_path / "mod.py"
    f.write_text("import agentops")

    config = rc.load_config(cfg)
    config["allowlist"] = rc.load_allowlist(allow)
    failures = rc.check_files([f], config)
    assert failures


def test_gather_files(monkeypatch):
    outputs = {
        "g1": "a.py\nb.py\n",
        "g2": "b.py\nc.py\n",
    }

    def fake_check(cmd, text=True):
        return outputs[cmd[2]]

    monkeypatch.setattr(rc.subprocess, "check_output", fake_check)
    files = rc.gather_files(["g1", "g2"])
    assert files == [Path("a.py"), Path("b.py"), Path("c.py")]


def test_main_failure(monkeypatch, tmp_path):
    cfg = tmp_path / ".regression.yml"
    cfg.write_text("forbidden:\n  - bad\nallowed_regex: []\n")
    allow = tmp_path / "regression_allowlist.yml"
    allow.write_text("allow: []")
    f = tmp_path / "test.py"
    f.write_text("bad")

    monkeypatch.setattr(rc, "gather_files", lambda globs=None: [f])
    orig_load = rc.load_config
    monkeypatch.setattr(rc, "load_config", lambda path=cfg: orig_load(cfg))
    orig_allow = rc.load_allowlist
    monkeypatch.setattr(rc, "load_allowlist", lambda path=allow: orig_allow(allow))
    ret = rc.main(["--allowlist", str(allow)])
    assert ret == 1
