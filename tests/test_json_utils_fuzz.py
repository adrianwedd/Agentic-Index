import json
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from agentic_index_cli.internal import json_utils
from agentic_index_cli.validate import load_repos

json_scalars = (
    st.none() | st.booleans() | st.integers() | st.floats(allow_nan=False) | st.text()
)
json_values = st.recursive(
    json_scalars,
    lambda children: st.lists(children) | st.dictionaries(st.text(), children),
    max_leaves=10,
)


@settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(data=json_values)
def test_load_json_roundtrip(data: object) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir) / "data.json"
        p.write_text(json.dumps(data))
        assert json_utils.load_json(p) == data


@settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(data=json_values)
def test_load_json_stream_roundtrip(data: object) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir) / "stream.json"
        p.write_text(json.dumps(data))
        fake_ijson = SimpleNamespace(load=lambda fh: json.load(fh))
        original = sys.modules.get("ijson")
        sys.modules["ijson"] = fake_ijson
        try:
            assert json_utils.load_json(p, stream=True) == data
        finally:
            if original is None:
                del sys.modules["ijson"]
            else:
                sys.modules["ijson"] = original


def _is_valid_json(text: str) -> bool:
    try:
        json.loads(text)
        return True
    except Exception:
        return False


invalid_strings = st.text(min_size=1).filter(lambda s: not _is_valid_json(s))


@settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(text=invalid_strings)
def test_load_json_invalid(text: str) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir) / "bad.json"
        p.write_text(text)
        with pytest.raises(Exception):
            json_utils.load_json(p)


simple_repo = st.builds(lambda name: {"name": name}, name=st.text(min_size=1))
repo_list = st.lists(simple_repo, unique_by=lambda r: r["name"], min_size=1, max_size=5)


@settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(repos=repo_list)
def test_load_repos_roundtrip(repos: list[dict]) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "repos.json"
        payload = {"schema_version": 1, "repos": repos}
        path.write_text(json.dumps(payload))
        assert load_repos(path) == repos


invalid_structs = st.one_of(
    st.integers(),
    st.floats(allow_nan=False),
    st.text(),
    st.booleans(),
    st.none(),
    st.dictionaries(st.text(), st.text()).filter(lambda d: "repos" not in d),
    st.builds(
        lambda version: {"schema_version": version, "repos": []},
        st.integers().filter(lambda v: v not in (1, 2, 3)),
    ),
    st.builds(
        lambda r: {"schema_version": 1, "repos": r},
        st.one_of(st.integers(), st.text(), st.none(), st.booleans()),
    ),
)


@settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(raw=invalid_structs)
def test_load_repos_invalid(raw: object) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "bad.json"
        path.write_text(json.dumps(raw))
        with pytest.raises(Exception):
            load_repos(path)


@settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(names=st.lists(st.text(min_size=1), min_size=1, max_size=4))
def test_load_repos_duplicates(names: list[str]) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        repos = [{"name": n} for n in names + [names[0]]]
        path = Path(tmpdir) / "dup.json"
        payload = {"schema_version": 1, "repos": repos}
        path.write_text(json.dumps(payload))
        with pytest.raises(Exception):
            load_repos(path)
