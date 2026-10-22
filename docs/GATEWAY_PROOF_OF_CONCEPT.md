# Aether AI — Gateway Proof of Concept Plan

**Status:** plan only; no gateway code or production service has been created.  
**Decision supported:** ADR-0005 — DIAL Core vs DevKit provider path vs hybrid.

## Goal

Use the same small set of test cases to compare an Aether-owned gateway contract backed by (A) DIAL Core and (B) WoHo AI DevKit/provider adapters. Decide whether one implementation is sufficient or whether a hybrid is justified by measured requirements.

## Non-goals

- No production deployment, billing integration, user data, or production provider credentials.
- No adoption of DIAL Chat as the product UI in this experiment.
- No edits to WoHo AI DevKit source, main branch, release pipeline, or package versions.
- No implementation of the full 33-repository system.

## Test environment

- Aether-owned minimal test harness, isolated from production.
- Mock provider for deterministic baseline; one non-production provider only if credentials and terms are approved.
- DIAL Core launched only in an isolated local/dev environment with minimal test configuration.
- Explicitly pinned package/container versions; record image/package digests, config and test commit.
- Synthetic prompts and tool results only. No real user data.

## Contract under test

The Aether gateway contract must define:

- Request: model/deployment ID, messages/input, supported response format/tool schema, request ID, tenant/principal context from trusted server middleware, cancellation signal, and policy-approved limits.
- Capability metadata: chat, streaming, tool calls, structured output, embeddings, and any provider-specific feature with an explicit support flag.
- Streaming events: start, text/content delta, tool-call delta if supported, usage where available, terminal finish reason, normalized error, and cancellation.
- Result: normalized content, tool calls, usage (with source/estimated marker), finish reason, provider/deployment metadata, and trace/request IDs.
- Errors: stable category/code, retryable flag, safe public message, upstream status when safe, and internal correlation ID; never expose raw credentials or provider response bodies by default.
- Policy: allowed deployment, tenant quota, rate/concurrency limits, timeout, input/output/token budgets, and provider data-handling constraints.

## Test scenarios

| ID | Scenario | Evidence required |
|---|---|---|
| G-01 | Mock non-streaming completion | Normalized response equals expected fixture. |
| G-02 | Streamed completion | Ordered events, exactly one terminal event, clean close. |
| G-03 | Client cancellation | Upstream request aborts when supported; no runaway stream remains. |
| G-04 | Timeout | Stable timeout error; bounded cleanup; no unbounded retry. |
| G-05 | Rate limit / 429 | Correct error classification and bounded retry policy; no duplicate side effects. |
| G-06 | Upstream 5xx / malformed response | Safe normalized error; no secret or raw sensitive body in logs. |
| G-07 | Tool call / structured output | Supported shape preserved or explicitly rejected as unsupported. |
| G-08 | Usage accounting | Provider-reported usage preserved; missing usage clearly marked unknown/estimated. |
| G-09 | Capability mismatch | Request fails safely or explicit compatible route selected; no silent behavior downgrade. |
| G-10 | Tenant/model denial | Request rejected before upstream call; audit event contains safe metadata. |
| G-11 | Secret redaction | Canary API key never appears in logs/traces/errors/client output. |
| G-12 | Provider outage | Bounded retries; fallback only if privacy, tool capability and cost constraints are equivalent. |
| G-13 | Embeddings | If needed for initial RAG scope, vector dimensions, batching, usage and errors are normalized. |
| G-14 | MCP interaction boundary | Gateway is not permitted to bypass the Aether tool registry; MCP tests are handled by the separate MCP compatibility harness. |

## Measurement record

For each path, record:

- Setup steps and operator time.
- Exact versions/digests and license inventory.
- p50/p95 latency from repeated synthetic requests (do not invent values; capture measurements).
- Streaming correctness and cancellation behavior.
- Memory/CPU footprint and failure recovery behavior.
- Supported features and unsupported cases.
- Retry ownership and whether retries can duplicate billable/side-effecting work.
- Logs/traces captured and evidence that sensitive payloads are redacted.
- Deployment complexity, upgrade process and on-call ownership.

## Decision rule

- Choose **DevKit path** if it meets the required capability matrix with materially lower integration/operational cost and Aether can enforce quotas, authorization and provider policies outside it.
- Choose **DIAL Core** if its model/deployment governance and provider coverage solve requirements that outweigh the additional Java runtime and operations.
- Choose **hybrid** only if measured, documented use cases need both and the stable contract prevents policy drift; otherwise do not pay the cost of two upstream paths.
- Defer any option that fails authorization, secret-redaction, cancellation, or tenant-isolation tests regardless of latency.

## Deliverables

1. Reproducible test harness and fixtures.
2. Test run logs with redacted configuration and versions/digests.
3. Completed scenario table and measurement record.
4. Dependency/license/SBOM report for exact artifacts.
5. ADR-0005 with chosen option, rejected alternatives, consequences, affected repos, rollback/migration plan and reviewer.

## Links

- [DIAL adoption evaluation](DIAL_ADOPTION_EVALUATION.md)
- [DevKit compatibility review](DEVKIT_COMPATIBILITY_REVIEW.md)
- [Dependency matrix](DEPENDENCY_MATRIX.md)
- [Security threat model](SECURITY_THREAT_MODEL.md)
