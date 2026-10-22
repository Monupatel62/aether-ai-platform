# Aether AI — Project-Wide Implementation Roadmap

**Current phase: Phase 0 — research and documentation. Do not start application coding until the documentation gate is explicitly reviewed.**

## Phase 0 — architecture and repository documentation

- [x] Create the first 10 Aether repositories.
- [x] Add initial repository-specific purpose and documentation structure.
- [x] Create master catalog and 33 individual repository specifications.
- [x] Structural audit of all 33 repository specifications; see [audit matrix](REPOSITORY_SPEC_AUDIT_MATRIX.md).
- [x] Inspect all 33 canonical repositories and synchronize their specification status/dependency sections.
- [x] Confirm the inspected default-branch trees are documentation-only; see [Implementation Status Audit](IMPLEMENTATION_STATUS_AUDIT.md).
- [ ] Verify each repository's full documentation checklist, README navigation, and repository-local relative links.
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
- [x] [Consolidated implementation gate blockers](IMPLEMENTATION_GATE_BLOCKERS.md)
- [ ] Final architecture decision review and explicit user approval before application coding


### Repository-tree and specification audit — 2026-10-23

- [x] Enumerate the recursive default-branch trees for all 33 canonical repositories; all trees returned without truncation and contained documentation only.
- [x] Synchronize `docs/REPOSITORY_SPECIFICATION.md` across all 33 repositories: current documentation-only status and a non-empty dependency section aligned with the proposed graph.
- [x] Scan the inspected Aether documentation/contracts for unrelated-project dependency markers and remove the remaining references.
- [x] Record evidence and limitations in [Implementation Status Audit](IMPLEMENTATION_STATUS_AUDIT.md).
- [ ] Finish semantic review of draft OpenAPI, event, authorization-context, and lifecycle contracts; close all P0 security/ownership blockers before implementation.
- [ ] Resolve remaining product/operations ADRs with explicit rationale and evidence. A proposed stack is not an accepted decision.

## Phase 1 — foundation vertical slice

Expected order: `aether-ai-platform` contracts → `aether-ai-security` and `aether-ai-auth` design → `aether-ai-providers` + `aether-ai-gateway` minimal model request → `aether-ai-api` authenticated endpoint → `aether-ai-web` minimal chat view → `aether-ai-observability` basics → `aether-ai-testing` smoke/contract tests.

Exit criteria: a single authorized user can make a model request through the backend with streaming/error handling, no browser secrets, tests, redacted telemetry, and documented local setup.

## Phase 2 — agent execution

Implement minimal agent/tool contracts, bounded run lifecycle, approval checkpoints, orchestration state machine, queue semantics, and run history. Use Aether-owned agent and tool contracts; external packages require an explicit architecture decision and compatibility review. No autonomous high-impact actions without policy and approval.

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

- [x] Define a reproducible gateway proof-of-concept plan and acceptance tests in [GATEWAY_PROOF_OF_CONCEPT.md](GATEWAY_PROOF_OF_CONCEPT.md).
- [ ] Verify exact registry package artifacts, integrity, exports and transitive licenses.
- [ ] Run the gateway proof-of-concept and accept/reject ADR-0005 based on recorded evidence.

- [x] Research data-layer options and define tenant-isolation, durability, recovery and retrieval acceptance tests in [DATA_INFRASTRUCTURE_EVALUATION.md](DATA_INFRASTRUCTURE_EVALUATION.md).
- [ ] Confirm data residency, budget, RPO/RTO, expected tenant/corpus scale and retention requirements.
- [ ] Run representative database restore, vector retrieval, queue recovery and cache outage tests before accepting ADR-0007.


## Research checkpoint — identity and tenant security (2026-10-22)

Completed the documentation evaluation for authentication, identity, sessions, authorization, multi-tenancy and repository boundaries. The evaluation document is `docs/IDENTITY_AND_TENANT_SECURITY_EVALUATION.md`.

Next gate: compare managed and self-hosted OIDC options and define the proof-of-concept scorecard; resolve the related open ADRs before implementation. No application code was written and no POC results are claimed.


## Research checkpoint — identity-provider shortlist (2026-10-22)

Added `docs/IDENTITY_PROVIDER_SHORTLIST_AND_SCORECARD.md`, which defines candidate options and a common proof-of-concept scorecard. Next gate is evidence collection via equivalent tests, pricing/plan confirmation, operations review and migration rehearsal. ADR-0008 remains open; no provider has been selected and no implementation has begun.


## Research checkpoint — browser session and authorization architecture (2026-10-22)

Added `docs/BROWSER_SESSION_AND_AUTHORIZATION_ARCHITECTURE.md`. It evaluates the browser BFF/session approach and an RBAC + resource-level authorization baseline, with CSRF, tenant enforcement and session revocation requirements. Next gate: review the proposed architecture and align it with the identity-provider shortlist before running a POC. ADR-0019/0020 remain open; no code or tests have been run.


## Research checkpoint — authorization permission matrix (2026-10-22)

Added `docs/AUTHORIZATION_PERMISSION_MATRIX.md`. It defines a proposed role/action matrix, mandatory invariants and testable negative cases. The next gate is a semantic audit of permissions against all protected resource classes and the repository contracts; product-owner approval is still required. No application code or POC tests have been run.


## Cross-repository consistency gate — 2026-10-22

- [x] Perform manual consistency review across the dependency matrix, all 33 spec headings, and selected high-risk repository contracts.
- [x] Record findings and proposed remediations in [CROSS_REPOSITORY_CONSISTENCY_AUDIT.md](CROSS_REPOSITORY_CONSISTENCY_AUDIT.md).
- [ ] Reconcile workflow, auth/security/enterprise, knowledge/RAG, API/orchestration/agents, queue, database/domain-schema, and search/RAG ACL boundaries.
- [ ] Type every dependency edge (package import, network API, event, generated artifact, infrastructure, documentation).
- [ ] Run and record automated cycle detection on the explicit package-import graph; separately review runtime call loops.
- [ ] Resolve tenant/workspace membership ownership and resource ACL/revocation authority before implementation.

The manual review is not an automated cycle check. Do not advance to application implementation until the open findings are dispositioned and the user explicitly approves.


### Consistency-audit remediation update — 2026-10-22

- [x] Reconcile workflow schema dependencies and durable execution ownership.
- [x] Align API durable runs with orchestration and remove direct agent-runtime dependency from the API specification.
- [x] Align knowledge/RAG/Search ownership and describe indexes as projections rather than permission authorities.
- [x] Clarify queue producer/consumer direction and database tooling versus domain schema ownership.
- [x] Separate authentication/session lifecycle from resource authorization and narrow security package dependencies.
- [x] Clarify enterprise membership/role ownership as unresolved pending ADR-0021.
- [ ] Classify every matrix edge as package import, synchronous API, event/queue, generated artifact, infrastructure, or documentation-only.
- [ ] Run automated cycle detection on an explicit package-import graph and record evidence; separately review runtime call/event loops.
- [ ] Resolve membership/role-grant ownership and ACL revocation/deletion targets.

See [Cross-Repository Consistency Audit](CROSS_REPOSITORY_CONSISTENCY_AUDIT.md). Documentation corrections reduce known conflicts but do not prove the graph is cycle-free.


### Dependency edge register and preliminary graph check — 2026-10-22

- [x] Create [DEPENDENCY_EDGE_REGISTER.md](DEPENDENCY_EDGE_REGISTER.md) with proposed edge types and explicit cycle-prevention non-edges.
- [x] Run a preliminary DFS cycle detector on a manually transcribed candidate package graph: 33 nodes, 61 edges, 0 cycles reported.
- [ ] Normalize the register into machine-readable data and generate the graph directly from it.
- [ ] Repeat cycle detection against generated graph data and retain reproducible evidence.
- [ ] Review runtime synchronous call loops and asynchronous event feedback loops separately.

The preliminary result does not prove the Markdown edge register is complete or the runtime architecture cycle-free. Implementation remains gated on these checks and explicit user approval.


### Machine-readable package graph verification — 2026-10-22

- [x] Add [dependency-package-graph.json](dependency-package-graph.json) as the proposed machine-readable package-import graph.
- [x] Fetch the JSON from GitHub, parse it, validate 33 nodes and 61 typed package-import edges, and run DFS cycle detection: **0 cycles reported in the encoded candidate graph**.
- [ ] Compare the JSON graph against every typed relationship in [DEPENDENCY_EDGE_REGISTER.md](DEPENDENCY_EDGE_REGISTER.md), record intentional differences, and review runtime API/event loops.
- [ ] Before implementation, validate the graph against actual source imports/build manifests once packages exist; keep proposed-graph checks separate from code-derived checks.

This result only establishes that the proposed JSON graph has no cycles; it does not establish that future or existing source imports conform to it.


### Tenant membership and ACL consistency gate — 2026-10-22

- [x] Compare tenant/workspace membership ownership options and record recommendation/risks in [TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md](TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md).
- [x] Specify revocation safety invariants and POC failure cases across API, sessions, workers, caches, files, search/RAG indexes and citations.
- [ ] Product owner confirms universal tenant-domain ownership versus an approved change to the 33-repository plan.
- [ ] Approve retention/deletion semantics and numeric projection-cleanup SLOs after workload requirements and benchmarks are available.
- [ ] Run identity/authorization POC only after explicit approval; no code or POC was run in this checkpoint.


### Cross-repository contract audit — 2026-10-22

- [x] Audit dependency contract prose against master dependency matrix.
- [x] Correct API → orchestration → agents durable-run contract and remove workflow runtime dependencies on orchestration/agents/database.
- [x] Reconcile master catalog with connected GitHub repository visibility; see [CROSS_REPOSITORY_CONTRACT_AUDIT.md](CROSS_REPOSITORY_CONTRACT_AUDIT.md).
- [ ] Confirm the two additional repositories reported by the user by name/URL.
- [ ] Populate documentation in existing empty repositories after identity/status is confirmed.
- [ ] Draft P0 machine-readable API, authorization, tool invocation, durable run/event, and source ACL/deletion schemas; no schemas or tests were created in this audit.


### Draft machine-readable contract schemas — 2026-10-22

- [x] Add draft JSON Schemas for error envelope, event envelope, verified auth context, tool invocation, durable run events and resource ACL/lifecycle events.
- [x] Parse the six files as JSON after writing.
- [ ] Run a JSON Schema Draft 2020-12 validator and add valid/invalid fixtures after the contract semantics are reviewed.
- [ ] Approve membership/ACL ownership and versioning policy before treating schemas as stable.
- [ ] Draft the canonical versioned OpenAPI baseline and stable error-code catalog.
- Note: JSON parsing is not schema validation, contract testing, or runtime security verification.


### Contract semantic review checkpoint — 2026-10-22

- [x] Record semantic gaps and runtime-only invariants in [SCHEMA_SEMANTIC_REVIEW.md](contracts/SCHEMA_SEMANTIC_REVIEW.md).
- [x] Add proposed public codes and HTTP/retry mappings in [ERROR_CODE_CATALOG.md](contracts/ERROR_CODE_CATALOG.md).
- [x] Link draft artifacts from the contract registry README.
- [ ] Resolve tenant-context requirements, tool argument bounds, event-specific required fields, ordering/replay/idempotency semantics, and contract owners/versioning.
- [ ] Draft and review the versioned OpenAPI baseline.
- [ ] Run a Draft 2020-12 validator with format assertions and add positive/negative fixtures after semantics are agreed.

These additions remain documentation proposals. No schema validation, runtime tests, or application implementation occurred in this checkpoint.


### Draft OpenAPI v1 baseline checkpoint — 2026-10-22

- [x] Add provisional OpenAPI 3.1.0 document for health, text completion, durable run creation/status, and cancellation in [openapi.v1.yaml](contracts/openapi.v1.yaml).
- [x] Record scope, security constraints, unresolved decisions, and validation limits in [OPENAPI_V1_BASELINE.md](contracts/OPENAPI_V1_BASELINE.md).
- [x] Link the baseline from the contract registry README.
- [ ] Review route surface, endpoint ownership, identity/tenant authorization, limits, idempotency, run lifecycle, and cancellation semantics.
- [ ] Run an OpenAPI 3.1 validator and add positive/negative contract fixtures after review.

This baseline is documentation-only. No API endpoint or runtime behavior is implemented or verified.


### OpenAPI semantic review checkpoint — 2026-10-22

- [x] Manually review the draft OpenAPI and record P0/P1 findings in [OPENAPI_V1_REVIEW_MATRIX.md](contracts/OPENAPI_V1_REVIEW_MATRIX.md).
- [x] Identify client-supplied system/developer roles as a P0 contract defect requiring separate request/response message schemas.
- [ ] Review and remediate message-role policy, trusted tenant resolution, agent input schemas, run result authorization/retention, and cancellation semantics.
- [ ] Define accepted/cancellation response bodies, endpoint limits, streaming policy, and token-validation rules.
- [ ] Run OpenAPI 3.1 validation and add positive/negative contract fixtures after decisions are reviewed.

Manual text review only; no OpenAPI parser or runtime security test has been run.


### OpenAPI message-role remediation checkpoint — 2026-10-22

- [x] Replace the shared chat message schema with separate request and response schemas in the draft OpenAPI.
- [x] Constrain client request message role to `user` and generated response message role to `assistant` in the draft contract.
- [x] Add [OPENAPI_V1_CONTRACT_TEST_PLAN.md](contracts/OPENAPI_V1_CONTRACT_TEST_PLAN.md) and record remediation in the review matrix.
- [x] Add provisional response schemas for accepted run creation and cancellation, with explicit acknowledgement semantics.
- [ ] Validate the OpenAPI document with a parser/validator; these changes have not yet been validated.
- [ ] Implement positive/negative contract fixtures only after review and explicit approval; no runtime tests have run.
- [ ] Resolve remaining tenant, agent-input, output-retention, cancellation, limits, streaming, and identity decisions.

Documentation-only correction; no implementation or security certification is implied.
