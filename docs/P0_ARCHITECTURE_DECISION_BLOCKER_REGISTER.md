# P0 Architecture Decision and Blocker Register

**Date:** 2026-10-23  
**Status:** Proposed decision-management register; no architecture decision is accepted by this document.  
**Gate:** Application implementation remains blocked until each P0 item has an accepted ADR/contract or an explicitly approved, reviewed deferral.

## Decision-state rules

- **Open / blocked:** Evidence or owner decision is missing. Do not treat recommendations as selected architecture.
- **Proposed:** A candidate option exists, but approval and consequences are not recorded.
- **Accepted:** The decision has an ADR with context, alternatives, chosen option, rationale, trade-offs, security/license impact, affected repositories, date, and reviewer.
- **Deferred:** Must identify the approving authority, reason, scope, expiry/revisit trigger, compensating controls, and risks accepted.
- **Verified:** Acceptance criteria have evidence attached (validator/test run, commit, report, or reviewed artifact). A written plan alone is not verification.

## P0 register

| ID | Decision / blocker | Current status | Decision owner (proposed accountable role) | Affected repositories | Required evidence before acceptance | Acceptance criteria | Gate |
|---|---|---|---|---|---|---|---|
| P0-01 | Identity provider, token validation, session lifecycle, workload identity (ADR-0008 open) | Open / blocked | Auth owner; Security reviews | auth, api, web, admin, gateway, integrations, enterprise, security | Threat model; provider comparison; issuer/audience/signature/key rotation/expiry/logout/revocation/workload-flow decision; POC report with synthetic identities | Invalid issuer/audience/signature and expired/replayed tokens rejected; approved rotation and session/revocation bounds measured; login/CSRF/cookie tests pass | Blocks all protected vertical slices |
| P0-02 | Canonical tenant/workspace membership authority and version source | Open / blocked | Product/API domain owner to nominate one canonical membership owner; Security reviews | auth, api, security, enterprise, admin, database, files, knowledge, memory, search, rag, billing | ADR naming authoritative write/read owner, version semantics, tenant selector rules, outage/staleness behavior, migration and event contract | Client tenant selector never grants scope; removed membership is denied within approved bound; stale/unavailable authority fails closed; ownership agrees with repository specs | Blocks multi-tenant protected operations |
| P0-03 | Authorization-context trust and transport | Proposed contract; not approved or implemented | Security owner; Auth and API implementers | security, auth, api, gateway, agents, tools, mcp, orchestration, queue, files, knowledge, rag, search | Accepted trust profile defining issuer, service identity, integrity, audience, principal/tenant/resource/action binding, lifetime, freshness, replay, revocation and key rotation | Tampered/unsigned/wrong-audience/wrong-scope/expired/stale/replayed contexts are rejected; secrets are not logged; failure is deny-by-default | Blocks trusted cross-component authorization |
| P0-04 | Resource-level authorization and privileged/support access | Proposed matrix; unresolved policy decisions remain | Security + product policy owner; each domain owner owns enforcement | auth, security, api, web, admin, files, memory, knowledge, rag, search, tools, mcp, billing, enterprise, observability | Approved permission matrix; owner for each protected resource; support/admin boundaries; role-change protections; explicit grants/approvals; negative test evidence | Deny-by-default; cross-tenant read/list/search/export/stream/tool/background/result access denied; operators have no implicit customer-content access; support access is approved, scoped, time-bound and audited | Blocks protected data access and privileged actions |
| P0-05 | Agent/tool input and output schemas, risk tiers, approval binding and limits | Open / blocked | Agents and Tools owners; Security reviews; MCP owns protocol mapping | agents, workflows, orchestration, tools, mcp, api, gateway, evaluations | Versioned per-agent/tool schemas; unknown-field policy; byte/depth/property/time limits; risk classes; approval identity/scope/version/expiry; execution-time reauthorization | Invalid/oversized inputs rejected before scheduling; high-impact tools require valid bound approval; stale/revoked approvals rejected; outputs are bounded and safely handled | Blocks agent/tool execution |
| P0-06 | Durable run lifecycle, cancellation, idempotency and side-effect safety | Open / blocked | Orchestration owner; API and Queue provide contracts | api, orchestration, queue, agents, workflows, tools, observability, database | State-transition table; durable acknowledgment definition; idempotency scope/retention/fingerprint; cancellation race semantics; worker fencing; retry/recovery policy | Duplicate create with same key returns same logical run; key/payload conflict rejected; terminal transitions are monotonic; stale workers cannot commit; side effects are not blindly replayed | Blocks durable asynchronous runs |
| P0-07 | Run result schema, visibility, retention, deletion and revocation propagation | Open / blocked | Orchestration owns run result; domain data owners set retention; Privacy/Security review | orchestration, api, database, memory, files, knowledge, rag, search, observability, evaluations, deployment | Versioned output schema; result access policy; retention/deletion/export schedule; deletion propagation map and SLO; backup/log/index/cache behavior; legal-hold and restoration policy where applicable | Every result read reauthorizes; deleted/revoked data is removed or made inaccessible across projections, caches, queued jobs and logs within approved bounds; retention is measurable and documented | Blocks persistence and data-bearing features |
| P0-08 | Contract validation and compatibility gates | Validator workflow exists on PR #27 branch; no approval/merge implied | Platform/docs owner; API/SDK/contract owners | platform, api, sdk, gateway, providers, agents, workflows, tools, mcp, queue, database, testing | Pinned validator versions; committed CI run on current commit; approved schema dialect and format assertions; fixture inventory and owner-reviewed expected outcomes; compatibility policy | OpenAPI 3.1 and JSON Schema Draft 2020-12 validation passes; all fixtures execute with expected outcomes; catalog/graph checks pass; negative and boundary fixtures are reviewed; failures block merge once required checks are enabled | Blocks contract approval |
| P0-09 | Gateway/provider-neutral contract and integration choice (ADR-0005 open) | Open / blocked | Gateway owner; Providers owner; Architecture reviewer | gateway, providers, api, agents, evaluations, observability | Aether-owned request/response/error/capability contract; mock/non-production comparison; provider capability/fallback/timeout/retry/cancellation behavior; credential/privacy and license review for any external candidate | Adapter conformance tests pass; provider failures are normalized safely; fallback does not bypass policy or duplicate side effects; no vendor dependency is selected without accepted ADR | Blocks production model routing |
| P0-10 | Release gate, CI ownership, branch protection and implementation authorization | Workflow proposed in PR #27; branch protection unverified; implementation not authorized | Platform/release owner; repository administrator must verify rulesets | all 33 repos; central platform, docs, testing, deployment, infrastructure | Approved per-repo CI strategy and toolchain; required check list; administrator evidence for rulesets/reviews/bypass/force-push settings; security/license/secret scanning; release/rollback evidence; explicit user approval to enter implementation | Required checks actually run on proposed changes and are required by branch rules; releases bind artifact to commit and evidence; rollback/recovery tested in non-production; P0s accepted or formally deferred; explicit implementation authorization recorded | Blocks implementation, merge policy, and release claims |

## P1 decisions that must not be silently treated as settled

| ADR / topic | Current state | Next evidence / trigger |
|---|---|---|
| ADR-0005 gateway strategy | Open | Complete compatibility/licensing/operations comparison and non-production POC. |
| ADR-0006 frontend/backend stack | Open | Record supported languages/frameworks, maintainability rationale and package compatibility. |
| ADR-0007 data infrastructure | Open; baseline candidates only | Benchmark query, tenancy, latency, recall, backup/restore, operations and cost. |
| ADR-0011 monorepo/package/CI strategy | Open | Choose release/version model and cross-repository contract workflow before package implementation. |
| ADR-0012 retention and telemetry | Open | Approve default metadata-only telemetry, retention, deletion/export, residency and redaction policy before persistence. |
| ADR-0013 MCP compatibility | Proposed | Pin protocol revision/transports and record conformance evidence. |
| ADR-0014 AI security baseline | Proposed | Map threat model to selected guidance and executable abuse-case tests. |
| ADR-0015 GenAI observability/privacy | Proposed | Approve telemetry fields, redaction, access, retention and raw-prompt capture default. |
| ADR-0016 CI supply-chain policy | Proposed | Approve action pinning, least-privilege tokens, dependency scanning and release provenance. |

## Required decision workflow

1. Assign a named human owner/reviewer for each row; role labels above are proposed, not confirmed assignments.
2. Create or update the relevant ADR. Include alternatives and consequences; do not turn a recommendation into an accepted decision by rewriting a summary.
3. Link the evidence: reviewed contract, validator/test run, POC report, security review, license review, or administrator ruleset evidence as applicable.
4. Mark acceptance criteria individually **Not started**, **In progress**, **Pass**, or **Fail** with a link to evidence. Never mark a test as passed because a test plan exists.
5. If deferring, record explicit approver, risk, compensating controls, affected scope, expiry/revisit trigger, and why the deferral is safe.
6. Reconcile affected repository specifications, dependency matrix, API/event/schema contracts, and implementation gates after a decision is accepted.
7. Recheck the current PR head SHA and CI before any merge decision. Draft PRs stay unmerged unless explicitly authorized.

## Current verified checkpoint

- The implementation gate document lists 10 P0 areas; this register maps them to proposed owners, affected repositories, evidence and acceptance criteria.
- The architecture decision log marks ADR-0005 through ADR-0012 open (with ADR-0013 through ADR-0016 proposed in its later section); no choices here silently change those statuses.
- Platform documentation/contract validation workflow was added on PR #27 and an earlier PR-branch run passed. A later tracker-only update triggered another run; check its latest status before relying on it.
- Branch protection could not be verified because the connected GitHub integration was denied access to the protection endpoint. This is **unknown**, not proof protection is disabled.
- This register is a documentation artifact. It does not prove identity, authorization, privacy, release, or runtime controls are implemented.
