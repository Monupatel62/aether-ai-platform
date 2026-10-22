# Aether AI — Architecture Audit, Pass 1

**Audit date:** 2026-10-22  
**Scope:** 33-repository design catalog, the 10 existing GitHub repositories, and official technical/security references.  
**Result:** documentation gaps and architecture decisions identified; this is not a code or production audit.

## 1. Repository state verified

The GitHub contents API was checked for all 10 existing repositories. Each is on the `main` branch and currently has a documentation-only footprint. The 9 component repositories each have eight files under `docs/`: project specification, architecture, dependencies/contracts, implementation plan, research/licenses, work log, engineering standard, and technical design. The platform repository has the master docs and repository-spec directory. This check confirms files exist; it does not independently prove every statement in every file is correct.

The catalog contains 33 planned Aether repositories. Ten exist; 23 remain planned. The separate `Monupatel62/woho-ai-devkit` project is not part of that count.

## 2. Findings that must be resolved before coding

### A-01 — MCP version assumption is now time-sensitive

The official MCP project announced specification version `2026-07-28`. It introduces a stateless protocol core, header-based routing, updated authorization, Tasks as an extension, and other changes. The TypeScript SDK v2 is the current stable release line for that revision; SDK v1.x implements the 2025-11-25 specification and is a separate maintenance line. Therefore, Aether must not silently assume that existing DevKit MCP primitives support the latest spec.

**Required action:** add an MCP compatibility ADR and a matrix covering spec revision, SDK major/version, supported transports, auth, capability discovery, task/long-running behavior, backward compatibility, and deprecation policy. Use an adapter boundary so older servers can be supported intentionally rather than accidentally.

Sources: [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/), [TypeScript SDK v2](https://ts.sdk.modelcontextprotocol.io/v2/), [v2 migration guide](https://ts.sdk.modelcontextprotocol.io/v2/migration/support-2026-07-28), [v1 support statement](https://ts.sdk.modelcontextprotocol.io/).

### A-02 — AI security register must use the 2026 OWASP release

OWASP's GenAI Security Project announced its 2026 Top 10 for LLM Applications on September 1, 2026. Existing Aether docs mention broad risks but do not yet map controls/tests to the current 2026 list and its companion agent-control guidance.

**Required action:** maintain a threat model and security test matrix covering prompt injection, sensitive-information disclosure, supply-chain risks, data/model poisoning, output handling, excessive agency, prompt leakage, vector/embedding weaknesses, misinformation, and unbounded consumption as the applicable 2026 categories evolve. Treat this as a threat checklist, not a claim that a single control eliminates prompt injection.

Sources: [OWASP 2026 announcement](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/), [OWASP current Top 10 project](https://owasp.github.io/www-project-top-10-for-large-language-model-applications/).

### A-03 — Agent tool security needs a policy-enforced reference monitor

A model should propose tool calls; trusted application code must validate schema, user/tenant authority, risk class, scopes, resource limits, and approval requirements before executing them. Prompt instructions or a tool description are not authorization. External tool output and retrieved documents must be treated as untrusted data.

**Required action:** define a single tool invocation envelope and authorization policy contract used by first-party tools, MCP tools, integrations, agents, and admin operations. Require negative tests for cross-tenant access, prompt injection, SSRF/path traversal where relevant, output exfiltration, and duplicate side effects.

Source: [OWASP excessive agency guidance](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

### A-04 — Observability must not turn prompts into a sensitive-data store

OpenTelemetry's GenAI semantic conventions include fields that may contain sensitive content, including retrieval query text and system instructions. A generic “log everything” strategy would conflict with the project's privacy goals.

**Required action:** define default-off/opt-in capture for prompt and completion bodies; redact secrets and personal data; use bounded retention; and allow correlation through run/request IDs without storing full payloads. Use standard semantic attribute names where practical, but do not enable sensitive attributes by default.

Sources: [OpenTelemetry GenAI attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/), [OpenTelemetry conventions](https://opentelemetry.io/docs/specs/otel/semantic-conventions/).

### A-05 — CI supply-chain policy should be documented before workflows are created

GitHub recommends pinning third-party Actions to full-length commit SHAs as the immutable reference and auditing the code of actions that handle repository content or secrets. Tag pinning is convenient but can move.

**Required action:** define approved action sources, full-SHA pinning policy (or a reviewed lockfile alternative), minimal workflow token permissions, protected release environments, secret handling, and dependency/license/security scans before implementing CI in all repositories.

Source: [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use).

### A-06 — 33 repositories must not force 33 services

The design correctly says repository boundaries are ownership boundaries, not automatic deployment boundaries. However, this rule must be applied in the first architecture ADR. Otherwise, independent repositories can create unnecessary network hops, version drift, and operational overhead.

**Required action:** decide a modular runtime/package map first. Only split a component into a network service for an explicit scaling, isolation, ownership, or release reason.

### A-07 — WoHo AI DevKit integration is unverified at the package/API level

The DevKit README and root package metadata provide a useful starting point, but do not prove that every feature or export is present in every published package. MCP spec changes make this especially important.

**Required action:** before choosing direct dependencies, inspect the exact npm package versions, export maps, types, changelogs, test coverage, transitive licenses, and protocol versions. Run a mock-based compatibility spike. Do not modify the DevKit main branch or release pipeline for Aether.

## 3. Ownership/contract risks to check

- API vs auth: auth provides identity primitives; API/domain components must authorize each resource/action.
- Gateway vs providers: gateway owns routing, policy, normalization, and lifecycle; providers own wire formats and capability declarations.
- Agents vs orchestration vs workflows: agents own bounded agent behavior, workflows own definitions, orchestration owns durable run state and recovery.
- Tools vs MCP vs integrations/plugins: all invocation paths must converge on the same security policy, audit envelope, timeout/output limits, and approval rules.
- Files vs knowledge vs RAG vs search: file lifecycle, collection permissions, retrieval pipeline, and query/index implementation must remain distinct contracts.
- Database vs domain services: database owns schema/migrations; services still own domain authorization and behavior.
- Billing vs observability: billing usage events must be derived from trusted server-side events, not client claims or unvalidated log data.

## 4. Audit method and limitations

- Verified repository metadata and top-level `docs/` contents for the 10 existing repositories.
- Reviewed the current 33-repository catalog and individual specification index.
- Researched official MCP, OWASP GenAI, OpenTelemetry, GitHub Actions, and AI DIAL Core sources.
- Did not run code, build, tests, license scanner, SBOM, security scanner, or deployment checks because this is a documentation-only stage and application code is not present.
- This is Pass 1. The next audit pass must validate all 33 specifications against a common checklist and produce a dependency-cycle/ownership review before coding.

## 5. Exit criteria for the documentation phase

- [ ] MCP protocol/SDK compatibility ADR accepted.
- [ ] 2026 OWASP threat model mapped to controls and tests.
- [ ] Privacy/retention and observability policy approved.
- [ ] Runtime/module boundaries selected without assuming 33 services.
- [ ] WoHo DevKit compatibility spike plan is complete and license review requirements are explicit.
- [ ] API, event, tool, workflow, and run-state contracts are reviewed together.
- [ ] Every planned repository spec passes the same checklist.
- [ ] User approves the transition to implementation.
