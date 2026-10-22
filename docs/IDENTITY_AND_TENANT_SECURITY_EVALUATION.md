# Authentication, Identity, Multi-Tenancy and Authorization Evaluation

**Research date:** 2026-10-22  
**Status:** Research proposal; no identity provider or authorization implementation selected.  
**Phase:** Documentation and research only. No application code was written.

## 1. Executive summary

Aether AI needs a clear separation between (1) authenticating a person or workload, (2) mapping that identity to an Aether principal, (3) authorizing an action against a specific resource and tenant, and (4) enforcing that decision at each service/data boundary. A valid login or token must never be treated as proof that the caller may access every resource named in a request.

The current recommendation is to evaluate a managed OpenID Connect (OIDC) identity provider against a self-hosted option before selecting one. Keep Aether-owned tenant membership, roles, resource grants, policy decisions, and audit events in Aether's own domain model even if a third party handles credentials and login. Prefer standards-based OIDC/OAuth integration over provider-specific coupling. This is a direction to test, not an accepted ADR.

## 2. Scope and exclusions

In scope:
- Human users, organizations/workspaces, invitations, membership, roles, permissions and service identities.
- Login, logout, session lifecycle, recovery, MFA/passkeys, federation, API access and token validation.
- Tenant-aware authorization, database isolation, audit, security tests, account lifecycle and provider migration.
- Repository contracts for `aether-ai-auth`, `aether-ai-security`, `aether-ai-api`, `aether-ai-gateway`, `aether-ai-database`, `aether-ai-admin` and `aether-ai-enterprise`.

Out of scope:
- Selecting a vendor based on marketing alone.
- Building a custom password/identity provider before comparative evaluation.
- Treating UI hiding as authorization.
- Treating a tenant ID supplied by the client as trusted.
- Starting implementation before the documentation gate is approved.

## 3. Evidence and standards baseline

1. **OAuth 2.0 Security Best Current Practice, RFC 9700 (IETF, January 2025):** use authorization code flow with PKCE, exact redirect URI matching, transaction-bound state/nonce as applicable, and avoid deprecated/insecure flows. Source: https://www.rfc-editor.org/rfc/rfc9700.html
2. **NIST SP 800-63B-4 (July 2025):** current NIST guidance on authentication and authenticator management, assurance levels, and session considerations. It is a reference baseline, not a claim that Aether is a US government system. Source: https://csrc.nist.gov/pubs/sp/800/63/b/4/final
3. **PostgreSQL row-level security:** database policies can provide defense-in-depth, but table owners and privileged roles may bypass ordinary policies unless carefully configured. Source: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
4. **OpenID Connect Core 1.0 with errata set 2:** standard identity layer on OAuth 2.0. Source: https://openid.net/specs/openid-connect-core-1_0.html

Standards are minimum inputs to design; final implementation must verify the chosen provider and libraries against the exact flows and deployment architecture.

## 4. Identity-provider options to compare

| Option | Strengths | Risks / cost drivers | Required proof |
|---|---|---|---|
| Managed OIDC provider | Faster launch; hosted credential lifecycle, MFA and federation capabilities | Subscription/MAU costs, provider lock-in, data residency, outage dependency, limits and migration complexity | OIDC conformance, export/deletion, MFA/passkey support, custom domains, tenant/org features, logs, regional processing and outage behavior |
| Self-hosted identity platform | More control over hosting, configuration and data location | Operating and patching a security-critical service; upgrades, backups, abuse controls, key rotation and incident response become Aether's burden | Supported release cadence, security advisories, backup/restore, HA, federation, recovery flows and upgrade rehearsal |
| Build identity from scratch | Maximum local control | Highest security and maintenance risk; easy to mishandle passwords, recovery, MFA, sessions and OAuth/OIDC edge cases | Not recommended without a documented, exceptional requirement and independent security review |

**Evaluation rule:** compare at least one credible managed OIDC service and one credible self-hosted OIDC service using the same checklist. Do not pick a vendor until price, operational burden, security capabilities, data location, portability and failure modes are documented.

## 5. Proposed identity and authorization model

### 5.1 Principal types
- **User:** a human identity authenticated by an external or self-hosted identity provider.
- **Service principal:** a workload identity for service-to-service calls; no shared human credentials.
- **Tenant / organization:** the billing and administrative boundary.
- **Workspace / project:** an optional sub-scope inside a tenant.
- **Membership:** explicit link between a user/service principal and a tenant, with status and role/grants.
- **Resource:** a conversation, file, knowledge collection, agent, workflow, API key, billing record or other protected object.

### 5.2 Trust boundaries
- Treat email, display name and other profile attributes as claims, not stable authorization keys.
- Use the OIDC issuer + subject pair as the external identity key; do not assume email is immutable or globally unique.
- Resolve tenant membership server-side from trusted records. Do not authorize based solely on a request header, URL parameter, JWT custom claim, or client-supplied tenant ID.
- Every protected operation must evaluate principal, active membership, tenant/resource scope, requested action and resource state.
- Background jobs must carry an immutable actor/run/tenant context and revalidate authorization when executing sensitive or delayed actions.
- Service-to-service calls need explicit audience/scope and workload identity; do not forward a browser session token indiscriminately between services.

### 5.3 Authorization approach
Start with role-based access control (RBAC) for understandable organization roles, combined with resource-level checks and explicit policy conditions where needed. Do not adopt a complex policy language until actual requirements justify it.

Candidate built-in roles for evaluation, not final product commitments:
- Tenant Owner
- Tenant Admin
- Member
- Read-only Viewer
- Service principal with narrowly scoped grants

Avoid relying on a single broad role for system operators. Separate platform support access from tenant ownership, require reason/ticket and audit for privileged support access, and default to time-limited elevation where feasible.

## 6. Sessions, tokens and account lifecycle

- Browser: evaluate a backend-for-frontend (BFF) pattern with opaque server-side session identifiers in Secure, HttpOnly, appropriately SameSite cookies. Compare with a direct SPA OAuth flow only if a concrete need exists.
- API: validate issuer, audience, signature, expiry, allowed algorithms and required claims. Reject tokens intended for another service or environment.
- OAuth/OIDC: authorization code flow with PKCE; exact redirect URI allowlists; transaction-specific state and nonce; protect callback routes; never accept arbitrary redirect destinations.
- Token lifetimes: choose access-token lifetime from threat and latency requirements; document refresh-token rotation/reuse detection or provider-managed equivalent. Define revocation propagation expectations.
- Logout: distinguish local session termination from identity-provider global logout. Ensure local sessions can be revoked without waiting for access-token expiry.
- Sensitive changes: require recent authentication or step-up for password/email changes, MFA removal, API-key creation, tenant ownership changes, billing/security settings and other high-impact actions.
- Recovery and MFA: assess phishing-resistant passkeys/WebAuthn, recovery codes, abuse-resistant account recovery and support procedures. Avoid weak recovery channels becoming an MFA bypass.
- Secrets: keep provider secrets and signing material server-side; use a managed secret store where available, rotate keys, and never log credentials, authorization codes, tokens or recovery codes.
- API keys: store only a verifier/hash where feasible; show a new secret once; scope to tenant, purpose and permissions; support expiry, rotation and revocation; audit use; do not use API keys as human login sessions.

## 7. Multi-tenancy and data isolation

1. A tenant context is established by the API after authentication and membership lookup, not trusted directly from the client.
2. Tenant-owned tables should include tenant scope where appropriate and use composite constraints/foreign keys to prevent cross-tenant relationships.
3. Add database row-level security as a second enforcement layer if PostgreSQL is selected. Use a non-owner runtime role without BYPASSRLS; evaluate FORCE ROW LEVEL SECURITY where appropriate. Test pooled connections for context leakage/reset on success and failure.
4. Cross-tenant administrative workflows must be explicit, separately authorized and audited.
5. Tenant scope must flow through caches, queues, search/vector indexes, object storage, logs, analytics and exports. Namespacing alone is not authorization.
6. Search and retrieval results must be filtered by current authorization before content is passed to a model. A model must not be relied on to enforce access policy.
7. Deletion, membership removal and tenant suspension must propagate to sessions, API keys, queued work, caches, search indexes and object storage within documented bounds.
8. Billing and usage attribution must derive from trusted server-side tenant context and usage events, not client-supplied labels.

## 8. Repository ownership and contracts

| Repository | Responsibility | Must not own |
|---|---|---|
| `aether-ai-auth` | Identity-provider adapter, login callback/session integration contracts, account lifecycle integration | Product-wide resource authorization decisions hidden inside UI-specific code |
| `aether-ai-security` | Shared policy interfaces, permission evaluation, security primitives and threat-policy contracts | Credentials database or provider-specific login implementation |
| `aether-ai-api` | Authenticate requests, resolve principal and tenant context, call authorization before protected operations | Trusting client tenant IDs or duplicating inconsistent policy logic |
| `aether-ai-gateway` | Authenticate/authorize model requests and enforce tenant/provider/model limits | Assuming a valid user token grants access to every model/provider |
| `aether-ai-database` | Schema, migrations, database roles, tenant constraints and RLS policy migrations | Owning application-level identity provider selection |
| `aether-ai-admin` | Administrative UI for allowed operations | Being a security boundary; UI controls never replace API checks |
| `aether-ai-enterprise` | Enterprise SSO/SCIM and tenant policy requirements if adopted | Reimplementing core authentication and authorization logic |
| `aether-ai-observability` | Redacted security/audit telemetry and correlation | Storing raw tokens, secrets or unnecessary identity attributes |

Contracts should be versioned and stable. Avoid cyclic dependencies: auth supplies identity context; security evaluates policies against domain contracts; APIs and workers enforce decisions; database policies provide additional containment.

## 9. Threat scenarios and required mitigations

| Threat | Minimum design/test response |
|---|---|
| Cross-tenant IDOR/BOLA | Test every read/write endpoint with a valid user from another tenant; deny by default |
| Forged tenant header/claim | Ignore untrusted tenant selection; resolve active membership server-side |
| Token substitution or replay across services | Enforce issuer/audience, signature and expiry; separate token purposes; test wrong-audience tokens |
| OAuth callback CSRF/code injection | PKCE, state/nonce binding, exact redirect URIs and single-use callback handling |
| Session fixation/theft | Rotate session on login/privilege change; secure cookie flags; revoke session on logout and risk events |
| Privilege escalation | Central policy checks; prohibit self-granting owner/admin roles; require dual control for sensitive operations where appropriate |
| Stale membership/queued work | Re-check authorization for delayed sensitive jobs; revoke sessions/keys and define propagation bounds |
| RLS bypass | Runtime role is not owner/superuser and lacks BYPASSRLS; negative tests against real database role |
| Secret/token leakage | Structured redaction in logs, traces, errors and support tooling; automated canary-secret tests |
| Identity-provider outage | Document fail-closed behavior for new authentication; define safe handling for existing sessions and admin recovery |
| Account recovery takeover | Threat-model recovery; rate-limit; notify user; require stronger proof for high-risk account changes |
| SCIM/invitation abuse | Validate issuer and tenant, idempotent provisioning, verified domain rules, invitation expiry and audit |

## 10. Proof-of-concept acceptance tests

The identity-provider and authorization POC must include at least:
1. OIDC login success and failure; invalid issuer, signature, audience, nonce, state and expired token rejection.
2. PKCE required for authorization code flow; exact redirect URI mismatch rejected.
3. Session cookie flags, session rotation at login/privilege change, logout and server-side revocation.
4. Refresh token rotation/reuse behavior or provider-managed equivalent.
5. MFA/passkey enrollment, recovery and removal; step-up on high-impact actions.
6. User with no tenant membership cannot access tenant resources.
7. Tenant A cannot read/update/delete Tenant B resources through IDs, filters, exports, search, files or tools.
8. Forged tenant headers/parameters cannot change effective tenant context.
9. Member cannot grant themselves Owner/Admin; removed members lose access within defined propagation target.
10. API key scope, expiry, rotation and revocation; key cannot cross tenant or service boundaries.
11. Worker re-checks permissions for delayed sensitive jobs and cannot act with stale tenant membership.
12. RLS tested as the actual non-owner application role, including pooled-connection reuse and missing context.
13. Audit records contain actor, tenant, action, target, result and correlation ID without raw secrets/tokens.
14. Provider outage and signing-key rotation are exercised; key cache refresh and failure behavior are documented.
15. Accessibility, rate limiting, enumeration resistance and account-recovery abuse checks.
16. Deletion and offboarding propagate to caches, queues, indexes and storage within the documented service-level objective.

No POC is claimed to have run. These are acceptance criteria.

## 11. Open decisions

- ADR-0008: managed versus self-hosted identity provider; provider shortlist and evaluation scorecard.
- ADR-0019: browser session architecture (BFF/server-side session versus direct SPA flow).
- ADR-0020: authorization model and policy engine scope (RBAC baseline plus resource checks versus richer ABAC/ReBAC).
- ADR-0021: tenant/workspace hierarchy and support-operator access model.
- ADR-0022: API-key, workload identity and service-to-service token standards.
- ADR-0023: MFA/passkey, recovery, session duration and revocation SLOs.
- ADR-0024: tenant isolation strategy, PostgreSQL RLS rollout and test ownership.

All remain open pending comparison and explicit review. No vendor or architecture choice is accepted by this document.

## 12. Research links

- IETF RFC 9700, OAuth 2.0 Security BCP: https://www.rfc-editor.org/rfc/rfc9700.html
- NIST SP 800-63B-4: https://csrc.nist.gov/pubs/sp/800/63/b/4/final
- OpenID Connect Core 1.0: https://openid.net/specs/openid-connect-core-1_0.html
- PostgreSQL Row Security Policies: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
