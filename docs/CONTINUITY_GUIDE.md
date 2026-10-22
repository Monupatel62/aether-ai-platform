# Aether AI — New-Chat Continuity Guide

Use this file as the handoff context when work continues in a new ChatGPT conversation. Read it before asking the user to repeat decisions.

## Project identity

- Proposed name: **Aether AI** (not yet verified for domain/trademark availability).

## Current repository count/status — 2026-10-23

- All 33 canonical Aether repositories exist on GitHub.
- Recursive trees for all 33 default branches were inspected and contained documentation only; no application source, manifests, test suites, or CI workflows were present in the audited trees.
- All 33 repositories now have a README and `docs/REPOSITORY_SPECIFICATION.md`; the README/spec audit found no broken local links and no unrelated-project/package markers in those files.
- Current stage is still documentation-only. Resolve implementation-blocking contracts and obtain explicit documentation-gate approval before application coding.

## First read order

1. [Master catalog](REPOSITORY_CATALOG.md)
2. [Dependency matrix](DEPENDENCY_MATRIX.md)
3. [Repository specification audit matrix](REPOSITORY_SPEC_AUDIT_MATRIX.md)
4. [Architecture audit](ARCHITECTURE_AUDIT.md)
5. [Security threat model](SECURITY_THREAT_MODEL.md)
6. [Open decisions and research](OPEN_DECISIONS_RESEARCH.md)
7. [Master architecture](MASTER_ARCHITECTURE.md)
8. [Roadmap](IMPLEMENTATION_ROADMAP.md)
9. [Decision log](DECISION_LOG.md)
10. Individual repository specification in `repositories/`
11. For an existing repository, read its README and available docs: PROJECT_SPEC, ARCHITECTURE, DEPENDENCIES_AND_CONTRACTS, IMPLEMENTATION_PLAN, RESEARCH_AND_LICENSES, TECHNICAL_DESIGN, SECURITY_REVIEW, ENGINEERING_STANDARD, and WORKLOG.

## How to continue safely

- Inspect actual GitHub state before claiming a document or repo exists.
- Update docs first; do not code until the design gate is accepted.
- Work one repository at a time; record exact files and commit URLs in WORKLOG.
- Do not assume AI DIAL or ELITEA is fully open-source as a whole. Check exact repo/file/dependency license and preserve notices.
- Do not assume 33 repositories means 33 independently deployed services.
- Do not claim build/tests passed when no code has been written.

## Required work-log entry for every future change

Date; repository; exact paths changed; purpose; why this design was chosen; dependencies/connections affected; research links; tests/evidence; security/license impact; open questions; next step.

## Audit updates — 2026-10-22

- Read [Architecture audit, pass 1](ARCHITECTURE_AUDIT.md) before further design work.
- Read [Security threat model](SECURITY_THREAT_MODEL.md) and [Open decisions/research](OPEN_DECISIONS_RESEARCH.md).
- OWASP GenAI announced the 2026 LLM Top 10 on 2026-09-01; use the canonical current edition for the threat/control matrix.
- Raw prompts/completions and sensitive GenAI trace attributes must not be captured by default.
- GitHub Actions policy should cover full-SHA pinning or an approved equivalent lockfile, least-privilege workflow permissions, and protected releases.

## Documentation audit pass 2 — 2026-10-22

- All 33 repository specifications now contain the required sections: mission, dependencies/connections, security/privacy, test plan, implementation gates, and related documentation.
- Historical snapshot: the first 10 repositories had repository-specific `docs/SECURITY_REVIEW.md` files at this audit point. The later 33-repository tree audit is documented in [Implementation Status Audit](IMPLEMENTATION_STATUS_AUDIT.md).
- Read [Dependency Matrix](DEPENDENCY_MATRIX.md) before making architecture changes. It documents one-way ownership rules and known cycle risks; it is still proposed and has not been mechanically cycle-checked.
- Do not claim the security controls are implemented. Only design requirements/checklists have been added.

## Latest architecture research — 2026-10-22

- User-selected target: 33 repositories. This does not mean 33 separately deployed services; ADR-0004 accepts modular runtime boundaries.
- DIAL Core is a candidate upstream model gateway; DIAL Chat is a full application. Neither has been selected for adoption. ADR-0005 remains open pending a small proof-of-concept.

- Read [Data Infrastructure Evaluation](DATA_INFRASTRUCTURE_EVALUATION.md) before choosing database, vector engine, queue, cache or search service. PostgreSQL/pgvector + BullMQ is only a benchmark baseline, not an accepted stack.


## Latest continuation point — identity and tenant security (2026-10-22)

Continue from `docs/IDENTITY_AND_TENANT_SECURITY_EVALUATION.md`. The next decision work is to compare one managed OIDC provider and one self-hosted OIDC option with a common scorecard, then resolve browser sessions, authorization model, tenant hierarchy, workload/API-key identity, MFA/recovery and RLS testing. Do not start application coding; no provider or policy architecture has been accepted. See `docs/OPEN_DECISIONS_RESEARCH.md` and `docs/DECISION_LOG.md` for open ADRs.


## Latest continuation point — identity provider shortlist (2026-10-22)

The next file to read is `docs/IDENTITY_PROVIDER_SHORTLIST_AND_SCORECARD.md`. Candidates are ZITADEL, Keycloak and Auth0 as different managed/self-hosted operating models. Do not treat the initial shortlist as a decision. Populate the scorecard only from tests and verified commercial/operational evidence; security acceptance gates are mandatory. No POC has run and application coding remains blocked pending explicit review.


## Latest continuation point — browser session and authorization design (2026-10-22)

Read `docs/BROWSER_SESSION_AND_AUTHORIZATION_ARCHITECTURE.md`. It uses IETF RFC 10017 (August 2026), RFC 9700 and OWASP guidance. The current candidate for first-party web is BFF + server-side sessions; the authorization baseline candidate is RBAC plus resource-level checks with deny-by-default. Both remain unapproved. Continue by checking how these choices interact with the shortlisted identity providers and writing a concrete POC test matrix. No implementation should start until the documentation gate is explicitly approved.


## Latest continuation point — authorization permission matrix (2026-10-22)

Read `docs/AUTHORIZATION_PERMISSION_MATRIX.md`. This is a draft permission specification, not accepted policy. It covers Owner/Admin/Member/Viewer, scoped Resource Manager, Service Principal, Platform Operator and controlled Support Operator access. Continue by checking consistency with the 33 repo contracts, identifying role conflicts/overbroad grants and refining the launch resource inventory. Keep implementation blocked until explicit documentation-gate approval.
