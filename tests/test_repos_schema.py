import json
from pathlib import Path

from jsonschema import Draft7Validator


def test_repos_schema():
    root = Path(__file__).resolve().parent.parent
    data_path = root / "data" / "repos.json"
    schema_path = root / "data" / "repos.schema.json"
    data = json.loads(data_path.read_text())
    schema = json.loads(schema_path.read_text())
    Draft7Validator(schema).validate(data)
