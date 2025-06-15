import agentic_index_cli.inject_readme as ir


def test_cli_forwards_force(monkeypatch):
    called = {}

    def fake_main(force=False):
        called["force"] = force

    monkeypatch.setattr(ir, "main", fake_main)
    ir.cli(["--force"])
    assert called["force"] is True
