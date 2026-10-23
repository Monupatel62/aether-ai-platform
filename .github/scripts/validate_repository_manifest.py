#!/usr/bin/env python3
"""Validate repository manifest coverage and dependency references."""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
manifest_path = root / "docs" / "repository-manifest.json"
matrix_path = root / "docs" / "DEPENDENCY_MATRIX.md"
catalog_path = root / "docs" / "REPOSITORY_CATALOG.md"
try:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"FAIL: manifest is not valid JSON: {exc}")
    sys.exit(1)

repos = manifest.get("repositories")
errors = []
if not isinstance(repos, list):
    print("FAIL: repositories must be an array")
    sys.exit(1)
ids = [item.get("id") for item in repos if isinstance(item, dict)]
if len(repos) != 33:
    errors.append(f"expected 33 repository records, found {len(repos)}")
if len(ids) != len(set(ids)):
    errors.append("duplicate repository IDs found")
valid = set(ids)
if len(valid) != 33:
    errors.append("expected 33 distinct repository IDs")
for item in repos:
    rid = item.get("id", "<missing>")
    if not isinstance(rid, str) or not re.fullmatch(r"aether-ai-[a-z0-9-]+", rid):
        errors.append(f"invalid repository ID: {rid!r}")
        continue
    deps = item.get("dependencies")
    if not isinstance(deps, list):
        errors.append(f"{rid}: dependencies must be an array")
        continue
    if rid in deps:
        errors.append(f"{rid}: self-dependency")
    for dep in deps:
        if dep not in valid:
            errors.append(f"{rid}: dependency not in manifest: {dep}")
    if item.get("owner") != "TBD":
        errors.append(f"{rid}: owner must remain TBD until explicitly assigned")
    if item.get("edgeTypes") != "unclassified":
        errors.append(f"{rid}: edge types must remain unclassified until reconciled")
platform = next((x for x in repos if x.get("id") == "aether-ai-platform"), None)
if platform and platform.get("dependencies") != []:
    errors.append("aether-ai-platform must have no runtime dependencies")

matrix = matrix_path.read_text(encoding="utf-8")
catalog = catalog_path.read_text(encoding="utf-8")
for rid in sorted(valid):
    if rid not in matrix:
        errors.append(f"{rid}: absent from dependency matrix")
    if rid not in catalog:
        errors.append(f"{rid}: absent from repository catalog")

if errors:
    print("\n".join("FAIL: " + e for e in errors))
    sys.exit(1)
print("PASS: 33 unique repository records.")
print("PASS: dependency references resolve; no self-dependencies.")
print("PASS: platform runtime dependency list is empty.")
print("PASS: all manifest IDs appear in the dependency matrix and catalog.")
print("NOTE: owner and edge types are deliberately unclassified; this validator does not approve architecture.")
