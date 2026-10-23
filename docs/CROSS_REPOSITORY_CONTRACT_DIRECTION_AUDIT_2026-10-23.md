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


## Follow-up findings — identity and execution dependency direction

### F-12 — Agents declares Orchestration as a direct dependency (high)

`aether-ai-agents/docs/DEPENDENCIES_AND_CONTRACTS.md` lists `aether-ai-orchestration` as a direct dependency, while Orchestration itself depends on Agents. This reverses the intended ownership and can create a package cycle. The master matrix and repository specifications assign durable run state to Orchestration and describe Agents as the execution contract it invokes.

**Correction:** Remove Orchestration from Agents' direct dependencies. Orchestration consumes the versioned Agent execution contract; Agents returns typed results or emits versioned lifecycle events without importing Orchestration internals.

### F-13 — Auth lists API and domain consumers as dependencies (high)

`aether-ai-auth/docs/DEPENDENCIES_AND_CONTRACTS.md` lists “API and domain consumers” under Dependencies, contradicting the master matrix and Auth repository specification. Auth is a low-level identity/session owner; higher-level APIs and domains consume its public principal/session contract.

**Correction:** Keep Auth dependencies limited to the selected identity-provider adapter, narrow principal/session primitives, and required low-level Security contracts. Explicitly prohibit Auth → API/domain implementation imports. Tenant membership/role-grant ownership remains unresolved under ADR-0021 and must not be inferred.

## Follow-up status

- Draft correction PRs created: [Agents PR #1](https://github.com/Monupatel62/aether-ai-agents/pull/1) and [Auth PR #1](https://github.com/Monupatel62/aether-ai-auth/pull/1).
- Both edited dependency documents were fetched back from their branches and the intended boundary statements were verified.
- The ADR decision log confirms tenant hierarchy/membership ownership is still an open decision; no ownership choice was made by this audit.


### F-14 — Billing usage-event register reverses edge endpoints (high)

The master dependency edge register labels the two asynchronous usage-event rows as `aether-ai-billing → aether-ai-api` and `aether-ai-billing → aether-ai-gateway`, while each row's own contract text says the events flow from API/Gateway to Billing. This makes the machine-readable direction disagree with the stated contract and can mislead graph generation or implementation planning.

**Correction:** Change the rows to `aether-ai-api → aether-ai-billing` and `aether-ai-gateway → aether-ai-billing`. Keep both relationships classified as asynchronous event/queue edges; do not add them to the package-import graph.

**Follow-up:** A documentation-only correction is proposed in [master edge-direction PR](https://github.com/Monupatel62/aether-ai-platform/pull/2). The register rows were fetched back from the working branch and checked against the stated event flow.


### F-15 — Database tenancy mission risks implying unresolved ownership (medium)

The Database repository specification and architecture mission list a “tenancy model” alongside persistence and migration responsibilities, while the decision log leaves canonical tenant/workspace membership and role-grant ownership unresolved under ADR-0021. This wording could be interpreted as assigning canonical membership ownership to Database before the required decision is accepted.

**Correction:** Clarify that Database owns low-level tenant-isolation patterns and persistence guidance only. It must not become the canonical membership/role-grant authority unless an accepted ADR explicitly assigns that responsibility. Preserve domain-owned table semantics and resource-boundary authorization.

**Status:** A documentation-only correction is proposed in [Database PR #1](https://github.com/Monupatel62/aether-ai-database/pull/1). The edited architecture document was fetched back from the branch and the narrowed mission and explicit ownership boundary were verified. The PR remains draft and unmerged.

## 2026-10-23 repository and open-PR inventory

### Canonical repository inventory

A fresh connected-repository search returned all **33/33 canonical Aether AI repositories**, each with `main` as its default branch. No additional repository is proposed by this audit.

### Open documentation PR inventory

A fresh open-PR search found **17 open PRs across 12 repositories** after adding the agentic-security mapping PR:

| Repository | Open PRs |
|---|---|
| `aether-ai-platform` | [#1 cross-repository audit](https://github.com/Monupatel62/aether-ai-platform/pull/1); [#2 billing event-edge direction](https://github.com/Monupatel62/aether-ai-platform/pull/2); [#3 agentic security mapping](https://github.com/Monupatel62/aether-ai-platform/pull/3) |
| `aether-ai-api` | [#1 durable-run routing](https://github.com/Monupatel62/aether-ai-api/pull/1); [#2 architecture dependency alignment](https://github.com/Monupatel62/aether-ai-api/pull/2) |
| `aether-ai-agents` | [#1 remove Orchestration back-dependency](https://github.com/Monupatel62/aether-ai-agents/pull/1) |
| `aether-ai-tools` | [#1 Tools/MCP dependency direction](https://github.com/Monupatel62/aether-ai-tools/pull/1) |
| `aether-ai-files` | [#1 Files/API dependency direction](https://github.com/Monupatel62/aether-ai-files/pull/1) |
| `aether-ai-auth` | [#1 Auth dependency direction](https://github.com/Monupatel62/aether-ai-auth/pull/1) |
| `aether-ai-billing` | [#1 Billing/API dependency direction](https://github.com/Monupatel62/aether-ai-billing/pull/1) |
| `aether-ai-deployment` | [#1 deployment control-plane boundary](https://github.com/Monupatel62/aether-ai-deployment/pull/1); [#2 architecture boundary](https://github.com/Monupatel62/aether-ai-deployment/pull/2) |
| `aether-ai-database` | [#1 tenant-ownership boundary](https://github.com/Monupatel62/aether-ai-database/pull/1) |
| `aether-ai-queue` | [#1 queue/authorization boundary](https://github.com/Monupatel62/aether-ai-queue/pull/1) |
| `aether-ai-cache` | [#1 cache dependency clarification](https://github.com/Monupatel62/aether-ai-cache/pull/1); [#2 architecture dependency alignment](https://github.com/Monupatel62/aether-ai-cache/pull/2) |
| `aether-ai-plugins` | [#1 plugin dependency direction](https://github.com/Monupatel62/aether-ai-plugins/pull/1) |

These are open-PR search results, not evidence of merge or approval. Treat proposed corrections as branch-only until individually reviewed and merged by an authorized maintainer. The default branches still retain any affected old wording until merge; this is especially relevant to API architecture, Files architecture, Plugins architecture, Database ownership wording, and the Billing event-edge register.

### Newly verified branch corrections

- [Files PR #1](https://github.com/Monupatel62/aether-ai-files/pull/1): fetched back `docs/ARCHITECTURE.md`; it now explicitly states Files does not depend on API and API consumes Files' public lifecycle/authorization contract.
- [Plugins PR #1](https://github.com/Monupatel62/aether-ai-plugins/pull/1): fetched back `docs/ARCHITECTURE.md`; Admin is explicitly not a direct dependency and operator workflows use the owning API/domain contract.
- [Database PR #1](https://github.com/Monupatel62/aether-ai-database/pull/1): fetched back both `docs/ARCHITECTURE.md` and `docs/DEPENDENCIES_AND_CONTRACTS.md`; Database provides tenant-isolation primitives/guidance only and does not establish canonical membership or role-grant ownership.

### Gate decision

**Implementation gate remains BLOCKED.** The P0 blockers in `IMPLEMENTATION_GATE_BLOCKERS.md` still require explicit accepted decisions or documented, reviewed deferrals. ADR-0021 remains open for canonical tenant/workspace membership and role-grant ownership. This audit did not run application builds/tests, did not merge any PR, and does not claim runtime validation.


### F-16 — Agentic-specific threat mapping was not operationalized (medium)

The security threat model mapped the OWASP GenAI LLM Top 10 2026, but only referenced the OWASP Top 10 for Agentic Applications and Agent Control Standard as further reading. Aether includes tool-using agents, orchestration, durable memory, queue messages, and potential inter-agent workflows; without an explicit agentic risk-to-component/test map, goal hijack, identity/privilege abuse, unexpected code execution, inter-agent message spoofing, cascading failures, and approval binding could be missed by the implementation test plan.

**Correction proposed:** Add a separate mapping for all ten OWASP Top 10 for Agentic Applications 2026 risks, component ownership, required tests, and agentic release-gate additions. Keep this as a design checklist only; it does not establish control implementation or test completion.

**Status:** Proposed in [platform PR #3](https://github.com/Monupatel62/aether-ai-platform/pull/3), a draft documentation-only PR. The branch version of `docs/SECURITY_THREAT_MODEL.md` was fetched back and its new mapping verified. ADR-0014 remains proposed; no implementation or security tests were run.
