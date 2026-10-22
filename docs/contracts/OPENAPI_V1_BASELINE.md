# OpenAPI v1 Baseline — Draft

**Status:** Proposal for review only. This is not an implemented API or approved production contract.

## File

- [openapi.v1.yaml](openapi.v1.yaml) — OpenAPI 3.1.0 document, draft API version 1.0.0-draft.

## Included provisional surfaces

- `GET /v1/health` — health/readiness placeholder.
- `POST /v1/chat/completions` — synchronous JSON text completion only.
- `POST /v1/runs` — proposed idempotent durable-run creation.
- `GET /v1/runs/{run_id}` — proposed run-status read.
- `POST /v1/runs/{run_id}/cancel` — proposed cancellation request.

The route names and request/response fields are candidate shapes to make review concrete, not accepted product decisions. Streaming, multimodal messages, tool execution APIs, conversation persistence, files, knowledge, model catalog, approvals, usage, and admin endpoints are deliberately not specified yet.

## Security and ownership constraints

- Bearer/JWT is a placeholder scheme, not a selected identity provider or a complete token-validation profile.
- Tenant identity and permissions must come from trusted authentication and membership state, not client-supplied body fields.
- The API delegates durable execution through orchestration and must not directly depend on agent/database implementation internals.
- Run status and output must be protected by current authorization; queued requests and cached/search projections are not permanent grants.
- Idempotency key retention, scope, request fingerprint, cancellation races, and side-effect semantics remain open.
- Error shape is aligned with the draft error envelope; code catalog mappings remain proposals.

## Review blockers before approval

1. Confirm public route surface and endpoint owners/consumers.
2. Decide authentication issuer/audience, session/BFF model, and service-to-service identity.
3. Define tenant/membership authority and resource-level authorization behavior.
4. Decide request size, token/output limits, timeouts, rate limits, and retry policy.
5. Define streaming protocol and disconnect/cancellation behavior if required.
6. Define agent-specific input schemas, run result shape, approval flow, and output retention.
7. Align error code/status/retryability mappings and field-path syntax.
8. Validate the OpenAPI document with an OpenAPI 3.1 validator; add positive/negative contract fixtures and consumer compatibility tests after semantic approval.

## Verification status

This file is authored as YAML text. No OpenAPI parser/validator, generated client, endpoint implementation, contract test, or runtime security test has been run. Do not treat its presence as proof of API validity or implementation.
