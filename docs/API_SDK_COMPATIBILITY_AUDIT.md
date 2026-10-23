# API and SDK Contract Versioning & Compatibility Audit — 33 Repositories

**Date:** 2026-10-23  
**Status:** Documentation audit only. No API or SDK contract is approved by this report.  
**Scope:** All 33 canonical repositories and the central OpenAPI/dependency design documents.

## Executive result

The repository specifications frequently require a “typed/versioned interface” and a “compatibility policy,” but this is generally a baseline requirement rather than an actionable policy. The text scan found explicit `compatibility policy` language in 21 of 33 specifications; 12 did not contain that exact phrase. This is a keyword/section scan, not proof that the 21 have a complete compatibility policy. Only `aether-ai-plugins` in the scan contained explicit breaking-change/deprecation-window/compatibility-matrix wording; it still needs concrete policy details and evidence. The central OpenAPI review explicitly says the draft is not parsed/validated and no generated client or endpoint tests have run.

## Repository-by-repository documentation scan

“Phrase present” means the specification contains explicit compatibility-policy language; it does not mean the policy is complete. “Missing” means the scan did not find the phrase and should trigger a targeted review, not a claim that no relevant material exists elsewhere.

| Repository | Explicit compatibility-policy phrase | Follow-up |
|---|---|---|
| `aether-ai-platform` | Present | Define central policy owner and gate; control plane remains documentation-only. |
| `aether-ai-web` | Present | Define supported API versions, generated-client pinning, and behavior for unknown response fields. |
| `aether-ai-api` | Present | Define OpenAPI compatibility rules, error envelope stability, pagination/idempotency semantics, and deprecation. |
| `aether-ai-gateway` | Present | Version provider-neutral capability/request/response contracts and fallback/error semantics. |
| `aether-ai-providers` | Present | Define adapter contract version, capability negotiation, provider-specific error mapping, and conformance fixtures. |
| `aether-ai-agents` | Present | Version agent input/output and tool-call contracts; keep durable run ownership with Orchestration. |
| `aether-ai-workflows` | Present | Define workflow schema versions, migration rules, unknown-field behavior, and validation compatibility. |
| `aether-ai-orchestration` | Present | Version run/step events and APIs; specify idempotency, cancellation, replay, and persisted-state migration. |
| `aether-ai-tools` | Present | Version tool manifest/input/output/error/approval contracts and require per-tool schema compatibility tests. |
| `aether-ai-mcp` | Present | Define MCP protocol-version negotiation and mapping to the stable internal tool contract. |
| `aether-ai-memory` | Present | Specify memory record/schema evolution, export/deletion compatibility, and authorization metadata migrations. |
| `aether-ai-rag` | Present | Version retrieval request/result and source/citation/ACL metadata contracts. |
| `aether-ai-files` | Present | Define upload/download metadata, content-type/size limits, signed-link behavior, and lifecycle-event compatibility. |
| `aether-ai-knowledge` | Present | Version source/collection/ACL contracts and deletion/revocation event semantics. |
| `aether-ai-auth` | Present | Version identity/session claims and token/session lifecycle contracts; coordinate with unresolved membership authority. |
| `aether-ai-security` | Present | Version authorization decision/context contracts and fail-closed semantics; do not treat shape validation as trust. |
| `aether-ai-admin` | Present | Define admin API and permission-matrix compatibility; UI role changes must not widen server authority. |
| `aether-ai-billing` | Present | Version trusted usage events, idempotency keys, pricing/entitlement snapshots, and invoice-state transitions. |
| `aether-ai-sdk` | Present | Add explicit package SemVer rules, supported server API range, generated-client provenance, and breaking-change policy. |
| `aether-ai-evaluations` | Present | Version evaluation dataset/result formats and metrics so historical results remain interpretable. |
| `aether-ai-observability` | Missing | Add telemetry/event schema compatibility rules and retention/redaction behavior across versions. |
| `aether-ai-deployment` | Missing | Define deployment manifest/config schema versioning and backward/forward compatibility across rollout/rollback. |
| `aether-ai-docs` | Missing | Define how published contract references are versioned, validated, and kept aligned with source contracts. |
| `aether-ai-database` | Missing | Define migration compatibility, expand/contract sequencing, rollback limits, and schema/API ownership. |
| `aether-ai-queue` | Missing | Define event envelope versioning, consumer tolerance, replay behavior, and producer/consumer rollout order. |
| `aether-ai-cache` | Missing | Define cache key/schema versioning, invalidation on contract changes, and safe stale-entry handling. |
| `aether-ai-search` | Missing | Define indexed-document/query schema versions, rebuild requirements, and compatibility during projection rollout. |
| `aether-ai-plugins` | Present | Specify manifest SemVer, breaking-change/deprecation windows, compatibility matrix, and disabled-plugin behavior. |
| `aether-ai-integrations` | Missing | Define external connector contract versions, webhook/event evolution, retry semantics, and provider API drift handling. |
| `aether-ai-testing` | Missing | Define contract fixture/version ownership, compatibility-suite maintenance, and supported test harness versions. |
| `aether-ai-ui-components` | Missing | Define component package SemVer, prop/event breaking changes, accessibility guarantees, and design-token compatibility. |
| `aether-ai-enterprise` | Missing | Define enterprise policy/entitlement/tenant contract versioning and safe rollout across API/admin consumers. |
| `aether-ai-infrastructure` | Missing | Define infrastructure module/input/output versioning, state migration constraints, and rollback/upgrade compatibility. |

## Central contract review observations

1. `docs/contracts/OPENAPI_V1_REVIEW_MATRIX.md` labels OpenAPI v1 as a draft and says no parser/validator, generated-client, endpoint, or runtime security tests were run.
2. A targeted static scan previously reported five unique operation IDs and 51 local component references with no unresolved names. This is not OpenAPI 3.1 validation.
3. `docs/DEPENDENCY_MATRIX.md` and `docs/DEPENDENCY_EDGE_REGISTER.md` remain proposed architecture artifacts. They identify versioned contracts as an intent, but do not prove source imports or runtime call paths match them.
4. The public API, SDK package release, event contracts, persisted workflow/run state, database migrations, search projections, and MCP protocol boundary have different compatibility needs. A single blanket “SemVer” rule is insufficient.

## Proposed minimum policy (decision required)

- **HTTP API:** OpenAPI is source of truth; additive changes are compatible only when existing clients tolerate added fields and new enum values. Removing/renaming fields, tightening accepted input, changing auth semantics, error meaning, ordering, or idempotency behavior is potentially breaking. Maintain an explicit API version and sunset/deprecation process.
- **SDK packages:** SemVer with generated artifact provenance, supported server API range, lockfile/pin policy, migration notes, and CI compatibility tests against supported API versions.
- **Events/queues:** versioned envelope plus event-type schema; define producer/consumer rollout order, unknown-field handling, replay compatibility, and a policy for incompatible changes (new event type/version rather than silent reinterpretation).
- **Persisted data/workflows/indexes:** version stored records and schemas; require expand/contract migrations, reprocessing/rebuild plans, and rollback limits. Do not assume a code rollback reverses a data migration.
- **Tool/provider/MCP contracts:** version capability and invocation schemas separately from transport; run positive, negative, and compatibility fixtures for adapters and untrusted payloads.
- **Governance:** each contract names owner, consumers, version, compatibility class, deprecation window, migration guide, and automated check. Breaking changes require consumer-impact review and explicit approval.

## Required next actions

1. Resolve the compatibility-policy owner and approval workflow.
2. Decide versioning schemes by contract family rather than imposing one scheme on all artifacts.
3. Add a machine-readable contract inventory mapping owner, schema path, version, consumers, compatibility class, and validator.
4. Add OpenAPI/JSON Schema validation and generated SDK diff checks to CI; fail on unresolved references or unapproved breaking changes.
5. Add producer/consumer compatibility fixtures for events, tool/provider adapters, persisted workflow/run state, and search projections.
6. Define deprecation/sunset and rollback/migration runbooks before declaring any public contract stable.

## Verification limits

This audit checked repository specification text and the existing central design/review documents. It did not run OpenAPI or JSON Schema validators, generate an SDK, compare real source imports, inspect every contract artifact in all repositories, or execute compatibility tests. No runtime compatibility claim is made. Implementation remains blocked by unresolved Phase 0 P0 decisions unless formally deferred by the authorized owner.
