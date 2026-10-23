# Contract Validation Runbook

**Status:** Proposed procedure; not evidence of a completed validation run.

## Purpose

Run the draft JSON Schema fixtures against the schemas using JSON Schema Draft 2020-12, with format assertion enabled. This is a structural validation step only; it does not prove authorization freshness, tenant ownership, replay protection, cross-field time ordering, or runtime behavior.

## Preconditions

- Run from the repository root.
- Use Python 3.11 or newer in a clean virtual environment.
- Install pinned or lockfile-controlled validation dependencies before relying on results.
- Use the fixture inventory at `docs/contracts/contract-fixtures.v1.json`.
- Each fixture's `schema` value must resolve to a file under `docs/contracts/`; do not follow arbitrary paths from untrusted fixture data.

## Repeatable local procedure

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "jsonschema[format]>=4.23,<5"
python - <<'PY'
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

root = Path(".")
contracts = root / "docs" / "contracts"
fixture_path = contracts / "contract-fixtures.v1.json"
fixtures = json.loads(fixture_path.read_text(encoding="utf-8"))
cases = fixtures["cases"]
if not cases:
    raise SystemExit("FAIL: fixture inventory is empty")

validators = {}
failures = []
for case in cases:
    case_id = case["case_id"]
    schema_name = case["schema"]
    schema_path = (contracts / schema_name).resolve()
    if schema_path.parent != contracts.resolve():
        failures.append(f"{case_id}: schema path escapes contracts directory")
        continue
    if not schema_path.is_file():
        failures.append(f"{case_id}: missing schema {schema_name}")
        continue
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = validators.setdefault(
            schema_name,
            Draft202012Validator(schema, format_checker=FormatChecker()),
        )
        errors = sorted(validator.iter_errors(case["payload"]), key=lambda e: list(map(str, e.absolute_path)))
        actual_valid = not errors
        expected_valid = case["expected_valid"]
        if actual_valid != expected_valid:
            details = "; ".join(
                f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
                for e in errors[:3]
            )
            failures.append(
                f"{case_id}: expected_valid={expected_valid}, actual_valid={actual_valid}"
                + (f" ({details})" if details else "")
            )
    except Exception as exc:
        failures.append(f"{case_id}: validator error: {type(exc).__name__}: {exc}")

print(f"Fixtures checked: {len(cases)}")
print(f"Schemas checked: {len(validators)}")
if failures:
    print(f"FAILURES: {len(failures)}")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)
print("PASS: every fixture matched its expected structural validity.")
PY
```

## Interpretation and required follow-up

1. Save the full command output, Python version, and installed `jsonschema` version in the review record.
2. A failed fixture is a contract/schema mismatch. Do not silently change `expected_valid` to make the suite pass; inspect whether the schema or fixture is wrong.
3. A pass means only that the fixtures match their declared expected validity under this validator configuration.
4. Validate the OpenAPI document separately with an OpenAPI 3.1-compatible validator. Record the exact validator and version, and do not treat a generic YAML parse as OpenAPI validation.
5. Add these commands to CI only after the repository's CI/implementation gate and dependency-management choices are approved.
6. Keep the implementation gate blocked until schema validation, OpenAPI validation, authorization/tenant decisions, and runtime/security tests are independently reviewed.

## Current limitation

This runbook has been authored but has **not** been executed as part of this change. Do not report the schemas or fixtures as validated until a real run is recorded.
