# Cross-Repository Ownership Consistency Audit — Follow-up

**Date:** 2026-10-23  
**Status:** Focused documentation comparison; proposed findings only.  
**Scope:** Master dependency matrix/register and repository specifications for Workflows, Knowledge, RAG, API, Orchestration, Queue, Database, Auth, Security, and Enterprise.  
**Implementation status:** Documentation-only repositories; this audit does not establish runtime dependency behavior.

## Result

The focused comparison shows several ownership statements are already aligned, but cross-repository consistency is not yet fully proven. No source-import graph or runtime dependency graph exists to validate because the inspected repositories remain documentation-only.

## Confirmed aligned statements

1. **Workflow definitions vs execution:** Workflows owns versioned schema/validation; Orchestration owns durable run/step state, retries, cancellation, and recovery.
2. **Durable run routing:** API delegates durable runs to Orchestration; API may call Gateway only for explicitly bounded synchronous completion.
3. **Queue direction:** Queue owns transport/envelope/delivery mechanics; producers and consumers own business decisions and idempotent handlers.
4. **Database boundary:** Database owns shared persistence/migration tooling and backup/restore conventions; domain owners retain data semantics and migration intent.
5. **Identity vs authorization:** Auth owns principal/session/token lifecycle; Security owns shared policy contracts/primitives; domain/API boundaries enforce resource-level decisions.
6. **Knowledge/RAG/Search:** Knowledge owns authoritative source/collection metadata and ACL references; RAG/Search are consumers/projections and cannot become final authorization authority.

These statements were checked in the current main-branch repository specifications and master matrix/register. They are documentation claims, not runtime evidence.

## Remaining ownership and contract gaps

| ID | Gap | Risk | Required next decision/evidence |
|---|---|---|---|
| OWN-01 | Canonical tenant/workspace membership and role-grant owner remains undecided under ADR-0021. | Services may resolve tenant membership differently or duplicate authority. | Approve one source of truth, version/revocation semantics, and conflict behavior. |
| OWN-02 | Security's deployment shape is unresolved: dependency-light library vs remote policy service. | Timeout, consistency, availability, and trust assumptions differ materially. | Choose via ADR; define authenticated caller contract and fail-closed behavior. |
| OWN-03 | API ↔ Orchestration and API ↔ Gateway are described as synchronous/network boundaries in some docs but could be package contracts in the initial modular runtime. | Unclear error propagation, deployment assumptions, and versioning expectations. | Label each edge as in-process contract or network API for the first vertical slice. |
| OWN-04 | Database migration files are domain-owned in semantics, but physical packaging/composition remains open. | Migration ordering, rollback ownership, and cross-domain deployment coupling. | Decide per-domain migration ownership and deployment composition; document rollback limits. |
| OWN-05 | Knowledge-to-RAG indexing status/event direction requires one stable public contract. | Circular package dependency or inconsistent indexing/deletion state. | Define event producer, schema/version, consumer, retry/deduplication, and reconciliation owner without a reverse implementation import. |
| OWN-06 | Revocation/deletion propagation latency from Knowledge to RAG/Search/cache has no accepted target. | Stale projections may remain visible after revocation. | Set a measurable propagation target, but require fresh authorization before serving protected results regardless of projection delay. |
| OWN-07 | Repository specifications use broad dependency labels in places, while the matrix distinguishes package imports, network APIs, events, artifacts, and infrastructure edges. | A logical relationship can accidentally become a reverse package dependency. | Normalize every edge using the edge-register taxonomy and specify the public contract owner. |
| OWN-08 | Domain-specific authorization, retention, output schemas, limits, and failure contracts are not equally detailed across all 33 specs. | Generic boilerplate can be mistaken for a complete implementation contract. | Prioritize high-risk repositories and add resource/action-level contract tables before implementation. |

## Edge-direction invariants to preserve

- Workflows must not import Orchestration, Agents, or Database runtime internals.
- Queue must not import Orchestration, Billing, or consumer implementations.
- Security must not import its callers or own identity/session/membership state.
- Knowledge must not import RAG/Search implementation; those systems consume versioned contracts/events.
- Provider adapters must not import Gateway implementation.
- API must not create its own durable run state machine or bypass Orchestration for durable work.
- Search/RAG/cache/vector metadata must not grant authorization; protected reads and side effects must re-check authoritative policy.
- Platform/docs repositories have documentation-only relationships and no runtime imports.

## Verification limits

- Compared the current master dependency matrix, edge register, and ten repository specifications listed in the scope.
- Did not inspect all 33 specs in this focused follow-up; earlier structural inventory is not equivalent to semantic validation of every contract.
- Did not run a package-import graph scan, OpenAPI validator, JSON Schema validator, runtime tests, or integration tests.
- No repository specs were changed by this follow-up; no conflicting statements were silently rewritten.

## Exit criteria

1. Resolve or explicitly defer OWN-01 through OWN-07 in reviewed ADRs/contracts.
2. Normalize direct dependency edges and assign an owner and consumer list for each public contract.
3. Re-scan all 33 specifications against the accepted matrix and record exact file/line evidence for each mismatch.
4. After implementation approval, automate package-import cycle detection and contract compatibility checks in CI.
5. Keep Phase 0 open until P0 implementation blockers are accepted/deferred and the user explicitly authorizes implementation.
