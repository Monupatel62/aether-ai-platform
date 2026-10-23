# Cross-Repository Contract Audit

**Audit date:** 2026-10-22  
**Status:** Documentation-level audit of visible GitHub repository metadata, master contracts and selected per-repository contract files. Not a source-code audit.  
**Scope:** 33-repository target; currently visible repositories; dependency and interface consistency; no implementation work.

## 1. Executive result

The proposed 33-node package graph has previously been checked for internal cycles, but that does not prove the contracts are implementable or the runtime call graph is safe. This audit found two concrete contradictions in per-repository dependency declarations and a broader gap: the current contract documents define governance rules but do not yet provide complete, machine-testable API schemas, event schemas, error catalogs or compatibility fixtures.

### Repository visibility snapshot

The connected GitHub listing returned **20 repositories named `aether-ai-*`**:
- 10 repositories with documentation already present: `aether-ai-platform`, `aether-ai-web`, `aether-ai-api`, `aether-ai-gateway`, `aether-ai-providers`, `aether-ai-agents`, `aether-ai-workflows`, `aether-ai-orchestration`, `aether-ai-tools`, `aether-ai-mcp`.
- 10 additional repositories exist but their GitHub repository metadata reports size 0 and the contents endpoint reports the repository is empty: `aether-ai-rag`, `aether-ai-files`, `aether-ai-knowledge`, `aether-ai-auth`, `aether-ai-security`, `aether-ai-admin`, `aether-ai-billing`, `aether-ai-sdk`, `aether-ai-evaluations`, `aether-ai-observability`.
- The user reports having created 22 repositories. Two additional repositories could not be reconciled in the connected listing; they may have different names or be outside the connected account's visible results. Do not assume they are missing from the user's full GitHub account without confirming names.

This snapshot is not a claim that the project is only 20 repositories in total. It describes what the connected GitHub listing exposed during this audit.

## 2. Concrete inconsistencies corrected

### CONTRACT-GAP-01 — API bypassed orchestration in its repository contract
The `aether-ai-api/docs/DEPENDENCIES_AND_CONTRACTS.md` direct-dependency list named `agents` and `database`, while the master dependency matrix says durable runs flow API → orchestration → agents and forbids importing database implementation internals. This could lead to direct execution that bypasses durable run state, cancellation and recovery.

**Correction made:** the API contract now names orchestration as the durable-run boundary, documents bounded synchronous gateway calls separately, and limits database usage to public/domain contracts where explicitly justified.

### CONTRACT-GAP-02 — Workflow contract contradicted its low-level boundary
The `aether-ai-workflows/docs/DEPENDENCIES_AND_CONTRACTS.md` listed orchestration, agents and database as direct dependencies, while the master matrix says workflow schema/validation must not import those implementations.

**Correction made:** the workflow contract now has no runtime dependency on orchestration, agents or database and explicitly states that workflow definitions do not schedule, execute or persist steps.

Both files were fetched again after the writes to verify the corrected text. These corrections change documentation only.

## 3. Cross-repository contract maturity

| Contract area | Current documentation state | Required before implementation |
|---|---|---|
| REST API | API contract requires OpenAPI and stable errors, but no canonical OpenAPI document is registered as an accepted artifact in this audit | Versioned OpenAPI spec, request/response schemas, auth/tenant requirements, error codes, pagination, limits, idempotency and compatibility policy |
| Model gateway | Gateway contract calls for streaming, usage, timeouts, cancellation, retries and fallback; detailed protocol artifact still needed | Capability schema, normalized errors, streaming frame/end/error semantics, cancellation and retry safety table |
| Provider adapters | Capability declaration is specified conceptually | Versioned capability JSON schema, provider conformance fixtures, normalized error mapping and secrets policy |
| Agent/tool calls | Tool manifests, risk class, approval and audit are required conceptually | Versioned manifest/invocation schemas, permission scope, side-effect class, approval envelope, output bounds and idempotency/retry declaration |
| Workflow schema | Version/versioned graph and validation are described | Machine-readable schema, validation error catalog, compatibility/version migration policy, graph-cycle and bounds tests |
| Durable run/queue events | Run IDs, event version, correlation, retries and idempotency are required in prose | Canonical envelope schema, run/step state machine, dedupe key, lease/fencing rules, retry/dead-letter and replay contract |
| Membership and ACL | Owner remains open; revocation safety principles documented | Product decision on membership owner, versioned grant/policy contract, lifecycle/tombstone events and denial semantics |
| Knowledge/RAG/Search | Ownership boundaries documented; RAG/Search are projections | Source/version/ACL schema, ingestion status events, deletion tombstones, citation schema, current-policy reauthorization requirements |
| File lifecycle | File boundary and authorization ownership are described | Upload/download states, scanning outcome, object-key isolation, signed URL lifetime, delete/export and event contracts |
| Billing/usage | Trusted usage events and entitlement contract are described | Usage event schema, idempotency/dedupe, currency/units, adjustments, quota decision contract and reconciliation behavior |
| Public SDK | Intended generated/public schema relationship documented | Generated from accepted OpenAPI/schema source, compatibility/version policy, language support and consumer smoke tests |
| Observability | Metadata-first telemetry and redaction rules documented | Canonical safe attributes, redaction tests, trace propagation and retention/tenant visibility policy |
| Deployment/infrastructure | Logical ownership documented | Environment contract, secret injection, readiness/liveness, migration/rollback and resource ownership; only after runtime topology decision |

## 4. Contract governance rules

Before a contract is called stable, it must include:
1. Owner and authoritative source of truth.
2. Consumer list and direction of dependency.
3. Machine-readable schema and version policy where applicable.
4. Authentication, authorization, tenant and resource-scope rules.
5. Stable error codes and retryability classification.
6. Payload limits, timeouts, rate limits and cancellation behavior.
7. Idempotency, duplicate delivery, ordering, replay and recovery semantics where applicable.
8. Secret/content redaction and correlation IDs.
9. Positive and negative contract tests, including cross-tenant denial.
10. Compatibility/upgrade rules, deprecation period and migration/rollback notes.
11. License and supply-chain review for external dependencies.
12. Named reviewer and explicit status: draft, proposed, accepted, deprecated.

Do not infer acceptance from the presence of a Markdown heading or a package graph edge.

## 5. Priority order for contract artifacts

### P0 — required before security-sensitive implementation
- Auth context and tenant-resolution contract.
- Membership/role/resource ACL decision and policy request/decision schema.
- API OpenAPI baseline and stable error schema.
- Tool invocation/approval envelope and secret redaction rules.
- Durable run/step state machine and queue event envelope.
- Source/ACL version and deletion/tombstone contract for Knowledge/RAG/Search.
- Session/revocation and workload-credential scope rules.

### P1 — required before end-to-end feature integration
- Provider capability schema and gateway streaming/error contract.
- File lifecycle/upload scanning/download contract.
- Billing usage/entitlement events.
- Memory scope/retention contract.
- Observability attributes and privacy controls.
- SDK generation/versioning contract.

### P2 — required before production operations
- Deployment/runtime topology and readiness/health contracts.
- Backup/restore/deletion reconciliation.
- Release, migration, rollback and compatibility test pipeline.
- Operational SLOs, alert ownership and incident access rules.

## 6. Current repository status and limitations

The master catalog must distinguish:
- **Repository exists and contains documentation**
- **Repository exists but is empty**
- **Planned repository not found in connected listing**
- **User-reported repository not yet reconciled**

Do not label an empty repository as documentation-complete. Do not assume the 33-repository package graph means all 33 repositories have been created or populated.

This audit did not inspect or test application source code, run CI, validate generated OpenAPI, test events, check licenses for every dependency, or prove runtime authorization. The graph remains a proposed package-import graph only.

## 7. Next gate

1. Reconcile the two user-reported additional repositories by name/URL.
2. Populate documentation in the 10 currently empty repositories only after confirming their identity and intended status; do not create duplicates.
3. Approve the membership/ACL ownership decision before freezing security schemas.
4. Create P0 machine-readable contract artifacts in the master documentation area and link each consumer.
5. Add schema validation and contract tests only after explicit approval to move beyond documentation-only work.

No application code or deployment was performed.
 

## Follow-up status — 2026-10-23

The repository visibility section above is a historical snapshot from 2026-10-22 and is superseded for repository-count purposes: the latest documentation pass confirmed all 33 canonical repository names are present and added a repository specification to each. The substantive contract-maturity findings above remain open unless explicitly corrected in a later audited artifact. The new repository specs do not by themselves establish machine-testable OpenAPI, event schemas, provider conformance fixtures, or runtime correctness.


## Follow-up contract review — 2026-10-23 (additional repositories)

This section records a documentation-level review of additional repository contracts and open draft PRs. It does not establish implementation readiness or runtime correctness.

### Reviewed boundaries

| Area | Reviewed contract | Required invariant | Remaining verification |
|---|---|---|---|
| Plugins | [Dependencies and contracts](https://github.com/Monupatel62/aether-ai-plugins/blob/main/docs/DEPENDENCIES_AND_CONTRACTS.md) | Plugin manifests request capabilities but cannot grant themselves permissions; invocation binds to a specific plugin/version; Tools owns execution policy. Admin is not a direct plugin dependency. | Manifest schema, artifact provenance policy, isolation runtime, and resource limits remain unselected. |
| Integrations | [Dependencies and contracts](https://github.com/Monupatel62/aether-ai-integrations/blob/main/docs/DEPENDENCIES_AND_CONTRACTS.md) | Credential references rather than raw secrets; verify webhook signatures and deduplicate events; reauthorize before side effects; use the shared Tools egress policy where applicable. | Provider-specific signature behavior, OAuth scope lifecycle, egress implementation and retry/idempotency tests are not verified. |
| SDK | [Dependencies and contracts](https://github.com/Monupatel62/aether-ai-sdk/blob/main/docs/DEPENDENCIES_AND_CONTRACTS.md) | API contract is the source of truth; API must not import its own SDK; mutation retries require explicit idempotency semantics. | Language, generator, runtime targets and package registry remain open; no release pipeline is proven by the document. |
| Evaluations | [Technical design](https://github.com/Monupatel62/aether-ai-evaluations/blob/main/docs/TECHNICAL_DESIGN.md) | Version datasets, rubrics and reports; bound cost/time/tool access; incomplete cases must not pass. | Runner, artifact storage, judge method and score aggregation require ADR/POC evidence. |
| Observability | [Technical design](https://github.com/Monupatel62/aether-ai-observability/blob/main/docs/TECHNICAL_DESIGN.md) | Metadata-first telemetry; redact sensitive values before export; bound cardinality and buffers. | Backend, retention, sampling, audit-event durability and redaction tests remain unverified. |
| Deployment | [Technical design](https://github.com/Monupatel62/aether-ai-deployment/blob/main/docs/TECHNICAL_DESIGN.md) | Runtime secrets, protected environments, immutable artifacts where feasible, explicit rollback and migration order. | Deployment topology, numeric SLOs, environment contract and provider integration remain open. |
| Enterprise | [Security review](https://github.com/Monupatel62/aether-ai-enterprise/blob/main/docs/SECURITY_REVIEW.md) | SSO and privileged export paths need server-side authorization and audit; enterprise must not create a second membership authority. | ADR-0021 remains open; no membership-owner choice is implied by these docs. |
| Infrastructure | [Security review](https://github.com/Monupatel62/aether-ai-infrastructure/blob/main/docs/SECURITY_REVIEW.md) | Default-deny public exposure, least-privilege IAM, protected state, runtime secrets, separated environments and tested restore. | Provider, state backend, secret manager and network design remain open; checklist is not infrastructure test evidence. |

### Draft PR and CI status observed during this review

The following proposals were found open and marked draft when inspected:

- [Plugins #1 — dependency direction](https://github.com/Monupatel62/aether-ai-plugins/pull/1)
- [Integrations #1 — connection and webhook security](https://github.com/Monupatel62/aether-ai-integrations/pull/1)
- [SDK #1 — contract compatibility and release gates](https://github.com/Monupatel62/aether-ai-sdk/pull/1)
- [Evaluations #1 — corpus integrity and grading contract](https://github.com/Monupatel62/aether-ai-evaluations/pull/1)
- [Observability #1 — GenAI telemetry privacy](https://github.com/Monupatel62/aether-ai-observability/pull/1)
- [Deployment #1](https://github.com/Monupatel62/aether-ai-deployment/pull/1) and [Deployment #2](https://github.com/Monupatel62/aether-ai-deployment/pull/2)
- [Enterprise #1 — unresolved membership ownership](https://github.com/Monupatel62/aether-ai-enterprise/pull/1) and [Enterprise #2 — SSO/directory lifecycle security](https://github.com/Monupatel62/aether-ai-enterprise/pull/2)

The GitHub connector returned no PR-triggered workflow runs for the inspected head commits of Plugins #1, Integrations #1, SDK #1, Evaluations #1, Observability #1, Deployment #2 and Enterprise #2. CI is therefore **unverified by this check**; this does not prove that no other workflows ran. No PR was merged as part of this review.

### Dependency-graph audit limitation

The master dependency matrix defines intended ownership and several cycle-prevention rules, but explicitly says edge types are still being normalized and does not certify package imports or runtime call graphs. The current review did not inspect all source files or execute a graph detector. Therefore:
- do not claim the current codebase is cycle-free based on the proposed matrix alone;
- keep package-import, synchronous-call, event/queue, generated-artifact, infrastructure and documentation edges distinct;
- next verify actual source/package manifests against the matrix and run cycle detection on the package-import graph;
- separately inspect synchronous request paths for loops and verify that durable runs follow API → orchestration → agents;
- retain ADR-0021 as open until the product owner explicitly chooses the membership/role-grant authority.

No runtime code, infrastructure, production configuration or deployment was changed by this audit.
