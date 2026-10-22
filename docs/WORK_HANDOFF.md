# Aether AI — Current Work Handoff

**Last updated:** 2026-10-22

## User intent and hard constraints

- Build a new AI platform separate from WoHoTech.
- Use the existing WoHo AI DevKit where it fits; do not rewrite it.
- Plan 33 Aether AI repositories. The first 10 have been created; 23 remain planned.
- Documentation first. Do not start application coding until the full docs and dependency contracts are reviewed.
- Every component needs a clear purpose, scope, connections, APIs/contracts, implementation order, license notes, and work log.
- Explain non-obvious code choices with comments when coding eventually begins; comments must explain why/invariants, not repeat syntax.

## Repository state

### Existing Aether repositories (10)

1. https://github.com/Monupatel62/aether-ai-platform
2. https://github.com/Monupatel62/aether-ai-web
3. https://github.com/Monupatel62/aether-ai-api
4. https://github.com/Monupatel62/aether-ai-gateway
5. https://github.com/Monupatel62/aether-ai-providers
6. https://github.com/Monupatel62/aether-ai-agents
7. https://github.com/Monupatel62/aether-ai-workflows
8. https://github.com/Monupatel62/aether-ai-orchestration
9. https://github.com/Monupatel62/aether-ai-tools
10. https://github.com/Monupatel62/aether-ai-mcp

Each existing repository has documentation-only files: README, PROJECT_SPEC, ARCHITECTURE, DEPENDENCIES_AND_CONTRACTS, IMPLEMENTATION_PLAN, RESEARCH_AND_LICENSES, WORKLOG, ENGINEERING_STANDARD, and repository-specific TECHNICAL_DESIGN. No application source code has been added as part of this work.

### Remaining planned repositories (23)

`aether-ai-memory`, `aether-ai-rag`, `aether-ai-files`, `aether-ai-knowledge`, `aether-ai-auth`, `aether-ai-security`, `aether-ai-admin`, `aether-ai-billing`, `aether-ai-sdk`, `aether-ai-evaluations`, `aether-ai-observability`, `aether-ai-deployment`, `aether-ai-docs`, `aether-ai-database`, `aether-ai-queue`, `aether-ai-cache`, `aether-ai-search`, `aether-ai-plugins`, `aether-ai-integrations`, `aether-ai-testing`, `aether-ai-ui-components`, `aether-ai-enterprise`, `aether-ai-infrastructure`.

Each has an individual specification in [docs/repositories/](repositories/) before the repo is created.

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

## Separate WoHo AI DevKit integration note

- Repository: https://github.com/Monupatel62/woho-ai-devkit
- Documentation-only draft PR: https://github.com/Monupatel62/woho-ai-devkit/pull/139
- Branch: `docs/aether-ai-integration-plan`
- PR is open and draft, not merged. It changes only `docs/aether-ai-integration-plan.md`; no source code or release metadata changed.
- Inspected root metadata: version 0.8.37, Apache-2.0, Node >=20. Verify exact package versions/exports before consuming them.

## Research notes

- AI DIAL Core official repository: https://github.com/epam/ai-dial-core. Its README describes a unified API/proxy for chat-completion and embedding models/apps, Java 21 + Vert.x; repository has Apache-2.0 LICENSE.
- AI DIAL Chat: https://github.com/epam/ai-dial-chat. Current architecture describes React/TypeScript frontend and NestJS backend-for-frontend; inspect file-level license notices before reuse.
- ELITEA SDK: https://github.com/EliteaAI/elitea-sdk. It expects an active ELITEA deployment and project credentials; not a drop-in DevKit replacement.
- MCP specification: https://modelcontextprotocol.io/.

## Next work

1. Verify every existing Aether repository has all 8 expected docs and cross-links.
2. Verify the 33 individual repo specs are complete and consistent with the catalog.
3. Review for circular dependencies, duplicate ownership, and unnecessary service boundaries.
4. Resolve open ADRs (name/branding, stack, database, queue, identity provider, model gateway strategy, data retention, deployment).
5. Only after documentation review and user approval, start Phase 1 coding.

## Explicit no-go items until approved

- No application code, no provider secrets, no production deployment, no billing integrations, and no automatic high-impact tools.
- Do not rename or modify WoHoTech.
- Do not rewrite or release WoHo AI DevKit as part of Aether work.
- Do not claim the project is implemented or production-ready; it is still in the documentation phase.

## Latest audit update — 2026-10-22

- Added [Architecture audit](ARCHITECTURE_AUDIT.md), [Security threat model](SECURITY_THREAT_MODEL.md), and [Open decisions research](OPEN_DECISIONS_RESEARCH.md).
- Key research findings: MCP `2026-07-28` is published and materially changes protocol behavior; MCP TypeScript SDK v2 is the current stable line for that spec while v1.x targets `2025-11-25`. Verify `@woho/mcp` exact package support before integration.
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

- Added [AI DIAL adoption evaluation](DIAL_ADOPTION_EVALUATION.md), comparing DIAL Core, DevKit provider path, a hybrid gateway, and DIAL Chat as a product.
- Added [Gateway proof-of-concept plan](GATEWAY_PROOF_OF_CONCEPT.md) with 14 test scenarios, measurement requirements, and decision rules. It is a plan only; no gateway code has been created.
- Added [WoHo AI DevKit compatibility review](DEVKIT_COMPATIBILITY_REVIEW.md) from the current GitHub `main` manifests and selected source files. Current observed versions: `@woho/core 0.2.24`, `@woho/provider-openai 0.2.22`, `@woho/agents 0.3.28`, `@woho/tools 0.4.25`, `@woho/memory 0.6.18`, `@woho/mcp 0.6.28`; verify exact registry tarballs before use.
- The DevKit MCP package has useful generic JSON-RPC-like/stdio primitives, limits and allowlists, but this source review does not prove full MCP `2026-07-28` conformance. A protocol compatibility harness is required; do not alter DevKit to fit Aether.
- ADR-0003 (33 repositories) and ADR-0004 (repository boundaries do not imply 33 services) are recorded as accepted. ADR-0005 (DIAL Core vs DevKit gateway vs hybrid) remains open until a proof-of-concept produces evidence.
- No Aether application code was written and no DevKit source code was modified.

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

GitHub visibility check found 20 canonical-name Aether repos: 10 with docs and 10 empty. Thirteen canonical planned names were not found in the connected listing. The user reports 22 created; two additional names/URLs are not yet reconciled. Catalog updated to state the observed evidence without claiming those two do not exist elsewhere. Next: reconcile the two names, populate documentation in empty repos after confirming their identities, then draft P0 machine-readable contracts. Continue docs-only; no code/tests run and do not alter WoHo AI DevKit.


## Latest checkpoint — draft contract schemas (2026-10-22)

Added [docs/contracts/README.md](contracts/README.md) plus six draft JSON Schemas: `error.schema.json`, `event-envelope.schema.json`, `auth-context.schema.json`, `tool-invocation.schema.json`, `run-event.schema.json`, and `resource-change-event.schema.json`. All six were parsed as valid JSON after creation; JSON Schema semantics and runtime behavior have not been validated. These are draft artifacts, not approved public contracts. Next: review schema semantics and decisions, add a versioned API/OpenAPI baseline and positive/negative fixtures only after approval. Keep documentation-only; no code/tests or DevKit changes.


## Latest checkpoint — contract semantic review and error catalog (2026-10-22)

Added [draft schema semantic review](contracts/SCHEMA_SEMANTIC_REVIEW.md) and [draft public error-code catalog](contracts/ERROR_CODE_CATALOG.md). Review highlights: tool arguments and generic event payloads are currently unconstrained objects; tenant/actor/step/failure fields may need event-specific required rules; format assertion and event ordering/replay/deduplication semantics remain unresolved; JSON Schema cannot enforce trusted authentication, current authorization, approval binding, or revocation behavior. The error catalog proposes codes and HTTP/retry mappings but is not approved for implementation.

Verified status remains limited: the six schemas were previously parsed as JSON; no Draft 2020-12 validator, OpenAPI validation, positive/negative fixtures, runtime tests, or security tests have been run. Next: resolve ownership/versioning and tenant/ACL/event semantics, then draft the versioned OpenAPI baseline. Documentation only; no application code, POC, new repository, or WoHo AI DevKit changes.
