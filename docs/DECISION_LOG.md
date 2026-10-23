# Aether AI — Architecture Decision Log

This is the decision register. A decision is **proposed** until its status is changed to **accepted** with rationale and date. Do not infer that a proposed stack has been selected.

| ID | Decision | Status | Reason / next action |
|---|---|---|---|
| ADR-0001 | Aether AI is a standalone project | Accepted | Own architecture, repository identity, and product decisions. |
| ADR-0002 | Do not assume external runtime dependencies | Accepted | Add external dependencies only through an explicit, reviewed architecture decision. |
| ADR-0003 | Plan 33 Aether repositories | Accepted | The 33 canonical repositories now exist. This is a repository-organization target, not a requirement to deploy 33 services. |
| ADR-0004 | Treat repository boundaries separately from deployable-service boundaries | Accepted | Use the smallest viable modular runtime first; create a separate service only for a documented scaling, isolation, ownership, or release reason. Runtime topology is still undecided. |
| ADR-0005 | AI DIAL integration strategy: adopt, adapter, or custom gateway | Open | Run a small compatibility/licensing/operational evaluation before choosing. |
| ADR-0006 | Frontend/backend technology stack | Open | DIAL Chat is a reference, not a binding stack choice. Decide based on maintainability and existing package compatibility. |
| ADR-0007 | Database, queue, cache, vector/search engine | Open | Compare data model, operations, cost, tenancy, backup, and licensing before selection. |
| ADR-0008 | Identity provider and session model | Open | Need threat model, user/tenant requirements, and deployment assumptions. |
| ADR-0009 | Provider/model list and fallback policy | Open | Compare supported features, cost, privacy, streaming, tool calls, and model terms. |
| ADR-0010 | Project name and public branding | Open | Aether AI is provisional; check GitHub/domain/trademark availability before public launch. |
| ADR-0011 | Monorepo vs multi-repo package management and CI | Open | Avoid duplicate release/version complexity; document ownership and cross-repo CI before coding. |
| ADR-0012 | Prompt/file/memory retention and telemetry policy | Open | Privacy/security requirement; define defaults and user controls before persistence features. |
| ADR-0013 | MCP protocol/SDK compatibility | Proposed | Use an explicit adapter/version matrix and validate against the selected official protocol revision. |
| ADR-0014 | AI security baseline | Proposed | Map the threat model and tests to OWASP GenAI LLM Top 10 2026; prompt text alone is not a security control. |
| ADR-0015 | GenAI observability and privacy | Proposed | Use OpenTelemetry conventions where useful, but keep raw prompt/completion capture disabled by default and define retention/redaction first. |
| ADR-0016 | CI action and release supply-chain policy | Proposed | Pin Actions to full commit SHAs unless an approved lockfile/policy gives equivalent immutability; use least-privilege workflow tokens and protected releases. |

## ADR format for new decisions

Each accepted ADR must include: context/problem, options considered, chosen option, reasons, consequences/tradeoffs, security/license implications, migration plan, affected repositories, date, and reviewer. If a decision changes, supersede it with a new ADR rather than silently rewriting history.

## Architecture review update — 2026-10-22

| ID | Decision | Status | Evidence / next action |
|---|---|---|---|
| ADR-0003 | Plan 33 Aether repositories | Accepted | User explicitly chose 33. This is a repository organization target, not a requirement to deploy 33 services. Remaining 23 can be created after the documentation phase. |
| ADR-0004 | Repository boundaries are separate from service boundaries | Accepted | Dependency matrix requires a modular runtime/package map first. Create a separate network service only for a documented scaling, isolation, ownership or release reason. |
| ADR-0005 | Native gateway vs optional external gateway | Open | [Gateway architecture evaluation](DIAL_ADOPTION_EVALUATION.md) compares the native approach with an optional external adapter. No external dependency is accepted. |

## Data infrastructure review — 2026-10-22

| ID | Decision | Status | Evidence / next action |
|---|---|---|---|
| ADR-0007 | Database, queue, cache, vector/search engine | Open; baseline proposed | [Data infrastructure evaluation](DATA_INFRASTRUCTURE_EVALUATION.md) recommends benchmarking PostgreSQL + pgvector/full-text, BullMQ, and a Valkey-compatible cache first. No final provider, queue, vector DB, or cache vendor selected. |
| ADR-0018 | Data-layer ownership and source-of-truth rules | Proposed | PostgreSQL candidate is the transactional source of truth; search/vector indexes are rebuildable projections; queue payloads carry opaque IDs; orchestration persists durable run state; cache is reconstructible only. Validate via failure, isolation, restore and benchmark tests. |


## 2026-10-22 — Identity and tenant security research

- Added `docs/IDENTITY_AND_TENANT_SECURITY_EVALUATION.md` covering identity-provider options, OIDC/OAuth session design, tenant isolation, authorization contracts, threat scenarios and POC acceptance criteria.
- ADR-0008 (identity provider/session) remains open; this research does not select a vendor.
- New proposed ADRs: ADR-0019 browser session architecture; ADR-0020 authorization model/policy engine scope; ADR-0021 tenant hierarchy and support access; ADR-0022 API-key/workload identity; ADR-0023 MFA/recovery/session/revocation SLOs; ADR-0024 tenant isolation and RLS rollout.
- No application code or security control implementation was added.


## 2026-10-22 — Identity-provider shortlist research

- Added `docs/IDENTITY_PROVIDER_SHORTLIST_AND_SCORECARD.md` comparing ZITADEL, Keycloak and Auth0 using official documentation and a weighted POC scorecard.
- No identity provider was selected. The scorecard must be populated with observed POC evidence; unknowns remain N/T rather than guessed scores.
- Next gate: run equivalent protocol, tenant authorization, lifecycle, audit, operations and migration tests. No POC was executed in this research step.


## 2026-10-22 — Browser session and authorization architecture research

- Added `docs/BROWSER_SESSION_AND_AUTHORIZATION_ARCHITECTURE.md` using IETF RFC 10017 (August 2026), RFC 9700, OWASP guidance and PostgreSQL RLS documentation.
- BFF with server-side sessions is the preferred candidate for the first-party web POC, not an accepted ADR. RBAC plus resource-level checks is the baseline candidate; ABAC/ReBAC/policy-engine scope remains open.
- ADR-0019, ADR-0020 and related ADRs remain open. No POC tests or application code were run.


## 2026-10-22 — Authorization permission matrix research

- Added `docs/AUTHORIZATION_PERMISSION_MATRIX.md` defining proposed principal/resource/action vocabulary, a baseline role matrix, mandatory security invariants, policy decision contract and negative-test plan.
- Role permissions are a proposal and need product-owner review; they are not implemented or accepted as final product policy.
- ADR-0020, ADR-0021, ADR-0022, ADR-0023 and ADR-0024 remain open. No application code or tests were added/run.


## 2026-10-22 — Tenant membership and ACL revocation consistency

- Added [TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md](TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md) to compare membership ownership options and define proposed access-revocation safety invariants.
- Recommendation for review: `aether-ai-enterprise` may own universal tenant/workspace membership only if its contract works for all customer tiers; otherwise a dedicated tenancy repository requires explicit approval to revise the 33-repository plan. `aether-ai-auth` remains identity/session owner, not automatically the membership authority.
- Protected operations must re-check authoritative authorization; search/RAG/cache/index cleanup is asynchronous projection work and cannot be the access-denial barrier. Numeric projection-cleanup SLOs remain unapproved pending requirements and measurement.
- ADR-0020, ADR-0021, ADR-0023 and ADR-0024 remain open. No code, provider selection, repository creation, or numeric SLO commitment was made.


## 2026-10-22 — Authorization policy gap audit

- Added [AUTHORIZATION_POLICY_GAP_AUDIT.md](AUTHORIZATION_POLICY_GAP_AUDIT.md) after semantic review of the draft permission matrix.
- Recorded high-risk ambiguities involving workspace creation defaults, support-operator modeling, admin access to conversations/memory, ownership transfer/grant ceilings, action-level permissions, approval tiers, membership/ACL versioning, workload identity and billing permissions.
- These are policy gaps and proposed dispositions, not accepted product decisions. ADR-0012, ADR-0015 and ADR-0020 through ADR-0024 remain open as applicable. No code or tests were run.


## 2026-10-22 — Retention, deletion, export and telemetry policy proposal

- Added [DATA_RETENTION_DELETION_EXPORT_TELEMETRY_POLICY.md](DATA_RETENTION_DELETION_EXPORT_TELEMETRY_POLICY.md) with data-category ownership candidates, metadata-first telemetry defaults, deletion/revocation distinctions, backup restore reconciliation, export controls and acceptance tests.
- Numeric retention periods, legal-hold rules, residency, export entitlements, backup targets and telemetry retention remain open for product/privacy/legal review. ADR-0012 and ADR-0015 remain open; no compliance claim or implementation was made.


## 2026-10-22 — Identity and authorization POC runbook

- Added [IDENTITY_AUTHORIZATION_POC_RUNBOOK.md](IDENTITY_AUTHORIZATION_POC_RUNBOOK.md) with 24 scenarios, hard security gates, reproducible test-fixture guidance, measurement rules and an evidence-based weighted scorecard.
- No provider was tested or selected. Running the POC remains gated on explicit approval of scope, environment, operators and budget. All hard-gate failures block candidate acceptance regardless of weighted score.


## 2026-10-23 — Consolidated ADR status register (reconciliation, no decisions made)

**Why this section exists.** The tables above only list ADR-0001 through ADR-0016, ADR-0007 and ADR-0018 updates. ADR-0019 through ADR-0024 appear only in dated narrative bullets, so the critical open decision ADR-0021 had no register row, status or owner-approval requirement. This section is append-only: earlier entries above are preserved as history and are not rewritten. It records **status as written in this log**; it accepts, selects or ranks nothing.

| ID | Subject (wording as used in the cited documents) | Status per this log | Source of status |
|---|---|---|---|
| ADR-0001 – ADR-0004 | Standalone project; no assumed external runtime dependencies; 33 repositories; repository ≠ service boundary | Accepted | Register table above |
| ADR-0005 | Gateway approach (adopt / adapter / custom, also worded as native vs optional external gateway) | Open | Register table; 2026-10-22 update |
| ADR-0006 | Frontend/backend technology stack | Open | Register table |
| ADR-0007 | Database, queue, cache, vector/search engine | Open; baseline proposed | Data infrastructure review |
| ADR-0008 | Identity provider and session model | Open | Register table; identity research entries |
| ADR-0009 – ADR-0012 | Provider/fallback policy; branding; monorepo vs multi-repo CI; retention/telemetry policy | Open | Register table |
| ADR-0013 – ADR-0016 | MCP compatibility; AI security baseline; GenAI observability/privacy; CI supply chain | Proposed | Register table |
| ADR-0017 | **No entry found** in this log or in any other file of this repository | Unknown; number unassigned or entry missing | See finding R-2 |
| ADR-0018 | Data-layer ownership and source-of-truth rules | Proposed | Data infrastructure review |
| ADR-0019 | Browser session architecture (BFF/server-side session vs alternatives) | Proposed / open | 2026-10-22 identity research |
| ADR-0020 | Authorization model and policy-engine scope (RBAC baseline vs ABAC/ReBAC/engine) | Proposed / open | 2026-10-22 identity research |
| **ADR-0021** | **Tenant/workspace hierarchy, privileged support access, and canonical tenant/workspace membership and role-grant ownership** | **Open — owner approval required; no option accepted** | 2026-10-22 identity research; tenant membership and ACL consistency entry; [owner decision brief](TENANT_MEMBERSHIP_OWNER_DECISION_BRIEF.md) |
| ADR-0022 | API-key and workload identity | Proposed / open | 2026-10-22 identity research |
| ADR-0023 | MFA/recovery/session/revocation targets | Proposed / open | 2026-10-22 identity research |
| ADR-0024 | Tenant isolation and PostgreSQL RLS rollout | Proposed / open | 2026-10-22 identity research |

### ADR-0021 — what is blocked and what the owner must decide

- **Decision needed:** which component is the single canonical owner of tenant/workspace membership, invitations, role grants and membership lifecycle. Authentication identity, resource ACLs, policy evaluation and billing entitlements stay separate concerns whichever owner is chosen.
- **Options on record** (from the [owner decision brief](TENANT_MEMBERSHIP_OWNER_DECISION_BRIEF.md); not accepted):
  - **A — `aether-ai-enterprise` owns tenancy for every customer tier.** Keeps the 33-repository scope. Implication: Enterprise must work for personal/free/team customers without SSO, SCIM or billing, and must expose a narrow versioned membership contract.
  - **B — new `aether-ai-tenancy` repository.** Implication: changes the accepted 33-repository plan (ADR-0003), so it needs explicit owner approval plus catalog, dependency-graph and specification updates. **Do not create it without that approval.**
  - **C — `aether-ai-auth` owns tenancy.** Implication: couples membership lifecycle to login/provider concerns; the brief keeps it only as a fallback if that coupling is intended.
- **About the brief's recommendation:** the brief records a review recommendation favoring Option A, explicitly stated as not an accepted ADR. This log does **not** adopt it.
- **Owner approval required before:** freezing the auth, enterprise, security and database contracts; classifying any membership edge as final in the dependency matrix, edge register or `dependency-package-graph.json`; any membership/role-grant persistence in any repository.
- **Owner's questions to answer** (brief, "Acceptance questions"): personal users without an organization; multi-tenant membership and switching; workspace nesting and role scope; first-tenant creation and ownership recovery; revocation behavior for sessions, queued jobs, search/RAG results and signed file links; whether Enterprise is intended to serve every customer tier.
- **Until accepted:** `aether-ai-enterprise`, `aether-ai-auth` and `aether-ai-database` must each state that canonical membership ownership is unresolved. Open correction PRs exist for Enterprise ([#1](https://github.com/Monupatel62/aether-ai-enterprise/pull/1)) and Database ([#1](https://github.com/Monupatel62/aether-ai-database/pull/1)); they are drafts and are not merged.

### Findings recorded by this reconciliation (documentation defects, not decisions)

- **R-1 — Table layout defect (fixed in this change).** Rows ADR-0013 to ADR-0016 followed the "ADR format" paragraph with no table header, so they rendered as plain text outside the register table. The paragraph now sits after the ADR-0016 row. Row text is unchanged.
- **R-2 — ADR-0017 is absent.** Numbering jumps from ADR-0016 to ADR-0018 with no entry or reference anywhere in the repository. The owner should state whether the number was reserved, skipped or lost. Nothing was invented here.
- **R-3 — ADR-0021 scope is worded inconsistently.** Most documents describe it as "tenant/workspace hierarchy and support access". The tenant membership consistency decision, the work log and the owner brief treat it as including the canonical membership owner. The register row above combines the phrasings; the owner should confirm that is one decision, or split membership ownership into its own ADR number.
- **R-4 — Possible overlap between ADR-0008 and ADR-0019.** ADR-0008 covers "identity provider and session model"; ADR-0019 covers browser session architecture, and some documents label ADR-0019 "identity provider and browser session". Boundary between them should be stated when either is accepted.
- **R-5 — Stale count in a historical entry.** The "Architecture review update — 2026-10-22" row for ADR-0003 says the remaining 23 repositories can be created after the documentation phase. All 33 repositories now exist (verified 2026-10-23 through public git refs). The earlier text is preserved as history; ADR-0003's accepted status is unchanged.
- **R-6 — Status vocabulary.** The log mixes "Proposed" and "Open" for the same ADRs (for example ADR-0019 to ADR-0024). Both mean not accepted. Standardize on one vocabulary when the register is next revised.

No ADR status was changed by this reconciliation. No application code, build or test was run for this entry.
