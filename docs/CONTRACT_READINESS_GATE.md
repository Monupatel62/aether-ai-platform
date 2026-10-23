# Aether AI — Contract Readiness Gate

**Audit date:** 2026-10-23  
**Status:** Proposed engineering gate; not an accepted architecture decision.  
**Scope:** Required evidence before cross-repository contracts are treated as implementation-ready.

## Purpose

The repository specifications establish component responsibilities, but prose alone is insufficient to implement and test compatible services and packages. This gate defines the minimum artifacts and checks required before a contract is marked stable. It does not select vendors, runtime topology, or unresolved product policy.

## Current audit result

The documentation audit identified these contract areas that still require machine-readable artifacts or acceptance evidence:

| Contract area | Minimum required artifact | Acceptance evidence |
|---|---|---|
| Product API | Versioned OpenAPI document | Schema validation, auth/tenant requirements, stable errors, pagination and limits, idempotency rules, compatibility check |
| Model gateway/providers | Capability schema, normalized error catalog, streaming event contract | Provider conformance fixtures; timeout, cancellation, retry-safety and malformed-response tests |
| Agent and tool invocation | Versioned tool manifest and invocation/approval envelope | Permission-scope tests, risk/approval tests, output bounds, idempotency and denied-action tests |
| Workflows | Versioned workflow JSON schema and validation error catalog | Schema fixtures, graph-cycle detection, bounded graph/resource tests, migration/compatibility fixtures |
| Durable runs and queue | Versioned event envelope and run/step state machine | Duplicate-delivery, ordering, lease/fencing, retry/dead-letter, cancellation and recovery tests |
| Identity and authorization | Principal, resource, action, grant and policy-decision contract | Cross-tenant denial, revoked-session/grant tests, resource-level authorization tests |
| Files and knowledge | File lifecycle, ACL reference/version, deletion tombstone and indexing-status contracts | Unauthorized download, stale ACL, deletion propagation and signed-URL expiry tests |
| Billing and entitlements | Trusted usage event and entitlement decision schema | Dedupe/replay, quota race, adjustment and reconciliation tests |
| Public SDK | Generated types from accepted API/schema source | Compatibility policy, package export checks and consumer install/import smoke tests |
| Observability | Allowlisted safe-attribute schema and redaction policy | Tests proving prompt/completion bodies and secrets are excluded by default |
| Deployment | Environment, readiness, migration and rollback contract | Configuration validation, readiness checks and restore/rollback drill |

These are readiness requirements, not claims that the listed artifacts or tests already exist.

## Contract record required for every interface

Every cross-repository interface must document:

1. **Owner:** one authoritative repository and file path.
2. **Consumers:** direct consumers and permitted dependency direction.
3. **Versioning:** schema version, compatibility promise, deprecation and migration policy.
4. **Trust boundary:** authentication, tenant scope, resource authorization and approval requirements.
5. **Validation:** required/optional fields, size bounds, unknown-field handling and canonical encoding.
6. **Failures:** stable error codes, retryability, timeout, cancellation and rate-limit behavior.
7. **Delivery semantics:** idempotency, ordering, duplicate delivery, replay and recovery where applicable.
8. **Privacy:** secret handling, payload redaction, retention and safe correlation identifiers.
9. **Tests:** positive fixtures, negative fixtures, cross-tenant denial and backward-compatibility fixtures.
10. **Release control:** how consumers detect incompatible changes and how rollback is performed.

## Non-negotiable security invariants

- Browser code never receives provider credentials or privileged service credentials.
- Every domain operation authorizes the requested resource and action; authentication alone is not authorization.
- Tenant identity must come from a trusted, validated principal/context, not an untrusted request-body field.
- All tool invocation paths (first-party tools, MCP, plugins, integrations and agents) converge on the same server-side policy enforcement boundary.
- Retrieved documents and tool results are untrusted input; they cannot grant permissions or override policy.
- Search/vector results must be re-authorized against current source permissions before content is returned.
- Usage/billing events are derived from trusted server-side execution facts, not client-supplied claims.
- Prompt/completion content is excluded from telemetry by default; any exception requires documented purpose, access, redaction and retention.
- Secrets never appear in logs, fixtures, committed configuration or error messages.

## Dependency and ownership review checklist

Before approving the implementation graph, reviewers must verify:

- API delegates durable runs to orchestration; it does not execute durable agent runs directly.
- Workflow definitions/schema validation do not import orchestration, agent runtime or database implementation internals.
- Gateway consumes the provider-owned interface; provider adapters do not depend on gateway implementation.
- Tools own the invocation policy boundary; MCP/plugins/integrations cannot bypass it.
- Auth owns identity/session primitives; product/domain ownership of tenant membership and role grants must be explicitly decided.
- Knowledge owns collection/source metadata and ACL references; RAG and search remain projections and do not become ACL sources of truth.
- Database, queue, cache and observability provide infrastructure capabilities without taking over domain policy.
- Repository boundaries are not treated as automatic network-service boundaries.

## Required CI checks once implementation begins

1. Validate every JSON Schema/OpenAPI document.
2. Generate a dependency graph from actual package manifests/imports and fail on prohibited cycles.
3. Validate internal package names, versions, exports and dependency direction.
4. Run contract fixtures against producers and consumers.
5. Run negative authorization and tenant-isolation tests.
6. Check compatibility against the previous released contract version.
7. Run secret, dependency vulnerability, license and SBOM checks.
8. Keep deployment and release checks blocked until required secrets, approvals and environment protection are configured.

No CI result is claimed by this document. These checks are a proposed gate and must be wired into the repositories when implementation is authorized.

## Exit criteria for the documentation phase

- [ ] Product decisions affecting contracts are recorded in accepted ADRs.
- [ ] Every stable interface has one owner and a versioned machine-readable schema where applicable.
- [ ] The dependency matrix is reconciled against all 33 repository specifications.
- [ ] Automated graph analysis confirms no prohibited dependency cycles.
- [ ] Authorization, tenancy, data retention and telemetry defaults are decided.
- [ ] Contract fixtures and acceptance tests are specified for each interface.
- [ ] The user explicitly approves the transition from documentation to implementation.

Until these criteria are met and approved, the project remains in the documentation/design phase. Do not describe it as implemented or production-ready.
