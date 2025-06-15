import pytest
from agentic_index_cli.__main__ import run
import requests
from unittest import mock


def test_network_exitcode():
    def fail(*args, **kwargs):
        raise requests.RequestException("fail")

    with mock.patch('agentic_index_cli.agentic_index.requests.get', fail):
        with pytest.raises(SystemExit) as exc:
            run(['scrape'])
    assert exc.value.code == 2
