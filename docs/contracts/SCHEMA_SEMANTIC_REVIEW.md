# Draft Contract Schema Semantic Review

**Status:** Design review, not approval. This review covers the seven JSON schema files currently listed in docs/contracts/. Their JSON syntax has been parsed, but a JSON Schema Draft 2020-12 validator with format assertions and runtime contract tests have not been run.

## Findings and required disposition

| Priority | Schema | Finding | Proposed action |
|---|---|---|---|
| P0 | authorization-context.schema.json | The shape can express an allow decision and version strings, but cannot prove issuer trust, integrity, audience binding, expiry enforcement, freshness, replay resistance, or current authorization. | Review AUTHORIZATION_CONTEXT_TRUST_PROFILE.md alongside this schema; select and approve the transport/integrity, issuer/audience, lifetime, revision freshness, revocation and replay profiles before implementation. Never accept it as a client grant. |
| P0 | auth-context.schema.json | tenant_id is optional, but some protected operations may require an unambiguous tenant context. | Define when tenant context is mandatory; validate membership server-side and do not treat this object as an authorization grant. |
| P0 | tool-invocation.schema.json | arguments accepts an arbitrary object with no size/depth bound; resource scope and approval reference are optional. | Define per-tool argument schemas and payload limits. Require resource scope/approval conditionally based on tool risk. Re-authorize at execution time. |
| P0 | event-envelope.schema.json | Generic payload is an unconstrained object and tenant/principal metadata are optional. | Use event-type-specific payload schemas and classify which events require tenant scope. Never rely on envelope metadata alone for authorization. |
| P0 | run-event.schema.json | step_id, attempt, and failure_code are optional for all event types; lifecycle-specific requirements are not encoded. | Add conditional requirements for step events, retry events, and failed events; define ordering and duplicate-delivery semantics. |
| P0 | resource-change-event.schema.json | acl_version is conditional only for ACL-changed and access-revoked; actor/tenant metadata are optional. | Decide required audit metadata per event type and require monotonic version semantics for ACL changes. Deletion events must not imply access is already denied unless authoritative policy says so. |
| P1 | error.schema.json | details.field and details.reason are unconstrained strings beyond length; there is no catalog constraint on error.code. | Adopt the draft error catalog, define field-path syntax, and keep reasons safe/non-sensitive. |
| P1 | Date-time formats | Several schemas use format: date-time; JSON Schema implementations may treat format as annotation unless assertion is configured. | Require format assertion in the chosen validator and test malformed timestamps explicitly. |
| P1 | Event identity | Length/pattern constraints do not establish uniqueness, authenticity, ordering, or replay resistance. | Define producer authentication, deduplication storage/window, replay handling, and aggregate/run version checks outside JSON Schema. |
| P1 | Unknown fields | Top-level objects mostly reject additional properties, but generic nested payload/arguments objects allow arbitrary keys. | Reject unknown fields inside each concrete event/tool payload schema once those schemas are defined. |
| P1 | Identifier semantics | IDs are plain strings with limited shape checks; tenant/resource IDs can be confused across systems if namespaces are not defined. | Define opaque ID ownership, normalization, case sensitivity, and cross-service namespace rules. |

## Event envelope and revocation follow-up — 2026-10-23

Added [Event Envelope and Resource Revocation Test Plan](EVENT_ENVELOPE_REVOCATION_TEST_PLAN.md) with proposed cases for producer authentication, event-type authorization, tenant/actor claims, duplicate and out-of-order delivery, aggregate/ACL versions, lifecycle transitions, and revocation across caches, search/RAG, queued jobs, and tool execution. The plan deliberately leaves event-specific required-field policy and version/replay thresholds as owner decisions. No validator or runtime tests were run; the P0 schema and consumer-semantics gate remains open.

## Invariants JSON Schema cannot enforce by itself

- A client cannot author trusted authentication context or self-assert a tenant, role, scope, authorization decision, or approval.
- An authorization-context object is only a decision record; trust requires authenticated issuer/consumer binding, integrity, bounded lifetime, exact operation scope, current authorization versions and replay/revocation controls outside JSON Schema.
- Every tool execution must re-check current authorization, approval binding, resource version, and idempotency.
- Event producers must be authenticated; consumers must deduplicate, handle out-of-order delivery, and reject stale state transitions.
- Revocation must take effect at the authoritative authorization boundary before asynchronous cache/search/RAG cleanup completes.
- Error messages, event payloads, arguments, traces, and logs must follow data minimization and redaction policy.
- Schema validity does not establish correct runtime behavior, tenant isolation, privacy compliance, or security certification.

## Fixture coverage (draft)

`contract-fixtures.v1.json` contains 19 author-defined examples: the original valid/invalid pair for each of the seven schema files plus five conditional run-event cases. The invalid examples target a required-field omission, unknown property, unsupported enum value, or conditional requirement. These are fixture definitions only; no JSON Schema validator has executed them yet. Before treating this set as a gate, run it with a Draft 2020-12 validator configured to assert `format`, review each validator result, and add boundary cases for malformed timestamps, unknown nested fields, and conditional event semantics.

## Review gate

Before approval, assign an owner and consumer list to every contract; decide tenant/ACL authority and event semantics; add valid and invalid fixtures; run a Draft 2020-12 validator with format assertions; and run consumer compatibility tests in CI after explicit implementation approval.

## Current verification status

- JSON syntax: parsed successfully for all seven schema files in the current focused check; this is not JSON Schema validation.
- Draft-only hardening: bounded generic event payload and tool argument object property counts to 100; added conditional requirements for step events, retry scheduling, and failed run/step events.
- JSON Schema semantic validation: not run.
- Positive/negative fixtures: 19 author-defined cases added in `contract-fixtures.v1.json`; not executed or validator-verified.
- Runtime enforcement and security tests: not run.
- Production contract approval: none.


## 2026-10-23 follow-up check

- Parsed the seven contract schema JSON files, the fixture JSON, and the package graph as JSON: all nine parsed successfully.
- Fixture integrity check: 19 unique case IDs; all fixture schema references resolve to one of the seven contract schemas.
- Manually evaluated the five newly added run-event conditional cases against the draft conditional rules: all five expected outcomes matched.
- This was a focused JavaScript check of JSON syntax, fixture references, and the new conditions only. It was not a JSON Schema Draft 2020-12 validator run, did not assert `format`, and did not validate OpenAPI YAML or runtime behavior.
