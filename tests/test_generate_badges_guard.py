import json
import urllib.request
from pathlib import Path

from scripts.generate_badges import main as generate_main


def test_generate_badges_once(tmp_path, monkeypatch):
    data = {"repos": [{"name": "x", "AgenticIndexScore": 1.0}]}
    json_path = tmp_path / "repos.json"
    json_path.write_text(json.dumps(data))
    badges = tmp_path / "badges"
    badges.mkdir()
    monkeypatch.chdir(tmp_path)

    def fake_open(url):
        class Resp:
            def read(self):
                return b"<svg></svg>"

            def close(self):
                pass

        return Resp()

    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **kw: fake_open(a[0]))

    generate_main(str(json_path))
    stamp = Path("state/generate_badges.date")
    assert stamp.exists()
    first_mtime = stamp.read_text()
    generate_main(str(json_path))
    assert stamp.read_text() == first_mtime
