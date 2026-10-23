# Aether AI — Current Work Handoff

**Last updated:** 2026-10-22

## User intent and hard constraints

- Plan 33 Aether AI repositories. The first 10 have been created; 23 remain planned.
- Documentation first. Do not start application coding until the full docs and dependency contracts are reviewed.
- Every component needs a clear purpose, scope, connections, APIs/contracts, implementation order, license notes, and work log.
- Explain non-obvious code choices with comments when coding eventually begins; comments must explain why/invariants, not repeat syntax.

## Repository state

**Latest connected GitHub check (2026-10-22):** 27 canonical-name Aether AI repositories are visible. Twenty-two have documentation foundations; five remain empty on the default branch. Six canonical names are not found. The earlier user-reported count of 22 is superseded by this current listing; reconcile any noncanonical repository names separately.

### Repositories with documentation foundations (22)

1. `aether-ai-platform` — master architecture, ADRs, roadmap and contracts.
2. `aether-ai-web`
3. `aether-ai-api`
4. `aether-ai-gateway`
5. `aether-ai-providers`
6. `aether-ai-agents`
7. `aether-ai-workflows`
8. `aether-ai-orchestration`
9. `aether-ai-tools`
10. `aether-ai-mcp`
11. `aether-ai-deployment`
12. `aether-ai-docs`
13. `aether-ai-database`
14. `aether-ai-queue`
15. `aether-ai-cache`
16. `aether-ai-search`
17. `aether-ai-plugins`
18. `aether-ai-rag`
19. `aether-ai-files`
20. `aether-ai-knowledge`
21. `aether-ai-auth`
22. `aether-ai-security`

The twelve repositories added in the latest documentation passes have README plus project specification, architecture, dependencies/contracts, implementation plan, technical design, security review, research/licenses, engineering standard and work log. This is documentation only, not implementation evidence.

### Existing repositories still empty on the default branch (5)

`aether-ai-admin`, `aether-ai-billing`, `aether-ai-sdk`, `aether-ai-evaluations`, `aether-ai-observability`.

### Canonical repositories not found in the latest listing (6)

`aether-ai-memory`, `aether-ai-integrations`, `aether-ai-testing`, `aether-ai-ui-components`, `aether-ai-enterprise`, `aether-ai-infrastructure`.

Create no new repositories without explicit approval. Continue documentation-first work in existing repositories and do not start application coding until the full docs and dependency contracts are reviewed.

## Master docs

- [Repository catalog](REPOSITORY_CATALOG.md)
- [Dependency matrix](DEPENDENCY_MATRIX.md)
- [Repository specification audit matrix](REPOSITORY_SPEC_AUDIT_MATRIX.md)
- [Architecture audit](ARCHITECTURE_AUDIT.md)
- [Security threat model](SECURITY_THREAT_MODEL.md)
- [Open decisions and research](OPEN_DECISIONS_RESEARCH.md)
- [Individual spec index](REPOSITORY_SPEC_INDEX.md)
- [Engineering and commenting standard](ENGINEERING_AND_COMMENTING_STANDARD.md)
- [Master architecture](MASTER_ARCHITECTURE.md)
- [Implementation roadmap](IMPLEMENTATION_ROADMAP.md)
- [Decision log](DECISION_LOG.md)
- [Research/license register](RESEARCH_AND_LICENSES.md)
- [Engineering/commenting standard](ENGINEERING_AND_COMMENTING_STANDARD.md)
- [Continuity guide](CONTINUITY_GUIDE.md)


## Research notes

- AI DIAL Core official repository: https://github.com/epam/ai-dial-core. Its README describes a unified API/proxy for chat-completion and embedding models/apps, Java 21 + Vert.x; repository has Apache-2.0 LICENSE.
- AI DIAL Chat: https://github.com/epam/ai-dial-chat. Current architecture describes React/TypeScript frontend and NestJS backend-for-frontend; inspect file-level license notices before reuse.
- MCP specification: https://modelcontextprotocol.io/.

## Next work

1. Verify every existing Aether repository has all 8 expected docs and cross-links.
2. Verify the 33 individual repo specs are complete and consistent with the catalog.
3. Review for circular dependencies, duplicate ownership, and unnecessary service boundaries.
4. Resolve open ADRs (name/branding, stack, database, queue, identity provider, model gateway strategy, data retention, deployment).
5. Only after documentation review and user approval, start Phase 1 coding.

## Explicit no-go items until approved

- No application code, no provider secrets, no production deployment, no billing integrations, and no automatic high-impact tools.
- Do not claim the project is implemented or production-ready; it is still in the documentation phase.

## Latest audit update — 2026-10-22

- Added [Architecture audit](ARCHITECTURE_AUDIT.md), [Security threat model](SECURITY_THREAT_MODEL.md), and [Open decisions research](OPEN_DECISIONS_RESEARCH.md).
- OWASP GenAI announced its 2026 LLM Top 10 in September 2026. Update the security control/test matrix to that edition.
- OpenTelemetry GenAI attributes can contain sensitive data; telemetry must be metadata-only by default.
- GitHub recommends full-length commit SHA pins for immutable Action references (or an approved dependency lockfile approach).
- No application code has been written. The next work remains documentation audit and architecture decision closure.

## Documentation audit pass 2 — 2026-10-22

- Verified all 33 individual repository specs exist under `docs/repositories/` and all include the required mission, dependency, security/privacy, test-plan, implementation-gate, and related-doc sections.
- Added [Dependency Matrix](DEPENDENCY_MATRIX.md), including cycle-prevention rules for MCP/tools, knowledge/RAG, API/orchestration/agents, billing/usage, plugins/admin, and enterprise/admin.
- Added a component-specific `docs/SECURITY_REVIEW.md` to each of the 10 existing Aether repositories.
- This validates document presence and consistency only. It is not a code audit, automated cycle proof, legal review, SBOM, or penetration test.
- Next: review and accept the dependency matrix through ADRs, resolve runtime boundaries and open decisions, then ask the user to approve the transition to implementation.

- The security threat model now maps all ten official OWASP GenAI LLM Top 10 2026 categories by name to Aether components and required tests. Pair it with OWASP's Top 10 for Agentic Applications and Agent Control Standard.

## Architecture decision review — 2026-10-22

- Added [Gateway proof-of-concept plan](GATEWAY_PROOF_OF_CONCEPT.md) with 14 test scenarios, measurement requirements, and decision rules. It is a plan only; no gateway code has been created.

- Added [Data Infrastructure Evaluation](DATA_INFRASTRUCTURE_EVALUATION.md): PostgreSQL/pgvector, Qdrant, BullMQ, NATS JetStream, Valkey-compatible cache, and dedicated search alternatives, with acceptance tests and unresolved operational decisions.
- ADR-0007 remains open. The proposed initial benchmark baseline is PostgreSQL + pgvector/full-text, BullMQ, and a cache limited to reconstructible data; no production vendors are selected.


## Current stage — identity and tenant security research (2026-10-22)

Read `docs/IDENTITY_AND_TENANT_SECURITY_EVALUATION.md` next. It documents the identity-provider comparison criteria, OIDC/OAuth safety baseline, tenant-aware authorization model, session lifecycle, repository responsibilities, threat scenarios and POC acceptance tests.

Hard constraints remain: documentation/research only; do not write application code or choose a vendor until the comparison and explicit review are complete. ADR-0008 remains open; ADR-0019 through ADR-0024 are proposed open decisions. POC tests listed in the document are planned, not executed.


## Latest identity-provider research checkpoint — 2026-10-22

Read `docs/IDENTITY_PROVIDER_SHORTLIST_AND_SCORECARD.md`. A shortlist and weighted scorecard now compare ZITADEL, Keycloak and Auth0. Treat this as candidate research only: no vendor selected, no POC executed, no code written. Next work should test the same OIDC/PKCE, tenant-isolation, revocation, audit, operations and migration scenarios across candidates, then record evidence and costs before deciding ADR-0008.


## Latest architecture research checkpoint — browser sessions and authorization (2026-10-22)

Read `docs/BROWSER_SESSION_AND_AUTHORIZATION_ARCHITECTURE.md`. It evaluates BFF/server-side sessions, CSRF and cookie controls, session lifecycle, RBAC/resource-level checks, alternatives, repository boundaries and POC tests. BFF and RBAC are candidates only, not accepted decisions. No application code or POC tests were run. Keep ADR-0019 and ADR-0020 open pending review.


## Latest research checkpoint — authorization permission matrix (2026-10-22)

Read `docs/AUTHORIZATION_PERMISSION_MATRIX.md`. It proposes roles, resource classes, action vocabulary, baseline permissions, mandatory invariants, repository ownership and a POC test plan. Treat all permissions as draft product policy requiring review; none are implemented. Next: refine first-launch resources and risk tiers, then define revocation/consistency targets and turn the negative cases into POC tests after architecture review. Do not start application code without explicit approval.


## Latest checkpoint — cross-repository consistency audit (2026-10-22)

Read [Cross-Repository Consistency Audit](CROSS_REPOSITORY_CONSISTENCY_AUDIT.md) before further architecture work. The manual review found conflicts in workflow dependencies, auth/security/enterprise ownership, knowledge↔RAG direction, API→agent execution, queue dependency direction, database/domain schema ownership, ACL enforcement across search/RAG/knowledge, and overly broad security dependencies. It also found that repository edges are not consistently typed as package/API/event/artifact/infrastructure/docs.

This is a documentation-level review only. No automated cycle detector, build, runtime test, or security test was run. Do not claim the graph is cycle-free. Next: reconcile the affected specs and dependency matrix, preserve open ADRs, type the graph edges, and only then run an explicit graph check. Application coding remains blocked until documentation review and explicit user approval.


## Remediation checkpoint — cross-repository consistency (2026-10-22)

Committed coordinated documentation corrections to the dependency matrix and affected specs: workflows, API, knowledge, queue, database, auth, security, enterprise, RAG, Search and orchestration. The audit document records which contradictions were addressed and what remains open.

Still required: type every dependency edge, construct separate package-import and runtime-call/event graphs, run and record automated package-cycle detection, and decide the canonical tenant/workspace membership/role-grant owner plus ACL revocation/deletion consistency targets. The graph is not certified cycle-free. Documentation-only work continues; no application code without explicit approval.


## Latest checkpoint — typed dependency edges (2026-10-22)

Added [DEPENDENCY_EDGE_REGISTER.md](DEPENDENCY_EDGE_REGISTER.md), with proposed classifications for package imports, synchronous API calls, events/queues, generated artifacts, infrastructure provisioning and documentation-only relationships. A preliminary DFS check over a manually transcribed candidate package graph reported 0 cycles across 33 nodes and 61 edges. Because the graph was not generated from a machine-readable register, this is preliminary evidence only. Next: normalize the edge register to machine-readable data, generate and rerun cycle detection, then separately review runtime call/event loops. Tenant/workspace membership ownership and ACL revocation/deletion targets remain open. No application code without explicit approval.


## Latest checkpoint — machine-readable package graph verified (2026-10-22)

Created [dependency-package-graph.json](dependency-package-graph.json) and fetched it back from GitHub. The JSON was parsed, its 33 nodes and 61 package-import edges were validated, and a DFS cycle detector reported **0 cycles in the proposed encoded graph**. See [Dependency Edge Register](DEPENDENCY_EDGE_REGISTER.md) and [Cross-Repository Consistency Audit](CROSS_REPOSITORY_CONSISTENCY_AUDIT.md).

This is a check of the proposed graph data, not a scan of actual source imports. Next: compare each JSON edge against the typed Markdown register, record intentional differences, and review runtime API/event loops. Tenant/workspace membership ownership and ACL revocation/deletion targets remain open. No application code without explicit approval.


## Latest verification — dependency register reconciled (2026-10-22)

Compared [DEPENDENCY_EDGE_REGISTER.md](DEPENDENCY_EDGE_REGISTER.md) with [dependency-package-graph.json](dependency-package-graph.json): 61 internal package-import edges match exactly, with no duplicates, missing edges or extras. Five external backend/library/test-fixture relationships are intentionally excluded from the internal graph. Re-running DFS on the latest fetched JSON reported 0 cycles. This verifies consistency of the proposed docs graph only; actual source imports and runtime API/event loops are not verified. Remaining product decisions include tenant/workspace membership ownership and ACL revocation/deletion targets.


## Latest checkpoint — tenant membership and ACL consistency (2026-10-22)

Read [Tenant Membership, Resource ACL and Revocation Consistency Decision](TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md). It compares three membership-owner options and defines the safety contract for revoking access across API reads, files, queues/workers, caches, search/RAG indexes, chunks and citations. The preferred candidate is `aether-ai-enterprise` only if it is intended to be the universal tenant domain; otherwise a dedicated `aether-ai-tenancy` repo would change the approved 33-repo scope and requires explicit approval. No owner or numeric projection-cleanup SLO has been accepted. Immediate protected-operation denial must rely on authoritative re-authorization, never on eventual index/cache cleanup.

**Next:** confirm the tenant/workspace product model and membership owner; review the draft permission matrix; define data retention/deletion requirements and realistic freshness/availability targets; then plan the identity/authorization POC. Continue documentation/research only. Do not write application code or create another repository without explicit approval.


## Latest checkpoint — authorization policy gap audit (2026-10-22)

Read [Authorization Policy Gap Audit](AUTHORIZATION_POLICY_GAP_AUDIT.md) before implementation planning. The semantic review found 14 gaps, including an inconsistency between the Member workspace-creation cell and its default-deny footnote; the missing Support Operator role in the matrix; ambiguous tenant-admin access to conversation/memory content; incomplete ownership-transfer and grant-ceiling rules; broad action bundles; and undefined high-risk approval tiers. These are not accepted decisions. Next, review the high-severity findings, approve/reject proposed clarifications, then revise the matrix and repository contracts. Data retention/deletion, audit policy and ADR-0020–0024 remain open. No code/tests were run; do not start implementation without explicit approval.


## Latest checkpoint — retention, deletion, export and telemetry policy (2026-10-22)

Read [DATA_RETENTION_DELETION_EXPORT_TELEMETRY_POLICY.md](DATA_RETENTION_DELETION_EXPORT_TELEMETRY_POLICY.md). It defines proposed metadata-first telemetry defaults, data-category ownership candidates, immediate access revocation versus asynchronous physical deletion, export controls, backup restore reconciliation, and planned acceptance tests. Numeric retention, residency, legal hold, export rights, backup RPO/RTO and telemetry retention remain open; this is not a compliance certification. Review with product/privacy/legal owners before implementing persistence or deletion workflows. No code/tests were run.


## Latest checkpoint — identity and authorization POC runbook (2026-10-22)

Read [IDENTITY_AUTHORIZATION_POC_RUNBOOK.md](IDENTITY_AUTHORIZATION_POC_RUNBOOK.md). It defines 24 scenarios, synthetic tenant fixtures, hard security gates, measurement protocol and a weighted scorecard for ZITADEL, Keycloak and an optional Auth0 benchmark. No provider has been tested, scored or selected. Do not run until the user explicitly approves scope, environment, operators and budget. Hard-gate failures in auth/session safety, tenant isolation, revocation, secret redaction or fail-closed behavior block selection regardless of score. No application code or tests were run.


## Latest checkpoint — cross-repository contract audit (2026-10-22)

Read [CROSS_REPOSITORY_CONTRACT_AUDIT.md](CROSS_REPOSITORY_CONTRACT_AUDIT.md). It found two real contract contradictions and corrected them: API now routes durable runs through orchestration instead of declaring direct agents/database implementation dependencies; workflows no longer depend at runtime on orchestration, agents or database. The other main finding is that current contracts are mostly governance prose; machine-readable OpenAPI, event envelopes, provider capabilities, tool invocation and lifecycle schemas remain to be authored before implementation.



## Latest checkpoint — draft contract schemas (2026-10-22)



## Latest checkpoint — contract semantic review and error catalog (2026-10-22)

Added [draft schema semantic review](contracts/SCHEMA_SEMANTIC_REVIEW.md) and [draft public error-code catalog](contracts/ERROR_CODE_CATALOG.md). Review highlights: tool arguments and generic event payloads are currently unconstrained objects; tenant/actor/step/failure fields may need event-specific required rules; format assertion and event ordering/replay/deduplication semantics remain unresolved; JSON Schema cannot enforce trusted authentication, current authorization, approval binding, or revocation behavior. The error catalog proposes codes and HTTP/retry mappings but is not approved for implementation.



## Latest checkpoint — draft OpenAPI v1 baseline (2026-10-22)

Added [openapi.v1.yaml](contracts/openapi.v1.yaml) and [OPENAPI_V1_BASELINE.md](contracts/OPENAPI_V1_BASELINE.md), linked from the contract registry README. The provisional API surfaces are health, synchronous text completion, durable run creation, run-status reads, and cancellation. Streaming, multimodal input, tool APIs, conversation persistence, files/knowledge, model catalog, approvals, usage, and admin APIs remain out of scope for this draft. Route and schema shapes are proposals, not approved or implemented contracts. Bearer/JWT is only a placeholder; identity issuer/audience, tenant/membership authority, limits, streaming, idempotency retention, cancellation races, and output retention remain unresolved.



## Latest checkpoint — OpenAPI semantic review findings (2026-10-22)

Added [OPENAPI_V1_REVIEW_MATRIX.md](contracts/OPENAPI_V1_REVIEW_MATRIX.md) and linked it from the contract registry. A P0 design defect was found: the current request message schema permits client-supplied `system` and `developer` roles, and the response reuses that same schema. Before approval, separate request/response message schemas and keep privileged instructions server-owned. Other blockers include trusted tenant resolution, per-agent input schemas and size limits, run output authorization/retention, cancellation races, response schemas for 202 accepted operations, error schema drift, streaming decisions, and token validation rules.



## Latest checkpoint — OpenAPI message-role remediation (2026-10-22)

Updated `contracts/openapi.v1.yaml` to use separate `RequestChatMessage` and `ResponseChatMessage` schemas (`user` input, `assistant` output), and added provisional JSON bodies for accepted run creation and cancellation. Added [OPENAPI_V1_CONTRACT_TEST_PLAN.md](contracts/OPENAPI_V1_CONTRACT_TEST_PLAN.md) and updated [OPENAPI_V1_REVIEW_MATRIX.md](contracts/OPENAPI_V1_REVIEW_MATRIX.md). This addresses the schema-level P0 role finding in the draft but has not been validated by an OpenAPI parser or runtime test. Other blockers remain: trusted tenant resolution, agent-specific input schemas and limits, run output authorization/retention, cancellation races/idempotency semantics, streaming decisions, identity token validation, and formal OpenAPI validation.



## Latest checkpoint — repository inventory refreshed (2026-10-22)

The connected GitHub listing now shows **32 of the 33 canonical Aether AI repository names**. The only name not found is [aether-ai-memory](https://github.com/Monupatel62/aether-ai-memory); verify its exact identity before assuming it exists or creating it. Five formerly unlisted names are now present but empty: aether-ai-integrations, aether-ai-testing, aether-ai-ui-components, aether-ai-enterprise, and aether-ai-infrastructure.

Current documented status: **23 repositories have documentation foundations; 9 existing repositories are empty on the default branch; 1 canonical name was not found**. The aether-ai-admin repository now has its 10-file documentation foundation, and all 10 files were fetched back successfully.



## Latest checkpoint — billing docs verified (2026-10-22)

Added and fetched back all 10 standard documentation files in [aether-ai-billing](https://github.com/Monupatel62/aether-ai-billing). Current inventory: 32/33 canonical names visible, 24 repositories with documentation foundations, 8 existing repositories still empty, and aether-ai-memory not found in the connected GitHub listing. Billing/payment technology and pricing remain undecided; no application code or tests were run.

Next: document aether-ai-sdk, then evaluations, observability, integrations, testing, UI components, enterprise, and infrastructure. Do not create or rename a repository until the exact identity of aether-ai-memory is confirmed.


## Repository-tree audit — 2026-10-23

- Inspected the recursive Git trees of all 33 canonical repositories on their `main` branches.
- All 33 repository names are present. The inspected trees contain documentation files only; no application source, package manifest, test suite, CI workflow, or runtime implementation appeared in those trees.
- The master repository contains architecture, security and authorization reviews, a proposed dependency graph, API schemas, implementation plans, and research documents. These are design artifacts, not proof of working software.
- The earlier repository inventory notes in this handoff are historical snapshots and are superseded by this audit.
- The next gate is to finish the cross-repository contract/security review and close implementation-blocking decisions. Do not invent a stack or start implementation against unresolved contracts. Once the design gate is satisfied, implement the smallest vertical slice with tests, then expand repository by repository.
- Aether AI is standalone. Do not introduce unrelated brands, repositories, packages, or assumed dependencies into Aether AI documentation or implementation.


## Latest checkpoint — standalone boundary and repository-spec audit (2026-10-23)

- Removed unrelated project/package references from the gateway proof-of-concept plan, identity/authorization POC runbook, technical design, dependency edge register, cross-repository contract audit, work log, repository spec index, and the affected individual repository specifications.
- Scanned the master documentation set, all 33 master repository specifications, contract schemas, and the machine-readable dependency graph for unrelated-project markers. The updated inspected text files return zero matches for those markers.
- Corrected all 33 master repository specification status lines: every canonical repository exists, and its inspected `main` tree is documentation-only. Filled missing dependency sections in the affected specs and reconciled their direction with the proposed dependency graph.
- Enumerated recursive Git trees for all 33 repositories; every tree returned `truncated: false` and contained only README and/or `docs/` files. No source files, manifests, test suites, or CI workflows were present in those default-branch trees.
- Updated [Implementation Status Audit](IMPLEMENTATION_STATUS_AUDIT.md) with the full-tree evidence. This is not a local clone, build, runtime test, security test, or audit of other branches.
- No application code was written and no tests were run. Continue reviewing unresolved contracts and security decisions. Do not invent a stack or claim implementation readiness.


- Synchronized `docs/REPOSITORY_SPECIFICATION.md` in all 33 repositories: current documentation-only status, non-empty dependency section, and dependency direction aligned with the proposed master graph. All 33 files were fetched back and checked; no unrelated-project/package markers remained in those specifications.


- Local documentation-link validation is complete for the master documentation set and all 33 master repository specifications: no unresolved relative links were found. External URLs and heading anchors remain unverified.


- Added root README entry points to `aether-ai-memory` and `aether-ai-observability`. Audited README files across all 33 repositories: no broken local relative links and no unrelated-project/package markers remained in the inspected READMEs.


- Completed an additional documentation scan across the component repositories. Removed unrelated project/package assumptions from affected README, project-specification, work-log, research/license, architecture, dependency, technical-design, and implementation-plan files. The inspected README/spec files for all 33 repositories and the additional standard docs inspected now return zero matches for the unrelated-project markers.


- Added [Implementation Gate Blockers](IMPLEMENTATION_GATE_BLOCKERS.md) to consolidate the remaining P0 contract/security blockers and P1 product/operations decisions. This is a review checklist, not an implementation approval.


## Dependency direction audit — 2026-10-23

- Added [Dependency Direction Audit](DEPENDENCY_DIRECTION_AUDIT_2026-10-23.md) and corrected three repository-level contract declarations on review branches: provider adapters no longer depend on gateway; agents no longer depend on orchestration implementation; files lists API as a consumer rather than a dependency.
- The three component files and the new master report were fetched back after writes. These are documentation-only corrections, not source-import verification.
- Review the four draft pull requests before merging. Next: compare all 33 dependency contracts with the typed edge register and JSON graph, then verify graph consistency without claiming source-level cycle freedom.
- End-to-end application integration and production release remain gated by unresolved P0 security/identity/tenant decisions; isolated foundation coding is now explicitly authorized.


## Dependency direction audit — second pass (2026-10-23)

- Extended [Dependency Direction Audit](DEPENDENCY_DIRECTION_AUDIT_2026-10-23.md) with three additional concrete contradictions: cache depended on application consumers/database; plugins depended on admin; deployment listed platform/services without distinguishing release artifacts from runtime dependencies.
- Corrected the contracts for cache, plugins and deployment on review branches and fetched the changed files back from GitHub.
- Total targeted findings now documented: six. Review all six component PRs and the master audit PR; do not merge automatically.
- Next: inspect remaining repository-level contracts against the machine-readable graph and typed edge register. Source imports and runtime behavior remain unverified; no application integration or production readiness is claimed.


## Implementation progress — 2026-10-23

The user explicitly authorized starting coding. Work is proceeding as isolated, draft-only implementation slices; no PRs have been merged and no production deployment has been attempted. P0 identity, tenant/membership, authorization-context trust, run-state/idempotency, tool-execution and retention/deletion decisions still block end-to-end runtime integration and production release.

Draft implementation PRs:
- SDK client + bounded SSE parser: https://github.com/Monupatel62/aether-ai-sdk/pull/4 — Node.js 22 dependency audit, typecheck, unit tests and build passed. Dependency audit remains open; initial install reported 3 vulnerabilities (1 moderate, 2 critical).
- Shared test helpers + JSON Schema Draft 2020-12 validator: https://github.com/Monupatel62/aether-ai-testing/pull/2 — Node.js 22 dependency audit, typecheck, unit tests and build passed.
- Provider-neutral adapter contracts/registry: https://github.com/Monupatel62/aether-ai-providers/pull/6 — Node.js 22 dependency audit, typecheck, unit tests and build passed. Gateway/provider contract remains a proposal.
- Tenant-scoped cache interface + bounded in-memory reference adapter: https://github.com/Monupatel62/aether-ai-cache/pull/8 — Node.js 22 dependency audit, typecheck, unit tests and build passed. In-memory adapter is not production/distributed storage.
- Deterministic evaluation dataset validator/scorer: https://github.com/Monupatel62/aether-ai-evaluations/pull/4 — Node.js 22 dependency audit, typecheck, unit tests and build passed. No model calls or release thresholds implemented.
- Versioned workflow definition/graph validator: https://github.com/Monupatel62/aether-ai-workflows/pull/5 — Node.js 22 dependency audit, typecheck, unit tests and build passed.
- Metadata-only telemetry contract/sanitizer: https://github.com/Monupatel62/aether-ai-observability/pull/4 — Node.js 22 dependency audit, typecheck, unit tests and build passed. No exporter or retention enforcement implemented.
- Deterministic RAG text chunker: https://github.com/Monupatel62/aether-ai-rag/pull/3 — Node.js 22 dependency audit, typecheck, unit tests and build passed. Pure chunking utility only; no extraction, embeddings, persistence, or ACL enforcement.
- Best-effort secret redaction helpers: https://github.com/Monupatel62/aether-ai-security/pull/5 — Node.js 22 dependency audit, typecheck, unit tests and build passed. Not a DLP scanner or security certification.
- Bounded file-signature/upload metadata validation: https://github.com/Monupatel62/aether-ai-files/pull/6 — Node.js 22 dependency audit, typecheck, unit tests and build passed. No malware scanning, storage, authorization, or deletion lifecycle implemented.

All ten isolated implementation PRs listed above pass the Node.js 22 dependency-audit, typecheck, unit-test and build workflow. Vitest was upgraded to patched 5.0.5 and `npm audit --audit-level=high` is enforced. Node.js 20 CI was removed after dependency installation failed with an npm Arborist `edgesOut` error even after npm upgrades; package manifests still declare Node >=20, so Node 20 compatibility is not verified and must be resolved before claiming it. These are initial foundations, not complete repositories. All must remain draft until cross-repository contracts, dependency/license checks, security review, and integration gates are addressed. Do not mark a repository production-ready solely because its local package CI passes.


- Database migration metadata validator: https://github.com/Monupatel62/aether-ai-database/pull/4 — Node.js 22 dependency audit, typecheck, unit tests and build passed. It validates metadata only; no database adapter or SQL execution.
- Gateway request validator: https://github.com/Monupatel62/aether-ai-gateway/pull/5 — Node.js 22 dependency audit, typecheck, unit tests and build passed. It validates request shape/limits only; no authorization, provider routing, or model execution.

- API safe error/request metadata contract: https://github.com/Monupatel62/aether-ai-api/pull/5 — Node.js 22 dependency audit, typecheck, unit tests and build passed. No authentication middleware or product routes implemented.

- Queue envelope/retry utilities: https://github.com/Monupatel62/aether-ai-queue/pull/4 — Node.js 22 dependency audit, typecheck, unit tests and build passed. No broker adapter, durable idempotency, or worker runtime.

- Deterministic lexical search baseline: https://github.com/Monupatel62/aether-ai-search/pull/4 — Node.js 22 dependency audit, typecheck, unit tests and build passed. No backend, ACL integration, or deletion propagation.
- Tool manifest validator/fail-closed preflight: https://github.com/Monupatel62/aether-ai-tools/pull/6 — Node.js 22 dependency audit, typecheck, unit tests and build passed. No executor/sandbox; tool-policy ADR remains a release blocker.

- MCP JSON-RPC request/response validator: https://github.com/Monupatel62/aether-ai-mcp/pull/4 — Node.js 22 dependency audit, typecheck, unit tests and build passed. No transport or server trust implementation.

- Plugin manifest/version compatibility validator: https://github.com/Monupatel62/aether-ai-plugins/pull/5 — Node.js 22 CI pending. Requested capabilities are not grants; artifact verification and isolation are not implemented.
