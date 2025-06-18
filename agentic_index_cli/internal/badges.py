from __future__ import annotations

import os
import urllib.request
from pathlib import Path

__all__ = ["fetch_badge", "generate_badges"]


def fetch_badge(url: str, dest: Path) -> None:
    """Download an SVG badge or create a local placeholder when offline."""
    if os.getenv("CI_OFFLINE") == "1":
        if dest.exists():
            return
        dest.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"></svg>')
        return
    try:
        resp = urllib.request.urlopen(url)
        try:
            content = resp.read().rstrip(b"\n")
            dest.write_bytes(content)
        finally:
            if hasattr(resp, "close"):
                resp.close()
    except Exception:
        if dest.exists():
            return
        dest.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"></svg>')


def generate_badges(top_repo: str, iso_date: str, repo_count: int) -> None:
    """Create Shields.io badges for the ranking results."""
    badges = Path("badges")
    badges.mkdir(exist_ok=True)

    sync_badge = (
        f"https://img.shields.io/static/v1?label=sync&message={iso_date}&color=blue"
    )
    top_badge = f"https://img.shields.io/static/v1?label=top&message={urllib.request.quote(top_repo)}&color=brightgreen"
    count_badge = f"https://img.shields.io/static/v1?label=repos&message={repo_count}&color=informational"

    fetch_badge(sync_badge, badges / "last_sync.svg")
    fetch_badge(top_badge, badges / "top_repo.svg")
    fetch_badge(count_badge, badges / "repo_count.svg")
