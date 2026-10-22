# Browser Session and Authorization Architecture Evaluation

**Research date:** 2026-10-22  
**Status:** Proposed design evaluation; no implementation or final ADR decision.  
**Phase:** Documentation and research only.

## 1. Executive summary

Aether AI should evaluate a Backend for Frontend (BFF) with a server-side session as the default browser architecture for its first-party web application. This keeps OAuth tokens out of browser JavaScript and provides a central place to enforce session expiry, revocation, tenant context, CSRF protection and audit correlation. The trade-offs are additional backend/session-store operations and the need to design CSRF defenses carefully.

This is a candidate recommendation, not an accepted ADR. Native/mobile apps, third-party API clients and service-to-service workloads have different threat models and should use appropriate client patterns.

The IETF published RFC 10017, OAuth 2.0 for Browser-Based Applications, in August 2026. It describes BFF, token-mediating backend and browser-based OAuth client patterns in decreasing order of security. Use this current BCP alongside RFC 9700. Sources: https://www.rfc-editor.org/rfc/rfc10017.html and https://www.rfc-editor.org/rfc/rfc9700.html.

## 2. Browser architecture options

| Pattern | Benefits | Risks / costs | Fit for Aether web |
|---|---|---|---|
| BFF + server-side session | Tokens remain server-side; central request boundary; server-side revocation | Session-store availability, CSRF protection, extra hop and backend capacity | Preferred candidate for first-party web POC |
| Token-mediating backend | Backend handles OAuth; browser can call resource APIs directly | Access token remains exposed to browser runtime; XSS impact and revocation need careful handling | Consider only if direct browser-to-resource access is required |
| Browser-based OAuth client (SPA) | Static deployment and direct API calls | Public client cannot protect a client secret; browser runtime is exposed to malicious scripts | Not preferred for the primary web app without a threat review |
| Native/mobile public client | Appropriate for installed apps using system browser and platform-specific redirects | Device compromise, secure token storage and callback risks | Separate future decision; do not blindly reuse web BFF design |

## 3. Proposed BFF request flow

1. Browser redirects to the configured identity provider.
2. Use authorization code flow with PKCE, exact registered redirect URIs, state binding and OIDC nonce validation.
3. BFF validates callback and exchanges the code server-side. Client secrets and provider tokens never enter browser JavaScript.
4. BFF creates a fresh, unpredictable server-side session after successful login and relevant privilege changes.
5. Browser receives only a session cookie with Secure, HttpOnly, an explicit SameSite policy and narrow host/path scope. Prefer a __Host- cookie when the deployment topology supports its requirements.
6. Each request resolves the session, checks expiry/revocation, maps identity by issuer + subject, resolves active tenant membership server-side and applies authorization.
7. Internal services receive only the minimum required validated principal/tenant context over authenticated channels. Do not blindly forward the browser cookie or identity-provider token.
8. Logout revokes the Aether session server-side and clears the cookie. Provider logout is a distinct operation.

A session cookie is a bearer credential. HttpOnly reduces direct JavaScript access to the cookie but does not stop XSS from issuing authenticated requests in the victim's browser.

## 4. Session lifecycle requirements

- Generate opaque, high-entropy session identifiers with a cryptographically secure generator. Do not encode PII, tenant names or roles in session IDs.
- Rotate session ID at login and after privilege elevation or other relevant authentication changes.
- Define idle and absolute expiry from risk and usability requirements; record values as open decision inputs.
- Support revocation by session, user, tenant, security event and administrative action.
- Define revocation propagation targets for APIs, caches, long-running jobs and streaming connections.
- Prevent pooled workers and concurrent requests from leaking session or tenant context.
- Keep OAuth tokens and session secrets out of URLs, browser storage, analytics, errors, traces and logs.
- Require recent authentication/step-up and re-check authorization for high-impact actions.
- If the server-side session store is unavailable, fail closed for protected operations.

## 5. CSRF, CORS and browser protections

Cookie-based authentication means the browser may attach credentials automatically. The BFF must explicitly handle CSRF rather than assuming SameSite is sufficient.

- Use a synchronizer token or another well-reviewed CSRF defense for state-changing requests; verify Origin/Referer as defense in depth where appropriate.
- Never use GET for state-changing actions.
- Set explicit SameSite=Lax or Strict after evaluating cross-site login callbacks; never use SameSite=None without Secure.
- Keep CORS origins exact and minimal. CORS is not an authorization system and does not replace CSRF controls.
- Apply CSP, output encoding, dependency hygiene and safe third-party script policies to reduce XSS likelihood.
- Do not put credentials in URLs or redirect to arbitrary client-supplied URLs.
- Use TLS end-to-end or document trusted proxy termination and forwarded-header handling.

## 6. Authorization model evaluation

### Candidate baseline: RBAC + resource-level checks

Use roles for broad administrative capabilities, but authorize each operation using explicit checks over:
- authenticated principal and principal status;
- active tenant membership and membership status;
- requested action;
- resource's authoritative tenant and ownership/sharing state;
- contextual conditions such as resource lifecycle, approval state or recent authentication;
- service/workload identity and audience where applicable.

Use deny by default and validate permission on every protected request. OWASP guidance: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html.

### Alternatives to consider only where needed

- ABAC: useful for conditions based on tenant, classification, environment or resource state; attribute freshness and policy complexity need controls.
- ReBAC: useful for sharing, ownership, groups, folders and nested resources; adds relationship storage and consistency complexity.
- Dedicated policy engine: can centralize policy decisions and testing but adds a runtime dependency, policy deployment lifecycle and availability concern.

Do not pick a policy engine before representative Aether use cases are documented. Start with a versioned authorization interface and a clear policy test suite so implementation can evolve without scattering rules across services.

## 7. Tenant context and enforcement

- Resolve active tenant from Aether membership and resource data, not solely from browser headers, URL parameters or identity-provider claims.
- Tenant switching is a request to select context; validate membership before using that context.
- Pass typed, validated principal/tenant context through service boundaries. Avoid mutable global request context.
- If PostgreSQL is selected, evaluate row-level security as defense in depth using a non-owner runtime role without BYPASSRLS.
- Search, RAG, file storage, caches, queues and model tool calls must preserve authorization context. Re-check access before returning or using retrieved content.
- Workers must re-check permissions for delayed sensitive operations; enqueue-time permission can become stale.
- Audit privileged denials without leaking whether inaccessible resources exist, where practical.

## 8. Repository responsibilities

| Repository | Responsibility |
|---|---|
| aether-ai-web | UI and login initiation; not a security boundary; no persistent OAuth secrets in browser storage |
| aether-ai-auth | OIDC callback integration, BFF/session lifecycle interface and identity mapping |
| aether-ai-security | Shared authorization interfaces, policy contracts, deny-by-default semantics and policy test fixtures |
| aether-ai-api | Validate principal/session, resolve tenant context and enforce policy on protected operations |
| aether-ai-gateway | Enforce model/provider/tenant limits and policy before model calls and tool use |
| aether-ai-orchestration | Persist actor/tenant/run context and re-check authorization for delayed/high-impact work |
| aether-ai-database | Session/membership schema, constraints, database roles and RLS migrations if selected |
| aether-ai-observability | Audit/telemetry redaction, correlation IDs and security event routing |

Repository boundaries do not imply one deployable service per repository. Keep contracts stable and avoid cyclic imports.

## 9. Threat model and POC tests

| Test | Expected result |
|---|---|
| Missing, malformed, expired or revoked session | Protected request denied |
| Reuse pre-login session ID | Rejected; new session ID issued |
| Wrong issuer/audience/signature or expired callback token | Login rejected |
| Open redirect or non-exact callback URI | Rejected |
| CSRF request from untrusted origin | State change denied |
| Tenant ID/header forged by client | Membership validated server-side; unauthorized tenant denied |
| Tenant A resource ID used under Tenant B | Denied for reads, writes, exports, search and tools |
| User removed from tenant | Access revoked within documented target |
| Session-store outage | Protected request fails closed |
| Worker has stale tenant context | Context revalidated or operation denied |
| Token/cookie appears in logs/traces/errors | Test fails; redaction corrected |
| Policy or role changes | Effective permissions update within documented consistency target |
| Unauthorized lookup | Safe denial without unintended existence disclosure |

No tests are claimed to have been executed. These are future POC acceptance criteria.

## 10. Open decisions

- ADR-0019: BFF + server-side session versus alternative browser architecture.
- ADR-0020: RBAC baseline and scope for ABAC/ReBAC/policy engine.
- ADR-0021: tenant/workspace hierarchy and privileged support access.
- ADR-0023: session expiry, MFA/step-up and revocation targets.
- ADR-0024: tenant isolation and database enforcement.
- Related ADR-0008: identity provider.

Before implementation, document user flows, client types, deployment topology, domain/subdomain model, concurrency, outage behavior and session/revocation targets. Then run the same acceptance tests against the shortlisted provider(s).

## 11. Sources

- IETF RFC 10017, OAuth 2.0 for Browser-Based Applications (August 2026): https://www.rfc-editor.org/rfc/rfc10017.html
- IETF RFC 9700, OAuth 2.0 Security Best Current Practice: https://www.rfc-editor.org/rfc/rfc9700.html
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- PostgreSQL Row Security Policies: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
