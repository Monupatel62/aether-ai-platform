#!/usr/bin/env python3
"""Validate Aether contract schemas and fixture expected outcomes.

Run from the repository root:
  python -m pip install -r requirements-contract-validation.txt
  python scripts/validate_contract_fixtures.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "docs" / "contracts"
FIXTURES_PATH = CONTRACTS / "contract-fixtures.v1.json"


def main() -> int:
    try:
        inventory = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot load fixture inventory: {exc}", file=sys.stderr)
        return 2

    cases = inventory.get("cases")
    if not isinstance(cases, list) or not cases:
        print("FAIL: fixture inventory must contain a non-empty cases array", file=sys.stderr)
        return 2

    failures: list[str] = []
    schema_cache: dict[str, Draft202012Validator] = {}
    seen_ids: set[str] = set()

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            failures.append(f"case index {index}: expected an object")
            continue

        case_id = case.get("case_id")
        schema_name = case.get("schema")
        if not isinstance(case_id, str) or not case_id:
            failures.append(f"case index {index}: missing case_id")
            case_id = f"index-{index}"
        if case_id in seen_ids:
            failures.append(f"{case_id}: duplicate case_id")
        seen_ids.add(case_id)

        if not isinstance(schema_name, str) or not schema_name or Path(schema_name).name != schema_name:
            failures.append(f"{case_id}: schema must be a simple filename")
            continue
        if not isinstance(case.get("expected_valid"), bool):
            failures.append(f"{case_id}: expected_valid must be boolean")
            continue
        if "payload" not in case:
            failures.append(f"{case_id}: missing payload")
            continue

        if schema_name not in schema_cache:
            schema_path = CONTRACTS / schema_name
            try:
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)
                schema_cache[schema_name] = Draft202012Validator(
                    schema, format_checker=FormatChecker()
                )
            except (OSError, json.JSONDecodeError, Exception) as exc:
                failures.append(f"{case_id}: cannot load/check schema {schema_name}: {exc}")
                continue

        validator = schema_cache[schema_name]
        errors = sorted(
            validator.iter_errors(case["payload"]),
            key=lambda err: (list(map(str, err.absolute_path)), err.message),
        )
        actual_valid = not errors
        if actual_valid != case["expected_valid"]:
            details = "; ".join(
                f"{'/'.join(map(str, err.absolute_path)) or '<root>'}: {err.message}"
                for err in errors[:3]
            )
            failures.append(
                f"{case_id}: expected_valid={case['expected_valid']}, "
                f"actual_valid={actual_valid}"
                + (f" ({details})" if details else "")
            )

    print(f"Fixture cases: {len(cases)}")
    print(f"Unique case IDs: {len(seen_ids)}")
    print(f"Schemas checked: {len(schema_cache)}")
    print("Format assertion: enabled")
    if failures:
        print(f"FAIL: {len(failures)} issue(s)")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: all fixtures matched expected structural validity.")
    print("NOTE: this does not test runtime authorization, revocation, or cross-field semantics.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
