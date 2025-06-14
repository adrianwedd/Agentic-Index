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
