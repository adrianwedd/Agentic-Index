import importlib
import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _setup_api_env():
    """Set API environment variables for testing before any imports."""
    # Set default API environment variables for testing
    os.environ.setdefault("API_KEY", "test-key")
    os.environ.setdefault("IP_WHITELIST", "")
    yield


@pytest.fixture(autouse=True)
def _offline_socket(monkeypatch):
    if os.getenv("CI_OFFLINE") == "1":
        import pytest_socket

        pytest_socket.disable_socket()
        yield
        pytest_socket.enable_socket()
    else:
        yield


@pytest.fixture(autouse=True)
def allow_testclient_unix_sockets():
    """Permit AF_UNIX sockets for FastAPI's TestClient when sockets are disabled."""
    import socket

    try:
        import pytest_socket
    except Exception:  # pragma: no cover - pytest-socket not installed
        yield
        return

    if socket.socket is pytest_socket._true_socket:
        # Network calls aren't blocked; nothing to do
        yield
        return

    pytest_socket.enable_socket()
    pytest_socket.disable_socket(allow_unix_socket=True)
    try:
        yield
    finally:
        pytest_socket.enable_socket()
        pytest_socket.disable_socket()


def pytest_sessionstart(session):
    required_env = ["CI_OFFLINE"]
    missing = [var for var in required_env if os.getenv(var) is None]
    if missing:
        pytest.exit(
            "Missing required environment variables: "
            + ", ".join(missing)
            + "\nSet them or run scripts/agent-setup.sh",
            returncode=1,
        )

    missing_mods = []
    for name in ["responses", "pytest_socket"]:
        try:
            importlib.import_module(name)
        except Exception:  # pragma: no cover - import error path
            missing_mods.append(name)
    if missing_mods:
        pytest.exit(
            "Missing test dependencies: "
            + ", ".join(missing_mods)
            + "\nRun 'pip install -r requirements.txt'",
            returncode=1,
        )


def pytest_runtest_setup(item):
    if item.get_closest_marker("network") and os.getenv("CI_OFFLINE") == "1":
        pytest.skip("network disabled")


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
