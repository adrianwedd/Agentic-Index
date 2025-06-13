import json
from pathlib import Path

import jsonschema

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "repo.schema.json"
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "repos.json"

with SCHEMA_PATH.open() as f:
    SCHEMA = json.load(f)

with DATA_PATH.open() as f:
    DATA = json.load(f)

def test_all_repos_validate():
    validator = jsonschema.Draft7Validator(SCHEMA)
    for idx, item in enumerate(DATA):
        errors = list(validator.iter_errors(item))
        assert not errors, f"Repo index {idx} failed validation: {errors}"
