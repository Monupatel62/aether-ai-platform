# Identity, Session, Tenant and Authorization POC Test Matrix

**Date:** 2026-10-23  
**Status:** Proposed acceptance plan; not executed and not an approval to implement production authentication.  
**Scope:** Aether-owned contract tests for the identity-provider shortlist and authorization boundary.

## Purpose

Turn the open identity and authorization decisions into observable pass/fail tests. Run the same cases against one managed OIDC candidate and one self-hosted candidate. Do not select a vendor from feature claims alone. Record exact versions, configuration, test evidence, failures, operational effort and cost assumptions.

## Preconditions

Before running a POC, the owner must approve:
- test environment and data classification;
- the canonical tenant/workspace membership owner;
- supported login and workload-identity flows;
- session and revocation targets;
- the trust profile for internal authorization context;
- who may approve privileged/support access.

Use synthetic users and tenants only. No production credentials, customer data, or production deployment.

## Required test identities

- User A: active member of Tenant A, ordinary role.
- User B: active member of Tenant B, ordinary role.
- User C: removed from Tenant A during a test.
- Tenant A Owner and Tenant A Admin.
- Service principal scoped to one named API audience and one allowed action.
- Platform operator without implicit access to tenant content.
- Support operator with no active grant, then a short-lived approved grant.

## Test cases and acceptance criteria

| ID | Test | Pass condition |
|---|---|---|
| ID-01 | OIDC issuer and audience validation | Tokens from an unapproved issuer or wrong audience are rejected. |
| ID-02 | Signature and key rotation | Invalid signatures are rejected; rotation succeeds without accepting revoked/unknown keys beyond the documented overlap. |
| ID-03 | Expiry and clock skew | Expired tokens and tokens outside approved clock skew are rejected. |
| ID-04 | Login callback state and nonce | Missing, mismatched, replayed state or nonce is rejected. |
| ID-05 | Authorization code flow | Redirect URI mismatch and code replay fail; PKCE is enforced where required by the selected flow. |
| ID-06 | Browser session cookie | Session cookie is Secure, HttpOnly and appropriately SameSite; session identifiers rotate after authentication and privilege changes. |
| ID-07 | CSRF and origin checks | Cross-site state-changing requests without valid anti-CSRF/origin protections are rejected. |
| ID-08 | Logout and revocation | Logout invalidates the server-side session; the observed revocation delay is measured and meets the approved target. |
| TEN-01 | Client-supplied tenant selector | A user cannot gain access by changing a tenant ID in path, query, header or request body. |
| TEN-02 | Membership removed mid-session | Subsequent protected operations fail within the approved revocation bound. |
| TEN-03 | Stale membership authority | If membership authority is unavailable or freshness cannot be established, protected actions fail closed. |
| AUTH-01 | Deny-by-default | Unknown role/action/resource combinations are denied. |
| AUTH-02 | Resource-level checks | Read, list, search, export, stream, tool, background-job and result-read paths each enforce authorization. |
| AUTH-03 | Cross-tenant isolation | Tenant A principal cannot read, mutate, infer existence of, or retrieve Tenant B resources through direct IDs or search. |
| AUTH-04 | Role escalation | A user cannot grant themselves a role or alter their own membership/owner status. |
| AUTH-05 | Support access | Support access requires an approved reason-bound, time-limited grant; every use is audited and expires automatically. |
| AUTH-06 | Operator separation | Platform operator permissions do not implicitly authorize customer-content reads. |
| CTX-01 | Authorization context integrity | Modified or unsigned/untrusted internal context is rejected. |
| CTX-02 | Audience and scope binding | A context issued for one consumer, principal, tenant, resource or action cannot authorize another. |
| CTX-03 | Expiry and freshness | Expired context or stale membership/ACL/policy version is rejected. |
| CTX-04 | Replay | Reuse of a one-time context for a non-idempotent/high-impact action is rejected. |
| CTX-05 | Revocation | Membership, ACL, tenant suspension and approval revocation take effect within their approved bounds. |
| WORK-01 | Workload identity | Service principal is authenticated, audience-bound and restricted to explicit least-privilege actions. |
| WORK-02 | Credential rotation | Rotated/revoked workload credentials are handled within the approved overlap and revocation targets. |
| OBS-01 | Audit trail | Security events identify actor, tenant, action, resource class, decision and reason code without logging tokens, secrets or raw prompts by default. |
| FAIL-01 | Dependency outage | Identity, membership or policy dependency outage fails closed for protected actions and produces safe, useful operational signals. |

## Evidence to record

For each test: case ID, provider and version, configuration commit, timestamp, steps, expected result, observed result, sanitized logs, pass/fail, defect reference, owner and retest result. Capture latency and measured revocation delay rather than asserting them from configuration.

## Decision gates

1. All security-critical cases must pass or have an explicitly accepted, time-bounded risk.
2. Cross-tenant negative tests must pass before any integration with real data.
3. The canonical membership owner and authorization-context trust profile must be accepted before freezing dependent schemas.
4. Compare provider operational burden, upgrade/rotation behavior, portability, data residency, pricing/plan restrictions and failure recovery using evidence.
5. Record the outcome in the relevant ADRs. A passing POC does not by itself approve production deployment.

## Related documents

- [Identity and tenant security evaluation](IDENTITY_AND_TENANT_SECURITY_EVALUATION.md)
- [Identity provider shortlist and scorecard](IDENTITY_PROVIDER_SHORTLIST_AND_SCORECARD.md)
- [Browser session and authorization architecture](BROWSER_SESSION_AND_AUTHORIZATION_ARCHITECTURE.md)
- [Authorization permission matrix](AUTHORIZATION_PERMISSION_MATRIX.md)
- [Tenant membership and ACL consistency decision](TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md)
- [Authorization context trust profile](contracts/AUTHORIZATION_CONTEXT_TRUST_PROFILE.md)
- [Implementation gate blockers](IMPLEMENTATION_GATE_BLOCKERS.md)
