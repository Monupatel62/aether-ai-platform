# Aether AI — Dependency Matrix (Proposed)

**Status:** design proposal, not a final implementation graph. All edges must be reviewed against the contracts and ADRs before coding. “Consumes” means uses a public package/API/event contract; it does not necessarily mean a network call or separate deployed service.

## Dependency direction rules

1. The platform repository is a documentation/control plane and has no runtime dependencies.
2. UI depends on public API/client contracts; backend credentials and provider APIs never enter the browser.
3. Shared/low-level libraries must not import higher-level applications.
4. Provider adapters must not import gateway implementation. The provider contract is owned by `aether-ai-providers`; the gateway consumes that interface and adapters are registered by a composition root.
5. Workflow definitions are validated in `aether-ai-workflows`; durable execution belongs to `aether-ai-orchestration`. Workflow schema code must not import orchestration internals.
6. Agent tool calls, including MCP and plugin calls, must pass through the `aether-ai-tools` policy boundary.
7. Auth provides identity/session primitives. Every domain/API operation still enforces resource-level authorization.
8. Database, queue, cache, search, and observability are infrastructure capabilities; they must not own application business rules.
9. Cross-repository contracts are versioned and reviewed. Never read another component's private tables or import its private source internals.
10. A repository does not automatically require a separate deployed service. Select runtime boundaries by a documented operational need.

## Proposed matrix

| # | Repository | Consumes / direct dependencies | Connection and boundary rule |
|---:|---|---|---|
| 1 | [`aether-ai-platform`](repositories/aether-ai-platform.md) | None at runtime | System docs/ADRs/catalog only; must not be imported by runtime components. |
| 2 | [`aether-ai-web`](repositories/aether-ai-web.md) | aether-ai-api; aether-ai-ui-components; aether-ai-sdk public types | Browser calls API only; never provider/gateway directly. |
| 3 | [`aether-ai-api`](repositories/aether-ai-api.md) | aether-ai-auth; aether-ai-gateway; aether-ai-agents or aether-ai-orchestration; aether-ai-files; aether-ai-knowledge; aether-ai-billing; aether-ai-database contracts; aether-ai-observability | Product API composes services; use public contracts, not private tables. Decide whether API talks to orchestration or agents directly in an ADR. |
| 4 | [`aether-ai-gateway`](repositories/aether-ai-gateway.md) | aether-ai-providers (provider interface/capability registry); aether-ai-security; aether-ai-observability | Gateway depends on provider abstraction; provider adapters must not import gateway implementation. |
| 5 | [`aether-ai-providers`](repositories/aether-ai-providers.md) | Shared provider contract owned here; compatible WoHo DevKit provider packages optionally | Owns provider interface/adapters; avoid importing gateway/API/agents. |
| 6 | [`aether-ai-agents`](repositories/aether-ai-agents.md) | aether-ai-gateway; aether-ai-tools; aether-ai-memory; aether-ai-security; aether-ai-observability; compatible WoHo DevKit core/agents where selected | Agent uses gateway and tool policy; orchestration owns durable run state for long-running tasks. |
| 7 | [`aether-ai-workflows`](repositories/aether-ai-workflows.md) | Schema/contracts only; no runtime dependency on orchestration | Defines workflow schemas/validation; orchestration consumes versioned workflow definitions. |
| 8 | [`aether-ai-orchestration`](repositories/aether-ai-orchestration.md) | aether-ai-workflows contracts; aether-ai-agents; aether-ai-queue; aether-ai-database; aether-ai-security; aether-ai-observability | Owns durable run state, retries and recovery; workflow definitions remain separate. |
| 9 | [`aether-ai-tools`](repositories/aether-ai-tools.md) | aether-ai-security; aether-ai-observability; aether-ai-mcp adapter interface where needed; compatible WoHo DevKit tools optionally | All tools pass through this policy boundary; MCP adapters cannot bypass it. |
| 10 | [`aether-ai-mcp`](repositories/aether-ai-mcp.md) | aether-ai-tools contract; aether-ai-security; aether-ai-observability; compatible WoHo DevKit MCP only after compatibility test | MCP discovers/invokes external tools, but policy enforcement remains in tool registry. |
| 11 | [`aether-ai-memory`](repositories/aether-ai-memory.md) | aether-ai-database contracts; aether-ai-security; compatible WoHo DevKit memory optionally | Memory retrieval must be scoped to user/session/tenant. |
| 12 | [`aether-ai-rag`](repositories/aether-ai-rag.md) | aether-ai-files; aether-ai-knowledge; aether-ai-search; aether-ai-providers embedding contract; aether-ai-security | Retrieval pipeline composes indexing and search; do not own file lifecycle. |
| 13 | [`aether-ai-files`](repositories/aether-ai-files.md) | aether-ai-database contracts; aether-ai-security; aether-ai-observability; object storage adapter to be selected | File lifecycle and download authorization live here. |
| 14 | [`aether-ai-knowledge`](repositories/aether-ai-knowledge.md) | aether-ai-files; aether-ai-rag indexing contract; aether-ai-search; aether-ai-database; aether-ai-auth | Knowledge owns collection/source metadata and permissions. |
| 15 | [`aether-ai-auth`](repositories/aether-ai-auth.md) | Selected identity provider adapter (TBD); aether-ai-security policy primitives | Identity primitives; domain services still authorize individual resources. |
| 16 | [`aether-ai-security`](repositories/aether-ai-security.md) | No higher-level runtime dependency; shared policy contracts only | Lowest-level security library/policy service; avoid importing API, agents, or UI. |
| 17 | [`aether-ai-admin`](repositories/aether-ai-admin.md) | aether-ai-api; aether-ai-auth; aether-ai-ui-components | UI only; privileged action authorization and audit happen server-side. |
| 18 | [`aether-ai-billing`](repositories/aether-ai-billing.md) | aether-ai-database; aether-ai-queue; trusted usage events from API/gateway; aether-ai-security | Never trust browser-supplied usage totals. |
| 19 | [`aether-ai-sdk`](repositories/aether-ai-sdk.md) | Generated/public schemas from aether-ai-api; stable event schemas | Public client SDK; API should not import its own client SDK. |
| 20 | [`aether-ai-evaluations`](repositories/aether-ai-evaluations.md) | aether-ai-agents; aether-ai-gateway; aether-ai-testing; aether-ai-observability | Use synthetic/sanitized datasets by default; no production prompt corpus without approval. |
| 21 | [`aether-ai-observability`](repositories/aether-ai-observability.md) | OpenTelemetry interfaces/exporters selected later; no dependency on domain business logic | Cross-cutting telemetry library/adapter; sensitive payload capture off by default. |
| 22 | [`aether-ai-deployment`](repositories/aether-ai-deployment.md) | aether-ai-infrastructure modules; versioned release artifacts from components | Deployment config only; no domain logic. |
| 23 | [`aether-ai-docs`](repositories/aether-ai-docs.md) | Published docs from all repos; no runtime dependency | Aggregates and publishes versioned docs. |
| 24 | [`aether-ai-database`](repositories/aether-ai-database.md) | Selected database driver/migration tooling (TBD); no import of domain services | Owns schema/migrations and persistence contracts; domain logic remains with services. |
| 25 | [`aether-ai-queue`](repositories/aether-ai-queue.md) | Selected queue adapter (TBD); versioned event contracts | Delivery semantics and envelope schema; no hidden business workflows. |
| 26 | [`aether-ai-cache`](repositories/aether-ai-cache.md) | Selected cache adapter (TBD); shared key/TTL contracts | Never source of truth for auth, billing or durable run state. |
| 27 | [`aether-ai-search`](repositories/aether-ai-search.md) | Selected lexical/vector backend (TBD); aether-ai-database metadata contract; aether-ai-security access filters | Access filters must be enforced before snippets are returned. |
| 28 | [`aether-ai-plugins`](repositories/aether-ai-plugins.md) | aether-ai-tools manifest/policy; aether-ai-auth; aether-ai-security; aether-ai-admin API contracts | Plugins receive explicit capability grants; cannot self-authorize. |
| 29 | [`aether-ai-integrations`](repositories/aether-ai-integrations.md) | aether-ai-tools; aether-ai-auth; aether-ai-security; aether-ai-mcp only where protocol use is justified | Connector logic uses narrow credentials and passes calls through tool policy. |
| 30 | [`aether-ai-testing`](repositories/aether-ai-testing.md) | Shared test fixtures/contracts and CI policy; no production runtime dependency | Provides reusable fixtures/contract harness; test repos use synthetic data. |
| 31 | [`aether-ai-ui-components`](repositories/aether-ai-ui-components.md) | No runtime dependency on product APIs; shared UI primitives only | UI-only package; no business authorization. |
| 32 | [`aether-ai-enterprise`](repositories/aether-ai-enterprise.md) | aether-ai-auth; aether-ai-security; aether-ai-admin; aether-ai-billing; aether-ai-observability | Enterprise controls extend core auth/tenant policies rather than creating a parallel identity system. |
| 33 | [`aether-ai-infrastructure`](repositories/aether-ai-infrastructure.md) | Selected infrastructure providers/modules (TBD); no application service dependency | Infrastructure-as-code and environment foundations; deployment repo consumes its modules. |

## Important architecture decisions still open

- Whether `aether-ai-api` delegates long-running work to orchestration directly or uses an agents API; avoid two owners for run state.
- Whether `aether-ai-knowledge` calls RAG as a library/package or through a service API.
- The composition root and registration strategy for provider adapters, tools, plugins, and MCP servers.
- Which infrastructure adapters (database, queue, cache, object storage, vector/search) are selected.
- Whether any repositories are consolidated into one runtime/package during the first release.

## Cycle review checklist

Before coding, represent runtime package imports and service calls as separate graphs. Run cycle detection on package imports and review synchronous service-call chains for loops. In particular, verify no cycle exists among gateway/providers, workflows/orchestration, tools/MCP/plugins/integrations, and API/agents/orchestration.

## External dependency policy

[WoHo AI DevKit](https://github.com/Monupatel62/woho-ai-devkit) remains separate. Any package integration requires exact version/export/license verification and contract tests. [AI DIAL Core](https://github.com/epam/ai-dial-core) is a candidate gateway option, not an accepted architecture choice. Current MCP protocol compatibility is tracked in [Open Decisions and Research](OPEN_DECISIONS_RESEARCH.md).
