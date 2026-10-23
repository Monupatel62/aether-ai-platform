#!/usr/bin/env python3
"""Validate Aether AI's documented contracts; this does not validate runtime behavior."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from openapi_spec_validator import validate as validate_openapi_spec

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "docs" / "contracts"
errors: list[str] = []
checks = 0


def fail(message: str) -> None:
    errors.append(message)
    print(f"ERROR: {message}")


def load_json(path: Path):
    global checks
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        checks += 1
        return value
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)} is not valid JSON: {exc}")
        return None


def validate_catalog() -> None:
    global checks
    path = ROOT / "docs" / "REPOSITORY_CATALOG.md"
    text = path.read_text(encoding="utf-8")
    names = re.findall(r"\[`(aether-ai-[a-z-]+)`\]\(https://github\.com/Monupatel62/\1\)", text)
    unique = set(names)
    if len(names) != 33 or len(unique) != 33:
        fail(f"catalog must contain 33 unique canonical repository links; found {len(names)} links and {len(unique)} unique names")
    else:
        checks += 1
        print("PASS: catalog contains 33 unique canonical repository links")


def validate_json_schemas() -> dict[str, dict]:
    global checks
    schemas: dict[str, dict] = {}
    for path in sorted(CONTRACTS.glob("*.schema.json")):
        schema = load_json(path)
        if not isinstance(schema, dict):
            fail(f"{path.relative_to(ROOT)} must contain a JSON Schema object")
            continue
        try:
            Draft202012Validator.check_schema(schema)
            schemas[path.name] = schema
            checks += 1
        except Exception as exc:
            fail(f"{path.relative_to(ROOT)} failed Draft 2020-12 meta-schema validation: {exc}")
    if not schemas:
        fail("no *.schema.json contract schemas were found")
    else:
        print(f"Validated JSON Schema definitions: {len(schemas)}")
    return schemas


def validate_fixtures(schemas: dict[str, dict]) -> None:
    global checks
    path = CONTRACTS / "contract-fixtures.v1.json"
    fixtures = load_json(path)
    if not isinstance(fixtures, dict) or not isinstance(fixtures.get("cases"), list):
        fail("contract-fixtures.v1.json must contain a cases array")
        return
    ids: set[str] = set()
    for index, case in enumerate(fixtures["cases"]):
        prefix = f"fixture case #{index + 1}"
        if not isinstance(case, dict):
            fail(f"{prefix} must be an object")
            continue
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            fail(f"{prefix} has no non-empty case_id")
        elif case_id in ids:
            fail(f"duplicate fixture case_id: {case_id}")
        else:
            ids.add(case_id)
        schema_name = case.get("schema")
        schema = schemas.get(schema_name) if isinstance(schema_name, str) else None
        if schema is None:
            fail(f"{case_id or prefix} references missing/unknown schema {schema_name!r}")
            continue
        expected = case.get("expected_valid")
        if not isinstance(expected, bool):
            fail(f"{case_id or prefix} must set boolean expected_valid")
            continue
        try:
            validator = Draft202012Validator(schema, format_checker=FormatChecker())
            valid = not any(validator.iter_errors(case.get("payload")))
            checks += 1
            if valid != expected:
                fail(f"{case_id or prefix}: expected_valid={expected}, actual_valid={valid}")
        except Exception as exc:
            fail(f"{case_id or prefix}: fixture validation raised {exc}")
    print(f"Evaluated contract fixtures: {len(fixtures['cases'])}")


def validate_openapi() -> None:
    global checks
    path = CONTRACTS / "openapi.v1.yaml"
    try:
        spec = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(spec, dict):
            fail("openapi.v1.yaml must parse to a YAML mapping")
            return
        validate_openapi_spec(spec)
        checks += 1
        print("PASS: OpenAPI specification validates")
    except Exception as exc:
        fail(f"OpenAPI validation failed for docs/contracts/openapi.v1.yaml: {exc}")


def validate_dependency_graph() -> None:
    global checks
    path = ROOT / "docs" / "dependency-package-graph.json"
    graph = load_json(path)
    if not isinstance(graph, dict):
        return
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list) or not all(isinstance(n, str) for n in nodes):
        fail("dependency graph nodes must be an array of strings")
        return
    if len(nodes) != len(set(nodes)):
        fail("dependency graph contains duplicate nodes")
    if not isinstance(edges, list):
        fail("dependency graph edges must be an array")
        return
    node_set = set(nodes)
    adjacency: dict[str, list[str]] = defaultdict(list)
    seen_edges: set[tuple[str, str, str]] = set()
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            fail(f"dependency graph edge #{index + 1} must be an object")
            continue
        source, target, edge_type = edge.get("from"), edge.get("to"), edge.get("type")
        if source not in node_set or target not in node_set:
            fail(f"dependency graph edge #{index + 1} references unknown node: {source!r} -> {target!r}")
            continue
        signature = (source, target, str(edge_type))
        if signature in seen_edges:
            fail(f"duplicate dependency graph edge: {signature}")
        seen_edges.add(signature)
        if edge_type == "package_import":
            adjacency[source].append(target)
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for target in adjacency[node]:
            if state.get(target, 0) == 0:
                visit(target)
            elif state.get(target) == 1:
                cycle = stack[stack.index(target):] + [target]
                fail("package-import cycle: " + " -> ".join(cycle))
        stack.pop()
        state[node] = 2

    for node in nodes:
        if state.get(node, 0) == 0:
            visit(node)
    checks += 1
    print(f"Checked dependency graph: {len(nodes)} nodes, {len(edges)} edges")


def main() -> int:
    validate_catalog()
    schemas = validate_json_schemas()
    if schemas:
        validate_fixtures(schemas)
    validate_openapi()
    validate_dependency_graph()
    if errors:
        print(f"FAIL: {len(errors)} issue(s); {checks} validation checks completed")
        return 1
    print(f"PASS: documentation/contract validation completed; {checks} checks")
    print("NOTE: this job validates documented artifacts only, not application source or runtime behavior.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
