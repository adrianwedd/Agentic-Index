import json
import subprocess


def test_validation_migrate(tmp_path):
    repo = {"name": "repo1", "AgentOpsScore": 5}
    path = tmp_path / "repos.json"
    path.write_text(json.dumps([repo]))
    result = subprocess.run(
        [
            "python",
            "-m",
            "agentic_index_cli.validate",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
