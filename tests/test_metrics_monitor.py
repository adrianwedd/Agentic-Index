import importlib.util
import json
from pathlib import Path
from unittest import mock

spec = importlib.util.spec_from_file_location(
    "monitor", Path("scripts/check_metrics.py")
)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


def test_alert_on_drop(monkeypatch, tmp_path):
    repo = {
        "full_name": "owner/repo",
        "stargazers_count": 10,
        "release_age": 5,
    }
    data = {"repos": [repo]}
    path = tmp_path / "repos.json"
    path.write_text(json.dumps(data))
    monkeypatch.setattr(
        monitor, "fetch_repo_data", lambda name: {"stars": 5, "release_age": 40}
    )
    alerts = []
    monkeypatch.setattr(monitor, "slack_alert", lambda msg: alerts.append(msg))
    monkeypatch.setattr(monitor, "email_alert", lambda subj, msg: alerts.append(msg))
    monitor.main(str(path))
    assert alerts
