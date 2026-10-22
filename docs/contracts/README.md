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

## Additional draft artifacts

- [Schema semantic review](SCHEMA_SEMANTIC_REVIEW.md): prioritizes contract gaps and separates schema validation from runtime security invariants.
- [Public error code catalog](ERROR_CODE_CATALOG.md): proposed codes and HTTP/retry mappings; not approved for service use.

## Current semantic review highlights

- Tool arguments and generic event payloads remain unconstrained nested objects until concrete per-tool and per-event schemas are designed.
- Tenant, actor, step, retry and failure metadata may need conditional requirements by operation/event type.
- Format assertions, event authentication, deduplication, ordering, replay resistance and execution-time authorization require explicit validation or runtime controls beyond JSON syntax.
- These findings are proposals, not final contract decisions.


## Versioned API baseline

- [OpenAPI v1 baseline](openapi.v1.yaml): provisional OpenAPI 3.1.0 document for health, synchronous text completion, durable run creation/status, and cancellation.
- [OpenAPI baseline review notes](OPENAPI_V1_BASELINE.md): endpoint scope, unresolved security/product decisions, and verification limitations.

The routes and fields are review candidates only. No OpenAPI validation or runtime implementation is claimed.


## OpenAPI review findings

- [OpenAPI v1 semantic review matrix](OPENAPI_V1_REVIEW_MATRIX.md) records P0/P1 review findings. Important: the current draft reuses a message schema that permits client-supplied system/developer roles; separate request/response schemas are required before approval.


## Tenant context and authorization contract

- [Tenant Context Resolution Contract](TENANT_CONTEXT_RESOLUTION_CONTRACT.md): proposed trusted tenant-resolution sequence, fail-closed behavior, versioning requirements, and negative acceptance cases. Membership ownership and cache/revocation thresholds remain open; no tests have been executed.

## OpenAPI role-schema remediation and test plan

- [OpenAPI v1 contract test plan](OPENAPI_V1_CONTRACT_TEST_PLAN.md): proposed positive/negative message-role, authorization, idempotency, revocation, cancellation, and limit cases; none have been executed.
- The draft OpenAPI uses separate request/response message schemas (`user` input, `assistant` output) and now defines provisional JSON bodies for accepted run creation and cancellation. These are draft-only changes; parser validation and runtime enforcement remain unverified.
