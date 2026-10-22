# AI DIAL Adoption Evaluation — Aether AI

**Review date:** 2026-10-22  
**Status:** options analysis; no adoption decision has been accepted.  
**Goal:** decide which parts of EPAM AI DIAL, if any, should be used with Aether and WoHo AI DevKit.

## 1. Do not treat “AI DIAL” as one package

The official AI DIAL ecosystem includes several distinct projects and product layers. Evaluate them independently:

- **[DIAL Core](https://github.com/epam/ai-dial-core)** — a Java 21 / Eclipse Vert.x HTTP proxy that provides a unified API to chat-completion and embedding models, assistants, and applications. The repository advertises an OpenAPI specification and an Apache-2.0 license. This is a candidate model gateway/control plane.
- **[DIAL Chat](https://github.com/epam/ai-dial-chat)** — a complete chat product, not just a UI component. The current architecture documentation describes a React 19 SPA, NestJS 11 backend-for-frontend, TypeScript, Vite, Nx, npm workspaces, and a large set of feature/UI libraries. It includes auth/session/CSRF, catalog, conversations, files, toolsets, prompts, publication/sharing, model/deployment listing and MCP-related surfaces. Review exact repository and per-package license notices before reusing any source or package.
- **[AI DIAL platform documentation](https://github.com/epam/ai-dial)** — documents the broader platform, including DIAL Chat, admin, application marketplace, access control and custom GenAI applications.

These components have different operational and licensing implications. “Open source” does not automatically mean every hosted feature, model, connector, or third-party dependency is free to operate or unrestricted to reuse.

## 2. Options

### Option A — Use DIAL Core as the model gateway

**Shape:** Aether product API/security policy → DIAL Core → configured model/provider deployments; Aether's agents, workflows, files, knowledge and UI remain separate.

**Benefits:** existing unified model/embedding API, OpenAPI contract, model/deployment abstraction, and mature Java/Vert.x service. May reduce custom provider integration work.

**Costs/risks:** introduces a Java service beside the TypeScript/Node DevKit; must operate and secure another component; DIAL configuration/auth/tenant policy must align with Aether; provider features and tool calling may differ; upgrades and deployment must be tested. DIAL Core does not automatically implement Aether's agent orchestration, billing, user experience or product authorization.

**Proof required:** connect two non-production model backends; verify streaming, tool calls, embeddings, timeouts/cancellation, error normalization, auth, tenant separation, quota accounting, telemetry redaction and model capability discovery. Measure operational cost and failure modes.

### Option B — Build Aether's gateway around WoHo AI DevKit

**Shape:** Aether API → Aether gateway contract → DevKit core/provider adapters; add adapters for providers that are missing.

**Benefits:** one TypeScript/Node ecosystem with the current DevKit; easier to reuse the provider-neutral client and streaming primitives; fewer language/runtime boundaries.

**Costs/risks:** DevKit's inspected provider package is OpenAI-compatible; broader provider support needs verified adapters. Aether must implement product model catalog, tenant quotas, provider routing policy, and provider compatibility tests. DevKit is a toolkit, not a turnkey enterprise model gateway.

**Proof required:** validate current package tarballs/exports; test at least two provider implementations; test stream cancellation, usage accounting, structured/tool calls, errors, retry idempotency, and capability differences.

### Option C — Hybrid: Aether gateway contract + pluggable upstreams

**Shape:** Aether owns a stable model gateway interface. One adapter may call DIAL Core, another may call DevKit/provider packages directly. Choose the route per deployment after policy checks.

**Benefits:** avoids locking product APIs to one upstream; permits a controlled comparison and migration.

**Costs/risks:** extra adapter and conformance-test work; can become unnecessary complexity if there is only one upstream. Must avoid duplicate retry/fallback logic across Aether, DIAL Core and DevKit.

**Proof required:** define a single retry owner, one normalized error/usage/event contract, capability metadata, and privacy-aware routing rules. Demonstrate that the abstraction is needed before maintaining multiple production paths.

### Option D — Adopt DIAL Chat as the product UI/backend

**Benefits:** substantial existing chat/product functionality, including conversations, files, catalogs, toolsets, model listings, authentication integration and UI building blocks.

**Costs/risks:** DIAL Chat is a full application with its own architecture, APIs, auth/session assumptions, UI libraries and release cadence. Replacing Aether's proposed web/API with it would be a product-architecture decision, not a small library addition. Forking it creates ongoing merge/security-update work; reusing private/not-yet-published packages may not be supported.

**Proof required:** map every Aether requirement to DIAL Chat features, verify extension points and license notices, test branding/customization, confirm deployment and auth integration, and compare the cost of maintaining a fork with building only the required Aether UI.

## 3. Comparison matrix

| Criterion | DIAL Core | WoHo DevKit gateway path | Hybrid | DIAL Chat product |
|---|---|---|---|---|
| Primary role | Model/embedding proxy | TypeScript AI client/provider primitives | Stable Aether contract over more than one upstream | Full chat application/BFF/UI libraries |
| Runtime fit with DevKit | Separate Java 21/Vert.x runtime | Same TypeScript/Node ecosystem | Both runtimes possible | React/TypeScript + NestJS, with its own workspace/tooling |
| Custom provider/model routing | Strong candidate; verify required features | Requires adapters and Aether policy | Can select per use case | Usually delegates to DIAL Core; not a substitute for the model gateway by itself |
| Aether-specific agents/workflows | Must be built separately | DevKit offers agent runtime primitives; Aether still owns durable orchestration | Must be built separately | Some application/agent/tool integration, but does not automatically equal Aether's planned contracts |
| Tenant/product authorization | Must be integrated and tested | Aether must implement it | Aether must implement it consistently across upstreams | Existing auth/BFF patterns are a reference; fit with Aether tenancy must be proven |
| Operational complexity | Adds Java service | Lowest runtime diversity | Highest integration complexity | Large application and its own release/extension lifecycle |
| Current recommendation | Evaluate as candidate | Reuse where package compatibility passes | Defer until a second upstream is justified | Reference implementation first; do not adopt wholesale yet |

## 4. Recommended provisional position

1. **Do not adopt DIAL Chat wholesale at this stage.** Treat its architecture and feature coverage as reference material while Aether's requirements and brand/product scope remain open.
2. **Do not immediately commit to a custom gateway or DIAL Core.** First run a narrow, documented proof-of-concept comparing DIAL Core with the DevKit provider path.
3. Keep the Aether gateway API provider-neutral and Aether-owned, but avoid a broad abstraction that has no second implementation. The initial implementation may use one adapter behind the stable contract.
4. Reuse WoHo DevKit agent/tools/memory/core primitives where the compatibility review passes. Aether retains tenant/resource authorization, billing, policy, audit and durable orchestration.
5. Do not copy source code until exact repository/package licenses, notices, dependencies and provenance have been reviewed.

## 5. Proof-of-concept acceptance checklist

- [ ] Run one chat completion with streaming through DIAL Core.
- [ ] Run the same request through a DevKit provider adapter with a mock and one non-production provider.
- [ ] Compare normalized text/events, usage, finish reasons, tool calls, errors, timeout and cancellation.
- [ ] Verify provider credentials never reach browser code, logs, or model-visible context.
- [ ] Verify tenant/model allowlists, rate/quota policy and authorization are enforced by Aether.
- [ ] Check embeddings if RAG requires them.
- [ ] Record setup/deployment effort, latency, failure handling and maintenance ownership.
- [ ] Review exact license and transitive dependency inventory for chosen versions.
- [ ] Decide ADR-0005 only after evidence; record the decision, consequences and affected repositories.

## 6. Official sources

- [DIAL Core repository and OpenAPI description](https://github.com/epam/ai-dial-core)
- [DIAL Chat architecture](https://github.com/epam/ai-dial-chat/blob/development/docs/architecture.md)
- [AI DIAL platform architecture documentation](https://github.com/epam/ai-dial/blob/main/docs/platform/0.architecture-and-concepts/2.architecture.md)
- [WoHo AI DevKit](https://github.com/Monupatel62/woho-ai-devkit)
- [DevKit compatibility review](DEVKIT_COMPATIBILITY_REVIEW.md)
