# Aether AI — Open Architecture Decisions and Research

**Research date:** 2026-10-22. Decisions remain open until explicitly accepted in `DECISION_LOG.md`.

## ADR-0005 — AI DIAL Core vs custom gateway

**Official source:** [epam/ai-dial-core](https://github.com/epam/ai-dial-core). The repository describes a unified API for chat-completion and embedding models, assistants, and applications. The README says Java 21 and Eclipse Vert.x; the repository provides an Apache-2.0 license and a generated OpenAPI specification.

**Options:**

1. Operate AI DIAL Core as the gateway and put Aether product policy in front of it.
2. Build an Aether gateway and use selected DIAL/provider adapters through a stable boundary.
3. Implement provider adapters directly and defer DIAL.

**Evaluation criteria:** feature parity, model/provider coverage, auth/tenant integration, rate/quota enforcement, streaming/cancellation, observability, deployment complexity, security update cadence, operational burden, and total cost. Do not choose based on GitHub stars alone. The product team must also clarify whether Aether needs DIAL's application governance features or primarily model routing.

**Next evidence required:** proof-of-concept against at least two model providers using mock or non-production credentials; compare streaming, error normalization, model capability differences, and auth boundaries. Review exact version, dependency licenses, deployment docs, and security advisories.

## ADR-0013 — MCP protocol and SDK version

**New official evidence:** MCP published spec revision `2026-07-28`. It introduces a stateless protocol core, header-based routing, authorization hardening, Tasks as an extension, and other changes. The TypeScript SDK v2 implements the 2026-07-28 revision; v1.x is a separate maintenance line for the 2025-11-25 spec.

**Proposed decision:** build an adapter with an explicit protocol version and capability matrix. Select the SDK major only after checking the actual `@woho/mcp` package compatibility and testing both desired server types. Do not silently force all external servers onto one revision.

**Questions:** required transports (stdio, Streamable HTTP, or both); whether legacy servers are supported; auth/token storage; server allowlisting; extension/Tasks support; minimum security policy; upgrade/deprecation window.

Sources: [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/), [TypeScript SDK v2](https://ts.sdk.modelcontextprotocol.io/v2/), [v2 migration guide](https://ts.sdk.modelcontextprotocol.io/v2/migration/support-2026-07-28), [v1 support statement](https://ts.sdk.modelcontextprotocol.io/).

## ADR-0014 — AI security baseline

OWASP's GenAI Security Project announced its 2026 LLM Top 10 on 2026-09-01. Aether should map its threat model and test matrix to the current canonical 2026 publication before implementation and before major releases. The 2025 categories are useful background but should not be copied as if they are the current edition.

**Proposed decision:** use OWASP GenAI guidance as the risk checklist, with Aether-specific threat scenarios, controls, and tests. Security is enforced in application code and infrastructure; prompt wording alone is not a control.

Source: [OWASP 2026 announcement](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/).

## ADR-0015 — GenAI observability and privacy

OpenTelemetry publishes GenAI semantic conventions, but some attributes may contain sensitive content such as retrieval queries or system instructions.

**Proposed decision:** standardize trace/metric names where useful; default to metadata-only telemetry. Sensitive prompt/completion capture is disabled unless there is a documented purpose, access policy, redaction, and retention period.

Source: [OpenTelemetry GenAI attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/).

## ADR-0016 — CI action and release supply-chain policy

GitHub recommends full-length commit SHA pinning as the immutable reference for Actions, or a reviewed workflow dependency lockfile where supported. Aether should also use minimal token permissions and protected release environments.

**Proposed decision:** require full-SHA pins for third-party Actions unless an approved lockfile/policy provides equivalent control; use read-only permissions by default; publish only from protected, reviewed release workflows.

Source: [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use).

## Decisions still requiring product input

- Product name/domain/trademark availability.
- Frontend and backend languages/frameworks.
- Database, queue, cache, object storage, and vector/search engine.
- Identity provider and tenant model.
- Model providers, model catalog, privacy policy, and fallback rules.
- Billing provider and initial pricing/usage policy.
- Hosting and deployment model.
- Retention/export/deletion rules for chats, files, memory, traces, and evaluation data.
- Whether all 33 repositories remain separate repos or some are consolidated before implementation (without changing the user's target count unless approved).

### OWASP 2026 source review completed

The canonical [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) lists: Prompt Injection; Sensitive Information Disclosure; Excessive Agency; Supply Chain; Data and Model Poisoning; Unbounded Consumption; Misinformation; Hidden Context Exposure; Vector and Embedding Weaknesses; Improper Output Handling. This differs from some 2025 labels/order, so Aether's threat model now uses the 2026 names. Because Aether includes agents and tool execution, also review the [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/initiatives/top-10-for-llm-and-genai/) and [Agent Control Standard](https://genai.owasp.org/resource/agent-control-standard-acs/).
