# WoHo AI DevKit — Aether Compatibility Review

**Review date:** 2026-10-22  
**Scope:** repository metadata, README, root/package manifests, and selected public source files on the DevKit `main` branch.  
**Status:** preliminary source review; not a build, test, runtime, npm install, or security audit. No DevKit files were changed.

## 1. Exact repository/package versions observed

Source: [WoHo AI DevKit](https://github.com/Monupatel62/woho-ai-devkit), root `package.json` and package manifests on `main` at review time.

| Package | Version observed | Declared license | Aether candidate use | Decision |
|---|---:|---|---|---|
| `@woho/core` | `0.2.24` | Apache-2.0 | Provider-neutral AI client, retries/timeouts/cancellation/streaming/validation/errors/observability | Evaluate in gateway/provider spike; do not assume full Aether policy/tenant handling. |
| `@woho/provider-openai` | `0.2.22` | Apache-2.0 | OpenAI-compatible HTTP/SSE adapter | Candidate adapter only; test model capabilities and error/usage mapping. |
| `@woho/agents` | `0.3.28` | Apache-2.0 | Bounded agent runtime, tool lifecycle, approval hooks, checkpoints/events | Strong candidate for agent execution; Aether still owns product authorization, tenant scope and durable orchestration contract. |
| `@woho/tools` | `0.4.25` | Apache-2.0 | Reusable tool primitives and policies | Candidate primitives; every tool must be wrapped by Aether's policy/approval/audit boundary. |
| `@woho/memory` | `0.6.18` | Apache-2.0 | Conversation memory interfaces and bounded storage/search | Candidate abstraction; persistent storage, tenancy, retention and deletion must be reviewed separately. |
| `@woho/mcp` | `0.6.28` | Apache-2.0 | MCP protocol primitives and stdio transport | Do not assume compatibility with MCP spec `2026-07-28`; a versioned adapter and protocol conformance tests are required. |

**Version caveat:** these are the versions declared on the repository's `main` branch when inspected. They are not a lock on what the npm registry serves today. Before implementation, verify the exact published tarball, integrity, exports, dependency tree, license files and changelog. Use explicit version pins and a lockfile.

## 2. Source-level findings

### Root project

- Private pnpm workspace `woho-ai-devkit`, version `0.8.37`, Node engine `>=20`, package manager declared as pnpm `10.17.0`, license Apache-2.0.
- Root scripts include recursive build, test, typecheck, pack check, release-graph check and consumer-install smoke check.
- The README documents a model/agent/action/memory/execution platform, human approval, bounded execution and security-aware tools.

### `@woho/agents`

Public source types include run/project/session IDs, cancellation signal, approval handler, checkpoints, before/after tool lifecycle hooks, max steps, context bounds, tool-result bounds, max calls and token budgets. It depends on `@woho/core`, `@woho/memory`, and `@woho/mcp`.

**Aether implication:** reuse the bounded runtime where it fits, but put durable run ownership, tenant/resource authorization, usage accounting, and audit policy in the Aether service contracts. Do not fork or duplicate the DevKit agent loop without a demonstrated gap.

### `@woho/mcp`

The package manifest exposes a single ESM entry and declares no external MCP SDK dependency. The inspected source defines local interfaces for tools/resources/prompts, a generic JSON-RPC-like transport, protocolVersion configuration, allowed-method/tool/resource-scheme controls, byte limits, timeout handling, and a stdio subprocess transport. This is useful as a small primitive layer.

**What is not established by this review:** complete conformance to the official MCP revision `2026-07-28`, support for all official transports/authorization behaviors, Tasks extension support, or the current TypeScript SDK v2 behavior. The presence of a `protocolVersion` option does not prove protocol conformance.

**Required next test:** build a separate compatibility harness against the official MCP specification/SDK. Record pass/fail for initialization/version negotiation, capability discovery, tool/resource/prompt calls, transport framing, cancellation, timeouts, errors, authorization, unsupported methods, version mismatch and oversized payloads. Keep the harness in Aether; do not change DevKit to make this report pass.

### `@woho/tools`

Depends on `@woho/agents`, so it is not a low-level package. Aether should avoid creating an import cycle by defining its product tool manifest/policy boundary separately and wrapping DevKit tools behind an adapter.

### `@woho/core` and provider package

The README shows a provider-neutral client and an OpenAI-compatible HTTP/SSE provider. The selected provider package should be evaluated for cancellation, usage accounting, error normalization, structured/tool-call mapping, streaming termination and capability declaration before Aether relies on it as a general provider abstraction.

## 3. Proposed Aether dependency strategy

- Pin the exact DevKit package versions selected for the first vertical slice; use a lockfile and store the package integrity/SBOM.
- Depend on public package exports only; never import DevKit source paths or internal files.
- Keep Aether domain contracts independent of DevKit-specific types. Add thin adapters at Aether's composition root.
- Aether owns user/tenant authorization, product quotas/billing, data retention, approval policy, external connector credentials, and audit record access.
- Aether orchestration owns durable multi-process run state and queue recovery. A DevKit in-process runtime/checkpoint interface may be used beneath it, but do not claim durability until tested across process restart.
- All model tool calls must pass through Aether's policy dispatcher, including tools from DevKit, MCP, and plugins.
- Do not change DevKit code or release versions as part of this work.

## 4. License and supply-chain notes

The repository root and inspected package manifests declare Apache-2.0 and the package metadata includes license files in published files. This is not a full transitive-license review. Before shipping, inspect every resolved dependency, preserve notices, generate an SBOM, check published tarballs, and record license exceptions. A repository-level license alone does not automatically cover all transitive dependencies or third-party model/API terms.

## 5. Acceptance criteria before Aether integration

- [ ] Exact npm package versions and integrity verified against registry artifacts.
- [ ] Package exports/types and consumer import smoke tests pass.
- [ ] MCP protocol compatibility harness passes the selected spec/transport matrix or documents intentional unsupported features.
- [ ] Agent lifecycle tests pass for cancellation, approval, checkpoint/recovery, limits, duplicate tool-call protection and terminal states.
- [ ] Aether tenant authorization and audit policy cannot be bypassed through DevKit tool interfaces.
- [ ] Dependency/license/SBOM review is complete.
- [ ] No changes to DevKit main/release pipeline are needed to make Aether function.

## Sources

- [DevKit README](https://github.com/Monupatel62/woho-ai-devkit/blob/main/README.md)
- [Root package manifest](https://github.com/Monupatel62/woho-ai-devkit/blob/main/package.json)
- [Core package manifest](https://github.com/Monupatel62/woho-ai-devkit/blob/main/packages/core/package.json)
- [Agents package manifest](https://github.com/Monupatel62/woho-ai-devkit/blob/main/packages/agents/package.json)
- [Tools package manifest](https://github.com/Monupatel62/woho-ai-devkit/blob/main/packages/tools/package.json)
- [Memory package manifest](https://github.com/Monupatel62/woho-ai-devkit/blob/main/packages/memory/package.json)
- [MCP package manifest](https://github.com/Monupatel62/woho-ai-devkit/blob/main/packages/mcp/package.json)
- [MCP source](https://github.com/Monupatel62/woho-ai-devkit/blob/main/packages/mcp/src/index.ts)
- [MCP stdio transport source](https://github.com/Monupatel62/woho-ai-devkit/blob/main/packages/mcp/src/stdio.ts)
- [Official MCP specification release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [Official MCP TypeScript SDK v2](https://ts.sdk.modelcontextprotocol.io/v2/)
