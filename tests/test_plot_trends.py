import importlib.util
from datetime import datetime
from pathlib import Path

spec = importlib.util.spec_from_file_location("pt", Path("scripts/plot_trends.py"))
pt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pt)


def test_load_snapshots(tmp_path):
    hist = tmp_path
    good = hist / "2025-01-01.json"
    good.write_text('[{"name":"a"}]')
    bad_name = hist / "not-a-date.json"
    bad_name.write_text("[]")
    bad_json = hist / "2025-01-02.json"
    bad_json.write_text("invalid")

    dates, snaps = pt.load_snapshots(hist)
    assert dates == [datetime(2025, 1, 1), datetime(2025, 1, 2)]
    assert snaps[0] == [{"name": "a"}]
    assert snaps[1] == []


def test_build_timeseries():
    dates = [datetime(2025, 1, 1), datetime(2025, 1, 2)]
    snapshots = [
        [{"name": "a", "AgentOpsScore": 1}, {"name": "b", "AgentOpsScore": 2}],
        [{"name": "a", "AgentOpsScore": 2}, {"name": "b", "AgentOpsScore": 3}],
    ]
    series, repos = pt.build_timeseries(dates, snapshots)
    assert repos == ["b", "a"]
    assert series["a"] == [1, 2]
    assert series["b"] == [2, 3]


def test_plot_creates_file(tmp_path):
    import pytest

    pytest.importorskip("matplotlib")
    series = {"a": [1, 2]}
    dates = [datetime(2025, 1, 1), datetime(2025, 1, 2)]
    out = tmp_path / "out.png"
    pt.plot(series, dates, out)
    assert out.exists()


def test_cli_placeholder(capsys):
    from agentic_index_cli import plot_trends as cli

    cli.main()
    captured = capsys.readouterr()
    assert "not yet implemented" in captured.out
