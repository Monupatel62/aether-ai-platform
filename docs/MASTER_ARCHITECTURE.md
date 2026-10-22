# Aether AI — Master Architecture

**Status:** Proposed architecture; documentation phase only. No implementation or deployment is claimed.

## 1. Product intent

Aether AI is a proposed AI platform combining multi-provider model access, chat/workspaces, agents, workflows, tools/MCP, retrieval and knowledge, developer SDKs, evaluations, enterprise controls, and deployment/operations. WoHoTech remains a separate project. WoHo AI DevKit remains a separate existing dependency.

## 2. Layered architecture

1. **Experience layer:** `aether-ai-web`, `aether-ai-admin`, `aether-ai-ui-components`.
2. **Product API layer:** `aether-ai-api`, `aether-ai-auth`, `aether-ai-billing`, `aether-ai-enterprise`.
3. **AI execution layer:** `aether-ai-gateway`, `aether-ai-providers`, `aether-ai-agents`, `aether-ai-workflows`, `aether-ai-orchestration`.
4. **Capabilities layer:** `aether-ai-tools`, `aether-ai-mcp`, `aether-ai-memory`, `aether-ai-files`, `aether-ai-knowledge`, `aether-ai-rag`, `aether-ai-search`, `aether-ai-plugins`, `aether-ai-integrations`.
5. **Platform services:** `aether-ai-database`, `aether-ai-queue`, `aether-ai-cache`, `aether-ai-observability`, `aether-ai-security`.
6. **Engineering and delivery:** `aether-ai-sdk`, `aether-ai-evaluations`, `aether-ai-testing`, `aether-ai-deployment`, `aether-ai-infrastructure`, `aether-ai-docs`, plus this platform repository.

## 3. Main request path

1. Browser sends a request to the Aether API. It never receives provider API keys.
2. API authenticates the caller and authorizes the requested resource/action.
3. For a direct model call, API delegates to the gateway; the gateway chooses a configured provider adapter and normalizes errors/streaming.
4. For an agent run, API creates an authorized run and hands it to orchestration. Orchestration executes workflow/agent steps with bounded retries and cancellation.
5. Agent tool calls go through the tool registry. MCP/external connectors are untrusted and must be allowlisted, scoped, limited, and audited.
6. File/knowledge requests pass through file ownership checks and access-aware indexing/retrieval. RAG returns citations and source provenance.
7. Usage/run events are correlated for quotas/billing and observability. Sensitive prompts, credentials, and personal data are redacted by default.

## 4. Ownership rules

- Gateway owns model routing and provider-neutral model request semantics.
- Providers own vendor-specific wire formats and capability reporting.
- Agents own agent lifecycle and bounded execution; workflows own declarative workflow definitions; orchestration owns durable run state.
- Tools own the execution interface and risk metadata; MCP owns protocol transport/adapter behavior.
- Files own file lifecycle; knowledge owns collection/source metadata; RAG owns retrieval pipeline; search owns query/index abstraction.
- Auth owns identity/session primitives; each service still enforces authorization for its resources.
- Database owns migrations/contracts, not every service's business logic.
- Observability/security are shared platform capabilities, but each component must integrate them explicitly.

## 5. External integrations

### WoHo AI DevKit

Inspected README lists `@woho/core`, `@woho/provider-openai`, `@woho/agents`, `@woho/tools`, `@woho/memory`, and `@woho/mcp`. Inspected package metadata reports version 0.8.37, Apache-2.0, and Node.js >=20. Before coding, verify the exact published versions, package exports, license notices, compatibility, and current tests. Integrate through package boundaries; do not rewrite or copy the repository.

### AI DIAL

AI DIAL Core is a candidate model gateway/reference. Its current README describes a unified API/proxy for chat-completion and embedding models/applications and implementation in Java 21 on Eclipse Vert.x; its repository has Apache-2.0 LICENSE. AI DIAL Chat's current architecture describes a React frontend and NestJS BFF, with authentication/upstream calls owned by the backend. These are reference options, not mandatory dependencies. Aether must choose either to use DIAL as a component, implement a compatible gateway, or support both behind a stable adapter only after a technical spike.

### MCP

Use the official MCP specification as the protocol source of truth. Record exact supported protocol version and transport when implementing; do not rely on remembered protocol details.

## 6. Security boundaries

- All external input is untrusted, including prompts, uploaded files, model outputs, tool outputs, MCP descriptions, webhooks, and workflow documents.
- Use least privilege, tenant isolation, explicit tool scopes, payload limits, timeouts, rate limits, and approval for high-impact actions.
- Provider credentials and session secrets are server-side only and are never logged.
- Document retention, export, and deletion behavior for conversations, files, memories, and evaluation data.
- Avoid storing full prompts/results by default in logs. Add redaction and retention controls before enabling detailed traces.

## 7. Reliability contracts

- Long-running operations expose stable run IDs and states: accepted, queued, running, awaiting approval, succeeded, failed, cancelled, timed out.
- Retryable operations declare idempotency behavior. Tool side effects must not be replayed blindly.
- Queue delivery semantics and dead-letter handling are explicit.
- Cancellation is cooperative and its limits are documented; cancellation does not automatically mean all upstream work stopped.
- Errors have stable codes and safe messages; raw provider payloads are not exposed to end users.

## 8. Deployment strategy

The 33 repositories are ownership boundaries, not 33 required microservices. Start with the smallest viable runtime/package layout and extract deployable services only where scaling, isolation, independent release, or security requires it. Infrastructure and hosting choices remain open until an ADR is accepted.

## 9. Quality gates

Every component must have formatting/lint, typecheck or equivalent static checks, unit tests, contract tests, dependency/license scan, vulnerability scan, secret scan, and documented local run instructions. Agent/tool changes additionally need safety tests; data components need tenant isolation and retention/deletion tests; deployment changes need rollback validation.

## 10. References

- [Master repository catalog](REPOSITORY_CATALOG.md)
- [WoHo AI DevKit](https://github.com/Monupatel62/woho-ai-devkit)
- [AI DIAL Core](https://github.com/epam/ai-dial-core)
- [AI DIAL Chat architecture](https://github.com/epam/ai-dial-chat/blob/development/docs/architecture.md)
- [AI DIAL docs](https://github.com/epam/ai-dial)
- [MCP specification](https://modelcontextprotocol.io/)
