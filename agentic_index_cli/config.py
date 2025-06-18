from __future__ import annotations

"""Utilities for loading CLI configuration from YAML files."""

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

DEFAULT_PATH = Path(__file__).with_name("config.yaml")


class RankingConfig(BaseModel):
    """Configuration options for ranking."""

    top_n: int = 100
    delta_days: int = 7
    min_stars: int = 0


class OutputConfig(BaseModel):
    """Options controlling CLI output."""

    markdown_table_limit: int = 100


class AppConfig(BaseModel):
    """Root configuration model for the CLI."""

    ranking: RankingConfig = Field(default_factory=RankingConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)

    model_config = ConfigDict(extra="forbid")


def load_config(path: str | Path | None = None) -> dict:
    """Return validated configuration from ``path``."""
    p = Path(path) if path else DEFAULT_PATH
    with p.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    try:
        cfg = AppConfig(**raw)
    except ValidationError as exc:  # pragma: no cover - validated in tests
        errors = "; ".join(
            f"{'.'.join(str(x) for x in err['loc'])}: {err['msg']}"
            for err in exc.errors()
        )
        raise ValueError(f"invalid config file {p}: {errors}") from None

    return cfg.model_dump(exclude_none=True)
