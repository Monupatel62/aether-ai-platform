# Aether AI — New-Chat Continuity Guide

Use this file as the handoff context when work continues in a new ChatGPT conversation. Read it before asking the user to repeat decisions.

## Project identity

- Proposed name: **Aether AI** (not yet verified for domain/trademark availability).
- This project is separate from **WoHoTech**.
- Existing external project: [Monupatel62/woho-ai-devkit](https://github.com/Monupatel62/woho-ai-devkit). Do not rewrite or modify its application code as part of Aether work unless the user explicitly authorizes a separate change.

## Repository count/status at documentation start

- 33 Aether repositories are in the plan.
- The first 10 repositories exist: `aether-ai-platform`, `aether-ai-web`, `aether-ai-api`, `aether-ai-gateway`, `aether-ai-providers`, `aether-ai-agents`, `aether-ai-workflows`, `aether-ai-orchestration`, `aether-ai-tools`, `aether-ai-mcp`.
- 23 additional repositories are planned but not yet created.
- WoHo AI DevKit is a separate dependency and is not counted in the 33.
- Current stage is documentation-only. Do not start application coding until documentation is complete and the user approves the next phase.

## First read order

1. [Master catalog](REPOSITORY_CATALOG.md)
2. [Dependency matrix](DEPENDENCY_MATRIX.md)
3. [Architecture audit](ARCHITECTURE_AUDIT.md)
4. [Security threat model](SECURITY_THREAT_MODEL.md)
5. [Open decisions and research](OPEN_DECISIONS_RESEARCH.md)
2. [Master architecture](MASTER_ARCHITECTURE.md)
3. [Roadmap](IMPLEMENTATION_ROADMAP.md)
4. [Decision log](DECISION_LOG.md)
5. Individual repository specification in `docs/repositories/`
6. Local repo README, PROJECT_SPEC, ARCHITECTURE, DEPENDENCIES_AND_CONTRACTS, IMPLEMENTATION_PLAN, RESEARCH_AND_LICENSES, WORKLOG

## How to continue safely

- Inspect actual GitHub state before claiming a document or repo exists.
- Update docs first; do not code until the design gate is accepted.
- Work one repository at a time; record exact files and commit URLs in WORKLOG.
- Do not assume AI DIAL or ELITEA is fully open-source as a whole. Check exact repo/file/dependency license and preserve notices.
- Do not assume 33 repositories means 33 independently deployed services.
- Do not change WoHoTech, production systems, or the DevKit's implementation while preparing Aether documentation.
- Do not claim build/tests passed when no code has been written.

## Required work-log entry for every future change

Date; repository; exact paths changed; purpose; why this design was chosen; dependencies/connections affected; research links; tests/evidence; security/license impact; open questions; next step.

## Audit updates — 2026-10-22

- Read [Architecture audit, pass 1](ARCHITECTURE_AUDIT.md) before further design work.
- Read [Security threat model](SECURITY_THREAT_MODEL.md) and [Open decisions/research](OPEN_DECISIONS_RESEARCH.md).
- MCP spec revision 2026-07-28 is now published; do not assume current WoHo DevKit MCP primitives support it until the package-level compatibility spike is complete.
- OWASP GenAI announced the 2026 LLM Top 10 on 2026-09-01; use the canonical current edition for the threat/control matrix.
- Raw prompts/completions and sensitive GenAI trace attributes must not be captured by default.
- GitHub Actions policy should cover full-SHA pinning or an approved equivalent lockfile, least-privilege workflow permissions, and protected releases.
