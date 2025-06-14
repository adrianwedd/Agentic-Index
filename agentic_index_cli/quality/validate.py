"""Validate ``repos.json`` against the public schema."""

import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schemas" / "repo.schema.json"


def load_schema() -> dict:
    """Return the JSON schema used for validation."""
    return json.loads(SCHEMA_PATH.read_text())


def validate_file(path: str) -> list:
    """Validate ``path`` and return unique repos."""
    data = json.loads(Path(path).read_text())
    schema = load_schema()
    validator = Draft7Validator(schema)
    if not isinstance(data, list):
        raise ValidationError("Data must be a list of repositories")
    validated = {}
    duplicates = []
    for repo in data:
        validator.validate(repo)
        name = repo.get("full_name")
        if name in validated:
            prev = validated[name]
            prev_score = prev.get("AgenticIndexScore", 0)
            new_score = repo.get("AgenticIndexScore", 0)
            if new_score > prev_score:
                duplicates.append(prev)
                validated[name] = repo
            else:
                duplicates.append(repo)
        else:
            validated[name] = repo
    if duplicates:
        names = ", ".join(r.get("full_name", "?") for r in duplicates)
        raise ValidationError(f"duplicate entries: {names}")
    return list(validated.values())


def main(argv=None) -> int:
    """CLI wrapper for :func:`validate_file`."""
    argv = argv or sys.argv[1:]
    json_path = argv[0] if argv else "data/repos.json"
    try:
        validate_file(json_path)
    except ValidationError as e:
        print(f"ValidationError: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
