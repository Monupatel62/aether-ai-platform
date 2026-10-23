# OpenAPI v1 Contract Test Plan — Draft

**Status:** Test design only. No endpoint implementation exists and these cases have not been executed.

## P0 message-role regression tests

| ID | Input/condition | Expected result | Security purpose |
|---|---|---|---|
| MSG-001 | Chat request message with role `user` and non-empty text | Schema accepts | Baseline valid client message |
| MSG-002 | Chat request message with role `system` | Schema rejects | Client cannot set privileged instructions |
| MSG-003 | Chat request message with role `developer` | Schema rejects | Client cannot set developer instructions |
| MSG-004 | Chat request message with role `assistant` | Schema rejects under current user-only request draft | Prevent unreviewed history-replay semantics |
| MSG-005 | Generated response message with role `assistant` | Schema accepts | Baseline assistant response |
| MSG-006 | Generated response message with role `system` or `developer` | Schema rejects | Output role remains constrained |
| MSG-007 | Missing content, empty content, extra message properties | Schema rejects | Enforce required fields and reject unknown fields |

## Accepted-response contract tests

| ID | Scenario | Expected behavior |
|---|---|---|
| RESP-001 | Run creation accepted | HTTP 202 includes `run_id`, `status: queued`, and `request_id`; `Location` identifies the run resource. |
| RESP-002 | Cancellation accepted | HTTP 202 includes `run_id`, `status: cancellation_requested`, and `request_id`; response does not imply cancellation has completed. |
| RESP-003 | Accepted response has missing or unexpected fields | Schema rejects missing required fields and extra properties. |

These response shapes are provisional draft proposals and require review; tests are not executed.

## API authorization and lifecycle tests

| ID | Scenario | Expected behavior |
|---|---|---|
| AUTH-001 | Missing/invalid bearer token on protected endpoint | Safe 401 error envelope; no token details |
| AUTH-002 | Authenticated principal has no access to a run | Deny access; return 404 instead of 403 if resource-concealment policy requires it |
| AUTH-003 | Caller submits a tenant ID in metadata | Metadata grants no tenant access; server derives tenant from trusted membership state |
| RUN-001 | Run creation with an unknown agent ID | Safe validation/not-found response; no execution scheduled |
| RUN-002 | Run input contains unknown or disallowed fields for that agent | Rejected before queueing |
| RUN-003 | Same idempotency key and same request fingerprint repeated | One durable run; response semantics are consistent and documented |
| RUN-004 | Same idempotency key reused with a different request fingerprint | 409 conflict; second request does not execute |
| RUN-005 | Run result requested after access revocation | Current authorization denies access even if cached output remains |
| RUN-006 | Cancellation races with success/failure transition | One documented terminal state; no claim that external side effects were rolled back |
| ERR-001 | Internal dependency returns secret-bearing error payload | Public response is redacted; secret is not copied to ordinary logs |
| LIMIT-001 | Request exceeds configured byte/token/message limit | Rejected before expensive processing with documented safe error |

## Fixture and execution rules

- Store minimal synthetic fixtures only; do not use customer data, credentials, real prompts, or production identifiers.
- Validate OpenAPI 3.1 structure before using generated clients or treating fixtures as authoritative.
- Validate schema-level cases separately from HTTP/runtime tests; an OpenAPI schema rejection does not prove server enforcement.
- For negative authorization tests, use at least two synthetic tenants and verify no cross-tenant metadata, outputs, citations, files, or error details leak.
- Test idempotency persistence, retries, cancellation races and revocation using controlled fakes before any live provider integration.
- Record tool/version, command, exact result, and commit SHA in the work log when validation is actually run. Do not mark tests passing before execution.

## Current status

- Message request/response schemas were revised in the draft OpenAPI to restrict client request messages to role `user` and generated response messages to role `assistant`.
- No OpenAPI validator, schema fixture runner, generated client, endpoint test, or runtime security test has been run.


## Internal authorization-context trust tests

See [AUTHORIZATION_CONTEXT_TRUST_PROFILE.md](AUTHORIZATION_CONTEXT_TRUST_PROFILE.md) for the full proposed ACTX-001 through ACTX-014 acceptance set. These tests cover trusted issuer and consumer binding, integrity, exact principal/tenant/resource/action scope, expiry, version freshness, replay, approval revocation, fail-closed dependency behavior, model/tool boundary leakage, and safe audit logging. They are test requirements only and have not been executed.


## Draft JSON Schema conditional cases added — 2026-10-23

The shared fixture file now contains 19 author-defined cases. Five added cases cover required `step_id` on step events, `attempt` and `not_before` on retry scheduling, and `failure_code` on failed run/step events. These cases are authored but not executed. The event envelope payload and tool argument objects also have a `maxProperties: 100` draft limit; transport byte and nesting-depth limits remain separate decisions.
