from __future__ import annotations

"""Utilities for loading CLI configuration from YAML files."""

from pathlib import Path
import yaml

DEFAULT_PATH = Path(__file__).with_name("config.yaml")

def load_config(path: str | Path | None = None) -> dict:
    """Return YAML config as a dictionary."""
    p = Path(path) if path else DEFAULT_PATH
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data
