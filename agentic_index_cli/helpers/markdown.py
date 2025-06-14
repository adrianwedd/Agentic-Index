"""Markdown rendering helpers."""


def render_badge(label: str, url: str) -> str:
    """Return markdown for an image badge.

    Parameters
    ----------
    label:
        The alt text for the badge.
    url:
        The badge image URL or path.
    Returns
    -------
    str
        Markdown image tag, e.g. ``![label](url)``.
    Raises
    ------
    ValueError
        If ``label`` or ``url`` is empty or contains invalid characters.
    """
    if not isinstance(label, str) or not isinstance(url, str):
        raise TypeError("label and url must be strings")
    label = label.strip()
    url = url.strip()
    if not label or not url:
        raise ValueError("label and url required")
    if any(ch in label for ch in "]()\n"):
        raise ValueError("label contains invalid characters")
    if any(ch in url for ch in "()\n"):
        raise ValueError("url contains invalid characters")
    return f"![{label}]({url})"
