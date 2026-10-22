# Tenant Membership, Resource ACL and Revocation Consistency Decision

**Research date:** 2026-10-22  
**Status:** Proposed design for product-owner review; no ADR accepted and no implementation performed.  
**Phase:** Documentation and research only.

## 1. Decision required

Aether needs one canonical source for tenant/workspace membership and role grants, and a defined safety contract for revoking access when source permissions, membership, or content changes. These are related but distinct decisions. This document recommends a boundary to review; it does not silently close ADR-0020, ADR-0021, or ADR-0024.

## 2. Separate the authority domains

| Concern | Proposed authoritative owner | Must not be confused with |
|---|---|---|
| External identity proof, login integration, principal mapping, session lifecycle | `aether-ai-auth` | Tenant membership or resource permissions |
| Tenant/workspace membership, role grants, invitations, membership status and hierarchy | **Unresolved product ownership decision**; compare `aether-ai-enterprise` against a dedicated tenancy domain | Authentication identity, SSO configuration, billing entitlements |
| Shared policy evaluation contract and decision semantics | `aether-ai-security` | Ownership of membership data or resource ACL data |
| Resource/source ACL and lifecycle for knowledge collections/documents | `aether-ai-knowledge` | Search index metadata or model-generated judgments |
| File ownership and file lifecycle | `aether-ai-files` | Knowledge projections and search index state |
| Indexing, retrieval and deletion projections | `aether-ai-search` and `aether-ai-rag` within their boundaries | Authoritative access-control state |
| API request enforcement and tenant-context resolution | `aether-ai-api` plus each resource-owning boundary | Trusting a tenant ID supplied by a client |
| Tenant plan/usage entitlements | `aether-ai-billing` for commercial entitlement facts | Permission to read an arbitrary resource |

A single resource can require multiple checks: authenticated principal, active tenant membership, resource-specific ACL, action permission, and entitlement where relevant. A positive result from one domain does not substitute for the others.

## 3. Membership-owner options

### Option A — `aether-ai-enterprise` owns tenant/workspace membership and role grants
**Advantages:** aligns organization hierarchy, enterprise provisioning/SCIM and administration in one domain; avoids adding a repository.  
**Risks:** the repository may become a broad product-domain dependency even for non-enterprise tenants; membership lifecycle must not depend on enterprise SSO being enabled.  
**Guardrail:** if selected, define it as the tenant domain for all customer tiers, not merely an optional enterprise feature.

### Option B — introduce a dedicated `aether-ai-tenancy` repository
**Advantages:** explicit ownership for tenants, workspaces, membership, invitations and grants; separates core tenancy from identity-provider and enterprise federation concerns.  
**Risks:** expands the agreed 33-repository scope, adds a new package/API and migration owner, and requires updating the catalog, dependency graph, repository count and all contracts.  
**Guardrail:** do not create or count this repository without explicit approval to change the 33-repository plan.

### Option C — `aether-ai-auth` owns membership and grants
**Advantages:** fewer moving parts in an initial implementation.  
**Risks:** couples authorization data to login/session/provider integration; may make membership lifecycle, service principals, provisioning and resource-domain changes harder to evolve independently.  
**Assessment:** least preferred unless product scope proves membership is intentionally part of the identity boundary.

### Recommendation for review
Prefer **Option A** if enterprise is intended to be the universal tenant-management domain, with a strict contract that works when enterprise SSO/SCIM is absent. Otherwise, choose Option B only by explicitly revising the repository plan. Keep Option C as a fallback, not the default. No option is accepted until the product owner confirms the tenant/workspace product model.

## 4. Required contract regardless of owner

The canonical membership service/domain should expose versioned operations or events for:
- create/suspend/reactivate tenant;
- invite, accept, remove and restore membership;
- grant/revoke roles and resource-scoped grants;
- create/update/delete workspace and change hierarchy;
- rotate membership/policy version;
- emit auditable lifecycle events with stable tenant, subject, actor, event ID, version, timestamp and correlation ID.

Events are notifications, not the only authorization barrier. Consumers must handle duplicates, out-of-order delivery, retries, replay and missed events. They should reconcile against the canonical state or versioned contract. Do not let consumers write private membership tables.

## 5. Revocation and deletion safety contract

### Immediate safety rule
After an authoritative membership, grant, tenant-suspension or resource-ACL revocation is committed, **new protected reads and actions must be denied by a fresh authoritative authorization check**. Search/vector index deletion, cache invalidation and asynchronous event delivery are cleanup mechanisms, not the security boundary.

### Data and job behavior
1. **API and direct resource reads:** evaluate current membership and resource policy before returning protected metadata, snippets, files or content.
2. **Search/RAG:** apply tenant/ACL filters before results leave the search boundary; then re-authorize each candidate against current source policy before snippets or content are passed to a model. Never rely only on stale index metadata.
3. **Caches:** authorization-sensitive cache entries need policy/resource versioning and bounded lifetime; a cache hit must not bypass a fresh policy check for protected content. Invalidate on events as an optimization.
4. **Queues/workers:** include immutable actor, tenant, resource, requested action and originating policy/version context. At execution, re-check authorization for sensitive or delayed work. Cancel or quarantine work that no longer has permission; do not treat enqueue-time permission as permanent.
5. **Files and object storage:** revoke access through the owning file boundary immediately; asynchronous physical deletion may follow retention/legal-hold policy. Signed URLs must be short-lived and not become an unbounded bypass.
6. **Index/chunk/citation cleanup:** tombstone or suppress deleted/revoked sources immediately in the authoritative source contract, then asynchronously remove or rebuild projections. Citations must not expose content after revocation.
7. **Sessions and credentials:** tenant removal or principal disablement must invalidate applicable sessions, API keys and workload grants according to the selected session/credential design. A global session may remain valid for other tenants only if every request re-checks membership.
8. **Tenant deletion/suspension:** deny access first, then orchestrate data lifecycle, queue cancellation, cache/index cleanup and audit/retention actions.

## 6. Consistency targets — proposed, not approved SLOs

Do not promise a numeric propagation SLA before product requirements and load tests establish it. Use the following acceptance definitions for the POC:
- **Authorization denial:** zero stale-policy allows in deterministic tests after the authoritative revocation transaction commits and the next protected operation performs its required check.
- **Search/RAG leakage:** zero unauthorized content, snippets, embeddings-derived text or citations returned after a revocation is visible to the authoritative check, even if index cleanup is delayed.
- **Worker safety:** every delayed sensitive job revalidates permissions immediately before execution; stale queued jobs cannot execute protected actions.
- **Projection cleanup:** measure p50/p95/p99 time from committed delete/revoke to removal or suppression in search, vector, cache and object-storage projections. Product owner must set numeric targets after workload/retention requirements are known.
- **Recovery:** event loss, duplicate delivery and consumer outage must not restore access; reconciliation can repair projections without changing the authoritative policy.
- **Audit:** record actor, target, action, decision, policy/version, reason code and correlation ID without logging tokens or protected content.

The first three are safety invariants, not eventual-consistency SLAs. Projection cleanup targets are operational objectives to be selected after benchmarking.

## 7. Required failure-mode tests

- Remove a member while a browser session remains active; the next protected request is denied.
- Revoke a workspace role while search results are cached; no protected snippet or content is returned.
- Revoke a source ACL while vector chunks and citations remain indexed; retrieval re-authorizes and denies content.
- Delete a source while queue consumers are offline; replay/reconciliation does not resurrect it.
- Deliver duplicate and out-of-order membership/ACL events; final projection converges to authoritative state.
- Suspend a tenant with queued jobs; workers deny or cancel protected execution.
- Rotate policy/resource versions while cache entries exist; stale cache entries cannot grant access.
- Fail the authorization dependency; protected operations fail closed, with explicit availability and recovery behavior.
- Verify PostgreSQL RLS, if adopted, using the actual non-owner runtime role; RLS is defense-in-depth, not a substitute for domain authorization.
- Verify audit records for membership and ACL changes, including denied cross-tenant attempts.

## 8. ADR updates needed

- **ADR-0020:** choose the policy model and define policy-decision contract; RBAC baseline plus resource-level checks is a candidate, not a final selection.
- **ADR-0021:** choose tenant/workspace hierarchy, membership owner, and support access. Compare Option A with Option B; do not add a repository without approval.
- **ADR-0023:** define session, API-key, workload identity and revocation targets once operational requirements are known.
- **ADR-0024:** decide tenant isolation/RLS rollout and prove it with non-owner runtime roles.
- **Data lifecycle policy:** define retention, hard-delete/soft-delete, legal hold, export and audit-retention behavior separately from access revocation.

## 9. Decision status and next gate

**Open:** canonical membership owner, final role model, numeric projection-cleanup SLOs, retention/deletion policy, RLS rollout, and support-access workflow.

Before implementation:
1. Product owner confirms whether `aether-ai-enterprise` is the universal tenancy domain or approves a change to the 33-repository plan.
2. Review the permission matrix and mark product-policy decisions.
3. Define representative data volumes, freshness expectations, deletion/retention requirements and availability goals.
4. Run the planned identity/authorization POC and record measured evidence.
5. Update the dependency matrix, typed edge register, machine-readable graph, repository specs and ADRs after the ownership decision.

No application code, provider selection, repository creation, or numeric SLO commitment is made by this document.

## References
- [Authorization Permission Matrix](AUTHORIZATION_PERMISSION_MATRIX.md)
- [Identity and Tenant Security Evaluation](IDENTITY_AND_TENANT_SECURITY_EVALUATION.md)
- [Browser Session and Authorization Architecture](BROWSER_SESSION_AND_AUTHORIZATION_ARCHITECTURE.md)
- [Cross-Repository Consistency Audit](CROSS_REPOSITORY_CONSISTENCY_AUDIT.md)
- [Dependency Matrix](DEPENDENCY_MATRIX.md)
- [Decision Log](DECISION_LOG.md)
