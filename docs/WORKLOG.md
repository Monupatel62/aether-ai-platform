# Work log — aether-ai-platform

## 2026-10-22 — Documentation foundation

- Added repository purpose, project specification, architecture, dependency/contract policy, implementation gates, and research/license notes.
- No application source code, production configuration, infrastructure, or deployment was added.
- Reason: Aether AI is planned as a 33-repository ecosystem. Clear ownership and interfaces must be agreed before coding to prevent duplicate responsibilities, circular dependencies, and unsafe cross-service calls.
- Research references include the official AI DIAL repositories, the existing WoHo AI DevKit repository, and MCP documentation where relevant.
- Next: review this repo's contracts against the master catalog; resolve open choices in ADRs; only then begin the smallest testable implementation.

## Ongoing log format

For each future change, record: date; exact files; why the change is needed; alternatives considered; cross-repository connections affected; tests/evidence; security/privacy impact; known risks; follow-up work.

## Persistent decisions

- Aether AI is a proposed project name; verify GitHub/domain/trademark availability before public branding.
- WoHoTech remains a separate project.
- WoHo AI DevKit is a separate dependency and must not be rewritten as part of Aether AI.
- A planned repository is not automatically a separately deployed service.
- No coding starts until documentation and contracts are reviewed.

## 2026-10-22 — Technical design and navigation

- Added `docs/TECHNICAL_DESIGN.md` with repository-specific proposed internals, dependency connections, failure cases, and test plan.
- Added `docs/ENGINEERING_STANDARD.md` linking the project-wide code-commenting and engineering rules.
- Updated README documentation links so a new contributor can find the technical design and continuity handoff.
- No application source code was added; all changes in this phase are documentation-only.

## 2026-10-22 — Architecture and security audit pass 1

- Added `docs/SECURITY_REVIEW.md` with component-specific trust boundaries, threat scenarios, and verification checklist.
- Reviewed official MCP 2026-07-28 release notes, OWASP GenAI 2026 Top 10 announcement, OpenTelemetry GenAI conventions, GitHub Actions secure-use guidance, and AI DIAL Core documentation.
- Master audit and threat model are linked from the platform repository.
- No application code, production config, or security implementation was added; these are design requirements, not claims of implemented controls.

## 2026-10-22 — Architecture audit pass 2

- Enumerated all 33 individual repository specifications and checked required section coverage.
- Added missing security/privacy, test-plan, and related-documentation sections where the initial specs were inconsistent; rechecked all 33 and confirmed the required headings are present.
- Added a repository-specific security review checklist to each of the 10 existing repositories.
- Added the proposed 33-repository dependency matrix and clarified one-way ownership rules to avoid package/service cycles.
- Updated MCP research to the official 2026-07-28 spec and current TypeScript SDK v2/v1 support split; recorded OWASP 2026, OpenTelemetry GenAI privacy, and GitHub Actions supply-chain references.
- No application source code was written. No code tests, automated graph-cycle detection, SBOM, license scan, or penetration test was run.
- Next: review and accept the dependency matrix and resolve open runtime, provider, data, identity, and privacy decisions before implementation.

## 2026-10-22 — Architecture decision review and DevKit compatibility

- Inspected current WoHo AI DevKit `main` root/package manifests and selected MCP/agent source files. Recorded the declared package versions and source-level integration boundaries in `docs/DEVKIT_COMPATIBILITY_REVIEW.md`.
- Added `docs/DIAL_ADOPTION_EVALUATION.md` comparing DIAL Core, DevKit provider adapters, a hybrid gateway, and DIAL Chat as a complete product.
- Added `docs/GATEWAY_PROOF_OF_CONCEPT.md` defining 14 test scenarios, measurement requirements, and decision criteria for ADR-0005.
- Marked ADR-0003 (33 repositories) and ADR-0004 (repository boundaries do not imply 33 deployable services) accepted, consistent with the user's target and the architecture review.
- ADR-0005 remains open until the proof-of-concept is run; no gateway option has been selected.
- Updated gateway, agents, providers, MCP, and platform technical-design documents with the integration boundaries and links.
- No Aether application code was written. No DevKit code, version, main branch, or release pipeline was changed. No compatibility tests or proof-of-concept were run yet.

## 2026-10-22 — Data infrastructure research

- Added `docs/DATA_INFRASTRUCTURE_EVALUATION.md` with official-source research on PostgreSQL/RLS/PITR/full-text search, pgvector, Qdrant multitenancy, BullMQ retries/rate limiting, NATS JetStream durability/replay, and Valkey/Redis license considerations.
- Recorded a proposed baseline to benchmark: PostgreSQL as transactional source of truth; PostgreSQL full-text + pgvector for initial retrieval; BullMQ for Node.js background jobs; cache limited to reconstructible data. This is not an accepted production stack.
- Added ADR-0018 proposal for data-layer source-of-truth ownership and updated open-decision research, roadmap, handoff and continuity documents.
- Updated the 8 master repository specifications for database, queue, cache, search, RAG, orchestration, files and memory with concrete boundaries and acceptance tests.
- Key gates: RLS must be tested under non-owner runtime roles; queue consumers must be idempotent; vector/search indexes are rebuildable projections; tenant and ACL filters must be tested against revocation and deletion; cache must not authorize access or own durable records.
- No application code was written. No stack/vendor decision was accepted and no runtime benchmark or restore test was run.


## 2026-10-22 — Identity and tenant security research

- Added `docs/IDENTITY_AND_TENANT_SECURITY_EVALUATION.md` covering identity provider choices, OIDC/OAuth baseline, session lifecycle, authorization, tenant isolation, repository contracts, threat scenarios and POC acceptance criteria.
- Updated decision/research and continuity documentation to keep ADR-0008 and proposed ADR-0019–ADR-0024 open.
- No application code was added; no proof-of-concept tests were run.


## 2026-10-22 — Identity provider shortlist

- Added `docs/IDENTITY_PROVIDER_SHORTLIST_AND_SCORECARD.md` with official-source-based candidate comparison, weighted scorecard, POC phases, mandatory acceptance gates and migration checks.
- Updated handoff and architecture-decision notes. No vendor was selected and no POC tests or application code were run.


## 2026-10-22 — Browser session and authorization research

- Added `docs/BROWSER_SESSION_AND_AUTHORIZATION_ARCHITECTURE.md`, based on current IETF browser OAuth guidance and OWASP authorization/session guidance.
- Documented BFF/session options, CSRF defenses, tenant enforcement, authorization model trade-offs and POC acceptance tests.
- Updated handoff/decision documentation. No POC was run and no application code was written.


## 2026-10-22 — Authorization permission matrix

- Added `docs/AUTHORIZATION_PERMISSION_MATRIX.md` with proposed role matrix, resource/action vocabulary, tenant and service-principal invariants, policy decision contract and negative-test plan.
- Updated handoff and decision/research notes. Permissions remain draft; no code or tests were written/run.


## 2026-10-22 — Cross-repository consistency audit

- Reviewed the dependency matrix, structural audit matrix, authorization permission matrix, and selected repository specifications covering workflow validation, identity/security, queue, database, API/orchestration, knowledge/RAG/search, and enterprise controls.
- Added [CROSS_REPOSITORY_CONSISTENCY_AUDIT.md](CROSS_REPOSITORY_CONSISTENCY_AUDIT.md) with ten findings, severity, evidence, proposed corrections and implementation gates.
- Key mismatches: workflow dependency direction, identity/policy/enterprise ownership overlap, knowledge↔RAG dependency cycle risk, API→agents versus API→orchestration ambiguity, queue dependencies versus consumers, database/domain schema ownership, and overlapping ACL enforcement.
- No source code changed. No automated graph-cycle detector, build, integration/security test or POC was run. The graph is not certified cycle-free.


## 2026-10-22 — Dependency-boundary remediation

- Updated the master dependency matrix and 10 repository specifications following the cross-repository audit: workflows, API, knowledge, queue, database, auth, security, enterprise, RAG, Search and orchestration.
- Reconciled workflow schema direction, durable run ownership, knowledge-to-RAG/Search contract direction, queue producer/consumer semantics, database tooling/domain schema boundaries, and authentication/policy/enterprise ownership.
- Updated the consistency audit with remediation progress and remaining gates.
- No application code was written. Edge classification and automated package-cycle detection remain incomplete; no claim of cycle-free architecture is made. Tenant/workspace membership owner and ACL revocation/deletion targets remain open.


## 2026-10-22 — Typed dependency edge register and preliminary cycle check

- Added [DEPENDENCY_EDGE_REGISTER.md](DEPENDENCY_EDGE_REGISTER.md), classifying logical relationships as package imports, synchronous network APIs, asynchronous events/queues, generated/public artifacts, infrastructure provisioning, or documentation-only.
- Ran a DFS cycle detector over a manually transcribed candidate package graph: 33 nodes, 61 directed edges, zero cycles reported.
- Limitation: the graph was not generated from machine-readable edge data. The result is preliminary; normalize the register, generate the graph, rerun cycle detection, and review runtime call/event loops separately.
- Tenant/workspace membership ownership and ACL revocation/deletion consistency targets remain open. No application code was written.


## 2026-10-22 — Machine-readable package graph check

- Added `docs/dependency-package-graph.json` containing 33 proposed repository nodes and 61 typed package-import edges.
- Fetched the JSON back from GitHub, parsed it, validated edge types and node references, and ran DFS cycle detection against that parsed file: 0 directed cycles reported.
- Updated the edge register, cross-repository audit, handoff and roadmap with the result and limitations.
- This is a check of the proposed graph data, not source-import analysis. The next gate is reconciliation of JSON edges against the Markdown edge register and separate review of runtime API/event loops. No application code was written.


## 2026-10-22 — Tenant membership and ACL consistency design

- Added [TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md](TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md).
- Separated identity/session ownership, tenant membership/role grants, shared policy evaluation, resource ACLs, and search/RAG projections.
- Compared `aether-ai-enterprise` ownership against adding a dedicated `aether-ai-tenancy` repository; no owner chosen and the 33-repository scope was not changed.
- Defined fail-closed revocation invariants and POC tests for stale sessions, caches, queued jobs, search/vector indexes, citations, event replay and tenant suspension. Numeric cleanup targets remain open pending requirements and benchmarks.
- Documentation only; no implementation code or POC tests run.


## 2026-10-22 — Authorization policy gap audit

- Added [AUTHORIZATION_POLICY_GAP_AUDIT.md](AUTHORIZATION_POLICY_GAP_AUDIT.md) with 14 semantic findings, severity, impact and proposed disposition.
- Identified an internal contradiction in the workspace-creation row/footnote and unresolved high-risk policy around support access, admin access to conversation/memory content, ownership transfer, approval tiers and action-level permissions.
- Kept policy decisions open rather than treating draft matrix values as accepted. Documentation only; no application code or tests run.


## 2026-10-22 — Retention, deletion, export and telemetry policy proposal

- Added [DATA_RETENTION_DELETION_EXPORT_TELEMETRY_POLICY.md](DATA_RETENTION_DELETION_EXPORT_TELEMETRY_POLICY.md) covering data categories, proposed safe defaults, lifecycle semantics, exports, observability, backups and planned acceptance tests.
- Numeric retention periods and SLOs, legal hold, residency, export rights, backup recovery targets and telemetry retention remain undecided; no compliance claims are made.
- Documentation only; no code or tests were run.


## 2026-10-22 — Identity and authorization POC runbook

- Added [IDENTITY_AUTHORIZATION_POC_RUNBOOK.md](IDENTITY_AUTHORIZATION_POC_RUNBOOK.md) with 24 reproducible scenarios covering OIDC/PKCE, browser sessions, CSRF, tenant isolation, revocation, workload identity, RLS, support access, audit, privacy and lifecycle behavior.
- Defined hard security gates, measurement rules and weighted comparison template; no candidate scores are filled because no POC has run.
- POC execution remains gated on explicit user approval; no application code or tests were run.


## 2026-10-22 — Cross-repository contract audit

- Added [CROSS_REPOSITORY_CONTRACT_AUDIT.md](CROSS_REPOSITORY_CONTRACT_AUDIT.md), documenting contract maturity gaps, required machine-readable schemas, priority order and repository visibility evidence.
- Corrected `aether-ai-api/docs/DEPENDENCIES_AND_CONTRACTS.md`: durable runs go through orchestration; API no longer declares direct agents/database implementation dependencies.
- Corrected `aether-ai-workflows/docs/DEPENDENCIES_AND_CONTRACTS.md`: workflow schema/validation no longer declares runtime dependencies on orchestration, agents or database.
- Reconciled master catalog with connected GitHub listing: 20 canonical-name repositories visible, 10 documentation-populated and 10 empty; 13 planned canonical names not found in that listing. User reports 22; two additional names/URLs remain unreconciled.
- Documentation-only. No source code, API schemas, event schemas, CI or runtime tests were created/run.


## 2026-10-22 — Draft machine-readable contract schemas

- Added `docs/contracts/README.md` and six draft JSON Schema files: error envelope, event envelope, verified auth context, tool invocation, durable run event, and resource ACL/lifecycle change event.
- Parsed all six files as JSON after writing. This checks JSON syntax only; no JSON Schema validator, contract tests, API implementation, or runtime security tests were run.
- Kept schema status explicitly draft. The tenant-membership owner, authorization contract, API error catalog, retry/ordering semantics and public versioning policy remain open.
- Identifiers use the reserved `aether-ai.invalid` namespace to avoid implying a live product endpoint or coupling Aether to WoHoTech's domain.
- No application code or DevKit changes.


## 2026-10-22 — Contract semantic review and error-code proposal

- Added [SCHEMA_SEMANTIC_REVIEW.md](contracts/SCHEMA_SEMANTIC_REVIEW.md) documenting P0/P1 gaps in the six draft schemas, including optional tenant context, unconstrained tool/event payload objects, event-specific required fields, format assertion, and runtime invariants that JSON Schema cannot enforce.
- Added [ERROR_CODE_CATALOG.md](contracts/ERROR_CODE_CATALOG.md) with proposed public error identifiers and suggested HTTP/retry behavior.
- Updated the contract registry README with these draft artifacts and current limitations.
- No schema validator, OpenAPI validator, fixture suite, application code, or runtime security tests were run. Catalog and schemas remain unapproved.
- Next: resolve contract ownership/versioning and tenant/ACL/event semantics; then prepare a versioned OpenAPI baseline and valid/invalid fixtures for review. Keep implementation gated on explicit approval.


## 2026-10-22 — Draft versioned OpenAPI baseline

- Added [openapi.v1.yaml](contracts/openapi.v1.yaml), a provisional OpenAPI 3.1.0 baseline for health, synchronous text completion, durable run creation/status, and cancellation.
- Added [OPENAPI_V1_BASELINE.md](contracts/OPENAPI_V1_BASELINE.md) documenting provisional scope, security invariants, review blockers, and verification limits.
- Linked both artifacts from the contract registry README.
- Route names and fields are candidates for review, not approved or implemented endpoints. JWT bearer is a placeholder, not a selected identity design.
- No OpenAPI parser/validator, generated client, API implementation, contract fixtures, or runtime security tests were run.
- Next: review route scope and auth/tenant ownership, settle idempotency and lifecycle semantics, then validate OpenAPI and add positive/negative fixtures. Keep coding gated on explicit approval.


## 2026-10-22 — OpenAPI v1 semantic review

- Added [OPENAPI_V1_REVIEW_MATRIX.md](contracts/OPENAPI_V1_REVIEW_MATRIX.md) after manually reviewing the draft OpenAPI YAML.
- Flagged a P0 contract defect: the client request message schema permits system/developer roles, and the response reuses the same schema. The proposed remediation is to split request and response schemas and keep privileged instructions server-owned.
- Recorded further P0/P1 decisions around tenant resolution, agent-specific input schemas, run output authorization/retention, cancellation races, accepted response shapes, error-schema drift, limits, streaming and identity token validation.
- No OpenAPI parser/validator, generated client, endpoint implementation, or runtime security test was run. This is a manual design review, not evidence of a running exploit.
- Next: revise the draft schema after reviewing the role policy and endpoint semantics, then validate OpenAPI 3.1 and add negative contract fixtures. Documentation only; no implementation or DevKit changes.


## 2026-10-22 — OpenAPI message-role remediation and contract test plan

- Revised `contracts/openapi.v1.yaml` to separate `RequestChatMessage` and `ResponseChatMessage`; client messages are constrained to role `user`, generated messages to `assistant`. This addresses the previously identified schema-level P0 role issue in the draft.
- Added [OPENAPI_V1_CONTRACT_TEST_PLAN.md](contracts/OPENAPI_V1_CONTRACT_TEST_PLAN.md) with positive/negative message-role cases plus authorization, tenant isolation, idempotency, run revocation, cancellation, redaction, and limits scenarios.
- Updated [OPENAPI_V1_REVIEW_MATRIX.md](contracts/OPENAPI_V1_REVIEW_MATRIX.md) to record the draft correction and remaining validation requirements.
- No OpenAPI parser/validator, fixtures runner, generated client, endpoint implementation, or runtime security test was run. The correction is not yet validated.
- Next: validate OpenAPI 3.1, convert the plan into executable fixtures after review, and address remaining tenant/input/output/lifecycle decisions. Documentation only; no application code or DevKit changes.
