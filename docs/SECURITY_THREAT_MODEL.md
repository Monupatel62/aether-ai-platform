# Aether AI — Security Threat Model (Documentation Phase)

**Status:** initial design baseline; must be reviewed before implementation.  
**Primary reference:** [OWASP GenAI Security Project — current Top 10](https://owasp.github.io/www-project-top-10-for-large-language-model-applications/). OWASP announced the 2026 edition on 2026-09-01; this document must be checked against the canonical 2026 publication before each major release.

## 1. Assets to protect

- User identity, session tokens, organization membership, tenant identifiers, and permissions.
- Provider API keys, OAuth tokens, connector credentials, signing keys, and database credentials.
- Conversations, uploaded files, knowledge sources, retrieved passages, memories, tool outputs, and agent traces.
- Agent tools capable of reading files, sending network requests, modifying repositories, or triggering external side effects.
- Usage counters, billing/entitlement records, audit trails, model configuration, workflow definitions, and deployment secrets.
- Source code, release artifacts, package publishing credentials, CI tokens, and supply-chain metadata.

## 2. Trust boundaries

1. Browser/client → Aether API.
2. API → identity/auth and domain services.
3. Gateway → external model/provider API.
4. Agent/model output → tool policy/dispatcher.
5. MCP server/plugin/connector → Aether tool registry.
6. User-uploaded/retrieved content → model context.
7. Worker/queue message → durable orchestration state.
8. Application telemetry → logs/traces/metrics provider.
9. GitHub workflow/action/dependency → build and release credentials.
10. Tenant A data → any operation executed in Tenant B's context.

## 3. Threat scenarios and required controls

| Threat | Example | Required design controls | Required tests |
|---|---|---|---|
| Direct/indirect prompt injection | User, retrieved PDF, website, tool result, or MCP description tells agent to reveal secrets or perform an action | Treat content as data; isolate instructions from retrieved content where possible; enforce authorization outside the model; tool allowlists, scoped capabilities, approval for high-impact actions | Malicious prompt/retrieval/tool-result fixtures; verify no unauthorized tool call or cross-tenant data disclosure |
| Excessive agency | Model loops or sends email/modifies repo without intended permission | Max steps/time/tokens/cost, risk-classified tools, per-action authorization, human confirmation, cancellation, rate limits | Boundary and budget exhaustion tests; approval bypass tests; cancellation tests |
| Sensitive data disclosure | Prompt, memory, trace, or model response exposes another user's data or a credential | Tenant-scoped queries, output redaction, server-side secret store, no secrets in prompts, default-off prompt logging, least privilege | Cross-tenant tests, secret canary tests, log redaction tests, deletion/retention tests |
| Insecure output handling | Model output is rendered as HTML or passed to SQL/shell/path/network | Encode output for its sink; schema-validate tool args; avoid shell concatenation; restrict outbound network; path normalization and allowlists | XSS, command/path traversal, SSRF and malformed structured-output tests where applicable |
| Vector/embedding weakness | Poisoned chunk or filter omission retrieves another tenant's document | Authorization filters enforced before results reach model; source provenance; deletion propagation; index-version tracking | Cross-tenant retrieval, poisoned-document, stale-index, deletion-propagation tests |
| Supply-chain compromise | Compromised npm package or GitHub Action reads CI secrets | Pin versions; review provenance/licenses; full-SHA pin actions or reviewed lockfile; minimal workflow permissions; secret scanning and protected release environment | CI policy checks, dependency audit, secret scanning, reproducible build checks where feasible |
| Unbounded consumption | Infinite agent loop, giant tool output, expensive repeated model calls | Request/token/output caps, budgets, concurrency/rate limits, queue backpressure, timeouts and retry caps | Cost/step budget exhaustion, oversized payload/output, retry storm and load tests |
| MCP/connector abuse | Malicious remote server changes tool schema, steals token, or returns hostile content | Server allowlist, explicit credential scopes, protocol/version validation, per-call authorization, timeouts, output limits, audit trail; treat metadata/output as untrusted | Rogue server, changed capability, auth failure, token isolation, timeout and oversized output tests |
| Queue/state manipulation | Duplicate or stale event repeats side effect or reopens terminal run | Authenticated messages, schema/version validation, idempotency, monotonic state transitions, lease/recovery policy | Duplicate/out-of-order event, crash-after-side-effect, replay and race tests |
| Telemetry leakage | Trace includes full prompts, retrieval queries, or secrets | Explicit opt-in for sensitive fields; redaction; retention; access control; low-cardinality identifiers | Canary secrets in prompts/results must not appear in default logs/traces |
| CI/release compromise | Workflow token can write repo or publish packages from untrusted PR | Least privilege, fork-safe PR workflows, protected release approvals, full-SHA actions, scoped publish credentials | Permission review, untrusted PR secret test, release-environment checks |

## 4. Mandatory authorization model

- Authentication answers who the principal is; it does not itself grant access to a resource.
- Each API/domain operation checks the principal's permission for the specific tenant, resource, and action.
- Agent tool selection is a proposal, never an authorization decision.
- The tool dispatcher rechecks permission immediately before execution, including for tools surfaced by MCP or plugins.
- High-impact actions must use an explicit risk policy and human confirmation unless a reviewed product policy documents an allowed exception.
- Provider credentials and connector tokens must be scoped to the minimum required operation and never be placed in model-visible context.

## 5. Data and telemetry defaults

- Default logs: request/run IDs, component, operation, latency, status/error code, model/provider identifiers where safe, and bounded usage metadata.
- Default logs must exclude raw prompts/completions, uploaded file content, authorization headers, access tokens, API keys, and raw connector payloads.
- Sensitive tracing fields are opt-in, access-controlled, redacted, and time-limited.
- Every persisted data category must have an owner, purpose, retention rule, deletion behavior, export policy, and tenant boundary before implementation.

## 6. Security release gates

- Threat model updated for changed trust boundaries.
- Authorization and tenant-isolation tests pass.
- Dependency/license/SBOM and vulnerability scans pass or have documented accepted exceptions.
- Secret scan passes; no credentials in Git history or artifacts.
- Agent/tool/MCP changes pass adversarial fixtures and bounded-execution tests.
- Observability redaction and retention tests pass.
- Operational rollback and incident-response instructions exist for production changes.

## 7. References

- [OWASP GenAI Top 10 project](https://owasp.github.io/www-project-top-10-for-large-language-model-applications/)
- [OWASP 2026 announcement](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/)
- [MCP 2026-07-28 specification announcement](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [MCP TypeScript SDK v2](https://ts.sdk.modelcontextprotocol.io/v2/)
- [OpenTelemetry GenAI attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)

## 8. OWASP GenAI LLM Top 10 — 2026 mapping

The official 2026 document uses the following category names. This mapping is an Aether design checklist, not a claim that any control has already passed testing.

| OWASP 2026 category | Aether components most affected | Required Aether design/test focus |
|---|---|---|
| **LLM01 Prompt Injection** | web, agents, RAG, knowledge, memory, tools, MCP, integrations | Test direct, indirect, multimodal, retrieved-content, tool-output, and persistent-memory injection. Assume model instruction boundaries can fail; bound what tools can do and what output can reach. |
| **LLM02 Sensitive Information Disclosure** | API, auth, memory, files, knowledge, RAG, gateway, observability | Tenant isolation, least privilege, secret redaction, memory/file access checks, safe outputs, default-off prompt logging, retention/deletion. |
| **LLM03 Excessive Agency** | agents, orchestration, tools, workflows, MCP, plugins, integrations | Deterministic per-action authorization, tool risk classes, step/time/token/cost budgets, approval for privileged/irreversible/external actions, cancellation and audit. |
| **LLM04 Supply Chain** | all repos, providers, MCP, plugins, integrations, CI/deployment | Pin dependencies and actions, verify provenance/versions, review licenses, scan vulnerabilities/secrets, constrain release credentials, review tool descriptions and packages. |
| **LLM05 Data and Model Poisoning** | knowledge, RAG, search, memory, evaluations, providers | Source provenance, write permissions, ingestion review, poisoned-content fixtures, memory-write controls, dataset/model versioning, regression/evaluation controls. |
| **LLM06 Unbounded Consumption** | gateway, agents, orchestration, queue, tools, API, billing | Request/context/output caps, concurrency and rate limits, bounded retries, token/cost budgets, backpressure, queue limits, oversized tool-output tests. |
| **LLM07 Misinformation** | web, agents, RAG, knowledge, evaluations | Source grounding/citations, calibrated uncertainty, evaluation of factual claims, stale-source checks, safe handling of model-generated actions based on uncertain facts. |
| **LLM08 Hidden Context Exposure** | API, agents, gateway, memory, observability, web | Do not treat system prompts or internal context as secrets that can be safely revealed by the model; keep credentials and authorization out of prompts; restrict trace/context visibility and test extraction attempts. |
| **LLM09 Vector and Embedding Weaknesses** | RAG, search, knowledge, files, evaluations | Tenant filters before retrieval, embedding/index versioning, source provenance, poisoning and nearest-neighbor abuse tests, deletion propagation, retrieval permission checks. |
| **LLM10 Improper Output Handling** | web, API, agents, tools, providers, MCP, integrations | Validate structured outputs in trusted code; encode for sink; avoid shell/SQL concatenation; constrain paths/network; test XSS, SSRF, command/path injection and schema-valid malicious payloads where relevant. |

Official source: [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/). OWASP's 2026 document also points to the [Top 10 for Agentic Applications](https://genai.owasp.org/initiatives/top-10-for-llm-and-genai/) and the [Agent Control Standard](https://genai.owasp.org/resource/agent-control-standard-acs/). Because Aether includes tool-using agents, pair the LLM Top 10 with agentic-specific guidance rather than treating the LLM list as sufficient by itself.
