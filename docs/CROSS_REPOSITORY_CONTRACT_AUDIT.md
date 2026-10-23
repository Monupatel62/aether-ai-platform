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


## 2026-10-23 — Gateway capability metadata validation update

Gateway PR #3 is open as a draft and layers on the provider-neutral request contract branch: https://github.com/Monupatel62/aether-ai-gateway/pull/3. CI run 39931683878 completed successfully for commit `c78744bfd40266ce237628653b0fe178c8fb0912` (test job: success).

The change adds bounded validation for request fields and provider capability metadata, deterministic handling of duplicate provider IDs and routing priorities, stream capability checks, normalized provider failure categories, and negative tests. It does not select a vendor SDK, configure credentials, or add a production network client. Client-supplied tenant metadata remains untrusted and must not be used as authorization; trusted principal/tenant authorization must occur before routing.

**Status caveat:** green CI is not acceptance of the proposed contract or a production-readiness claim. PR #3 and the dependent Gateway PRs remain unmerged pending architecture/contract gates.


## 2026-10-23 — Security helper review finding

Review of draft [Security PR #2](https://github.com/Monupatel62/aether-ai-security/pull/2) identified that malformed policy obligations in an `allow` response were previously silently replaced with an empty list. The draft branch was updated to fail closed with `POLICY_ERROR` for malformed or over-limit obligations and to bound key request identifiers; negative tests were added. CI runs 39933221665 and 39933226791 were triggered and remain pending verification at the time of this entry.

This helper is a contract boundary, not an authorization authority. It does not authenticate identities or establish tenant/workspace membership. Trusted context provenance, authoritative grant ownership, and domain-level enforcement remain required; PR #2 remains open and unmerged.
