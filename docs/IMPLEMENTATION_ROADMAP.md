# Aether AI — Project-Wide Implementation Roadmap

**Current phase: Phase 0 — research and documentation. Do not start application coding until the documentation gate is explicitly reviewed.**

## Phase 0 — architecture and repository documentation

- [x] Create the first 10 Aether repositories.
- [x] Add initial repository-specific purpose and documentation structure.
- [x] Create master catalog and 33 individual repository specifications.
- [x] Structural audit of all 33 repository specifications; see [audit matrix](REPOSITORY_SPEC_AUDIT_MATRIX.md).
- [x] Verify all 10 existing repositories contain the required documentation and security review checklist.
- [ ] Resolve project name availability and final branding.
- [ ] Confirm license/SBOM approach and exact reused package versions.
- [x] Create proposed dependency matrix and identify likely cycle risks; [ ] accept the matrix and complete a formal package/service cycle review.
- [ ] Decide API style, runtime stack, database, queue, identity provider, model gateway strategy, and hosting through ADRs.
- [x] Create initial threat model mapped to OWASP GenAI LLM Top 10 2026 and component security checklists; [ ] approve retention, deletion, export, and telemetry policy.



### Phase 0 audit deliverables added on 2026-10-22

- [x] [Architecture audit pass 1 and 2](ARCHITECTURE_AUDIT.md)
- [x] [33-repository dependency matrix (proposed)](DEPENDENCY_MATRIX.md)
- [x] [Security threat model](SECURITY_THREAT_MODEL.md)
- [x] [Open decisions and official-source research](OPEN_DECISIONS_RESEARCH.md)
- [x] [Repository-specific security review checklists](repositories/)
- [ ] Final architecture decision review and explicit user approval before application coding

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

### Architecture research additions — 2026-10-22

- [x] Compare DIAL Core, DIAL Chat, DevKit gateway path and hybrid options in [DIAL adoption evaluation](DIAL_ADOPTION_EVALUATION.md).
- [x] Define a reproducible gateway proof-of-concept plan and acceptance tests in [GATEWAY_PROOF_OF_CONCEPT.md](GATEWAY_PROOF_OF_CONCEPT.md).
- [x] Inspect DevKit public package manifests and selected source-level integration boundaries in [DevKit compatibility review](DEVKIT_COMPATIBILITY_REVIEW.md).
- [ ] Verify exact registry package artifacts, integrity, exports and transitive licenses.
- [ ] Run a mock-based protocol compatibility harness for `@woho/mcp` against the selected official MCP spec/transport matrix.
- [ ] Run the gateway proof-of-concept and accept/reject ADR-0005 based on recorded evidence.

- [x] Research data-layer options and define tenant-isolation, durability, recovery and retrieval acceptance tests in [DATA_INFRASTRUCTURE_EVALUATION.md](DATA_INFRASTRUCTURE_EVALUATION.md).
- [ ] Confirm data residency, budget, RPO/RTO, expected tenant/corpus scale and retention requirements.
- [ ] Run representative database restore, vector retrieval, queue recovery and cache outage tests before accepting ADR-0007.
