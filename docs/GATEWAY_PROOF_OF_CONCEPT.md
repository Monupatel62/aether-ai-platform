# Aether AI — Gateway Proof of Concept Plan

**Status:** plan only; no gateway code or production service has been created.  
**Decision supported:** ADR-0005 — Aether-owned gateway vs AI DIAL Core vs a measured hybrid.

## Goal

Compare an Aether-owned gateway implementation with AI DIAL Core behind the same Aether-owned contract. Decide whether one path meets the requirements or whether a hybrid is justified by measured evidence. Any provider adapter must be native to Aether AI or an independently reviewed, explicitly approved dependency.

## Non-goals

- No production deployment, billing integration, user data, or production provider credentials.
- No adoption of AI DIAL Chat as the product UI in this experiment.
- No implementation of the full 33-repository system.
- No assumption that an external project is a dependency merely because it is mentioned in research.

## Test environment

- Aether-owned minimal test harness, isolated from production.
- Mock provider for deterministic baseline; one non-production provider only if credentials and terms are approved.
- AI DIAL Core launched only in an isolated local/dev environment with minimal test configuration, if selected for comparison.
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
| G-14 | MCP interaction boundary | Gateway cannot bypass the Aether tool registry; protocol-specific tests remain in the Aether MCP compatibility harness. |

## Measurement record

For each path, record:

- Setup steps and operator time.
- Exact versions/digests and license inventory.
- p50/p95 latency from repeated synthetic requests (capture measurements; do not invent values).
- Streaming correctness and cancellation behavior.
- Memory/CPU footprint and failure recovery behavior.
- Supported features and unsupported cases.
- Retry ownership and whether retries can duplicate billable/side-effecting work.
- Logs/traces captured and evidence that sensitive payloads are redacted.
- Deployment complexity, upgrade process and on-call ownership.

## Decision rule

- Choose an **Aether-owned gateway** if it satisfies the required capability and security matrix at an acceptable maintenance and operational cost.
- Choose **AI DIAL Core** if its model/deployment governance and provider coverage outweigh the additional runtime and operations, and the security/tenant policy boundary remains enforceable.
- Choose a **hybrid** only if measured use cases need both and the stable contract prevents policy drift; otherwise avoid the additional operational cost.
- Defer any option that fails authorization, secret-redaction, cancellation, or tenant-isolation tests regardless of latency.

## Deliverables

1. Reproducible test harness and fixtures.
2. Test run logs with redacted configuration and versions/digests.
3. Completed scenario table and measurement record.
4. Dependency/license/SBOM report for exact artifacts.
5. ADR-0005 with chosen option, rejected alternatives, consequences, affected Aether repositories, rollback/migration plan and reviewer.

## Links

- [DIAL adoption evaluation](DIAL_ADOPTION_EVALUATION.md)
- [Dependency matrix](DEPENDENCY_MATRIX.md)
- [Security threat model](SECURITY_THREAT_MODEL.md)
