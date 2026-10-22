# OpenAPI v1 Semantic Review Matrix — Draft

**Status:** Review findings only. The OpenAPI file is a proposal; no endpoint is implemented, approved, or validated by an OpenAPI parser.

## P0 — security-sensitive findings

| Area | Current draft observation | Risk | Required decision/remediation |
|---|---|---|---|
| Chat request roles | ChatMessage permits `system` and `developer` roles in the same schema used for client-supplied request messages. | A client may attempt to inject privileged instructions by submitting a system/developer message. | Split request and response message schemas. Client request roles should be limited to the explicitly allowed client roles (normally user, and possibly assistant only for a defined history-replay contract); trusted system/developer instructions must be server-owned. |
| Tenant resolution | No tenant field is required in request bodies, which is preferable to trusting client tenant IDs, but the identity/membership resolver is unspecified. | Services may disagree on which tenant context is authoritative or accidentally infer it from untrusted metadata. | Define a trusted tenant-resolution contract and require the API to validate membership/role for every tenant-scoped operation. Never accept body metadata as a grant. |
| Run creation | `CreateRunRequest.input` is an arbitrary object and agent-specific validation is deferred. | Oversized, unexpected, or unsafe data may reach an agent/tool boundary. | Require a versioned input schema per registered agent, payload size/depth limits, and server-side validation before scheduling. |
| Run status/result | `result` is an arbitrary object and may contain sensitive tool output or tenant data. | Output could leak data or expose internal execution details. | Define result/output schema, current authorization checks, redaction policy, and retention/deletion behavior before returning output. |
| Cancellation | The contract notes cancellation is not rollback, but no race/state-transition semantics are defined. | Callers may believe side effects were reversed or assume a terminal cancellation too early. | Define allowed state transitions, idempotency, race handling, and how the client observes the final state. |

## P1 — contract completeness findings

| Area | Current draft observation | Required action |
|---|---|---|
| Accepted run response | `POST /v1/runs` returns 202 without a JSON response schema. | Define the accepted response body, stable run identifier, and canonical Location semantics. |
| Cancellation response | `POST /v1/runs/{run_id}/cancel` returns 202 without a response schema. | Define whether the response returns current state, request ID, or only headers; document repeat behavior. |
| Chat response roles | The response reuses the request ChatMessage schema, which permits system/developer roles. | Use a response-specific schema and constrain the role to assistant for generated choices. |
| Error contract duplication | ErrorEnvelope is copied inline instead of referencing a single canonical contract source. | Decide whether the OpenAPI component is generated from the canonical JSON Schema or kept synchronized by a contract test; avoid manual drift. |
| Rate and size limits | Limits are mostly described as future decisions and are not represented as concrete bounds. | Decide endpoint-specific request byte, message count, input/output token, timeout, concurrency, and rate limits before implementation. |
| Streaming | The draft explicitly excludes streaming. | Confirm whether synchronous non-streaming chat is an intentional first vertical slice; if streaming is required, define SSE framing, terminal errors, disconnect and cancellation behavior before implementation. |
| Health semantics | One public `/v1/health` route combines health/readiness concepts. | Decide whether liveness and readiness are separate and which are exposed publicly; do not leak dependency details in readiness output. |
| Authentication scheme | Bearer/JWT is a placeholder without issuer, audience, claim, key rotation, session, or workload identity rules. | Resolve identity ADRs and document token validation and service-to-service authentication before treating security requirements as complete. |

## Review decision log

- **Do not approve as-is.** The client-controlled `system`/`developer` message-role issue is a concrete P0 contract defect.
- Preserve the existing baseline as a review artifact until route and identity semantics are reviewed; do not infer that the presence of the file makes it canonical.
- After decisions, revise the OpenAPI, validate it with an OpenAPI 3.1 validator, and add negative tests proving client messages cannot override server-owned instructions.
- Contract tests should also cover cross-tenant run reads, hidden-resource 404 behavior where required, invalid agent input, duplicate idempotency keys with matching/different payload fingerprints, and cancellation races.

## Verification status

This matrix is a manual reading of the current YAML text. No OpenAPI parser, validator, generated client, endpoint tests, or runtime security tests were run. The findings are design-review observations, not proof of exploitability in a running service.


## Follow-up correction — message-role draft fix (2026-10-22)

The OpenAPI YAML has now been edited to replace the shared message schema with separate `RequestChatMessage` and `ResponseChatMessage` schemas. Client request messages are constrained to role `user`; generated response messages are constrained to role `assistant`. This addresses the specific schema-level P0 finding in the draft. It is not yet validated by an OpenAPI parser, and runtime enforcement remains untested. See [OpenAPI contract test plan](OPENAPI_V1_CONTRACT_TEST_PLAN.md) for required positive and negative cases. The other findings in this review matrix remain open.
