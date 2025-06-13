from unittest import mock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.scrape as scrape


def make_response(remaining):
    resp = mock.Mock()
    resp.json.return_value = {"items": []}
    resp.headers = {"X-RateLimit-Remaining": str(remaining)}
    resp.links = {}
    resp.raise_for_status = mock.Mock()
    return resp


def test_rate_limit_drops():
    responses = [make_response(100), make_response(99), make_response(98), make_response(97)]
    with mock.patch("scripts.scrape.requests.get", side_effect=responses) as get:
        scrape.scrape(min_stars=0, token=None)
        assert scrape.RATE_LIMIT_REMAINING == 97
        assert int(responses[0].headers["X-RateLimit-Remaining"]) > scrape.RATE_LIMIT_REMAINING
        assert get.call_count == len(responses)
