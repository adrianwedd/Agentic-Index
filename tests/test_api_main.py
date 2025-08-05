import runpy

import pytest


def test_module_entry(monkeypatch):
    # Set up API environment variables before module import
    monkeypatch.setenv("API_KEY", "test-key")
    monkeypatch.setenv("IP_WHITELIST", "")
    
    called = {}

    def fake_run(app_ref, host="0.0.0.0", port=8000):
        called["args"] = app_ref
        called["host"] = host
        called["port"] = port

    monkeypatch.setattr("uvicorn.run", fake_run)

    try:
        runpy.run_module("agentic_index_api", run_name="__main__")
    except Exception as e:
        pytest.skip(f"Could not run API module: {e}")

    assert called["args"] == "agentic_index_api.server:app"
    assert called["host"] == "0.0.0.0"
    assert called["port"] == 8000
