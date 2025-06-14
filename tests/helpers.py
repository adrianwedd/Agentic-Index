import os
import re
import math
import difflib
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


def _extract_table(text: str) -> List[str]:
    """Return table lines between the TOP50 markers if present."""
    try:
        start = text.index("<!-- TOP50:START -->")
        end = text.index("<!-- TOP50:END -->", start)
    except ValueError:
        return [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    section = text[start:end]
    return [l.strip() for l in section.splitlines() if l.strip().startswith("|")]


def _parse_table(text: str) -> Tuple[List[str], List[List[str]]]:
    lines = _extract_table(text)
    if not lines:
        return [], []
    header_line = re.sub(r"<[^>]+>", "", lines[0])
    headers = [c.strip() for c in header_line.strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(headers):
            raise AssertionError(
                f"Column count mismatch: expected {len(headers)} got {len(cells)} in line: {line}"
            )
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
    try:
        exp_headers_raw, exp_rows = _parse_table(expected)
    except AssertionError as e:
        raise AssertionError(f"Failed to parse expected table: {e}")

    try:
        act_headers_raw, act_rows = _parse_table(actual)
    except AssertionError as e:
        raise AssertionError(f"Failed to parse actual table: {e}")

    if exp_headers_raw != act_headers_raw:
        diff = "\n".join(
            difflib.unified_diff(exp_headers_raw, act_headers_raw, "expected", "actual", lineterm="")
        )
        raise AssertionError(f"Header mismatch:\n{diff}")

    if len(exp_rows) != len(act_rows):
        raise AssertionError(
            f"Row count mismatch: expected {len(exp_rows)} rows but got {len(act_rows)}"
        )

    headers = exp_headers_raw
    for row_idx, (erow, arow) in enumerate(zip(exp_rows, act_rows)):
        if len(erow) != len(arow):
            raise AssertionError(
                f"Column count mismatch in row {row_idx}: expected {len(erow)} got {len(arow)}"
            )
        for col_idx, (ecell, acell) in enumerate(zip(erow, arow)):
            header = headers[col_idx]
            key = _canonical(header)
            val1, kind1 = _parse_value(ecell)
            val2, kind2 = _parse_value(acell)
            if kind1 == "text" or kind2 == "text":
                if ecell != acell:
                    diff = "\n".join(
                        difflib.unified_diff(
                            ["| " + " | ".join(erow) + " |"],
                            ["| " + " | ".join(arow) + " |"],
                            "expected",
                            "actual",
                            lineterm="",
                        )
                    )
                    raise AssertionError(f"Mismatch in row {row_idx} column {header}\n{diff}")
                continue
            tol = tols.get(key, 0.0)
            if kind1 == "int" and kind2 == "int" and "." not in ecell and "." not in acell:
                if abs(val1 - val2) > tol:
                    diff = "\n".join(
                        difflib.unified_diff(
                            ["| " + " | ".join(erow) + " |"],
                            ["| " + " | ".join(arow) + " |"],
                            "expected",
                            "actual",
                            lineterm="",
                        )
                    )
                    raise AssertionError(
                        f"Int mismatch in row {row_idx} column {header}: {val1} vs {val2}\n{diff}"
                    )
            else:
                if not math.isclose(float(val1), float(val2), rel_tol=tol):
                    diff = "\n".join(
                        difflib.unified_diff(
                            ["| " + " | ".join(erow) + " |"],
                            ["| " + " | ".join(arow) + " |"],
                            "expected",
                            "actual",
                            lineterm="",
                        )
                    )
                    raise AssertionError(
                        f"Float mismatch in row {row_idx} column {header}: {val1} vs {val2} tol={tol}\n{diff}"
                    )
