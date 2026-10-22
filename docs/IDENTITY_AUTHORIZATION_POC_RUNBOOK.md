# Identity and Authorization Proof-of-Concept Runbook

**Date prepared:** 2026-10-22  
**Status:** Execution plan only. Not approved to run; no provider selected; no tests performed.  
**Supports:** ADR-0008, ADR-0019 through ADR-0024.  
**Scope:** Compare identity/session candidates and validate Aether-owned authorization boundaries without production data or production credentials.

## 1. Purpose and guardrails

This runbook makes the identity/authorization evaluation repeatable. It does not implement the platform or decide an identity provider. Run only after the product owner explicitly approves the POC scope, test environment, cost ceiling and test operators.

Hard constraints:
- Use synthetic users, tenants, files and content only.
- Use isolated test tenants/projects and non-production credentials.
- Do not use real customer data, production signing keys, production OAuth clients or live customer integrations.
- Do not modify WoHo AI DevKit source, main branch, package versions or release pipeline.
- Do not expose tokens, cookies, authorization codes, secrets or prompt content in logs.
- Do not create or add Aether repositories during the POC.
- No provider is selected by the existence of this runbook.

## 2. Candidates and comparison fairness

Candidates already shortlisted:
1. ZITADEL (hosted and/or self-hosted, subject to confirmed feature and pricing availability).
2. Keycloak (self-hosted).
3. Auth0 (managed benchmark only if account access, plan features and budget allow).

Use the same logical scenarios, application-facing OIDC adapter contract, synthetic users, test data and acceptance rules for each candidate. Provider-specific configuration may differ, but document every difference. If a candidate cannot support a scenario on the evaluated plan/deployment, record **Unsupported/Not tested**; do not assume feature parity.

A provider's organization or group claims are identity inputs only. Aether's canonical membership and resource policy remain separate and must be evaluated server-side.

## 3. POC architecture and fixtures

### Components
- Minimal isolated test client representing the first-party web app.
- BFF/server-side session candidate with secure cookie and CSRF protection.
- OIDC provider under test.
- Mock Aether membership/policy adapter with versioned synthetic records.
- Protected test API with tenant-owned resources.
- Mock queue worker that re-checks permissions before delayed sensitive work.
- Synthetic search/RAG result fixture containing tenant/source/ACL versions.
- Redacted structured test results and an append-only run manifest.

### Synthetic fixture
- Tenant A: owner, admin, member, viewer and service principal.
- Tenant B: owner and member, used for cross-tenant denial tests.
- At least two workspaces per tenant, with separate membership and resource grants.
- A private file, a shared file, a conversation, a knowledge source with derived chunks/citation, a queued job, an API key/workload identity and an audit event.
- One suspended tenant, one removed member, one revoked grant and one expired credential.
- Unique canary strings for secrets and protected content; verify they never appear in logs/traces.

### Run manifest
For every run record: date/time, operator, candidate/provider version, deployment mode, region, relevant plan/tier, client/library versions, configuration digest (never secrets), test fixture version, scenario ID, result, sanitized evidence pointer, latency where measured, known deviations and reviewer. Store no tokens or raw protected content in evidence.

## 4. Test procedure

1. Approve scope, spend ceiling, test operators and data handling.
2. Capture candidate feature/pricing/region evidence from official vendor documentation; mark unknowns explicitly.
3. Provision isolated test environment with least-privilege admin accounts.
4. Configure OIDC authorization code flow with PKCE, exact redirect URIs and transaction-bound state/nonce as applicable.
5. Implement only the minimum test harness needed for the agreed scenarios; no product features or production deployment.
6. Run baseline login/logout/session tests, then authorization and tenant isolation cases.
7. Run failure tests: provider outage, policy dependency timeout, session revocation, duplicate/out-of-order lifecycle events, worker retry and stale search fixture.
8. Export redacted results and dependency/license information.
9. Repeat failures to confirm reproducibility; record nondeterministic behavior and environmental limitations.
10. Have a reviewer examine all hard-gate failures before scoring convenience, cost or performance.
11. Populate the scorecard; do not infer a winner from missing evidence.
12. Update the relevant ADR only after explicit review and approval.

## 5. Scenario register and acceptance gates

| ID | Scenario | Pass condition | Severity / gate |
|---|---|---|---|
| ID-01 | OIDC authorization-code login with PKCE | Valid flow succeeds; no implicit/password grant dependency | Hard security gate |
| ID-02 | Redirect URI mismatch | Provider rejects unregistered/mismatched URI | Hard security gate |
| ID-03 | State/nonce replay or mismatch | Callback is rejected safely; session is not created | Hard security gate |
| ID-04 | Secure browser session | HttpOnly, Secure and appropriate SameSite cookie controls; no provider token in browser JS | Hard security gate |
| ID-05 | CSRF on state-changing action | Missing/invalid CSRF defense is rejected | Hard security gate |
| ID-06 | Login and privilege-change session rotation | Old session cannot retain the previous privilege context | Hard security gate |
| ID-07 | Logout and server-side revocation | Revoked session cannot perform the next protected request | Hard security gate |
| ID-08 | Tenant A resource ID requested by Tenant B | Deny without content or existence leakage | Hard security gate |
| ID-09 | Forged tenant header/URL/claim | Server resolves tenant from trusted membership/resource records; forged selection does not grant access | Hard security gate |
| ID-10 | Removed membership with active global session | Tenant access is denied on the next protected operation; unrelated allowed tenant may remain available if designed so | Hard security gate |
| ID-11 | Role downgrade/grant revocation | Next protected operation uses current policy; no stale allow | Hard security gate |
| ID-12 | Admin attempts to read private conversation/memory | Matches the explicitly approved product policy; no implicit broad content access | Product-policy gate |
| ID-13 | Search/RAG stale index after ACL revoke | No protected snippet, content or citation enters API response or model context | Hard security gate |
| ID-14 | Delayed queue job after membership/ACL revoke | Worker rechecks authorization and denies/cancels sensitive action | Hard security gate |
| ID-15 | API key/workload credential scope | Wrong audience, tenant, scope or expired/revoked credential is denied | Hard security gate |
| ID-16 | Policy dependency timeout | Protected action fails closed with safe error and telemetry | Hard security gate |
| ID-17 | Database tenant isolation (if RLS adopted) | Cross-tenant access denied under actual non-owner runtime role; pooled context reset verified | Hard security gate if RLS is in scope |
| ID-18 | Support/emergency access | Disabled by default; only approved, time-bound, reason/ticket-bound flow works and is audited | Hard security gate if support access is in scope |
| ID-19 | Secret-canary logging test | Tokens, cookies, secrets and protected content do not appear in default logs/traces | Hard security gate |
| ID-20 | Audit completeness | Privileged changes and required denials record actor, tenant, action, target, outcome, policy/version and correlation ID without secrets | Hard security gate |
| ID-21 | Provider outage/recovery | Defined user-visible failure, safe retry and recovery behavior; no fail-open authorization | Hard security gate |
| ID-22 | Export/deletion lifecycle | Approved export scope enforced; deletion/revocation cannot be undone by stale projection or restore | Hard gate for lifecycle scope |
| ID-23 | MFA/passkey and recovery | Required assurance, recovery and step-up policy behave as approved; no recovery bypass | Hard security gate if in scope |
| ID-24 | Migration/exit | Principal mapping, membership and audit export behavior documented; vendor-specific claims isolated behind adapter | Portability gate |

**Hard-gate rule:** Any reproducible failure in authorization, cross-tenant isolation, token/session handling, secret redaction, or fail-closed behavior blocks candidate acceptance regardless of score, convenience or latency.

## 6. Measurement protocol

Measure only after correctness/security gates pass:
- Login/callback/session creation latency: p50/p95 over a documented number of synthetic trials.
- Protected API authorization overhead: p50/p95 with warm and cold policy/membership reads.
- Revocation: time from authoritative state change to denial on a fresh protected request; report p50/p95/p99 and test method.
- Projection cleanup: time to suppress/remove test data from search/RAG/cache/object storage; do not conflate this with the immediate authorization-denial gate.
- Availability/failure behavior: provider outage, network timeout and policy-service timeout.
- Operator effort: setup/upgrade/backup/monitoring tasks and measured time.
- Estimated cost: evaluated plan/region, expected MAU/tenant/traffic assumptions, infrastructure and support effort. Label estimates and assumptions; confirm current prices directly.

Do not invent targets after observing results. Product owner sets acceptable latency, availability, revocation and cost targets before comparing the measured outcomes.

## 7. Weighted scorecard template

First apply hard gates. Only candidates that pass all applicable hard gates may receive a weighted comparison.

| Criterion | Weight | Evidence required | Candidate score |
|---|---:|---|---|
| OIDC/OAuth correctness and client compatibility | 15 | ID-01 to ID-03; official conformance/features | TBD |
| Session, logout, CSRF and revocation | 15 | ID-04 to ID-07, ID-10, measured behavior | TBD |
| Tenant authorization integration | 15 | ID-08 to ID-14, policy/membership separation | TBD |
| MFA, recovery and step-up | 10 | ID-23, verified plan/features | TBD |
| Workload/API-key integration | 8 | ID-15, lifecycle and scope controls | TBD |
| Audit, logs and privacy controls | 8 | ID-19 to ID-20 | TBD |
| Operations, resilience and upgrade effort | 8 | ID-16, ID-21 and operator runbook | TBD |
| Portability and exit/migration | 6 | ID-24, export and claim-mapping review | TBD |
| Total cost at an explicit workload | 8 | Current official pricing plus infrastructure/support estimate | TBD |
| Developer/product integration effort | 7 | Recorded harness changes and maintainability review | TBD |
| **Total** | **100** | Hard gates are non-negotiable | **TBD** |

Scoring scale after evidence: 1 = unacceptable/high burden; 2 = weak; 3 = meets requirements; 4 = strong; 5 = excellent. **N/T is not zero and is not a score**; missing evidence remains unresolved. Record evidence links and assumptions beside each score.

## 8. Required outputs

- Completed run manifest and scenario-by-scenario results for each candidate.
- Hard-gate failures and retest evidence.
- Feature/plan/region comparison using current official vendor sources.
- Redacted operational observations and latency/revocation measurements.
- Dependency/license/SBOM evidence for any test harness dependencies.
- Data flow and threat-boundary diagram.
- Cost model with assumptions.
- Migration/exit notes.
- Recommendation with trade-offs, reviewer and explicit decision request.
- Updated ADRs only after the product owner accepts the result.

## 9. Decisions intentionally left open

- Identity provider and deployment mode (ADR-0008).
- Browser BFF/session design (ADR-0019).
- Authorization model/policy-engine scope (ADR-0020).
- Tenant hierarchy, membership owner and support access (ADR-0021).
- API-key/workload identity (ADR-0022).
- MFA, recovery and numeric session/revocation SLOs (ADR-0023).
- Tenant isolation/RLS rollout (ADR-0024).
- Retention, deletion, export and telemetry rules (ADR-0012/0015).

## 10. Current result

No candidate has been tested, scored, selected or rejected. This document is a reproducible plan, not test evidence. Do not start implementation, create repositories, or change WoHo AI DevKit as a consequence of this plan.

## References
- [Identity Provider Shortlist and Scorecard](IDENTITY_PROVIDER_SHORTLIST_AND_SCORECARD.md)
- [Identity and Tenant Security Evaluation](IDENTITY_AND_TENANT_SECURITY_EVALUATION.md)
- [Browser Session and Authorization Architecture](BROWSER_SESSION_AND_AUTHORIZATION_ARCHITECTURE.md)
- [Authorization Policy Gap Audit](AUTHORIZATION_POLICY_GAP_AUDIT.md)
- [Tenant Membership and ACL Consistency Decision](TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md)
- [Retention, Deletion, Export and Telemetry Policy](DATA_RETENTION_DELETION_EXPORT_TELEMETRY_POLICY.md)
