#!/usr/bin/env python3
"""Audit a local checkout of the canonical Aether AI repositories.

This is repository-readiness tooling, not a runtime component. It uses only the
Python standard library and does not access the network or inspect file contents.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

CANONICAL_REPOSITORIES = (
    "aether-ai-platform",
    "aether-ai-web",
    "aether-ai-api",
    "aether-ai-gateway",
    "aether-ai-providers",
    "aether-ai-agents",
    "aether-ai-workflows",
    "aether-ai-orchestration",
    "aether-ai-tools",
    "aether-ai-mcp",
    "aether-ai-memory",
    "aether-ai-rag",
    "aether-ai-files",
    "aether-ai-knowledge",
    "aether-ai-auth",
    "aether-ai-security",
    "aether-ai-admin",
    "aether-ai-billing",
    "aether-ai-sdk",
    "aether-ai-evaluations",
    "aether-ai-observability",
    "aether-ai-deployment",
    "aether-ai-docs",
    "aether-ai-database",
    "aether-ai-queue",
    "aether-ai-cache",
    "aether-ai-search",
    "aether-ai-plugins",
    "aether-ai-integrations",
    "aether-ai-testing",
    "aether-ai-ui-components",
    "aether-ai-enterprise",
    "aether-ai-infrastructure",
)

SOURCE_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cs", ".go", ".java", ".js", ".jsx", ".kt",
    ".mjs", ".php", ".py", ".rb", ".rs", ".swift", ".ts", ".tsx",
}
IGNORED_PARTS = {
    ".git", ".next", ".turbo", ".venv", "build", "coverage",
    "dist", "node_modules", "out", "target", "__pycache__",
}


def has_application_source(repository: Path) -> bool:
    """Return true when a repository has a source file outside generated/vendor dirs."""
    for path in repository.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.name.endswith(".d.ts"):
            continue
        return True
    return False


def audit(root: Path) -> list[dict[str, str]]:
    """Return one deterministic readiness record for each canonical repository."""
    records = []
    for name in CANONICAL_REPOSITORIES:
        path = root / name
        if not path.is_dir():
            status = "missing"
        elif has_application_source(path):
            status = "source-present"
        else:
            status = "docs-or-config-only"
        records.append({"repository": name, "status": status})
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Directory containing repository checkout folders")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    records = audit(args.root)
    if args.format == "json":
        print(json.dumps(records, indent=2))
    else:
        print("| Repository | Readiness |")
        print("|---|---|")
        for record in records:
            print(f"| `{record['repository']}` | {record['status']} |")
        counts = {}
        for record in records:
            counts[record["status"]] = counts.get(record["status"], 0) + 1
        print("\nTotals: " + ", ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
