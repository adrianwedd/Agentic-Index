import logging
from urllib.error import HTTPError
from unittest import mock
from pathlib import Path
import sys

# ensure project root on path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import scripts.rank as rank


def test_badge_fetch_fallback(tmp_path, caplog):
    caplog.set_level(logging.WARNING)
    badge = tmp_path / "badge.svg"
    badge.write_text("old")
    error = HTTPError(url="http://x", code=503, msg="fail", hdrs=None, fp=None)
    with mock.patch("urllib.request.urlopen", side_effect=error):
        rank._fetch("http://example.com", badge)
    assert badge.read_text() == "old"
    assert "badge fetch failed" in caplog.text
