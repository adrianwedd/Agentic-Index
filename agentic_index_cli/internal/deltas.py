from __future__ import annotations

"""Helpers for computing and formatting delta values."""


def _fmt_delta(old: int | None, new: int) -> str:
    """Return signed delta string for star counts.

    ``old`` may be ``None`` if no previous snapshot exists.
    ``new`` is the current star count.
    """
    if old is None:
        return "+new"

    diff = new - old
    if diff == 0:
        return ""
    return f"{diff:+d}"
