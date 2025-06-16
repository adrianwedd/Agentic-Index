import agentic_index_cli.inject_readme as ir


def test_cli_forwards_force(monkeypatch):
    called = {}

    def fake_main(force=False, top_n=100):
        called["force"] = force
        called["top_n"] = top_n

    monkeypatch.setattr(ir, "main", fake_main)
    ir.cli(["--force"])
    assert called["force"] is True
    assert called["top_n"] == 100
