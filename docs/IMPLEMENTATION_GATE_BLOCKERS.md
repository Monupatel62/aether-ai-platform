# Aether AI — Implementation Gate Blockers

**Status:** Consolidated review checklist; not an approval to start application coding.  
**Updated:** 2026-10-23  
**Source of truth:** The detailed contract reviews and open ADRs linked below take precedence if this summary drifts.

## Gate rule

Do not begin application implementation until every P0 blocker has an accepted contract/ADR or a documented, reviewed deferral. The existence of 33 repositories and completed documentation does not mean the architecture is implementation-ready.

## P0 — resolve before the first vertical slice

| Blocker | Current evidence | Required resolution |
|---|---|---|
| Identity and token validation | ADR-0008 is open; the OpenAPI bearer/JWT scheme is a placeholder. | Select the identity operating model; define issuer, audience, signature/key rotation, expiry, session/revocation behavior, and workload identity. Run the identity POC before treating auth as complete. |
| Canonical tenant membership authority | Tenant resolution is drafted, but the canonical membership owner and version source are undecided. | Name the source of truth for tenant/workspace membership, define how tenant selection is treated as an untrusted selector, and define fail-closed behavior when state is stale or unavailable. |
| Authorization-context trust | The schema validates shape only. Issuer trust, integrity, audience binding, expiry, freshness, replay and revocation are not implemented. | Accept the transport/integrity profile, workload identity, lifetime, version freshness, replay controls, and revocation bound in [Authorization Context Trust Profile](contracts/AUTHORIZATION_CONTEXT_TRUST_PROFILE.md). |
| Resource-level authorization | Permission matrix and tenant contract are proposals. | Define owner for each protected resource and require authorization at read/list/search/export/stream/tool/background-job/result boundaries. Add cross-tenant negative cases. |
| Agent input validation | The OpenAPI CreateRunRequest input is an arbitrary object. | Require a versioned schema per registered agent; define byte/depth/property limits and reject unknown fields before scheduling. |
| Run result and retention | RunStatus.result is not yet constrained by a stable output schema; retention/deletion periods remain open. | Define agent output schema/version, result visibility, redaction, current authorization on every read, retention/deletion/export behavior, and deletion propagation. |
| Cancellation and idempotency | Cancellation is correctly described as a request, but state transitions/races are open. Idempotency-key scope/retention are open. | Specify allowed run transitions, repeated cancellation behavior, terminal-state races, durable acknowledgment semantics, key scope/retention, payload fingerprinting, and duplicate side-effect protection. |
| Tool execution boundary | Tool schema and event schemas have unconstrained nested data and conditional security fields. | Define per-tool input/output schemas, scopes, risk class, approval binding, payload limits, execution-time reauthorization, producer identity, event deduplication and ordering rules. |
| Contract validation | JSON syntax and graph checks passed; OpenAPI YAML and JSON Schema semantics have not been validated by dedicated validators. | Run an OpenAPI 3.1 validator and a Draft 2020-12 JSON Schema validator with format assertions; execute all 24 fixtures and add any remaining boundary/conditional cases before approval. |
| Gateway/provider contract | ADR-0005 is open; gateway POC is a plan only. | Keep an Aether-owned request/response/error/capability boundary. Run the documented mock/non-production POC before deciding whether an optional external gateway is justified. |

## P1 — resolve before the relevant feature phase

| Decision area | Current recommendation for evaluation, not an accepted decision |
|---|---|
| Runtime and packaging | Prefer a modular runtime and versioned package/API contracts before splitting repositories into independently deployed services. Decide language/framework and cross-repository CI in ADRs. |
| Data layer | Benchmark PostgreSQL + full-text + pgvector first; compare a separate vector store only against measured latency, recall, filter and scale targets. |
| Queue/cache | Test BullMQ with a Redis-compatible backend for Node.js job processing; evaluate NATS JetStream only if replay and independent durable consumers are required. Cache remains reconstructible and non-authoritative. |
| Identity provider | Compare ZITADEL, Keycloak and Auth0 using the common scorecard; select only after mandatory security gates and operations/cost evidence. |
| MCP compatibility | Explicitly pin supported protocol revisions and transports; validate candidate SDK behavior rather than inferring conformance from a package name. |
| Privacy and observability | Metadata-only telemetry by default. Set retention, deletion, export, residency and redaction policy before persisting prompts, files, memory or traces. |
| Models and billing | Decide initial provider/model catalog, capability/fallback policy, usage source of truth, pricing, quotas and billing provider before exposing billable runs. |
| Public identity | Check product name, domains and trademark availability before public launch. |

## Evidence already recorded

- [OpenAPI semantic review matrix](contracts/OPENAPI_V1_REVIEW_MATRIX.md)
- [JSON Schema semantic review](contracts/SCHEMA_SEMANTIC_REVIEW.md)
- [Tenant context resolution contract](contracts/TENANT_CONTEXT_RESOLUTION_CONTRACT.md)
- [Authorization context trust profile](contracts/AUTHORIZATION_CONTEXT_TRUST_PROFILE.md)
- [Identity-provider scorecard](IDENTITY_PROVIDER_SHORTLIST_AND_SCORECARD.md)
- [Data infrastructure evaluation](DATA_INFRASTRUCTURE_EVALUATION.md)
- [Gateway proof-of-concept plan](GATEWAY_PROOF_OF_CONCEPT.md)
- [Architecture decision log](DECISION_LOG.md)
- [Implementation status audit](IMPLEMENTATION_STATUS_AUDIT.md)

## Exit criteria

The gate can be reviewed when:

1. Every P0 item has an accepted decision/contract or an explicitly approved deferral.
2. OpenAPI and JSON Schema validators pass; contract fixtures execute and negative cases fail as expected.
3. The dependency graph and repository specs agree with accepted ownership decisions.
4. No component can treat client-provided tenant/role/approval metadata as authority.
5. The user explicitly approves moving from documentation/research into implementation.

Until then, keep the project in Phase 0.

## Contract hardening update — 2026-10-23

- Added draft conditional requirements to run-event schema: step lifecycle events require `step_id`; retry scheduling requires `attempt` and `not_before`; failed run/step events require `failure_code`.
- Added property-count bounds (`maxProperties: 100`) to generic event payload and tool argument objects.
- Expanded fixture definitions from 14 to 19, then added five boundary cases (24 total). The fixtures are still unexecuted; these changes do not close the validator P0 gate.
