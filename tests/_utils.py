import re


def parse_delta(val: str):
    """Return numeric delta value or 'new'.

    Handles strings like '+42', '-3', '+0.3', '0', or '+new'.
    """
    val = val.strip()
    if not val:
        return 0
    if val.lower().lstrip('+') == 'new':
        return 'new'
    # allow leading '+'
    num = val.lstrip('+')
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


def assert_readme_diff(old: str, new: str, *, delta: float = 0.02) -> None:
    """Assert README tables differ only within ``delta`` for numeric cells."""
    old_lines = _extract_table_lines(old)
    new_lines = _extract_table_lines(new)
    assert len(old_lines) == len(new_lines)
    for i, (ol, nl) in enumerate(zip(old_lines, new_lines)):
        if i < 2:
            assert ol.strip() == nl.strip()
            continue
        ocells = [c.strip() for c in ol.strip().strip("|").split("|")]
        ncells = [c.strip() for c in nl.strip().strip("|").split("|")]
        assert ocells[0] == ncells[0]
        assert ocells[2] == ncells[2]
        for idx in (1, 3, 4, 6, 7):
            if ocells[idx] and ncells[idx]:
                assert abs(float(ocells[idx]) - float(ncells[idx])) <= delta
        assert ocells[5] == ncells[5]
        assert ocells[8] == ncells[8]
