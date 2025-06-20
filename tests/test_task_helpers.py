from pathlib import Path

import yaml

from scripts.rank_tasks import rank_tasks
from scripts.validate_tasks import validate_tasks


def test_validate_and_rank(tmp_path):
    tasks = [
        {
            "id": "B",
            "description": "Second",
            "component": "code",
            "dependencies": [],
            "priority": 2,
            "status": "todo",
        },
        {
            "id": "A",
            "description": "First",
            "component": "docs",
            "dependencies": ["B"],
            "priority": 1,
            "status": "done",
        },
    ]
    path = tmp_path / "tasks.yml"
    path.write_text(yaml.safe_dump(tasks))

    validated = validate_tasks(str(path))
    assert len(validated) == 2

    ranked = rank_tasks(str(path))
    assert [t["id"] for t in ranked] == ["A", "B"]
