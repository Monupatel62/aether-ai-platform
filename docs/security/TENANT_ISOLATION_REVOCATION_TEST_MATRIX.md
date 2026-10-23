# Tenant Isolation and Revocation Test Matrix

**Date:** 2026-10-23  
**Status:** Proposed acceptance tests; not executed.  
**Purpose:** Turn the Gemini architecture report's tenant-isolation acceptance criterion and the existing Aether revocation model into testable cases. This matrix does not select the membership owner or authorize implementation.

## Preconditions and evidence to capture

Before a run, record the build/commit under test, membership authority, authorization-policy version, data store and isolation configuration, queue/cache/search implementations, test identities, and the configured revocation objective. Do not use production tenant data. Each test record must include setup, request/job identifiers, expected result, observed result, logs/trace IDs and pass/fail.

## Required cases

| ID | Scenario | Action | Expected security outcome | Evidence |
|---|---|---|---|---|
| TENANT-001 | Direct cross-tenant read | User active in Tenant A requests a known resource ID owned by Tenant B | Deny without returning resource content or sensitive existence metadata; use the API's documented denial semantics | Response, audit event, resource-boundary trace |
| TENANT-002 | Forged tenant selector | Tenant A user submits Tenant B ID in header, query, body and path variants | Server resolves membership from trusted state; forged selector cannot grant access | Requests and authorization decision traces |
| TENANT-003 | Membership revoked after session issue | Issue valid session, revoke tenant membership, then make a new protected request | New protected operation is denied according to the agreed revocation objective; login validity alone is insufficient | Revocation commit time and first denied request time |
| TENANT-004 | Stale cache/projection | Keep an intentionally stale positive membership projection after revocation | Stale projection alone cannot authorize protected access; failure mode is documented and fail-closed where current authorization cannot be established | Projection version, authoritative version, decision trace |
| TENANT-005 | Queued work after revocation | Enqueue an authorized sensitive job, revoke membership before worker execution, then release the job | Worker re-checks current authorization and denies/cancels/quarantines the operation; enqueue-time authorization is not permanent | Job lifecycle, authorization check, side-effect audit |
| TENANT-006 | Search/RAG stale index | Keep a revoked document's chunks in a test index, then query as the formerly authorized user | Revoked content/snippets/citations are not returned or passed to the model after authoritative revocation | Query result, candidate filtering, source re-authorization trace |
| TENANT-007 | Signed file link after revocation | Issue a signed file link, revoke access, then access the link | Behavior matches the documented link design and expiry/revocation objective; no unbounded bypass is allowed | Link issue/expiry, access response, file-boundary logs |
| TENANT-008 | Resource ACL revoked, membership active | Remove read ACL while leaving tenant membership active | Resource access is denied; tenant membership does not substitute for resource authorization | ACL version, response, policy decision |
| TENANT-009 | Duplicate/out-of-order events | Deliver duplicate and out-of-order membership lifecycle events | Consumers are idempotent, detect version regressions, and reconcile rather than restoring stale authorization | Event IDs/versions, consumer state, reconciliation logs |
| TENANT-010 | Authorization service unavailable | Make authoritative authorization unavailable during a protected read/action | No protected side effect occurs without a valid authorization result; response and retry policy are bounded and documented | Fault injection, response, side-effect audit |
| TENANT-011 | Tenant suspended | Suspend a tenant while sessions and queued work exist | New protected operations and delayed sensitive work are denied according to the suspension policy | Suspension version, API and worker traces |
| TENANT-012 | Resource identifier guessing | Request resources across tenant boundaries using sequential/random IDs | No cross-tenant disclosure; rate limits and audit policy apply as designed | Request corpus, responses, audit events |

## Measurement rules

- Define the revocation objective before testing. Report observed elapsed time from authoritative revocation commit to denial for each surface; do not invent an acceptable SLO in this document.
- Test both read and write/action paths. A denial response is insufficient if a side effect occurred.
- Check response bodies, logs, traces, metrics and model/tool inputs for leaked content or secrets.
- Repeat tests under normal conditions and under stale cache, delayed queue, retry, and dependency-outage conditions.
- Test each relevant surface separately: API, direct resource access, search/RAG, file delivery, background workers and tool execution.
- Preserve failed cases; do not weaken expected outcomes merely to obtain a pass.

## Decision dependencies

1. Product owner must settle the tenant/workspace model and canonical membership owner (ADR-0021).
2. Architecture must define authoritative checks, event versioning/reconciliation, cache behavior, queue re-authorization, signed-link semantics and revocation objectives.
3. The test environment must support safe fault injection and auditable evidence capture.
4. Implementation gate remains closed until the test design is approved and results are observed.

## Related documents

- `docs/TENANT_MEMBERSHIP_OWNER_DECISION_BRIEF.md`
- `docs/TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md`
- `docs/AUTHORIZATION_POLICY_GAP_AUDIT.md`
- `docs/research/GEMINI_ARCHITECTURE_REPORT_REVIEW.md`
- `docs/IMPLEMENTATION_GATE_BLOCKERS.md`
