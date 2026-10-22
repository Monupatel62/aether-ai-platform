# Tenant Context Resolution Contract — Draft

**Status:** Proposed security contract for review; not approved or implemented.  
**Scope:** API/BFF request processing and downstream protected operations.  
**Related decisions:** `TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md`, `AUTHORIZATION_PERMISSION_MATRIX.md`, `AUTHORIZATION_POLICY_GAP_AUDIT.md`, ADR-0021 and ADR-0024.

## 1. Purpose

Prevent client-controlled tenant selection, stale membership data, or an identity-provider claim from being treated as sufficient authorization. This contract proposes a repeatable resolution and enforcement sequence without choosing the still-unresolved canonical membership repository.

## 2. Security invariants

1. Authentication identifies a principal; it does not grant access to a tenant or resource.
2. A tenant ID, workspace ID, role, membership status, resource grant, or approval in a request body, query string, custom header, cookie, model prompt, tool argument, or client metadata is an untrusted selector or hint—not proof of access.
3. Tenant context is accepted only after the server resolves the authenticated principal against authoritative Aether membership state.
4. Tenant membership alone is insufficient for a resource operation. The resource owner must enforce resource ACL, action permission, lifecycle state, and relevant entitlement checks.
5. Every protected read, list/search, export, stream, tool call, background job, retry, and result retrieval must be authorized at the operation boundary. Authorization from an earlier request is not a durable grant for later work.
6. If required authoritative authorization state is unavailable, stale beyond an explicitly approved bound, or inconsistent, deny protected operations. Do not fall back to a client claim or permissive cached result.
7. A denial must not reveal protected content or unnecessary resource existence details. Use the approved error/404 concealment policy.
8. Cache keys and stored authorization decisions must include the relevant principal, tenant, resource/action scope, and policy/membership/ACL versions. A cache hit must never bypass required revocation semantics.

## 3. Proposed request resolution sequence

1. **Authenticate:** validate the session or access token at the trusted API boundary, including issuer, audience, expiry, signature/key rotation and required claims under the yet-to-be-approved identity profile.
2. **Resolve principal:** map the validated identity to a stable Aether principal ID. Do not use an unverified subject string as a global user ID.
3. **Select candidate tenant:** use an explicitly documented tenant selector if the API design requires one. Treat it only as a request to operate in that tenant.
4. **Resolve membership:** query the canonical membership authority for the principal's current membership and status in the candidate tenant. Reject absent, suspended, expired, or revoked membership.
5. **Resolve resource:** load the resource through its owning domain, verifying that its canonical tenant/resource relationship is consistent. Never authorize from a caller-provided resource-to-tenant mapping.
6. **Evaluate action:** evaluate role/grant, resource ACL, requested action, data classification, resource lifecycle, approval/step-up obligations, and applicable entitlement.
7. **Bind trusted context:** create a server-internal immutable authorization context containing principal ID, tenant ID, resource/action scope, policy decision ID, relevant versions and request correlation ID. It must not be constructible or overrideable by client input.
8. **Execute and re-check:** immediately before delayed or high-impact work, re-check current membership and resource permissions. Background workers must not treat enqueue-time authorization as permanently valid.
9. **Audit safely:** record decision metadata and reason codes with redaction; never log raw credentials, secrets, or protected content by default.

## 4. Membership and ACL versioning

The canonical membership owner and exact version transport remain undecided. Before implementation, the contract must define:
- Monotonic or otherwise unambiguous membership/ACL revision identifiers.
- Which service is authoritative for each revision and how a consumer detects stale state.
- Event ordering, duplicate delivery, retries, replay and reconciliation behavior.
- Maximum acceptable authorization-cache age for each protected operation class.
- How deletion, tenant suspension, membership removal, role downgrade, resource unsharing and source deletion invalidate active work and derived projections.
- Behavior when the membership authority and resource owner disagree about tenant ownership.

**Proposed fail-closed baseline:** do not allow a protected operation on an unresolved ownership/version conflict. Record a sanitized security event and return the approved safe error.

## 5. Error semantics proposal

| Condition | Proposed external behavior | Internal handling |
|---|---|---|
| Missing/invalid authentication | 401 | No protected resource lookup before authentication |
| Authenticated principal lacks membership or action grant | 403, or 404 where concealment policy applies | Record sanitized deny reason |
| Tenant/resource mapping conflict | Safe denial, normally 404 or 409 according to approved policy | Fail closed; emit high-signal security event |
| Authorization authority unavailable | 503 for protected operations | No fallback to untrusted claims; bounded retry only where safe |
| Revoked permission detected during a run | Stop subsequent protected steps and deny new reads | Mark run/step outcome using approved lifecycle semantics; side effects already completed are not implied to be rolled back |

These are proposals, not approved HTTP semantics. They must be reconciled with the canonical error catalog before implementation.

## 6. Minimum acceptance cases

| ID | Test setup | Required result |
|---|---|---|
| TENANT-001 | Valid identity, no membership in requested tenant | Deny; no tenant resource data returned |
| TENANT-002 | Client forges tenant ID in body, header or metadata | Forged value alone grants no access |
| TENANT-003 | Valid member of tenant A requests tenant B resource | Deny without cross-tenant content leakage |
| TENANT-004 | Membership removed while global session remains valid | Next protected operation is denied under the approved revocation bound |
| TENANT-005 | Resource ACL revoked after a run is queued | Worker re-checks before the protected step and denies it |
| TENANT-006 | Membership authority times out | Protected operation fails closed; no permissive cached fallback |
| TENANT-007 | Resource owner and membership authority disagree on tenant ownership | Deny and emit sanitized security event |
| TENANT-008 | Stale cache has an older membership/ACL revision | Cache does not override required current authorization |
| TENANT-009 | Search returns a result whose ACL revision is stale or revoked | Result is filtered before it can be shown or supplied to a model |
| TENANT-010 | Retry/replayed lifecycle event arrives out of order | Revision checks and reconciliation prevent permission resurrection |
| TENANT-011 | Tenant is suspended | All tenant-protected operations follow the approved suspension policy; no selector-based bypass |
| TENANT-012 | Policy dependency fails during tool execution | No protected tool side effect starts without a valid allow decision |

## 7. Decisions still required

- Select the canonical tenant/membership owner; the existing decision document compares enterprise, dedicated tenancy, and auth ownership. This draft does not choose among them.
- Decide whether tenant selection is explicit in the API path/header or inferred from a single-tenant session.
- Approve membership/ACL revision model, cache bounds, and revocation convergence targets.
- Approve exact 403/404 concealment rules and policy-service outage behavior.
- Define the internal authorization-context schema and service-to-service trust mechanism.
- Align the run lifecycle, audit events, error catalog, search/RAG filtering, exports, and data-deletion behavior.

## 8. Approval and verification status

No implementation or tests were run. The acceptance cases are proposed test requirements, not passing test results. This document must be reviewed alongside the membership/ACL decision and authorization matrix before the OpenAPI contract is approved.
