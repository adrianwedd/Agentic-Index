from __future__ import annotations

import datetime
import json
import shutil
from pathlib import Path

from agentic_index_cli.constants import SCORE_KEY
from agentic_index_cli.validate import save_repos

__all__ = ["persist_history", "write_by_category"]


def persist_history(data_file: Path, repos: list[dict], *, delta_days: int) -> None:
    """Save ``repos`` snapshot and prune old entries."""
    history_dir = data_file.parent / "history"
    history_dir.mkdir(exist_ok=True)
    today_iso = datetime.date.today().isoformat()
    snapshot_path = history_dir / f"{today_iso}.json"
    shutil.copy(data_file, snapshot_path)
    (data_file.parent / "last_snapshot.txt").write_text(str(snapshot_path))
    snapshots = sorted(history_dir.glob("*.json"))
    for old in snapshots[:-delta_days]:
        old.unlink()


def write_by_category(data_dir: Path, repos: list[dict]) -> None:
    """Write per-category repo lists under ``data_dir/by_category``."""
    by_cat = data_dir / "by_category"
    by_cat.mkdir(exist_ok=True)
    index: dict[str, str] = {}
    for cat in sorted({r.get("category") for r in repos if r.get("category")}):
        cat_repos = [r for r in repos if r.get("category") == cat]
        cat_repos.sort(key=lambda r: r[SCORE_KEY], reverse=True)
        fname = f"{cat}.json"
        save_repos(by_cat / fname, cat_repos)
        index[cat] = fname
    (by_cat / "index.json").write_text(json.dumps(index, indent=2) + "\n")
