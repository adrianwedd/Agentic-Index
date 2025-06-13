import os
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
