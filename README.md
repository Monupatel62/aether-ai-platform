# aether-ai-platform

> **Status: Documentation phase.** No application code or production deployment has been started in this repository.

## Purpose

Canonical architecture, product vision, cross-repository contracts, ADRs, and roadmap for the Aether AI ecosystem.

## Responsibility boundary

System-of-record for architecture and repository specifications.

## Dependencies

None at runtime; references the Aether AI repositories only.

## Project rules

- Aether AI is a standalone project with its own repositories, architecture, branding, and roadmap.
- Do not assume dependencies on external projects; add one only after an explicit architecture decision and compatibility review.
- No implementation starts until the documentation and cross-repository contracts are reviewed.
- Do not commit secrets, API keys, user data, or production credentials.
- Public interfaces, security decisions, and non-obvious implementation choices must be documented.

## Documentation

- [Project specification](docs/PROJECT_SPEC.md)
- [Architecture and connections](docs/ARCHITECTURE.md)
- [Dependencies and contracts](docs/DEPENDENCIES_AND_CONTRACTS.md)
- [Implementation plan and acceptance criteria](docs/IMPLEMENTATION_PLAN.md)
- [Research and license notes](docs/RESEARCH_AND_LICENSES.md)
- [Repository-specific technical design and test plan](docs/TECHNICAL_DESIGN.md)
- [Repository-specific security review checklist](docs/SECURITY_REVIEW.md)
- [Engineering and commenting standard](docs/ENGINEERING_STANDARD.md)
- [Work log and decisions](docs/WORKLOG.md)
- [Master 33-repository catalog](https://github.com/Monupatel62/aether-ai-platform/blob/main/docs/REPOSITORY_CATALOG.md)
- [Dependency matrix](docs/DEPENDENCY_MATRIX.md)
- [Architecture audit](docs/ARCHITECTURE_AUDIT.md)
- [Security threat model](docs/SECURITY_THREAT_MODEL.md)
- [Open decisions and research](docs/OPEN_DECISIONS_RESEARCH.md)
- [Continuity handoff for new chats](https://github.com/Monupatel62/aether-ai-platform/blob/main/docs/WORK_HANDOFF.md)

## Before coding

Read the project specification, architecture, contracts, implementation plan, and work log. Update the docs in the same change whenever behavior, an API contract, a dependency, or a security boundary changes.
