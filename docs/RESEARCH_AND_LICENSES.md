# Research and license record — aether-ai-platform

**Research date:** 2026-10-22. Initial design research only; not legal advice or a complete SBOM.

## Primary sources

- Architecture sources: https://github.com/epam/ai-dial 
- https://github.com/epam/ai-dial-core 
- https://github.com/epam/ai-dial-chat 
- DevKit: https://github.com/Monupatel62/woho-ai-devkit

## Findings

AI DIAL Core's official README describes a unified model/API proxy, Java 21, and Eclipse Vert.x; its repository includes Apache-2.0 LICENSE. Current DIAL Chat describes React + NestJS BFF and modular libraries. DevKit metadata inspected: 0.8.37, Apache-2.0, Node >=20.

## Reuse and license policy

- No third-party source code has been copied into this repository as part of this documentation work.
- The inspected WoHo AI DevKit package metadata reports version 0.8.37, Apache-2.0, and Node.js >=20. Verify exact package versions, package-level licenses, exports, and compatibility at implementation time.
- AI DIAL Core's repository includes an Apache-2.0 license. AI DIAL Chat's README notes Apache-2.0 for rewritten code and MIT for portions retained from its original upstream. Check exact files and notices before reuse.
- An open-source license for one repository does not grant rights to another repository, trademark, model, hosted API, dataset, or dependency.
- Do not vendor or fork a component until its LICENSE, NOTICE, copyright headers, transitive dependencies, security posture, and redistribution conditions have been recorded.

## Required release checks

- [ ] Pin exact versions/tags/commits for every reused component.
- [ ] Generate an SBOM and review direct/transitive licenses.
- [ ] Run vulnerability and secret scanning.
- [ ] Preserve required copyright/license notices and document modifications.
- [ ] Confirm model-provider terms, API costs, data processing, and retention requirements separately.

## Open questions

Hosting topology, model provider selection, database, queue, cache, vector store, identity provider, and deployment target remain undecided. They must be resolved in an ADR, not silently assumed.

## Additional official references reviewed on 2026-10-22

### MCP protocol

- The official MCP project announced specification revision `2026-07-28`, including a stateless core, header-based routing, authorization hardening, Tasks as an extension, and a deprecation policy: https://blog.modelcontextprotocol.io/posts/2026-07-28/.
- The official TypeScript SDK v2 is the current stable line for the 2026-07-28 revision; v1.x implements 2025-11-25 and is a separate maintenance line: https://ts.sdk.modelcontextprotocol.io/v2/ and https://ts.sdk.modelcontextprotocol.io/.
- Action: verify the exact `@woho/mcp` package version, exports, supported protocol revisions, transports, and tests before integration. Do not infer support from the package name or README feature list.

### OWASP GenAI security

- OWASP announced its 2026 Top 10 for LLM Applications and new agent-control guidance in September 2026: https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/.
- Action: maintain a threat model and negative-test matrix against the canonical 2026 release. Prompt instructions are not an authorization control.

### OpenTelemetry GenAI conventions

- The official attribute registry describes GenAI telemetry attributes, including fields that may contain sensitive data such as retrieval query text and system instructions: https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/.
- Action: use standard conventions where useful, but keep prompt/completion capture disabled by default and define access, redaction, and retention before any sensitive field is recorded.

### GitHub Actions supply-chain security

- GitHub's secure-use guidance recommends full-length commit SHA pins as immutable action references, or an approved dependency-locking approach where available: https://docs.github.com/en/actions/reference/security/secure-use.
- Action: use least-privilege workflow permissions, protect release environments, and scan dependencies/secrets before implementing CI.

### AI DIAL Core

- Official repository: https://github.com/epam/ai-dial-core. The current README describes a unified API for chat-completion and embedding models/applications, Java 21 and Eclipse Vert.x; it exposes generated OpenAPI and includes an Apache-2.0 license.
- Action: evaluate integration, operational complexity, authentication/tenant policy, provider capabilities, release cadence, and license/dependency tree before adopting it as the gateway.

These are source-based design findings, not a completed legal review, SBOM, security audit, or proof that any external code has been reused.

### OWASP 2026 primary document and agent control

- [OWASP GenAI LLM Top 10 2026 — official resource](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/). Its category names include **Hidden Context Exposure** (broader than the former “System Prompt Leakage”) and **Data and Model Poisoning**, **Unbounded Consumption**, and **Improper Output Handling** under the 2026 ranking.
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/initiatives/top-10-for-llm-and-genai/) and [Agent Control Standard](https://genai.owasp.org/resource/agent-control-standard-acs/) are relevant companion references because Aether plans tool-using agents.
- Use the 2026 canonical names in threat matrices and map each to Aether components and negative tests. Keep this as a living review rather than treating a checklist as proof of security.
