import re


def parse_delta(val: str):
    """Return numeric delta value or 'new'.

    Handles strings like '+42', '-3', '+0.3', '0', or '+new'.
    """
    val = val.strip()
    if not val:
        return 0
    if val.lower().lstrip("+") == "new":
        return "new"
    # allow leading '+'
    num = val.lstrip("+")
    try:
        if re.search(r"\.\d", num):
            return float(num)
        return int(num)
    except ValueError:
        return num


def _extract_table_lines(text: str) -> list[str]:
    """Return only the table lines between the TOP50 markers."""
    try:
        start = text.index("<!-- TOP50:START -->")
        end = text.index("<!-- TOP50:END -->", start)
    except ValueError:
        return [l for l in text.splitlines() if l.startswith("|")]
    section = text[start:end]
    return [l for l in section.splitlines() if l.startswith("|")]


def _strip_html(text: str) -> str:
    """Return ``text`` with any HTML tags removed."""
    return re.sub(r"<[^>]+>", "", text)


def _normalize_header(line: str) -> list[str]:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return [re.sub(r"\s+", " ", _strip_html(c)).strip() for c in cells]


def assert_readme_diff(old: str, new: str, *, delta: float = 0.02) -> None:
    """Assert README tables differ only within ``delta`` for numeric cells.

    Header lines are normalized by stripping HTML and collapsing whitespace so
    minor formatting changes don't trigger failures. Numeric columns may vary
    within ``delta``.
    """

    old_lines = _extract_table_lines(old)
    new_lines = _extract_table_lines(new)
    assert len(old_lines) == len(
        new_lines
    ), f"row count {len(old_lines)} != {len(new_lines)}"

    if old_lines:
        assert _normalize_header(old_lines[0]) == _normalize_header(new_lines[0])

    ncols = len(_normalize_header(old_lines[0])) if old_lines else 0
    for i, (ol, nl) in enumerate(zip(old_lines[2:], new_lines[2:]), start=2):
        ocells = [c.strip() for c in ol.strip().strip("|").split("|")]
        ncells = [c.strip() for c in nl.strip().strip("|").split("|")]
        assert (
            len(ocells) == len(ncells) == ncols
        ), f"row {i} column count mismatch: {len(ocells)} vs {len(ncells)}"

        errors: list[str] = []

        if ocells[0] != ncells[0]:
            errors.append(f"rank {ocells[0]} != {ncells[0]}")
        if ocells[1] != ncells[1]:
            errors.append(f"repo '{ocells[1]}' != '{ncells[1]}'")

        for idx in range(2, 12):
            if ocells[idx] and ncells[idx]:
                try:
                    if abs(float(ocells[idx]) - float(ncells[idx])) > delta:
                        errors.append(f"col {idx} {ocells[idx]} != {ncells[idx]}")
                except ValueError:
                    if ocells[idx] != ncells[idx]:
                        errors.append(f"col {idx} '{ocells[idx]}' != '{ncells[idx]}'")

        assert not errors, f"row {i}: " + "; ".join(errors)
