# Authorization Context Trust Profile — Draft

**Status:** Proposed security contract for review; not approved or implemented.  
**Companion schema:** [authorization-context.schema.json](authorization-context.schema.json)  
**Related contracts:** [auth-context.schema.json](auth-context.schema.json), [Tenant Context Resolution Contract](TENANT_CONTEXT_RESOLUTION_CONTRACT.md).

## 1. Purpose and boundary

The authorization context is an internal representation of a previously evaluated allow decision. It is not an access token, does not authenticate its holder, and does not replace resource-owner enforcement. JSON Schema validates shape only; it cannot establish trusted origin, message integrity, freshness, current permissions, or non-replay.

## 2. Required trust properties

Before production use, the implementation must demonstrate all of the following:

1. **Trusted issuer:** only an explicitly authorized policy/API component may issue the context. The issuer identity and allowed consumers must be documented.
2. **Authenticated transport:** service-to-service calls use an approved workload identity and mutually authenticated transport or an explicitly approved equivalent. Network location alone is not trust.
3. **Integrity and binding:** the context is protected against modification and bound to the intended consumer/audience, request, principal, tenant, resource, action and decision. The signing/envelope mechanism remains an ADR decision.
4. **Short lifetime:** issued_at and expires_at are checked by the consumer. Reject future-issued contexts outside approved clock skew, expired contexts, invalid time ordering, and lifetimes exceeding the approved maximum for that operation class.
5. **Freshness:** consumers verify membership, resource ACL and policy versions against the canonical authorities or an approved freshness mechanism before protected/high-impact work. A version string alone does not prove that the version is current.
6. **Narrow scope:** a context for one resource/action cannot authorize another resource, action, tenant, principal, or consumer. Wildcard scope is not supported by this draft.
7. **Replay control:** contexts cannot be replayed across requests or consumers. For non-idempotent or high-impact actions, use a one-time decision/nonce or an equivalent server-side replay control.
8. **Revocation:** membership removal, ACL revocation, tenant suspension, policy changes and approval revocation invalidate affected decisions according to explicitly approved convergence bounds.
9. **Least privilege:** downstream services receive only the fields needed to enforce the decision. Do not pass the context to models, tools, external providers, or end users as prompt/content data.
10. **Safe telemetry:** logs may record decision ID, issuer/consumer identity, versions, outcome and correlation ID. Do not log bearer credentials, signatures, secrets or protected resource content.

## 3. Consumer verification sequence

1. Authenticate the calling workload and establish the expected issuer/consumer relationship.
2. Verify the context envelope's integrity and audience/consumer binding.
3. Validate the payload against the approved schema and reject unknown fields.
4. Validate issued_at, expires_at, allowed clock skew, and maximum lifetime.
5. Bind every decision field to the operation actually being executed: principal, tenant, resource type, resource ID and action.
6. Check the decision remains fresh enough under the approved membership/ACL/policy revision and revocation rules.
7. Enforce any approval reference against the exact action/resource and current approval status.
8. Reject on any mismatch or unavailable required authority; emit a sanitized denial event.
9. Re-evaluate at execution time for delayed jobs, retries, streaming steps and high-impact side effects.

## 4. Failure behavior proposal

| Failure | Proposed behavior |
|---|---|
| Missing, malformed or unknown-field context | Reject before protected work |
| Untrusted issuer, invalid integrity, wrong audience or consumer | Reject and emit a security event |
| Principal, tenant, resource or action mismatch | Reject; do not attempt to broaden scope |
| Expired, future-issued or overlong context | Reject; require fresh authorization |
| Stale or unverifiable membership/ACL/policy version | Fail closed for protected operations |
| Replay detected | Reject; do not repeat non-idempotent side effects |
| Authorization authority unavailable | Fail closed; safe dependency error where applicable |
| Approval missing, revoked, expired or action-mismatched | Reject; require a newly verified approval if policy allows |

These are proposed semantics and must be reconciled with the canonical error catalog and run lifecycle before approval.

## 5. Acceptance tests to implement later

| ID | Scenario | Required result |
|---|---|---|
| ACTX-001 | Valid context from approved issuer, matching audience/scope, fresh versions | Accept only for the bound operation |
| ACTX-002 | Client sends a syntactically valid context in a public API request | Ignore/reject as client authority; resolve authorization server-side |
| ACTX-003 | Context payload is modified after issuance | Integrity check fails before protected work |
| ACTX-004 | Context is issued by an unapproved workload | Reject |
| ACTX-005 | Context audience/consumer does not match caller | Reject |
| ACTX-006 | Action or resource ID differs from the authorized scope | Reject |
| ACTX-007 | Context is expired, future-issued beyond allowed skew, or exceeds maximum lifetime | Reject |
| ACTX-008 | Membership/ACL/policy version is stale or cannot be verified | Reject or reauthorize before execution |
| ACTX-009 | Same context is replayed for a non-idempotent operation | Replay control prevents duplicate side effect |
| ACTX-010 | Approval reference is revoked or bound to another action/resource | Reject |
| ACTX-011 | Context is reused after tenant suspension or membership removal | Reject under the approved revocation bound |
| ACTX-012 | Authorization service is unavailable and cache is beyond approved freshness | Fail closed |
| ACTX-013 | Context is passed to a model/tool/provider payload | Boundary test proves the context is not exposed |
| ACTX-014 | Audit logging processes a rejected context | No credentials, signatures, or protected content appear in ordinary logs |

## 6. Decisions required before implementation

- Choose the workload identity and authenticated service-to-service transport profile.
- Choose the integrity envelope/signature mechanism, issuer identifiers, key rotation and audience rules.
- Approve maximum context lifetime and clock-skew tolerance by operation class.
- Define revision semantics, freshness checks, revocation convergence and cache limits.
- Decide replay-control requirements by action idempotency and impact.
- Define whether a context is carried as an in-memory internal object or across a signed message boundary; do not serialize it to user-controlled storage.
- Align errors, audit event fields, approval semantics and background-run reauthorization.
- Assign schema owner, issuer, consumers and compatibility/version policy.

## 7. Verification status

This is a design artifact. No transport profile, signing scheme, validator, integration test, runtime test, or security certification has been implemented or executed. The schema and this profile must be reviewed together; neither alone proves authorization.
