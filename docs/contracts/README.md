# Contract Schemas — Draft Registry

**Status:** Draft for review only. No schema in this directory is approved as a production contract.

## Purpose

This directory holds machine-readable starting points for cross-repository contracts. These drafts must be reviewed against the unresolved identity, tenant-membership, authorization, data-retention and runtime-topology decisions before implementation.

## Draft schemas

- `error.schema.json`: stable public error envelope; must not include raw upstream errors or secrets.
- `event-envelope.schema.json`: common event metadata for asynchronous integration.
- `auth-context.schema.json`: verified principal and request context passed after authentication; it is not a client-supplied authorization assertion.
- `tool-invocation.schema.json`: bounded tool invocation request with explicit scope and approval references; execution must still re-authorize at the policy boundary.
- `run-event.schema.json`: draft durable run/step lifecycle events and idempotency metadata.
- `resource-change-event.schema.json`: draft ACL/revocation/deletion lifecycle events for search, RAG, cache and other projections.

## Mandatory implementation rules

1. Validate every payload at trust boundaries; reject unknown fields where security-sensitive.
2. Derive principal and tenant context from trusted authentication/membership state, never from untrusted request body fields alone.
3. Authorization is resource/action-specific and must be rechecked at execution time; queued payloads are not permanent grants.
4. Event consumers must be idempotent and must define retry, ordering and dead-letter behavior.
5. Redact secrets and sensitive prompt/content data from ordinary errors, logs and traces.
6. Schema changes require consumer inventory, compatibility tests, migration notes and a reviewed versioning decision.
7. These schemas are draft design artifacts; they do not certify compliance or prove runtime enforcement.

## Acceptance checklist

- [ ] Owners and consumers approved.
- [ ] Authentication, tenant and resource authorization rules approved.
- [ ] Positive, malformed-input and cross-tenant negative fixtures added.
- [ ] Compatibility/version policy approved.
- [ ] Retry/idempotency behavior reviewed for events and side effects.
- [ ] Privacy, retention, deletion and telemetry implications reviewed.
- [ ] Validation is wired into CI only after explicit implementation approval.
