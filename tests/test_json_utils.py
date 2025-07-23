import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest

from agentic_index_cli.internal import json_utils


def test_load_basic(tmp_path):
    p = tmp_path / "data.json"
    p.write_text(json.dumps({"a": 1}))
    data = json_utils.load_json(p)
    assert data == {"a": 1}


def test_load_cache(tmp_path):
    p = tmp_path / "cache.json"
    json_utils._cache.clear()
    p.write_text(json.dumps({"x": 2}))
    first = json_utils.load_json(p, cache=True)
    p.write_text(json.dumps({"x": 3}))  # change file
    json_utils._cache.clear() # Clear cache to force reload
    second = json_utils.load_json(p, cache=True)
    assert first == {"x": 2}
    assert second == {"x": 3}


def test_load_stream(monkeypatch, tmp_path):
    p = tmp_path / "stream.json"
    p.write_text(json.dumps([1, 2, 3]))
    fake_ijson = SimpleNamespace(load=lambda fh: [1, 2, 3])
    monkeypatch.setitem(sys.modules, "ijson", fake_ijson)
    data = json_utils.load_json(p, stream=True)
    assert data == [1, 2, 3]


def test_stream_fallback(monkeypatch, tmp_path):
    p = tmp_path / "data.json"
    p.write_text(json.dumps([4]))
    monkeypatch.setitem(sys.modules, "ijson", None)
    data = json_utils.load_json(p, stream=True)
    assert data == [4]


def test_invalid_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{")
    with pytest.raises(Exception):
        json_utils.load_json(p)
