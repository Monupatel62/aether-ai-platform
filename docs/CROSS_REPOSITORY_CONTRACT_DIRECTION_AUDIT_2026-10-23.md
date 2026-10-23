# Cross-Repository Contract Direction Audit — 2026-10-23

**Status:** Documentation-only review of proposed architecture. No application code changed and no implementation tests were run.

## Scope

Reviewed `docs/DEPENDENCIES_AND_CONTRACTS.md` in all 33 canonical Aether AI repositories against the master `docs/DEPENDENCY_MATRIX.md` and `docs/DEPENDENCY_EDGE_REGISTER.md`. Follow-up spot checks compared technical-design and architecture documents for API, Agents, Orchestration, Billing, Queue, Auth, Security, Enterprise, SDK, Cache, Database and Deployment.

## Findings requiring correction

### F-01 — Tools/MCP direction conflict (high)

`aether-ai-tools/docs/DEPENDENCIES_AND_CONTRACTS.md` lists the public `aether-ai-mcp` adapter contract as a direct dependency. The master matrix/register require the opposite direction: MCP depends on the public tool manifest/invocation contract; Tools must not import MCP. A composition root registers MCP-backed tools and avoids a package cycle.

**Correction:** Remove MCP from Tools' direct dependencies and document it as an explicit non-dependency. Keep `aether-ai-mcp → aether-ai-tools`.

### F-02 — Files/API direction ambiguity (high)

`aether-ai-files/docs/DEPENDENCIES_AND_CONTRACTS.md` lists “API, database, security, observability” under Dependencies. The master matrix/register define API as a consumer of Files' public lifecycle/download-authorization contract.

**Correction:** List database, security, observability, and selected storage/scanning adapters as Files dependencies. State that API consumes the Files contract and Files must not import API.

### F-03 — Plugins/Admin direction mismatch (medium)

`aether-ai-plugins/docs/DEPENDENCIES_AND_CONTRACTS.md` lists Admin as a dependency, while the master matrix lists Tools, Auth, and Security. Admin is a privileged UI/client and must not become a lower-level dependency of the plugin domain.

**Correction:** Remove Admin as a direct plugin dependency unless a specific versioned contract is justified and accepted. Admin should consume public domain APIs/contracts rather than be imported by Plugins.

### F-04 — Cache consumers confused with implementation dependencies (medium)

Cache dependency documents list API, Gateway, Search, and Database as dependencies. The master matrix describes Cache as depending on a selected cache adapter and shared key/TTL contracts; consumers should depend on Cache only through a stable public contract if that package is selected.

**Correction:** Separate cache backend/low-level contract dependencies from potential consumers. Keep cache reconstructible and non-authoritative for permissions, billing, and durable run state.

### F-05 — Deployment/Platform dependency ambiguity (medium)

Deployment dependency documents list “infrastructure, platform, and services being deployed.” The master matrix defines Platform as a documentation control plane with no runtime dependencies.

**Correction:** Describe Platform references as documentation/control-plane inputs only. Deployment consumes reviewed infrastructure modules and versioned release artifacts, not runtime code from Platform.

### F-06 — API durable-run path includes Agents ambiguously (high)

`aether-ai-api/docs/TECHNICAL_DESIGN.md` says “API -> orchestration/agents for run creation/status.” The master dependency matrix explicitly says durable runs flow API → Orchestration → Agents, and API must not bypass Orchestration for durable execution.

**Correction:** Route durable run create/status/cancel through Orchestration; Orchestration invokes Agents. Keep direct API → Gateway requests separately documented as bounded synchronous calls only.

### F-07 — Queue processing sequence may imply duplicated authorization ownership (medium)

`aether-ai-queue/docs/TECHNICAL_DESIGN.md` includes a generic queue-processing step to resolve trusted identity, tenant and resource scope and apply authorization. The master architecture treats Queue as a neutral transport/envelope abstraction; authorization belongs at the resource-owning consumer boundary, while Queue validates message shape and transport-level producer/replay constraints.

**Correction:** Clarify that Queue validates producer identity, envelope/schema/version, payload bounds and delivery/replay properties. The consumer owning the resource resolves current membership and enforces resource authorization before data access or side effects.

### F-08 — API architecture lists forbidden/obsolete direct dependencies (high)

`aether-ai-api/docs/ARCHITECTURE.md` lists Agents and Database among its direct dependencies. The master matrix says API must not import Agents for durable execution and may use generated/public database/domain contracts only where explicitly required, never database implementation internals. The API's dependency list also omits Orchestration, Security and Billing's public entitlement contract.

**Correction:** Align the list with the master matrix: Auth, bounded synchronous Gateway, Orchestration for durable runs, Files, Knowledge, Billing entitlement contract, Security, Observability, and narrowly scoped generated/public persistence contracts only where justified. Do not list Agents as a direct durable-run dependency.

### F-09 — Billing depends on API in the wrong direction (high)

`aether-ai-billing/docs/ARCHITECTURE.md` lists API as a Billing dependency for product-facing plan and usage queries. The master matrix says API consumes Billing's public entitlement contract and Billing must not call API back to validate usage.

**Correction:** Treat API as a consumer of Billing's public contract. Billing depends on producer usage events/contracts, database tooling, queue semantics if selected, Auth/Security and Observability; no Billing → API synchronous dependency.

### F-10 — Cache architecture repeats stale consumer dependencies (medium)

`aether-ai-cache/docs/ARCHITECTURE.md` lists API, Gateway, Search and Database as dependencies, contradicting the intended low-level cache adapter/key/TTL boundary.

**Correction:** Separate selected cache backend and low-level contracts from potential API/Gateway/Search consumers. Database is optional only if a concrete approved need is documented.

### F-11 — Deployment architecture repeats Platform dependency ambiguity (medium)

`aether-ai-deployment/docs/ARCHITECTURE.md` lists “Infrastructure, platform, and services being deployed” as dependencies, which may be read as a runtime dependency on the documentation/control-plane repository.

**Correction:** Name Infrastructure modules and versioned release artifacts as deployment inputs; treat Platform as documentation/governance reference only.

## Aligned boundaries observed

- Gateway consumes the provider interface; provider adapters do not import Gateway implementation.
- Workflows define versioned schema/validation; Orchestration consumes the contract and owns durable execution.
- Agents delegate model calls to Gateway and tool execution to Tools; Orchestration owns durable run state across process restarts.
- Billing's proposed ledger is append-oriented and duplicate events must not create a second charge.
- Auth owns principal/session lifecycle; authentication alone does not grant resource access.
- Security fails closed on missing or invalid protected-action context.
- Knowledge owns authoritative source/collection ACL references; RAG/Search consume versioned contracts and never write authoritative ACL state.
- Database and Queue define low-level tooling/transport contracts and must not import domain consumers.
- UI components remain presentation-only; Testing remains test-only; Infrastructure remains infrastructure-only.

## Limitations and gates

- This is a review of proposed Markdown documents, not actual package imports, runtime calls, or build manifests.
- Tenant/workspace membership and role-grant ownership remains unresolved; this audit does not select an owner.
- No repositories were added; the accepted 33-repository plan is unchanged.
- Implementation remains blocked until the required architecture/security decisions and implementation gate are approved.

## Next audit

Continue reviewing identity/tenant context, run lifecycle, billing/usage event direction, SDK generation, database/queue boundaries, and the remaining repository specifications. Keep changes documentation-only until the implementation gate is approved.
