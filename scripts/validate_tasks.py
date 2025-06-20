#!/usr/bin/env python3
"""Validate tasks.yml against the task schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "task.schema.json"


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


def validate_tasks(path: str) -> list[dict]:
    data = yaml.safe_load(Path(path).read_text())
    schema = load_schema()
    validator = Draft7Validator(schema)
    if not isinstance(data, list):
        raise ValidationError("tasks file must be a list")
    for item in data:
        validator.validate(item)
    return data


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    path = argv[0] if argv else "tasks.yml"
    try:
        validate_tasks(path)
    except ValidationError as e:
        print(f"ValidationError: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
