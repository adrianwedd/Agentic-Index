import subprocess


def detect_changes(repo):
    cmd = [
        "bash",
        "-c",
        (
            "if git diff --quiet --exit-code "
            "data/top100.md data/repos.json README.md; then "
            "echo changed=false; else echo changed=true; fi"
        ),
    ]
    result = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    return "changed=true" in result.stdout


def setup_repo(tmp_path):
    (tmp_path / "data").mkdir()
    (tmp_path / "data/top100.md").write_text("one")
    (tmp_path / "data/repos.json").write_text('{"schema_version": 1, "repos": []}')
    (tmp_path / "README.md").write_text("readme")
    subprocess.run(["git", "init"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True
    )
    subprocess.run(["git", "config", "user.name", "Tester"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, check=True)


def test_detect_changes_true(tmp_path):
    setup_repo(tmp_path)
    (tmp_path / "data/top100.md").write_text("two")
    assert detect_changes(tmp_path) is True


def test_detect_changes_false(tmp_path):
    setup_repo(tmp_path)
    assert detect_changes(tmp_path) is False
