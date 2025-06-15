import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _offline_socket(monkeypatch):
    if os.getenv("CI_OFFLINE") == "1":
        import pytest_socket

        pytest_socket.disable_socket()
        yield
        pytest_socket.enable_socket()
    else:
        yield


@pytest.fixture(scope="session")
def readme_fixture_path() -> Path:
    path = Path(__file__).resolve().parent / "fixtures" / "README_fixture.md"
    if not path.exists():
        pytest.xfail("README fixture missing")
    return path


@pytest.fixture(scope="session")
def data_fixture_dir() -> Path:
    path = Path(__file__).resolve().parent / "fixtures" / "data"
    if not path.exists():
        pytest.xfail("Data fixtures missing")
    return path
