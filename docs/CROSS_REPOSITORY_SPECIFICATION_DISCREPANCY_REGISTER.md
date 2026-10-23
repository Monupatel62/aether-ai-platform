# Cross-Repository Specification Discrepancy Register

**Review date:** 2026-10-23  
**Scope:** Review of the 32 non-platform `docs/REPOSITORY_SPECIFICATION.md` files, compared with the platform catalog and cross-repository decision documents. Documentation-only audit.

## Executive result

All 32 non-platform repository specifications were fetched successfully. Each contains sections covering dependencies, owned capabilities, contracts, security/privacy, tests, and implementation gates, although headings differ. This confirms document structure, not that contracts are executable or implementation is complete.

## Findings

| ID | Severity | Area | Finding | Required follow-up |
|---|---|---|---|---|
| SPEC-001 | High | Auth / Enterprise / Platform | Canonical tenant/workspace membership authority remains undecided. Auth owns identity/session primitives; Enterprise lists tenant controls, but research explicitly says Auth is not automatically membership authority. | Name one authoritative owner in an accepted contract/ADR; define source of truth, membership versioning and revocation propagation. |
| SPEC-002 | High | Agents / Orchestration / API | Agents owns an agent state machine; Orchestration owns the single authoritative durable run/step state machine; API must not create a second durable execution state machine. | Define agent-local lifecycle versus durable run/step state; test transitions, cancellation, recovery, retries and idempotency. |
| SPEC-003 | High | Auth / Security / API / Gateway / Tools | Authorization responsibilities span identity/session primitives, shared policy, API checks, gateway quotas and tool scopes. Decision authority and enforcement points need an explicit contract. | Define authoritative policy decision, trusted authorization context, enforcement responsibilities, stale-context handling and fail-closed behavior. |
| SPEC-004 | High | Files / Knowledge / RAG / Search / Database | Source metadata, indexing state, retrieval projections and deletion/revocation span multiple owners. Architecture requires access denial immediately on revocation, while projection cleanup may be asynchronous. | Define source owner, event/version contract, tombstones, replay semantics and tests across queues, caches, RAG and search. |
| SPEC-005 | Medium | API / Orchestration / Queue / Database | Durable submission, queue delivery, outbox and idempotency are described across specs, but crash-consistency requires a cross-repository contract. | Specify crash-after-commit, duplicate/out-of-order event, cancellation-race and recovery tests. |
| SPEC-006 | Medium | Web / API / SDK | Web consumes generated SDK types while API owns OpenAPI. Generation source, compatibility policy, release order and breaking-change gate need one process. | Define authoritative schema, deterministic generation, compatibility checks and consumer smoke tests. Do not assume the pipeline exists. |
| SPEC-007 | Medium | Gateway / Providers | Gateway owns normalized routing/streaming/cancellation; Providers owns adapters/capabilities. Provider and fallback policy remain open; external gateway is not approved. | Define provider-neutral capability, error and stream contracts before comparing options. |
| SPEC-008 | Medium | Workflows / Orchestration | Workflows owns schema validation, not execution; Orchestration owns retries, cancellation, idempotency and durable execution. | Preserve this boundary in the dependency matrix and tests. |
| SPEC-009 | Medium | Observability / Security / Memory / Files / Database | Telemetry, redaction, retention, deletion, export and backups need consistent policy. ADR-0012/0015 remain unresolved; no numeric retention duration is approved. | Define data classification and redaction contract; do not claim deletion SLAs or compliance without approval and evidence. |
| SPEC-010 | Medium | Queue / Cache / Database / Search | Infrastructure choices remain candidates. Logical dependencies must not be mistaken for selected vendors or separate network services. | Type edges as package, in-process, network, event or test-only; distinguish candidates from accepted choices. |
| SPEC-011 | Medium | Integrations / MCP / Plugins / Tools | Connector, MCP, plugin and tool manifests overlap around credentials, permissions, approvals and invocation. | Define manifest mapping, trust lifecycle, secret references, scopes, invocation envelope and compatibility. |
| SPEC-012 | Medium | Deployment / Infrastructure / Platform | Deployment owns packaging/release/rollback while Infrastructure owns provisioning/networking/managed services. Promotion and rollback boundaries need clarity. | Define environment ownership, secret/config sources, artifact provenance, migration ordering and operational handoff. |
| SPEC-013 | Medium | Testing / All repositories | The Testing repo owns shared fixtures and contract/integration/smoke tests, but this document review does not prove that acceptance criteria are executable or wired into required CI. | Map each contract to a test, owner and CI workflow before implementation approval. |
| SPEC-014 | Low | All specifications | Heading names vary across specs. Broad topics are present, but variation complicates automated parsing. | Add a small machine-readable metadata header/schema; avoid broad rewrites for style alone. |
| SPEC-015 | Medium | Search / Dependency matrix | Prior reconciliation noted that Search specifies a Database dependency for neutral metadata contracts, while the matrix does not clearly represent the edge. | Decide whether this is a direct dependency or logical/data-ownership relationship; type it consistently in both documents. |
| SPEC-016 | High | Implementation gate | Specifications are documentation, not proof of executable implementation, CI enforcement, secure runtime behavior or production readiness. | Keep implementation gated until P0 contracts/ADRs are accepted or reviewed as deferred, validators/fixtures pass and the user authorizes implementation. |

## Audit method and limitations

- Fetched all 32 non-platform repository specifications from their GitHub default branches.
- Checked section structure and inspected key ownership/dependency/contract sections for Web, API, Gateway, Providers, Agents, Workflows, Orchestration and Tools.
- Compared findings with platform catalog and identity, authorization, lifecycle, gateway and infrastructure decision documents.
- This was a manual consistency pass, not an exhaustive automated semantic comparison of every line in all 32 specifications.
- No application build, runtime, penetration, integration or deployment tests were run.

## Recommended next actions

1. Resolve tenant-membership authority and authorization-context contracts first.
2. Add a machine-readable repository metadata/contract manifest and validate it against the central dependency matrix.
3. Define cross-repository tests for durable run lifecycle, authorization revocation and knowledge/search deletion.
4. Keep vendor, topology, retention and identity choices open until required evidence and approvals exist.
