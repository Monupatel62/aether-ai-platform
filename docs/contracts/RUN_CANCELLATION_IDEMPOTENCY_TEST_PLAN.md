# Run Cancellation and Idempotency Test Plan — Draft

Status: proposed contract tests only; no validator or runtime tests have been run.

## Contract rules
- Cancellation is a request, not rollback or proof that the run is already cancelled.
- Durable run state is authoritative; queue messages and events are delivery mechanisms.
- Idempotency keys need an approved principal/tenant/operation scope, canonical request fingerprint, and retention period.
- Reuse with the same fingerprint must not create a duplicate run. Reuse with a different fingerprint must conflict.
- Workers must re-check authorization, approvals, resource versions, and cancellation before protected side effects.
- Run state transitions must be durable and versioned; consumers must deduplicate and reject stale events.

## Proposed cases
1. Identical create retry returns the original run.
2. Same key with different payload returns conflict and schedules no additional work.
3. Concurrent identical requests create one run.
4. Same key across different principals or tenants never reveals another run.
5. Key expiry follows a documented retry policy.
6. Cancellation while queued is observed before protected work starts.
7. Cancellation racing with worker start produces one legal state transition.
8. Cancellation during a non-interruptible action does not claim rollback.
9. Repeated cancellation is idempotent.
10. Cancellation after terminal state does not rewrite history.
11. Duplicate queue delivery does not execute a step twice.
12. Expired worker lease prevents the stale worker from committing.
13. Duplicate or stale run events do not roll state backward.
14. Version gaps or conflicting same-version events trigger reconciliation.
15. Crash between state persistence and event publication recovers without losing the event.
16. Crash after an external action uses downstream idempotency or explicit uncertain-outcome handling.
17. Revoked approval or access prevents a waiting run from executing.
18. Cross-tenant status/result requests do not expose run details.
19. Failed runs expose stable non-sensitive error codes only.
20. Failed durable cancellation persistence does not return a misleading success acknowledgement.
21. Dependency outages cannot trigger unsafe retries or permissive execution.
22. Expired/deleted results are not served from stale caches.
23. Concurrent success/cancellation commits preserve one legal terminal state.

## Decisions needed
- State machine and legal transitions, including uncertain external outcomes.
- Idempotency key scope, fingerprint, source of truth, retention and expiry behavior.
- Downstream idempotency and recovery behavior for each side-effecting tool/provider.
- Run version, worker lease/fencing, event publication and reconciliation rules.
- Cancellation guarantees per tool/provider; distinguish cooperative cancellation from rollback.
- Result authorization, redaction, retention/deletion and non-disclosing error behavior.
- OpenAPI 3.1 and JSON Schema Draft 2020-12 validators, format assertions and executable CI fixtures.

## Exit criteria
Run approved non-production tests for concurrency, crashes, duplicate/out-of-order messages, cancellation races, stale authorization, cross-tenant reads, and side-effecting tools. Schema parsing alone is insufficient. This draft does not approve implementation; the Phase 0 gate remains open.