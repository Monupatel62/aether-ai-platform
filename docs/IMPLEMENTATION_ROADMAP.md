# Aether AI — Project-Wide Implementation Roadmap

**Current phase: Phase 0 — research and documentation. Do not start application coding until the documentation gate is explicitly reviewed.**

## Phase 0 — architecture and repository documentation

- [x] Create the first 10 Aether repositories.
- [x] Add initial repository-specific purpose and documentation structure.
- [x] Create master catalog and 33 individual repository specifications.
- [ ] Verify every existing repository contains the complete documentation set.
- [ ] Resolve project name availability and final branding.
- [ ] Confirm license/SBOM approach and exact reused package versions.
- [ ] Review dependency graph for cycles and over-splitting.
- [ ] Decide API style, runtime stack, database, queue, identity provider, model gateway strategy, and hosting through ADRs.
- [ ] Review threat model, data retention, and user privacy requirements.

## Phase 1 — foundation vertical slice

Expected order: `aether-ai-platform` contracts → `aether-ai-security` and `aether-ai-auth` design → `aether-ai-providers` + `aether-ai-gateway` minimal model request → `aether-ai-api` authenticated endpoint → `aether-ai-web` minimal chat view → `aether-ai-observability` basics → `aether-ai-testing` smoke/contract tests.

Exit criteria: a single authorized user can make a model request through the backend with streaming/error handling, no browser secrets, tests, redacted telemetry, and documented local setup.

## Phase 2 — agent execution

Implement minimal agent/tool contracts, bounded run lifecycle, approval checkpoints, orchestration state machine, queue semantics, and run history. Integrate WoHo AI DevKit packages only after API/compatibility review. No autonomous high-impact actions without policy and approval.

Exit criteria: deterministic test agent can run with mock model/tools, enforce limits, emit trace/run IDs, cancel safely, and recover from simulated failures.

## Phase 3 — knowledge and files

Add secure file lifecycle, knowledge collections, indexing, search/RAG, citations, and deletion propagation. Use synthetic fixtures and tenant-isolation tests.

Exit criteria: authorized users can retrieve only permitted sources and responses include verifiable source references.

## Phase 4 — product controls

Add admin, billing/entitlements, plugin/integration registry, SDK, evaluations, enterprise controls, and UI component library as needed. Avoid creating runtime services solely to match repo names.

Exit criteria: API usage is metered from trusted server-side events; admin operations are authorized/audited; SDK/API versions are documented; eval regression gates exist.

## Phase 5 — release and operations

Container/deployment pipeline, infrastructure provisioning, monitoring/alerts, backups/restore, security review, SBOM, incident/rollback runbooks, and staged release.

Exit criteria: reproducible build, passing CI/security checks, successful staging smoke tests, documented rollback, and explicit release approval.

## Rule for moving phases

Do not move forward because files were created. Move only when the previous phase's acceptance criteria are evidenced in the work log and reviewed.
