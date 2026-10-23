#!/usr/bin/env python3
"""Check the canonical ADR index for duplicate IDs and controlled statuses."""
from __future__ import annotations
import re
import sys
from pathlib import Path

path = Path(__file__).resolve().parents[2] / "docs" / "ADR_INDEX.md"
text = path.read_text(encoding="utf-8")
allowed = {"Accepted", "Open", "Proposed", "Needs reconciliation"}
rows = []
in_table = False
for line in text.splitlines():
    if line.startswith("| ADR |"):
        in_table = True
        continue
    if in_table and line.startswith("|---"):
        continue
    if in_table and line.startswith("|"):
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and re.fullmatch(r"ADR-\d{4}", cells[0]):
            rows.append((cells[0], cells[2], line))
    elif in_table:
        in_table = False

errors = []
seen = set()
for adr, status, line in rows:
    if adr in seen:
        errors.append(f"duplicate canonical ADR ID: {adr}")
    seen.add(adr)
    if status not in allowed:
        errors.append(f"{adr}: invalid status {status!r}; allowed: {', '.join(sorted(allowed))}")
expected = {f"ADR-{i:04d}" for i in range(1, 25)}
missing = sorted(expected - seen)
if missing:
    errors.append("index missing expected IDs: " + ", ".join(missing))
if len(rows) != 24:
    errors.append(f"expected 24 canonical ADR rows, found {len(rows)}")

if errors:
    print("\n".join("FAIL: " + error for error in errors))
    sys.exit(1)
print(f"PASS: {len(rows)} unique ADR IDs; all statuses use controlled vocabulary.")
print("NOTE: this check validates index structure only, not the correctness or approval of decisions.")
