from pathlib import Path

from agentic_index_cli.helpers.once_per_day import once_per_day


def test_once_per_day(tmp_path):
    state = tmp_path / "state"
    assert once_per_day("foo", state_dir=state)
    assert not once_per_day("foo", state_dir=state)
    assert Path(state / "foo.date").exists()
