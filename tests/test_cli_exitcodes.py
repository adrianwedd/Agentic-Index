from unittest import mock

import pytest
import requests

pytestmark = pytest.mark.network

from agentic_index_cli.__main__ import run


def test_network_exitcode():
    def fail(*args, **kwargs):
        raise requests.RequestException("fail")

    with mock.patch(
        "agentic_index_cli.network.http_utils.sync_get",
        lambda *a, **k: (_ for _ in ()).throw(requests.RequestException("fail")),
    ):
        with pytest.raises(SystemExit) as exc:
            run(["scrape"])
    assert exc.value.code == 2
