# Tenant Membership Ownership — Decision Brief

**Date:** 2026-10-23  
**Status:** Decision requested; no option accepted.  
**Scope:** Aether AI's existing 33-repository plan. This brief does not authorize creating another repository or starting application implementation.

## Decision to make

Choose the canonical owner for tenant/workspace membership, invitations, role grants and membership lifecycle. Authentication identity, resource ACLs, policy evaluation and billing entitlements remain separate concerns.

## Options

### A — `aether-ai-enterprise` owns tenancy for every customer tier

**Meaning:** Enterprise owns tenant/workspace hierarchy, membership, invitations and role grants for free, individual, team and enterprise customers. SSO/SCIM integrations are optional capabilities; membership must work without them.

**Advantages**
- Preserves the accepted 33-repository scope.
- Gives tenant lifecycle and organization administration one clear owner.
- Avoids splitting core membership state across auth and product domains.

**Risks / controls**
- Enterprise must not become a catch-all for unrelated features.
- Core tenancy must not depend on enterprise SSO, SCIM or billing.
- Publish a narrow, versioned membership contract; other repositories must not read private tables.

### B — Add a dedicated `aether-ai-tenancy` repository

**Meaning:** A new domain owns tenant/workspace hierarchy and membership lifecycle.

**Advantages:** clearest standalone ownership and potentially simpler naming for core tenancy.

**Costs:** changes the accepted 33-repository plan, requires explicit approval, catalog and dependency graph updates, new specs/contracts, and a migration/ownership plan. Do not create it without that approval.

### C — `aether-ai-auth` owns tenancy

**Meaning:** Identity/session integration and tenant membership are in one domain.

**Advantages:** fewer initial components.

**Risks:** couples membership lifecycle to login/provider concerns and may complicate provisioning, service identities and resource-domain evolution. Keep as a fallback only if the product model confirms that coupling is intended.

## Recommendation for review

Prefer **Option A** if `aether-ai-enterprise` is defined as the universal tenant-management domain. It fits the existing 33-repository scope while keeping authentication and resource authorization separate. This is a recommendation, not an accepted ADR.

Do not infer acceptance from this document. The product owner must confirm the customer/tenant model before the dependency graph or security schemas are frozen.

## Required boundary contracts, whichever option is selected

- `aether-ai-auth`: external identity, principal mapping, login/session lifecycle and token validation.
- Membership owner: tenant/workspace lifecycle, membership state, invitations and role grants.
- `aether-ai-security`: shared policy-decision contract and deny-by-default semantics.
- Resource-owning domains: resource ACL and lifecycle enforcement at each protected operation.
- `aether-ai-billing`: commercial plan/usage entitlements; entitlement is not permission to access a resource.
- `aether-ai-api` and resource-owning domains: enforce current membership and resource authorization; never trust a client-supplied tenant ID as authority.
- Search/RAG, queues, caches and workers: treat events as projections/notifications, not the source of authorization truth; re-authorize protected content and delayed work.

## Acceptance questions

1. Does Aether support personal users without an organization, or must every user belong to a tenant?
2. Can a user belong to multiple tenants and switch between them?
3. Are workspaces nested under tenants, and can roles be scoped to a workspace or individual resource?
4. Who may create the first tenant and recover ownership if its owner is unavailable?
5. What is the required revocation behavior for active sessions, queued jobs, search/RAG results and signed file links?
6. Is `aether-ai-enterprise` explicitly intended to serve every customer tier, including customers with no enterprise features?

## Gate after the decision

1. Record the selected option and rationale in an accepted ADR.
2. Update the master dependency matrix, typed dependency-edge register, machine-readable graph and affected repository specifications.
3. Define versioned membership APIs/events, idempotency, ordering, replay and reconciliation rules.
4. Add cross-tenant and revocation contract fixtures.
5. Run the identity/authorization POC matrix and attach observed evidence.
6. Keep production implementation blocked until the documentation gate is explicitly approved.

## Related documents

- [Tenant membership and ACL consistency decision](TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md)
- [Authorization permission matrix](AUTHORIZATION_PERMISSION_MATRIX.md)
- [Identity/authorization POC test matrix](IDENTITY_AUTHORIZATION_POC_TEST_MATRIX.md)
- [Implementation gate blockers](IMPLEMENTATION_GATE_BLOCKERS.md)
- [Dependency matrix](DEPENDENCY_MATRIX.md)
- [Architecture decision log](DECISION_LOG.md)
