import os
import re
import math
from typing import List, Tuple, Dict, Any


def _canonical(name: str) -> str:
    name = re.sub(r"<[^>]+>", "", name)
    name = re.sub(r"[^\w\s]+", "", name)
    name = name.strip().lower()
    mapping = {
        "overall": "score",
        "score": "score",
        "repo": "repo",
        "stars gained in last 30 days": "stars",
        "stars d30d": "stars",
        "stars": "stars",
        "maint": "maint",
        "maintenance": "maint",
        "release": "release",
        "docs": "docs",
        "fit": "fit",
        "license": "license",
        "rank": "rank",
    }
    return mapping.get(name, name)


def _parse_table(text: str) -> Tuple[List[str], List[List[str]]]:
    lines = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    if not lines:
        return [], []
    headers = [c.strip() for c in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(headers):
            raise AssertionError(f"Column count mismatch in line: {line}")
        rows.append(cells)
    return headers, rows


def _parse_value(cell: str) -> Tuple[Any, str]:
    if re.fullmatch(r"-?\d+", cell):
        return int(cell), "int"
    if re.fullmatch(r"-?\d+\.\d+", cell):
        return float(cell), "float"
    return cell, "text"


def _load_tolerances(tols: Dict[str, float] | None) -> Dict[str, float]:
    result = {}
    if tols:
        result.update({_canonical(k): float(v) for k, v in tols.items()})
    env = os.getenv("README_TOLERANCES")
    if env:
        for part in env.split(","):
            if not part.strip():
                continue
            key, val = part.split("=", 1)
            result[_canonical(key)] = float(val)
    return result


def assert_readme_equivalent(expected: str, actual: str, tolerances: Dict[str, float] | None = None) -> None:
    tols = _load_tolerances(tolerances)
    exp_headers_raw, exp_rows = _parse_table(expected)
    act_headers_raw, act_rows = _parse_table(actual)
    assert exp_headers_raw == act_headers_raw, "Header mismatch"
    assert len(exp_rows) == len(act_rows), "Row count changed"
    headers = exp_headers_raw
    for row_idx, (erow, arow) in enumerate(zip(exp_rows, act_rows)):
        assert len(erow) == len(arow), f"Column count changed in row {row_idx}"
        for col_idx, (ecell, acell) in enumerate(zip(erow, arow)):
            header = headers[col_idx]
            key = _canonical(header)
            val1, kind1 = _parse_value(ecell)
            val2, kind2 = _parse_value(acell)
            if kind1 == "text" or kind2 == "text":
                assert ecell == acell, f"Mismatch in row {row_idx} column {header}"
                continue
            tol = tols.get(key, 0.0)
            if kind1 == "int" and kind2 == "int" and "." not in ecell and "." not in acell:
                assert abs(val1 - val2) <= tol, f"Int mismatch in row {row_idx} column {header}: {val1} vs {val2}"
            else:
                assert math.isclose(float(val1), float(val2), rel_tol=tol), (
                    f"Float mismatch in row {row_idx} column {header}: {val1} vs {val2} tol={tol}"
                )
