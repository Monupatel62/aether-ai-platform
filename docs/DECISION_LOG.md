# Aether AI — Architecture Decision Log

This is the decision register. A decision is **proposed** until its status is changed to **accepted** with rationale and date. Do not infer that a proposed stack has been selected.

| ID | Decision | Status | Reason / next action |
|---|---|---|---|
| ADR-0001 | Keep Aether AI separate from WoHoTech | Accepted | User requirement; separate product/repository identity. |
| ADR-0002 | Use WoHo AI DevKit as an external dependency, not rewrite it | Accepted in principle | Preserve existing project; verify package APIs and compatibility before implementation. |
| ADR-0003 | Plan 33 Aether repositories | Proposed | User requested a 33-repository ecosystem; review for boundaries/cycles before creating remaining 23. |
| ADR-0004 | Treat repository boundaries separately from deployable-service boundaries | Proposed | Avoid premature microservices; runtime topology is not decided. |
| ADR-0005 | AI DIAL integration strategy: adopt, adapter, or custom gateway | Open | Run a small compatibility/licensing/operational evaluation before choosing. |
| ADR-0006 | Frontend/backend technology stack | Open | DIAL Chat is a reference, not a binding stack choice. Decide based on maintainability and existing package compatibility. |
| ADR-0007 | Database, queue, cache, vector/search engine | Open | Compare data model, operations, cost, tenancy, backup, and licensing before selection. |
| ADR-0008 | Identity provider and session model | Open | Need threat model, user/tenant requirements, and deployment assumptions. |
| ADR-0009 | Provider/model list and fallback policy | Open | Compare supported features, cost, privacy, streaming, tool calls, and model terms. |
| ADR-0010 | Project name and public branding | Open | Aether AI is provisional; check GitHub/domain/trademark availability before public launch. |
| ADR-0011 | Monorepo vs multi-repo package management and CI | Open | Avoid duplicate release/version complexity; document ownership and cross-repo CI before coding. |
| ADR-0012 | Prompt/file/memory retention and telemetry policy | Open | Privacy/security requirement; define defaults and user controls before persistence features. |

## ADR format for new decisions

Each accepted ADR must include: context/problem, options considered, chosen option, reasons, consequences/tradeoffs, security/license implications, migration plan, affected repositories, date, and reviewer. If a decision changes, supersede it with a new ADR rather than silently rewriting history.
| ADR-0013 | MCP protocol/SDK compatibility | Proposed | Official MCP revision 2026-07-28 changes lifecycle and authorization; use explicit adapter/version matrix after DevKit compatibility tests. |
| ADR-0014 | AI security baseline | Proposed | Map the threat model and tests to OWASP GenAI LLM Top 10 2026; prompt text alone is not a security control. |
| ADR-0015 | GenAI observability and privacy | Proposed | Use OpenTelemetry conventions where useful, but keep raw prompt/completion capture disabled by default and define retention/redaction first. |
| ADR-0016 | CI action and release supply-chain policy | Proposed | Pin Actions to full commit SHAs unless an approved lockfile/policy gives equivalent immutability; use least-privilege workflow tokens and protected releases. |

## Architecture review update — 2026-10-22

| ID | Decision | Status | Evidence / next action |
|---|---|---|---|
| ADR-0003 | Plan 33 Aether repositories | Accepted | User explicitly chose 33. This is a repository organization target, not a requirement to deploy 33 services. Remaining 23 can be created after the documentation phase. |
| ADR-0004 | Repository boundaries are separate from service boundaries | Accepted | Dependency matrix requires a modular runtime/package map first. Create a separate network service only for a documented scaling, isolation, ownership or release reason. |
| ADR-0005 | DIAL Core vs DevKit gateway path vs hybrid | Open | [DIAL adoption evaluation](DIAL_ADOPTION_EVALUATION.md) compares the options. Run a controlled proof-of-concept and then decide. |
| ADR-0017 | WoHo DevKit package integration boundary | Proposed | [DevKit compatibility review](DEVKIT_COMPATIBILITY_REVIEW.md) records current package versions and source-level findings. Pin verified artifacts, use public exports/adapters, and keep Aether authorization/orchestration policy outside DevKit. |

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
