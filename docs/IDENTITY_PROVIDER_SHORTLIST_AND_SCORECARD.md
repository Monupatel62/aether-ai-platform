# Identity Provider Shortlist and Evaluation Scorecard

**Research date:** 2026-10-22  
**Status:** Comparative shortlist; no provider selected.  
**Project phase:** Documentation and research only.

## 1. Purpose

Compare realistic identity-provider candidates for Aether AI using official documentation and a repeatable proof-of-concept scorecard. This document is not a procurement decision and does not establish that any candidate has passed a security review.

The current shortlist is:
1. **ZITADEL Cloud / self-hosted** — standards-oriented IAM with a first-class organization model and both hosted and self-managed deployment paths.
2. **Keycloak** — self-hosted identity and access management with OIDC/SAML, organization features and WebAuthn/passkeys; operations and upgrades are Aether's responsibility.
3. **Auth0** — managed identity service with B2B Organizations, enterprise connections and hosted login; commercial plan limits and pricing need confirmation.

These candidates represent different operating models. Aether should compare a managed option with a self-hosted option under the same workload, not choose based only on a feature checklist.

## 2. Evidence reviewed

- ZITADEL product/docs: https://zitadel.com/docs
- ZITADEL end-user onboarding and identity-provider integration: https://zitadel.com/docs/guides/integrate/onboarding/end-users and https://zitadel.com/docs/guides/integrate/identity-providers/generic-oidc
- ZITADEL API overview: https://zitadel.com/docs/apis/introduction
- Keycloak Server Administration Guide 26.0.8: https://www.keycloak.org/docs/26.0.8/server_admin/
- Auth0 Organizations: https://auth0.com/organizations
- Auth0 passkey setup guidance: https://developer.auth0.com/resources/labs/authentication/passkeys
- IETF OAuth 2.0 Security BCP RFC 9700: https://www.rfc-editor.org/rfc/rfc9700.html
- OpenID Connect Core 1.0: https://openid.net/specs/openid-connect-core-1_0.html

**Evidence caveat:** vendor documentation confirms advertised capabilities, not security effectiveness, price suitability, uptime, regional processing, or behavior under Aether's exact configuration. Pricing, plan gates, contractual terms and release-specific support must be checked directly during the POC.

## 3. Candidate comparison

| Criterion | ZITADEL | Keycloak | Auth0 |
|---|---|---|---|
| Operating model | Cloud and self-hosted options | Primarily self-hosted; operator owns deployment | Managed service |
| OIDC/OAuth | Documented standards-based endpoints | Mature OIDC/OAuth and SAML support | Managed OIDC/OAuth integration |
| B2B organizations | First-class organization model | Organizations feature for B2B use cases | Organizations feature for B2B identity |
| Enterprise federation | External IdP support documented | Identity brokering/federation | Enterprise connections documented |
| Passkeys/WebAuthn | Passkeys listed in docs | Admin guide says passkeys are preview in version 26.0.8; verify current release status | Supported subject to flow/connection prerequisites |
| Audit | Audit/event capabilities documented; verify export and retention details | Verify event/audit configuration and retention | Verify log retention, export and plan limits |
| Operational burden | Low for cloud, higher for self-hosted | Highest of shortlist: patching, HA, backups, monitoring, upgrades | Low infrastructure burden, but provider dependency remains |
| Portability | OIDC reduces application coupling; management APIs/features can still be proprietary | Open-source/self-hosted path gives deployment control; custom extensions create upgrade burden | OIDC reduces app coupling; management workflows and vendor features may create lock-in |
| Commercial unknowns | Cloud plan/usage/support limits and self-hosted support model | Infrastructure and engineering cost; feature/version validation | MAU/enterprise feature pricing, quotas, support and log retention |
| Primary risk to validate | Fit between organization model and Aether's independent tenant authorization | Operational competence and upgrade/extension maintenance | Cost/plan gates, data location and exit/migration path |

## 4. Initial evaluation posture

This is a **shortlist**, not a ranking or selection.

- ZITADEL is a useful first candidate to test because its documentation describes both managed and self-hosted deployment, organization-level capabilities, OIDC/SAML and passkeys.
- Keycloak is the self-hosted control candidate; its operational cost and release-specific feature maturity must be treated as first-class evaluation items. In the reviewed 26.0.8 guide, passkeys are marked preview, so verify the version actually tested rather than assuming parity.
- Auth0 is the managed benchmark candidate for developer effort and B2B onboarding. Confirm all required organization, enterprise SSO, passkey, audit and export capabilities against the exact proposed commercial plan.

No vendor is selected by this document. If a candidate cannot meet a required control without a paid plan or a custom extension, record that as a measured trade-off.

## 5. Scorecard

Score each candidate 1–5 after testing, where 1 = fails/unacceptable, 3 = acceptable with documented caveats, and 5 = strong fit with repeatable evidence. Mark unsupported or untested as **N/T**, not as a guessed score.

| Category | Weight | Evidence required |
|---|---:|---|
| Protocol/security correctness | 20% | OIDC discovery, signature/issuer/audience checks, state/nonce, PKCE, redirect URI enforcement, key rotation |
| Tenant and organization model | 15% | Multi-org users, org-specific IdP, membership removal, no implied authorization from token tenant claims |
| Account security and recovery | 10% | MFA/passkeys, recovery, step-up, anti-enumeration and rate limits |
| Session/token lifecycle | 10% | Session revocation, refresh-token behavior, logout, key rotation and documented propagation bounds |
| Audit and export | 10% | Security events, admin actions, export API, retention, redaction and external SIEM compatibility |
| Operations and reliability | 10% | HA, backup/restore, upgrade rehearsal, outage behavior, key rollover and monitoring |
| Data residency and privacy | 10% | Processing regions, subprocessors, retention/deletion terms and contractual commitments |
| Cost and scalability | 10% | 12/24-month modeled total cost under low, expected and high MAU/SSO scenarios |
| Portability and exit | 5% | User export, identity mapping, migration rehearsal, application-side OIDC abstraction |

Do not produce a weighted winner until all mandatory security criteria pass. A high commercial score cannot offset a security failure.

## 6. Proof-of-concept plan

### Phase A — protocol and application integration
- Use a throwaway environment and non-production identities.
- Integrate a minimal test client using authorization code + PKCE.
- Verify issuer, audience, signature, expiry, nonce/state and exact redirect URI validation.
- Exercise login, logout, session expiry, key rotation and provider outage.
- Confirm secrets never enter the browser bundle, source control, logs or traces.

### Phase B — B2B and authorization
- Create two tenants and users with different roles.
- Verify users can belong to multiple tenants only when Aether membership records explicitly allow it.
- Test tenant switching, invitations, organization-specific enterprise IdP, member removal and account linking.
- Attempt cross-tenant reads/writes using guessed IDs, forged headers, token claims and search/file routes.
- Verify application authorization remains authoritative even when the identity provider emits organization or role claims.

### Phase C — operations, privacy and exit
- Test export, deletion and audit export.
- Rehearse signing-key rotation and a provider outage.
- For self-hosted candidates, rehearse backup restore, upgrade, rollback and alerting.
- For managed candidates, record data-processing region, subprocessors, log retention, plan limitations and support response commitments.
- Estimate total cost and engineering hours for launch and ongoing operations.

### Phase D — migration rehearsal
- Document the canonical Aether principal ID and mapping from issuer + subject.
- Test what happens if issuer, tenant, email or provider changes.
- Confirm migration does not merge accounts solely because email addresses match.
- Prove that a provider migration preserves tenant membership and audit identity, or document the unavoidable re-authentication/recovery steps.

## 7. Mandatory acceptance gates

A candidate fails if any of these occur:
- Wrong issuer/audience/signature or expired tokens are accepted.
- Redirect URI validation is permissive or PKCE/state/nonce controls can be bypassed.
- Provider organization claims grant access without an Aether-side membership/policy check.
- A user from Tenant A can read or modify Tenant B data.
- Revoked members or credentials retain access beyond the agreed and documented bound.
- Tokens, secrets, recovery codes or sensitive authentication payloads appear in logs.
- Backup/restore or key-rotation behavior is unknown for the selected operating model.
- Required export/deletion, data residency or contractual requirements cannot be met.

## 8. Aether-specific integration boundary

Regardless of the winner:
- Keep the Aether principal identifier stable and store external identity as issuer + subject.
- Keep tenant membership, roles, resource permissions, billing identity and security audit ownership inside Aether's domain.
- Wrap provider integration behind `aether-ai-auth`; avoid provider-specific imports throughout API/domain code.
- Put policy contracts and authorization decisions behind `aether-ai-security`.
- Require `aether-ai-api`, gateway and background workers to enforce authorization at each protected operation.
- Keep identity-provider organization claims as inputs to membership/onboarding workflows, not as a replacement for Aether authorization.
- Provide an exit/migration plan before production rollout.

## 9. Decisions still open

- ADR-0008: identity provider and deployment model.
- ADR-0019: browser session/BFF design.
- ADR-0020: authorization model and policy engine scope.
- ADR-0021: tenant hierarchy and privileged support access.
- ADR-0022: API keys and workload identity.
- ADR-0023: MFA, recovery, session and revocation targets.
- ADR-0024: database tenant isolation and RLS rollout.

Next decision checkpoint: run the same POC against ZITADEL and Keycloak, with Auth0 as the managed benchmark if budget and account access permit. Confirm current pricing and features directly before any selection. No POC has run as part of this research update.
