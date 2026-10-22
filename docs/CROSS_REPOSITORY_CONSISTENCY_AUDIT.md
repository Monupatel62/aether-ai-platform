# Aether AI — Cross-Repository Consistency Audit

**Audit date:** 2026-10-22  
**Scope:** Master dependency matrix, 33 repository specifications, security threat model, browser-session/authorization research, permission matrix, and current architecture decisions.  
**Status:** Documentation-level audit; findings require review. No application code was changed.

## Executive result

The documentation has a useful high-level architecture and several sound boundary rules, but it is **not yet ready to serve as an implementation-ready contract**. The structural audit confirms required sections exist; it does not prove semantic consistency. This pass identified specific mismatches and ownership ambiguities that should be resolved before the first vertical slice.

This is a manual consistency review of selected contract text and the master matrix. **No automated graph-cycle detector, full dependency parser, build, security test, or proof-of-concept was run.** Accordingly, this document does not claim that the dependency graph is cycle-free.

## Findings and required disposition

### F-01 — Workflow specification conflicts with the dependency matrix
**Severity:** High — architecture contract conflict  
**Evidence:** The dependency matrix says `aether-ai-workflows` owns schema/validation only and has no runtime dependency on orchestration. The repository specification lists `aether-ai-orchestration`, `aether-ai-agents`, and `aether-ai-database` as dependencies. That wording permits the exact reverse dependencies the matrix forbids and can create package cycles or inappropriate persistence/execution coupling.

**Required correction:** Make workflow definitions a low-level, versioned schema/validation contract. It may depend only on minimal shared schema/validation utilities (if any are later approved). Orchestration consumes workflow contracts; agent step contracts should be referenced through versioned types without making workflow validation import the agent runtime. Database persistence is owned by the relevant runtime/domain boundary, not workflow schema code. Update the spec and dependency matrix together.

### F-02 — Identity and authorization ownership overlap
**Severity:** High — security ownership ambiguity  
**Evidence:** `aether-ai-auth` claims roles and authorization primitives; `aether-ai-security` claims policy evaluation API and policy definitions; `aether-ai-enterprise` claims tenant hierarchy and organization roles; the API also explicitly owns authorization enforcement. The permission matrix requires a single, consistent decision contract.

**Required correction:** Separate responsibilities explicitly:
- **Auth:** authenticate principals, validate identity/session/token, map external identity to Aether principal, and expose session lifecycle.
- **Security:** define the shared policy decision/request/response contract and reusable enforcement primitives; do not become a parallel identity or tenant-membership database.
- **Domain/API owner:** enforce authorization at each resource/action boundary using the policy contract.
- **Enterprise:** own enterprise-specific organization hierarchy and SSO/SCIM administration only if product scope requires it; publish membership/role contracts instead of duplicating identity/session logic.
- **Product decision still required:** canonical owner of tenant/workspace membership and role grants, plus the policy engine scope. Do not silently pick one before ADR-0020/0021 review.

### F-03 — Knowledge and RAG dependency direction is inconsistent
**Severity:** High — possible cycle and ACL drift  
**Evidence:** The master dependency matrix states RAG consumes knowledge metadata/access rules and knowledge must not depend on RAG implementation. The knowledge repository spec lists RAG as a direct dependency, while the RAG spec also depends on knowledge.

**Required correction:** Remove the direct knowledge → RAG implementation dependency. Knowledge owns collection/source metadata, access policy references, source lifecycle and deletion events/contracts. RAG consumes those public contracts and emits versioned indexing-status/events only through a contract that does not require knowledge to import RAG implementation. Index/search data is a rebuildable projection, not the final authorization authority.

### F-04 — API-to-agent execution path has competing descriptions
**Severity:** High — duplicate run-state ownership risk  
**Evidence:** The dependency matrix says API delegates durable runs to orchestration, which invokes agents; the API repository spec lists agents as a direct dependency and does not list orchestration in its dependency section. This conflicts with the intended single owner of durable run state.

**Required correction:** For durable/long-running runs, API → orchestration public contract → agents. Orchestration owns run/step state, retry/recovery and cancellation coordination. API may call gateway directly for bounded synchronous model requests if that use case is explicitly defined. Remove direct API → agents dependency unless a concrete non-durable API use case is documented and it cannot create a second run lifecycle.

### F-05 — Queue dependency list appears to mix consumers with dependencies
**Severity:** Medium — dependency direction ambiguity  
**Evidence:** The queue specification lists orchestration, workflows, billing and observability as dependencies. The matrix describes queue as an adapter/envelope capability and describes billing consuming usage events while orchestration owns durable state. If the list is interpreted as package imports, queue can acquire reverse dependencies and domain coupling.

**Required correction:** Queue owns transport abstraction, envelopes, delivery/retry/dead-letter semantics and telemetry hooks. Producers/consumers depend on the queue contract; the queue implementation must not import orchestration, workflows or billing domain code. Observability should be an optional low-level instrumentation interface, not a mandatory reverse dependency. Record producer/consumer edges separately from package dependencies.

### F-06 — Database repository and domain schema ownership need a sharper contract
**Severity:** Medium — persistence coupling risk  
**Evidence:** Database spec describes ownership of schemas/migrations and names API, orchestration, memory, files and billing as dependencies, while the data-layer research says each domain owns its data/schema and the database repo owns migration conventions, connection/security guidance and restore verification.

**Required correction:** Treat database as migration/tooling/driver/contracts infrastructure. Domain owners own their tables, data semantics and migration intent; no domain service may bypass another domain's private schema. Clarify whether migrations are physically centralized or owned per domain and composed in deployment. Do not make the database package depend on domain services at runtime.

### F-07 — Search, RAG, and knowledge ACL responsibilities overlap
**Severity:** High — cross-tenant/source leakage risk  
**Evidence:** Search owns access-aware queries and filters; RAG owns authorized-source filtering; knowledge owns source ownership/access rules. All three can be read as the final authority.

**Required correction:** Choose one canonical policy source for source/collection ACLs (candidate: knowledge/domain authorization contract), one enforcement point for authorization decisions at query time, and explicit responsibilities for propagating filters into retrieval. Search filters are defense-in-depth and never replace a fresh resource authorization check. RAG must preserve source IDs, tenant, source/document version, ACL/version, and deletion state through chunks and citations. Define revocation/deletion consistency targets in ADRs.

### F-08 — Security repository's “all runtime components” dependency statement is too broad
**Severity:** Medium — dependency graph layering risk  
**Evidence:** The security specification says it depends on all runtime components, while the dependency matrix places security as a low-level shared policy capability and forbids imports of higher-level applications.

**Required correction:** Higher-level components may consume security contracts; the security library must not import all consumers. Define narrow contracts and use dependency inversion. If a remotely deployed policy service is ever considered, model its network calls separately from package imports and justify the runtime boundary.

### F-09 — Shared generic spec boilerplate obscures repository-specific controls
**Severity:** Medium — implementation readiness gap  
**Evidence:** Several specs repeat generic requirements and external reference lists, while some high-risk specs have concrete controls. Structural heading presence alone does not prove resource-specific permissions, error semantics, retention, failure handling or operational ownership are complete.

**Required correction:** Add per-repository contract tables for inputs/outputs, data ownership, direct package dependencies, network calls/events, authorization checks, sensitive fields, failure behavior, retention/deletion, and release gates. Prioritize API, auth, security, gateway, orchestration, tools, MCP, files, knowledge, RAG/search, billing, enterprise, queue and database.

### F-10 — 33-repository target is being confused with deployment topology in some wording
**Severity:** Medium — operational complexity risk  
**Evidence:** Master rules correctly say a repository does not imply a separate service, but specs sometimes list other repositories as dependencies without classifying package import, HTTP call, event, build-time artifact, or documentation link.

**Required correction:** Every edge must be typed as one of: package import, synchronous network API, asynchronous event/queue, generated/public artifact, infrastructure provisioner, or documentation-only. Track package-import and service-call graphs separately; apply cycle detection only to the package graph and separately review synchronous call loops.

## Current candidate dependency graph corrections

1. `workflows → orchestration/agents/database`: remove as runtime/package dependencies; orchestration consumes workflow schemas.
2. `knowledge → rag`: remove; publish contracts/events in one direction and avoid importing RAG implementation.
3. `api → agents`: remove for durable runs; route through orchestration. Keep only if a separately specified bounded synchronous use case is approved.
4. `queue → domain components`: replace with neutral queue contracts; record orchestration/workflows/billing as producers/consumers, not dependencies of the queue implementation.
5. `database → domain services`: remove runtime imports; domains own schema semantics, database owns shared persistence tooling/contracts.
6. `security → all runtime components`: reverse to consumers depending on narrow security contracts; security must not import its consumers.
7. Clarify the single authority for tenant/workspace membership and role grants before freezing auth, enterprise and policy contracts.

These are proposed consistency corrections, not silently accepted ADRs. Update the source specifications and matrix only after preserving decision history and confirming any product-policy choice.

## Required verification before implementation

- [ ] Reconcile the dependency matrix and affected repository specs (F-01 through F-08).
- [ ] Type every edge as package, network API, event, generated artifact, infrastructure, or docs.
- [ ] Generate separate package-import and runtime-call graphs from explicit edge data.
- [ ] Run package graph cycle detection and record tool/output/revision.
- [ ] Review synchronous network-call loops and event feedback loops manually.
- [ ] Approve one canonical tenant/workspace membership and role-grant owner.
- [ ] Approve resource-ACL authority and revocation/deletion consistency targets.
- [ ] Add resource-specific contract tables for high-risk repositories.
- [ ] Resolve related ADRs and get explicit user approval before application coding.

## Related documents

- [Dependency Matrix](DEPENDENCY_MATRIX.md)
- [Repository specification audit matrix](REPOSITORY_SPEC_AUDIT_MATRIX.md)
- [Authorization permission matrix](AUTHORIZATION_PERMISSION_MATRIX.md)
- [Browser session and authorization architecture](BROWSER_SESSION_AND_AUTHORIZATION_ARCHITECTURE.md)
- [Security threat model](SECURITY_THREAT_MODEL.md)
- [Data infrastructure evaluation](DATA_INFRASTRUCTURE_EVALUATION.md)
- [Decision log](DECISION_LOG.md)
- [Implementation roadmap](IMPLEMENTATION_ROADMAP.md)
- [Work handoff](WORK_HANDOFF.md)


## Remediation progress — 2026-10-22

The following documentation corrections have now been committed to the master repository:

- Dependency matrix: clarified low-level workflow contracts, API → orchestration → agents for durable runs, knowledge → RAG/Search contract direction, domain-neutral queue, domain-owned data semantics, narrow security contracts, and explicit edge-type vocabulary.
- Workflow spec: removed orchestration/agent/database dependencies from workflow schema validation.
- API spec: removed direct agent-runtime dependency for durable execution and documented routing/authorization boundaries.
- Knowledge spec: removed RAG/Search implementation dependencies and defined ACL/indexing contract expectations.
- Queue spec: clarified that orchestration/workflows/billing are producers or consumers, not queue package dependencies.
- Database spec: separated shared persistence tooling from domain schema ownership.
- Auth/security specs: separated principal/session lifecycle from resource authorization and prevented security from importing its consumers.
- Enterprise spec: clarified that tenant/workspace membership and role-grant ownership remains open pending ADR-0021.
- RAG/Search specs: made them ACL-aware consumers/projections rather than the authoritative permission source.
- Orchestration spec: made durable run/step state ownership explicit.

**Not yet complete:** all dependency edges have not been classified individually; no automated package-cycle detection has been run; the canonical tenant/workspace membership owner and resource ACL revocation/deletion SLOs remain open. These corrections reduce documented contradictions but do not prove a cycle-free graph or authorize implementation.


## Initial edge-typing and cycle-check checkpoint — 2026-10-22

Added [DEPENDENCY_EDGE_REGISTER.md](DEPENDENCY_EDGE_REGISTER.md), assigning proposed types to logical repository relationships and listing explicit non-edges for the known cycle risks. A DFS cycle detector was run against a manually transcribed candidate package graph: 33 nodes, 61 directed edges, and zero cycles reported.

This result is preliminary: the graph was manually transcribed, not generated from machine-readable edge data, and edge classifications remain proposals. Normalize the register, generate the graph from the normalized source, repeat the check, and separately review runtime call/event loops. Do not claim the whole architecture is certified cycle-free.
