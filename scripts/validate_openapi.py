#!/usr/bin/env python3
"""Validate the draft Aether OpenAPI 3.1 contract.

Run from the repository root:
  python -m pip install -r requirements-openapi-validation.txt
  python scripts/validate_openapi.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml
from openapi_spec_validator import validate_spec
from openapi_spec_validator.validation.exceptions import OpenAPIError

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "contracts" / "openapi.v1.yaml"


def main() -> int:
    try:
        spec = yaml.safe_load(SPEC_PATH.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"FAIL: cannot load OpenAPI document: {exc}", file=sys.stderr)
        return 2

    if not isinstance(spec, dict):
        print("FAIL: OpenAPI document must be a YAML object", file=sys.stderr)
        return 2
    if spec.get("openapi") != "3.1.0":
        print(
            f"FAIL: expected OpenAPI version 3.1.0, got {spec.get('openapi')!r}",
            file=sys.stderr,
        )
        return 1

    try:
        validate_spec(spec)
    except OpenAPIError as exc:
        print(f"FAIL: OpenAPI validation failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # validator may expose version-specific exceptions
        print(f"FAIL: validator could not complete: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    print(f"OpenAPI version: {spec['openapi']}")
    print(f"Paths checked: {len(spec.get('paths', {}))}")
    print("PASS: OpenAPI document passed openapi-spec-validator.")
    print("NOTE: structural validation does not approve the draft API or prove runtime behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
