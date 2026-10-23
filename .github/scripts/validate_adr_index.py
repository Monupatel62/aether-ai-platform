#!/usr/bin/env python3
"""Validate the canonical ADR index structure and coverage of the decision log."""
from __future__ import annotations
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
index_path = root / "docs" / "ADR_INDEX.md"
log_path = root / "docs" / "DECISION_LOG.md"
index_text = index_path.read_text(encoding="utf-8")
log_text = log_path.read_text(encoding="utf-8")
allowed = {"Accepted", "Open", "Proposed", "Needs reconciliation"}
rows = []
in_table = False
for line in index_text.splitlines():
    if line.startswith("| ADR |"):
        in_table = True
        continue
    if in_table and line.startswith("|---"):
        continue
    if in_table and line.startswith("|"):
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and re.fullmatch(r"ADR-\d{4}", cells[0]):
            rows.append((cells[0], cells[2]))
    elif in_table:
        in_table = False

errors = []
seen = set()
for adr, status in rows:
    if adr in seen:
        errors.append(f"duplicate canonical ADR ID: {adr}")
    seen.add(adr)
    if status not in allowed:
        errors.append(f"{adr}: invalid status {status!r}; allowed: {', '.join(sorted(allowed))}")

expected = {f"ADR-{i:04d}" for i in range(1, 25)}
missing_expected = sorted(expected - seen)
if missing_expected:
    errors.append("index missing expected IDs: " + ", ".join(missing_expected))
if len(rows) != 24:
    errors.append(f"expected 24 canonical ADR rows, found {len(rows)}")

log_ids = set(re.findall(r"ADR-\d{4}", log_text))
unindexed = sorted(log_ids - seen)
if unindexed:
    errors.append("decision log contains IDs absent from canonical index: " + ", ".join(unindexed))

if errors:
    print("\n".join("FAIL: " + error for error in errors))
    sys.exit(1)
print(f"PASS: {len(rows)} unique canonical ADR IDs; controlled statuses valid.")
print(f"PASS: all {len(log_ids)} distinct ADR IDs mentioned in DECISION_LOG.md are indexed.")
print("NOTE: duplicate historical mentions in the decision log are preserved; this check does not resolve status conflicts or approve decisions.")
