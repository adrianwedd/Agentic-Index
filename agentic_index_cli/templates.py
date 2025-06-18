from __future__ import annotations

from jinja2 import Template

SUMMARY_ROW_TMPL = Template(
    "| {{ i }} | {{ name }} | {{ desc }} | {{ score }} | {{ stars }} | {{ delta }} |"
)

FULL_ROW_TMPL = Template(
    "| {{ i }} | {{ name }} | {{ score }} | {{ stars }} | {{ sdelta }} | {{ scdelta }} | {{ rec }} | {{ health }} | {{ docs }} | {{ licfr }} | {{ eco }} | {{ log2 }} | {{ cat }} |"
)

__all__ = [
    "SUMMARY_ROW_TMPL",
    "FULL_ROW_TMPL",
    "clamp_name",
    "format_link",
    "short_desc",
]


def clamp_name(name: str, limit: int = 28) -> str:
    """Return ``name`` truncated and escaped for markdown."""
    safe = name.replace("|", "\\|").replace("`", "\\`")
    if len(safe) <= limit:
        return safe
    return safe[: limit - 3] + "..."


def format_link(name: str, url: str | None, *, limit: int = 28) -> str:
    """Return a markdown link for ``name`` clamped to ``limit``."""
    text = clamp_name(name, limit)
    if url:
        return f"[{text}]({url})"
    return text


def short_desc(desc: str | None, limit: int = 150) -> str:
    """Return ``desc`` escaped for markdown and truncated."""
    if not desc:
        return ""
    desc = desc.replace("|", "/").replace("`", "\\`").replace("\n", " ")
    if len(desc) <= limit:
        return desc
    return desc[: limit - 3] + "..."
