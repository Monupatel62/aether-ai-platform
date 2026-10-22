# Aether AI — Architecture Decision Log

This is the decision register. A decision is **proposed** until its status is changed to **accepted** with rationale and date. Do not infer that a proposed stack has been selected.

| ID | Decision | Status | Reason / next action |
|---|---|---|---|
| ADR-0001 | Keep Aether AI separate from WoHoTech | Accepted | User requirement; separate product/repository identity. |
| ADR-0002 | Use WoHo AI DevKit as an external dependency, not rewrite it | Accepted in principle | Preserve existing project; verify package APIs and compatibility before implementation. |
| ADR-0003 | Plan 33 Aether repositories | Proposed | User requested a 33-repository ecosystem; review for boundaries/cycles before creating remaining 23. |
| ADR-0004 | Treat repository boundaries separately from deployable-service boundaries | Proposed | Avoid premature microservices; runtime topology is not decided. |
| ADR-0005 | AI DIAL integration strategy: adopt, adapter, or custom gateway | Open | Run a small compatibility/licensing/operational evaluation before choosing. |
| ADR-0006 | Frontend/backend technology stack | Open | DIAL Chat is a reference, not a binding stack choice. Decide based on maintainability and existing package compatibility. |
| ADR-0007 | Database, queue, cache, vector/search engine | Open | Compare data model, operations, cost, tenancy, backup, and licensing before selection. |
| ADR-0008 | Identity provider and session model | Open | Need threat model, user/tenant requirements, and deployment assumptions. |
| ADR-0009 | Provider/model list and fallback policy | Open | Compare supported features, cost, privacy, streaming, tool calls, and model terms. |
| ADR-0010 | Project name and public branding | Open | Aether AI is provisional; check GitHub/domain/trademark availability before public launch. |
| ADR-0011 | Monorepo vs multi-repo package management and CI | Open | Avoid duplicate release/version complexity; document ownership and cross-repo CI before coding. |
| ADR-0012 | Prompt/file/memory retention and telemetry policy | Open | Privacy/security requirement; define defaults and user controls before persistence features. |

## ADR format for new decisions

Each accepted ADR must include: context/problem, options considered, chosen option, reasons, consequences/tradeoffs, security/license implications, migration plan, affected repositories, date, and reviewer. If a decision changes, supersede it with a new ADR rather than silently rewriting history.
| ADR-0013 | MCP protocol/SDK compatibility | Proposed | Official MCP revision 2026-07-28 changes lifecycle and authorization; use explicit adapter/version matrix after DevKit compatibility tests. |
| ADR-0014 | AI security baseline | Proposed | Map the threat model and tests to OWASP GenAI LLM Top 10 2026; prompt text alone is not a security control. |
| ADR-0015 | GenAI observability and privacy | Proposed | Use OpenTelemetry conventions where useful, but keep raw prompt/completion capture disabled by default and define retention/redaction first. |
| ADR-0016 | CI action and release supply-chain policy | Proposed | Pin Actions to full commit SHAs unless an approved lockfile/policy gives equivalent immutability; use least-privilege workflow tokens and protected releases. |

## Architecture review update — 2026-10-22

| ID | Decision | Status | Evidence / next action |
|---|---|---|---|
| ADR-0003 | Plan 33 Aether repositories | Accepted | User explicitly chose 33. This is a repository organization target, not a requirement to deploy 33 services. Remaining 23 can be created after the documentation phase. |
| ADR-0004 | Repository boundaries are separate from service boundaries | Accepted | Dependency matrix requires a modular runtime/package map first. Create a separate network service only for a documented scaling, isolation, ownership or release reason. |
| ADR-0005 | DIAL Core vs DevKit gateway path vs hybrid | Open | [DIAL adoption evaluation](DIAL_ADOPTION_EVALUATION.md) compares the options. Run a controlled proof-of-concept and then decide. |
| ADR-0017 | WoHo DevKit package integration boundary | Proposed | [DevKit compatibility review](DEVKIT_COMPATIBILITY_REVIEW.md) records current package versions and source-level findings. Pin verified artifacts, use public exports/adapters, and keep Aether authorization/orchestration policy outside DevKit. |
