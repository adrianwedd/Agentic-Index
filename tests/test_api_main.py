import runpy


def test_module_entry(monkeypatch):
    called = {}

    def fake_run(app_ref, host="0.0.0.0", port=8000):
        called["args"] = app_ref
        called["host"] = host
        called["port"] = port

    monkeypatch.setattr("uvicorn.run", fake_run)

    runpy.run_module("agentic_index_api", run_name="__main__")

    assert called["args"] == "agentic_index_api.server:app"
    assert called["host"] == "0.0.0.0"
    assert called["port"] == 8000
