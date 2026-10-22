# Aether AI — Dependency Matrix (Proposed)

**Status:** reconciled design proposal, not a final implementation graph. Edge types are still being normalized; all edges must be reviewed against contracts and ADRs before coding. The repository count is not a deployment topology. The matrix distinguishes intended consumers but does not yet certify package imports or runtime call graphs.

## Dependency direction rules

1. The platform repository is a documentation/control plane and has no runtime dependencies.
2. UI depends on public API/client contracts; backend credentials and provider APIs never enter the browser.
3. Shared/low-level libraries must not import higher-level applications.
4. Provider adapters must not import gateway implementation. The provider contract is owned by `aether-ai-providers`; the gateway consumes that interface and adapters are registered by a composition root.
5. Workflow definitions and validation are a low-level versioned contract owned by `aether-ai-workflows`; durable execution belongs to `aether-ai-orchestration`. Workflow schema code must not import orchestration, agent runtime, or database implementation internals.
6. Agent tool calls, including MCP and plugin calls, must pass through the `aether-ai-tools` policy boundary.
7. Auth owns principal authentication and session/token lifecycle. Tenant/workspace membership and role-grant ownership remains an open product decision. Every domain/API operation still enforces resource-level authorization through a shared policy contract.
8. Database tooling, queue transport, cache, search indexes, and observability adapters are infrastructure capabilities; they must not own application business rules or import domain consumers.
9. Cross-repository contracts are versioned and reviewed. Never read another component's private tables or import its private source internals.
10. A repository does not automatically require a separate deployed service. Select runtime boundaries by a documented operational need.

## Proposed matrix

| # | Repository | Consumes / direct dependencies | Connection and boundary rule |
|---:|---|---|---|
| 1 | [`aether-ai-platform`](repositories/aether-ai-platform.md) | None at runtime | System docs/ADRs/catalog only; must not be imported by runtime components. |
| 2 | [`aether-ai-web`](repositories/aether-ai-web.md) | aether-ai-api; aether-ai-ui-components; aether-ai-sdk public types | Browser calls API only; never provider/gateway directly. |
| 3 | [`aether-ai-api`](repositories/aether-ai-api.md) | aether-ai-auth; aether-ai-gateway (bounded synchronous model requests); aether-ai-orchestration (durable runs); aether-ai-files; aether-ai-knowledge; aether-ai-billing entitlement contract; aether-ai-security policy contract; aether-ai-observability; generated database/domain contracts only where needed | Product API enforces per-resource authorization and composes public contracts. Durable runs flow API → orchestration → agents; no direct API → agents dependency for durable execution. Do not import private database implementation. |
| 4 | [`aether-ai-gateway`](repositories/aether-ai-gateway.md) | aether-ai-providers (provider interface/capability registry); aether-ai-security; aether-ai-observability | Gateway depends on provider abstraction; provider adapters must not import gateway implementation. |
| 5 | [`aether-ai-providers`](repositories/aether-ai-providers.md) | Shared provider contract owned here | Owns provider interface/adapters; avoid importing gateway/API/agents. |
| 6 | [`aether-ai-agents`](repositories/aether-ai-agents.md) | aether-ai-gateway; aether-ai-tools; aether-ai-memory; aether-ai-security; aether-ai-observability | Agent uses gateway and tool policy; orchestration owns durable run state for long-running tasks. |
| 7 | [`aether-ai-workflows`](repositories/aether-ai-workflows.md) | Minimal schema/validation utilities only, if later justified; no dependency on orchestration, agents, or database runtime | Defines versioned workflow schemas and graph validation. Orchestration consumes its public contract; workflow code does not schedule or execute steps. |
| 8 | [`aether-ai-orchestration`](repositories/aether-ai-orchestration.md) | aether-ai-workflows contracts; aether-ai-agents; aether-ai-queue; aether-ai-database; aether-ai-security; aether-ai-observability | Owns durable run state, retries and recovery; workflow definitions remain separate. |
| 9 | [`aether-ai-tools`](repositories/aether-ai-tools.md) | aether-ai-security; aether-ai-observability | All tools pass through this policy boundary; MCP adapters cannot bypass it. |
| 10 | [`aether-ai-mcp`](repositories/aether-ai-mcp.md) | aether-ai-tools contract; aether-ai-security; aether-ai-observability | MCP discovers/invokes external tools, but policy enforcement remains in tool registry. |
| 11 | [`aether-ai-memory`](repositories/aether-ai-memory.md) | aether-ai-database contracts; aether-ai-security | Memory retrieval must be scoped to user/session/tenant. |
| 12 | [`aether-ai-rag`](repositories/aether-ai-rag.md) | aether-ai-files; aether-ai-knowledge public metadata/ACL contracts; aether-ai-search; aether-ai-providers embedding contract; aether-ai-security policy contract | RAG consumes source metadata and ACL versions, then coordinates chunking/embedding/retrieval. It does not become the source of ACL truth or own file lifecycle. Indexing status is published through versioned contracts/events, not reverse imports. |
| 13 | [`aether-ai-files`](repositories/aether-ai-files.md) | aether-ai-database contracts; aether-ai-security; aether-ai-observability; object storage adapter to be selected | File lifecycle and download authorization live here. |
| 14 | [`aether-ai-knowledge`](repositories/aether-ai-knowledge.md) | aether-ai-files; aether-ai-database contracts; aether-ai-auth principal/session contract; aether-ai-security policy contract | Knowledge owns collection/source metadata, source ACL references and lifecycle. It must not import RAG or Search implementation. RAG/Search consume versioned metadata, ACL and deletion/indexing events. |
| 15 | [`aether-ai-auth`](repositories/aether-ai-auth.md) | Selected identity provider adapter (TBD); narrow aether-ai-security principal/policy contract as needed | Owns identity/session/token validation and principal mapping, not a parallel resource ACL or tenant-membership database. Domain services still authorize individual resources. |
| 16 | [`aether-ai-security`](repositories/aether-ai-security.md) | Minimal crypto/policy primitives and low-level observability interface only, if needed | Exposes versioned policy request/decision contracts and shared security primitives. Higher-level components consume it; it must not import its consumers or own identity/session state. Remote policy service versus library remains undecided. |
| 17 | [`aether-ai-admin`](repositories/aether-ai-admin.md) | aether-ai-api; aether-ai-auth; aether-ai-ui-components | UI only; privileged action authorization and audit happen server-side. |
| 18 | [`aether-ai-billing`](repositories/aether-ai-billing.md) | Database persistence contract; queue consumer/producer contract; security policy contract; trusted versioned usage events from API/gateway | Billing consumes trusted usage events and publishes entitlement contracts/events. API may read entitlement data through a public contract; billing must not synchronously call back into API to validate usage. |
| 19 | [`aether-ai-sdk`](repositories/aether-ai-sdk.md) | Generated/public schemas from aether-ai-api; stable event schemas | Public client SDK; API should not import its own client SDK. |
| 20 | [`aether-ai-evaluations`](repositories/aether-ai-evaluations.md) | aether-ai-agents; aether-ai-gateway; aether-ai-testing; aether-ai-observability | Use synthetic/sanitized datasets by default; no production prompt corpus without approval. |
| 21 | [`aether-ai-observability`](repositories/aether-ai-observability.md) | OpenTelemetry interfaces/exporters selected later; no dependency on domain business logic | Cross-cutting telemetry library/adapter; sensitive payload capture off by default. |
| 22 | [`aether-ai-deployment`](repositories/aether-ai-deployment.md) | aether-ai-infrastructure modules; versioned release artifacts from components | Deployment config only; no domain logic. |
| 23 | [`aether-ai-docs`](repositories/aether-ai-docs.md) | Published docs from all repos; no runtime dependency | Aggregates and publishes versioned docs. |
| 24 | [`aether-ai-database`](repositories/aether-ai-database.md) | Selected database driver and migration tooling (TBD); no domain-service runtime imports | Owns shared persistence tooling, migration conventions, connection/security guidance, backup/restore verification and low-level persistence contracts. Domain owners own their data semantics and migration intent; deployment composition of migrations remains open. |
| 25 | [`aether-ai-queue`](repositories/aether-ai-queue.md) | Selected queue adapter (TBD); neutral versioned envelope/event contracts; optional low-level telemetry interface | Owns transport abstraction, envelope validation, retry/dead-letter/delivery semantics. Orchestration, workflows and billing are producers/consumers, not queue package dependencies. |
| 26 | [`aether-ai-cache`](repositories/aether-ai-cache.md) | Selected cache adapter (TBD); shared key/TTL contracts | Never source of truth for auth, billing or durable run state. |
| 27 | [`aether-ai-search`](repositories/aether-ai-search.md) | Selected lexical/vector backend (TBD); neutral index/document metadata contract; aether-ai-security policy contract | Search is a rebuildable projection and query enforcement boundary. It applies tenant/ACL filters before returning results; authoritative resource authorization and source ACL ownership remain in domain contracts. |
| 28 | [`aether-ai-plugins`](repositories/aether-ai-plugins.md) | aether-ai-tools manifest/policy; aether-ai-auth; aether-ai-security | Plugins receive explicit capability grants; cannot self-authorize. |
| 29 | [`aether-ai-integrations`](repositories/aether-ai-integrations.md) | aether-ai-tools; aether-ai-auth; aether-ai-security; aether-ai-mcp only where protocol use is justified | Connector logic uses narrow credentials and passes calls through tool policy. |
| 30 | [`aether-ai-testing`](repositories/aether-ai-testing.md) | Shared test fixtures/contracts and CI policy; no production runtime dependency | Provides reusable fixtures/contract harness; test repos use synthetic data. |
| 31 | [`aether-ai-ui-components`](repositories/aether-ai-ui-components.md) | No runtime dependency on product APIs; shared UI primitives only | UI-only package; no business authorization. |
| 32 | [`aether-ai-enterprise`](repositories/aether-ai-enterprise.md) | aether-ai-auth principal/session contracts; aether-ai-security policy contracts; aether-ai-billing entitlement contracts; aether-ai-observability | Enterprise-specific SSO/SCIM and org controls may extend core policies but must not duplicate identity/session logic. Canonical tenant/workspace membership and role-grant ownership remains open for explicit product decision. |
| 33 | [`aether-ai-infrastructure`](repositories/aether-ai-infrastructure.md) | Selected infrastructure providers/modules (TBD); no application service dependency | Infrastructure-as-code and environment foundations; deployment repo consumes its modules. |

## Important architecture decisions still open

- Confirm ADR acceptance for the proposed API → orchestration → agents path; avoid two owners for run state.
- Whether knowledge/RAG communication is an in-process package contract or service API; the ownership direction is knowledge contracts/events → RAG consumers, never knowledge importing RAG implementation.
- The composition root and registration strategy for provider adapters, tools, plugins, and MCP servers.
- Which infrastructure adapters (database, queue, cache, object storage, vector/search) are selected.
- Whether any repositories are consolidated into one runtime/package during the first release.

## Edge-type vocabulary

Every future dependency edge must be explicitly classified as one of: **package import**, **synchronous network API**, **asynchronous event/queue**, **generated/public artifact**, **infrastructure provisioning**, or **documentation-only**. A consumer relationship alone does not imply a package import or synchronous call. Maintain separate package-import and runtime-call/event graphs.

## Cycle review checklist

Before coding, represent runtime package imports and service calls as separate graphs. Run cycle detection on package imports and review synchronous service-call chains for loops. In particular, verify no cycle exists among gateway/providers, workflows/orchestration, tools/MCP/plugins/integrations, and API/agents/orchestration.

## External dependency policy

Aether AI is standalone; external dependencies require an explicit architecture decision and contract tests. [AI DIAL Core](https://github.com/epam/ai-dial-core) is a candidate gateway option, not an accepted architecture choice. Current MCP protocol compatibility is tracked in [Open Decisions and Research](OPEN_DECISIONS_RESEARCH.md).

## Cycle-prevention clarifications

- **MCP/tool registry:** `aether-ai-mcp` depends on the public tool manifest/invocation contract owned by `aether-ai-tools`. The tools repository must not import the MCP adapter. A composition root registers MCP-backed tools into the registry; this avoids a package cycle.
- **Knowledge/RAG/Search:** knowledge owns source/collection metadata and ACL references; RAG consumes those contracts; search is a rebuildable projection. Knowledge must not import RAG or search implementation. Fresh resource authorization remains mandatory; index filters are defense-in-depth. Define revocation/deletion consistency targets before implementation.
- **API/agent execution:** `aether-ai-api` delegates durable runs to `aether-ai-orchestration`; orchestration invokes `aether-ai-agents`. Direct bounded synchronous model completion may use the gateway. Remove API → agents as a direct dependency unless a distinct non-durable use case is approved.
- **Billing/usage:** API/gateway publish trusted, versioned usage events; billing consumes them. API may read an entitlement contract, but billing must not synchronously call back into API to validate usage. Use queue/event contracts to avoid a service-call cycle.
- **Plugins/admin:** the admin UI consumes plugin registry APIs; the plugin registry must not depend on the admin UI.
- **Enterprise/admin:** enterprise domain contracts are consumed by admin/API. The enterprise domain must not depend on the admin frontend.
