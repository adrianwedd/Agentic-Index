"""Utilities for once-per-day execution guards."""

from __future__ import annotations

import datetime as _dt
from pathlib import Path


def once_per_day(name: str, *, state_dir: Path | str = "state") -> bool:
    """Return ``True`` if ``name`` has not run today."""

    dir_path = Path(state_dir)
    dir_path.mkdir(parents=True, exist_ok=True)
    stamp = dir_path / f"{name}.date"
    today = _dt.date.today().isoformat()
    if stamp.exists() and stamp.read_text().strip() == today:
        return False
    stamp.write_text(today)
    return True
