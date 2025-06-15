"""Helper functions for Agentic Index."""


def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The sum of ``a`` and ``b``.
    """
    return a + b


from .markdown import render_badge

__all__ = ["add", "render_badge"]
