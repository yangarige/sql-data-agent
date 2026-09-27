#!/usr/bin/env python3
"""Validate the structure and minimum coverage of behavioral eval cases."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evals" / "cases.json"
REQUIRED_FIELDS = {
    "id",
    "category",
    "prompt",
    "expected_behaviors",
    "forbidden_behaviors",
}


def main() -> int:
    payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    cases = payload.get("cases")
    errors: list[str] = []

    if payload.get("version") != 1:
        errors.append("version must be 1")
    if not isinstance(cases, list) or len(cases) < 10:
        errors.append("at least 10 evaluation cases are required")
        cases = cases if isinstance(cases, list) else []

    identifiers: set[str] = set()
    categories: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"case {index} must be an object")
            continue
        missing = REQUIRED_FIELDS - set(case)
        if missing:
            errors.append(f"case {index} is missing: {', '.join(sorted(missing))}")
        identifier = case.get("id")
        if not isinstance(identifier, str) or not identifier:
            errors.append(f"case {index} has an invalid id")
        elif identifier in identifiers:
            errors.append(f"duplicate case id: {identifier}")
        else:
            identifiers.add(identifier)
        category = case.get("category")
        if isinstance(category, str):
            categories.add(category)
        for field in ("expected_behaviors", "forbidden_behaviors"):
            values = case.get(field)
            if not isinstance(values, list) or not values or not all(
                isinstance(value, str) and value for value in values
            ):
                errors.append(f"case {identifier or index} has invalid {field}")

    required_categories = {"safety", "missing_context", "execution_boundary"}
    missing_categories = required_categories - categories
    if missing_categories:
        errors.append("missing required categories: " + ", ".join(sorted(missing_categories)))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"OK: {len(cases)} evaluation cases across {len(categories)} categories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
