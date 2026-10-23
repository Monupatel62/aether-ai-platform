# Aether AI Authorization Permission Matrix and Policy Test Plan

**Research date:** 2026-10-22  
**Status:** Proposed authorization specification; no implementation or final ADR decision.  
**Phase:** Documentation and research only.

## 1. Purpose

Define an auditable, testable baseline for which principals can perform which actions on Aether resources. This matrix is a starting policy contract for the 33-repository architecture; it is not a claim that these roles, product features or permissions are already implemented.

Principles:
- Deny by default. Grant only the permissions explicitly needed.
- Authentication proves an identity; it does not automatically authorize a resource action.
- Every resource operation is checked server-side, including read, list, search, export, streaming, tool execution and background work.
- Tenant scope comes from authoritative Aether membership/resource data, not a client-supplied tenant ID.
- A user cannot grant themselves permissions or elevate their own role.
- A policy decision must be testable with positive and negative cases and an auditable reason code.
- UI visibility, hidden buttons and model instructions are not security controls.

## 2. Principal and resource vocabulary

### Principals
- **Anonymous:** no authenticated Aether principal.
- **User:** authenticated human identity.
- **Tenant Owner:** designated owner for one tenant.
- **Tenant Admin:** delegated tenant administrator.
- **Member:** ordinary tenant participant.
- **Viewer:** read-only tenant participant, subject to resource-specific access.
- **Resource Manager:** a narrowly scoped permission bundle for an assigned resource class, not a global role.
- **Service Principal:** non-human workload identity with explicit audience and least-privilege grants.
- **Platform Operator:** privileged Aether operations identity, separate from tenant roles and never implicitly entitled to customer content.
- **Support Operator:** time-limited, reason-bound access only where the product has an approved support workflow.

### Resource classes
- Identity and sessions; tenant and membership; workspace/project; files and uploads; conversations and AI memory; knowledge collections and retrieval; agents and workflows; tools and MCP servers/connections; provider/model configuration; API keys/secrets; usage and billing; audit/security events; platform settings.

## 3. Action vocabulary

- **Create:** create a resource inside the caller's authorized scope.
- **Read:** retrieve a single resource or content.
- **List/Search:** enumerate resources or discover content; must filter before results are returned or used for model context.
- **Update:** modify resource properties or content.
- **Delete:** soft/hard delete according to retention policy, with explicit destructive-action checks.
- **Share/Invite:** grant another principal access or invite them into a tenant/workspace.
- **Execute:** run an agent, workflow, tool, connector or model action.
- **Configure:** change security-sensitive configuration, provider/model access or resource policy.
- **Export:** export data, secrets metadata, audit or billing records.
- **Manage billing:** change plans/payment settings or view protected billing data.
- **Administer identity:** manage tenant membership, identity-provider connections, API keys and session revocation.

## 4. Baseline role matrix

Legend: **A** = allowed within authorized tenant/resource scope; **O** = own resources only; **G** = granted/assigned resources only; **R** = read-only and filtered; **J** = requires explicit approval or step-up; **—** = denied by default. This is a product-policy proposal; row-level checks and constraints still apply.

| Resource/action | Owner | Tenant Admin | Member | Viewer | Resource Manager | Service Principal | Platform Operator |
|---|---|---|---|---|---|---|---|
| View tenant profile | A | A | A | A | — | G | metadata only by default |
| Update tenant profile | A | A | — | — | — | — | controlled platform metadata only |
| Invite/remove members | A | A | — | — | — | — | — |
| Change owner/admin roles | A* | J | — | — | — | — | — |
| View workspace metadata | A | A | A | R | G | G | metadata only by default |
| Create workspace | A | A | Configurable; default deny | — | — | G only when explicitly granted | — |
| Update/delete workspace | A | A | O/G | — | G | G | — |
| Access assigned files | A | A | G/O | R/G | G | G | — |
| Export tenant content | J | J | O/G with limits | — | G with limits | G with limits | — |
| Read/run own conversations | A | A | O/G | R/G | G | G | — |
| Access AI memory | A | A | O/G | R/G | G | G | — |
| Create/run agents/workflows | A | A | A/G | — | G | G | — |
| Configure tools/MCP connections | A | A/G | — | — | G if assigned | G if assigned | platform scope only |
| Configure provider/model policy | A | A/G | — | — | G if assigned | — | platform scope only |
| Create/revoke API keys | A | A for tenant keys | O with scope/limits | — | G only if explicitly granted | Rotate own workload credentials only | platform keys via separate controls |
| View usage/billing | A | A | own usage summary only | — | — | G for metering only | platform financial metadata only |
| Change billing/payment method | A | —/J | — | — | — | — | — |
| Read security/audit events | A (tenant-scoped) | A (tenant-scoped) | own security events only | — | — | G for required telemetry only | platform events only |
| Manage platform-wide configuration | — | — | — | — | — | — | J with separate platform authorization |
| Access customer content for support | — | — | — | — | — | — | J, time-bound, reason/ticket and audited |

* Ownership transfer should require a dedicated flow, re-authentication and audit; no role may grant itself ownership.  
Member workspace creation is denied by default. A tenant policy may explicitly enable it; if enabled, the server must evaluate the authoritative tenant policy and resource limits for each creation request.  
These broad roles are not enough for resource-level security. Ownership, sharing, membership status, resource state, data classification and explicit grants can further restrict access.

## 5. Mandatory invariants

1. Tenant Owner is not a platform superuser.
2. Tenant Admin cannot view billing payment secrets or platform secrets unless a separate permission explicitly grants a narrow action.
3. Platform Operator is not automatically allowed to read customer content.
4. Service principals do not inherit human permissions and must have explicit tenant/resource scope, audience and expiry/rotation controls.
5. Viewer is never allowed to mutate, execute tools, create API keys, export restricted data or change policy by default.
6. Role assignment is a privileged action; callers cannot grant a role higher than their own authorized grant ceiling.
7. No resource may be accessed by guessing its ID. Every operation checks the authoritative resource tenant and permission.
8. List, search, autocomplete, vector retrieval, exports and aggregate queries must not leak unauthorized resource existence or content.
9. A revoked member, API key or service principal loses access within the documented revocation target.
10. Destructive actions, bulk exports, billing changes, role elevation and support access require appropriate re-authentication/approval and audit.
11. Policy errors must fail closed. A policy-service timeout cannot be interpreted as allow.
12. AI model/tool output never grants permissions. Tool execution is authorized by trusted server-side policy.
13. Cache keys and background job payloads preserve tenant and authorization context; cache hits cannot bypass current policy.
14. RLS, if selected, is defense-in-depth; application policy checks remain required.
15. Audit records must not include raw access tokens, session cookies, API secrets or recovery codes.

## 6. Resource-specific policy notes

### Identity, sessions and membership
- Users can manage their own profile and sessions within defined limits.
- Tenant membership changes require Owner/Admin permission and audit.
- Removing a member invalidates tenant access and schedules revocation/cleanup across sessions, keys, queued jobs, caches and search indexes.
- Invitations are tenant-bound, expire, are single-use and cannot elevate beyond the inviter's grant ceiling.
- Account recovery and MFA removal use dedicated high-risk flows.

### Files, knowledge and retrieval
- Upload, read, update, delete, share and export are separate permissions.
- Search results must be filtered before snippet text enters the model prompt.
- File-derived knowledge inherits source permissions; indexing must not broaden access.
- Deletion/ACL changes trigger reindexing and cache invalidation, with a documented propagation objective.

### Agents, workflows, tools and MCP
- Configure, execute, approve and inspect are distinct permissions.
- A user allowed to run an agent is not automatically allowed to configure its tools or secrets.
- Tool permissions are checked at invocation time, including tenant, resource, action, approval status and risk tier.
- High-impact tools require explicit approval and idempotency/reconciliation controls.
- MCP server registration/configuration is separate from permission to invoke each exposed tool/resource.
- Agents cannot approve their own privileged actions unless a separately reviewed policy explicitly permits it.

### Provider/model and secrets
- Model availability is a tenant policy and can be further restricted by user/resource scope.
- Provider credentials are write-only/secret references; never return raw stored secrets.
- Changing model/provider allowlists, spending caps or routing policy requires configure permission and audit.
- Provider/tool calls must be checked before execution, not only after the result returns.

### Billing and usage
- Billing owner, invoice viewer and usage viewer should be separable permissions in the detailed product model.
- Usage attribution comes from trusted server-side events and tenant context.
- Payment instrument secrets are handled by the payment provider and never exposed to Aether roles.
- Refunds, plan changes, spending-limit changes and credits need explicit permissions and audit.

### Audit and support
- Tenant audit views are tenant-scoped and redact secrets.
- Platform support content access is disabled by default, time-limited, tied to a ticket/reason and recorded immutably where possible.
- Emergency access is separate, monitored and reviewed after use; it is not a hidden universal role.

## 7. Authorization decision contract

A policy decision should be evaluated over a typed input containing:
- principal ID and type;
- authentication assurance and recent-authentication timestamp when relevant;
- tenant ID resolved from trusted membership;
- action and resource type/ID;
- authoritative resource tenant, owner and sharing/ACL attributes;
- membership and resource state;
- workload audience/scopes when the principal is a service;
- contextual constraints (risk tier, approval state, data classification, rate/spend limits).

Decision result should include:
- allow or deny;
- stable reason code suitable for logs and safe diagnostics;
- policy version;
- obligations such as step-up, approval, redaction or rate limit, if supported.

Do not expose internal policy details to an untrusted caller if they reveal sensitive information. The policy input must be derived from trusted data sources, not blindly copied from request JSON.

## 8. Test matrix

For every protected action, write at least:
- permitted role + correct tenant + valid resource => allow;
- same role + different tenant => deny;
- lower role + same tenant => deny;
- suspended/removed member => deny;
- expired/revoked session or API key => deny;
- forged tenant ID/header/resource owner => deny;
- resource moved/deleted/ACL revoked between enqueue and execution => re-check or deny;
- policy service unavailable => fail closed;
- list/search/export/aggregate endpoint => no unauthorized existence or content leakage;
- audit entry exists for privileged action/denial, with no secrets.

Minimum POC scenarios:
1. Tenant A member cannot read/update/delete Tenant B file, conversation, agent, workflow, tool connection or billing record by direct ID.
2. Tenant Admin cannot assign themselves Owner or access platform secrets.
3. Viewer cannot execute tools or export restricted content.
4. Resource Manager can act only on explicitly assigned resources and actions.
5. Service principal cannot use a token intended for another service or tenant.
6. Removed member loses access to active session, API key, queue job and search results within documented targets.
7. Support access requires a ticket/reason, approval, expiry and audit; no approval means deny.
8. Cross-tenant search/vector retrieval yields zero unauthorized snippets in both API response and model context.
9. Tenant context does not leak across pooled database connections, concurrent requests or worker reuse.
10. Revoked file access is respected by cache, index and agent/tool paths.
11. Policy change takes effect within the agreed consistency target.
12. Bulk export and destructive action require the correct grant and step-up.
13. Policy evaluation outage fails closed and emits safe telemetry.
14. Audit records include actor, tenant, action, target, outcome, reason code and correlation ID, but no raw secrets.

No tests have been run; this is the test specification only.

## 9. Proposed policy implementation ownership

- aether-ai-security: policy contract, decision result/reason codes, shared policy test fixtures and policy versioning.
- aether-ai-auth: authenticated principal, assurance/session facts and identity mapping; not the sole resource-authorization authority.
- aether-ai-api: enforce checks on each protected request and resolve trusted tenant/resource context.
- aether-ai-gateway: enforce model/provider/spend/tool-call constraints before external calls.
- aether-ai-orchestration: preserve actor/tenant context and re-authorize delayed sensitive work.
- aether-ai-tools / aether-ai-mcp: register and invoke tools only through trusted authorization and approval gates; MCP transport is not an authorization substitute.
- aether-ai-database: tenant constraints and RLS support if chosen.
- aether-ai-observability: safe audit events and policy-decision telemetry.

Do not let each repository invent its own role semantics. Publish versioned contracts and shared negative tests. Avoid cyclic dependencies and do not require one deployed service per repository.

## 10. Open decisions and gates

This matrix is a baseline proposal, not an accepted product permission policy. The product owner must confirm which roles and resource classes are required.

Related open ADRs:
- ADR-0020: RBAC baseline versus ABAC/ReBAC or dedicated policy engine.
- ADR-0021: tenant/workspace hierarchy and privileged support access.
- ADR-0022: API-key and workload identity.
- ADR-0023: step-up/MFA and revocation targets.
- ADR-0024: tenant isolation and RLS rollout.
- ADR-0008 / ADR-0019: identity provider and browser session architecture.

Before implementation:
1. Confirm the first-launch resource inventory and role names.
2. Specify which Member/Viewer actions are tenant-configurable.
3. Define high-risk action tiers and approval/step-up requirements.
4. Agree on revocation and policy consistency targets.
5. Turn the test matrix into automated test cases in a future implementation phase.
6. Review the permission matrix and explicitly approve the implementation gate.

## 11. Sources

- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP API Security Top 10 (2023), Broken Object Level Authorization: https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
- IETF RFC 9700, OAuth 2.0 Security Best Current Practice: https://www.rfc-editor.org/rfc/rfc9700.html
- PostgreSQL Row Security Policies: https://www.postgresql.org/docs/current/ddl-rowsecurity.html


## Membership ownership and revocation consistency

This matrix must be read together with [Tenant Membership, Resource ACL and Revocation Consistency Decision](TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md). The membership/role-grant owner is still unresolved; `aether-ai-enterprise` is only a candidate if it is intended to be the universal tenant domain, and adding `aether-ai-tenancy` requires explicit approval to change the 33-repository plan. `aether-ai-auth` owns identity/session integration but is not automatically the canonical membership owner.

Access revocation is a safety boundary, not an eventual-index-cleanup task: protected operations must re-authorize against authoritative current state. Search/RAG, caches, queues, object storage and citations must suppress or deny stale access while asynchronous cleanup converges. Numeric cleanup SLOs remain open until product requirements and benchmarks are reviewed.
