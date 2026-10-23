# Review of External Architecture Research — Gemini Report

**Review date:** 2026-10-23  
**Status:** Research reconciliation only; no architecture decision accepted.  
**Scope:** Existing 33-repository Aether AI plan. This document does not authorize a new repository, application implementation, deployment, or merge.

## Source reviewed

User-provided report: **“AETHER AI — ARCHITECTURE RESEARCH REPORT”**, dated October 23, 2026. It is treated as an external research proposal, not as verified implementation evidence. Its own text identifies ADR-0021 as unresolved and calls its recommendations proposals.

## Executive assessment

The report is useful as a shortlist of architectural options and acceptance scenarios. It does not provide enough product-owner evidence to accept its recommended hybrid membership model. In particular, it proposes a workspace/tenant microservice associated with `aether-ai-database` / the auth domain, while the existing Aether decision brief compares `aether-ai-enterprise`, a new `aether-ai-tenancy` repository, and `aether-ai-auth` as the ownership options. These are not equivalent choices and must not be silently combined.

## Reconciliation by domain

| Domain | Gemini report proposal | Existing Aether baseline | Review disposition |
|---|---|---|---|
| Tenant/membership ownership (ADR-0021) | Hybrid identity JWT plus asynchronous membership propagation; suggests database/auth domain as membership authority | Owner remains unresolved; existing decision brief compares Enterprise, new Tenancy repository, and Auth | Keep unresolved. Ask product owner to select the canonical owner. Do not designate Database as membership owner by implication. |
| Identity and authorization | Identity service issues signed JWTs; services validate claims | Authentication, active membership, resource ACL, action policy and commercial entitlement are separate checks | Preserve separation. A valid JWT or cached event projection alone must not authorize protected resource access. |
| API gateway | Custom application gateway for streaming, rate limiting and provider fallback | ADR-0005 remains open; DIAL/native gateway vs adapter needs compatibility, license and operational evaluation | Treat as a candidate. Do not lock the stack or gateway design before the POC. |
| Contract validation | OpenAPI 3.1 / JSON Schema validated in CI | Contract schemas and 24 draft fixtures exist; actual schema and OpenAPI validation are not yet evidenced | Add validator execution to the gate; do not describe contracts as validated until logs and versions are recorded. |
| Tool/MCP isolation | Restricted network namespaces and ephemeral containers | Tool execution boundary and threat controls remain design/gate items | Convert into testable requirements. Select a concrete isolation runtime only after threat, platform and operational evaluation. |
| Privacy/retention | Raises data residency and retention as open questions | ADR-0012 and privacy/telemetry policy remain open | Keep unresolved; define data classes, regional requirements, retention and deletion semantics before persistence implementation. |

## Security qualification: asynchronous membership propagation

The report identifies eventual-consistency lag and suggests short-lived JWTs/revocation blacklists as mitigations. These alone do not establish safe revocation. Before accepting an asynchronous design, specify and test:
- authoritative membership and grant source;
- maximum revocation propagation delay and fail-closed behavior during stale or unavailable checks;
- versioning, ordering, duplicate delivery, replay, reconciliation and missed-event recovery;
- fresh authorization at protected read/action boundaries, including workers and delayed jobs;
- cache, search/RAG, file-link and session behavior after membership or ACL revocation.

An event bus or edge cache may accelerate lookup, but must not become an unexamined replacement for authoritative authorization state.

## Testable follow-ups

1. **ADR-0021:** Update the existing decision brief with the Gemini option and its trade-offs, then obtain explicit owner selection. No option is accepted by this review.
2. **Gateway POC:** Define measurable SSE/streaming, timeout, cancellation, rate-limit, provider-fallback, and secret-handling cases before selecting native/custom/external architecture.
3. **Contract validation:** Execute the documented JSON Schema Draft 2020-12 fixture runner with format checking and separately validate the OpenAPI 3.1 document. Preserve command output, tool versions and failures.
4. **Tenant/revocation tests:** Cover cross-tenant direct reads, stale membership projection, revoked queued work, search/RAG snippets, file links and resource ACL changes.
5. **Tool isolation:** Test denied egress, filesystem boundary, credential exposure, resource limits, cancellation, cleanup and audit trails for the chosen execution environment.
6. **Privacy:** Record data classes, region constraints, retention/deletion rules and telemetry redaction before selecting persistence defaults.

## Decision and implementation status

- ADR-0021: **Open; owner decision required.**
- Gateway/provider strategy: **Open; POC required.**
- Contract schemas/OpenAPI: **Not yet proven validated by this report or this review.**
- Tool isolation implementation: **Not selected or implemented.**
- Repository count: **Remain exactly 33.**
- Application implementation and production changes: **Not authorized by this document.**

## Related Aether documents

- `docs/TENANT_MEMBERSHIP_OWNER_DECISION_BRIEF.md`
- `docs/TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md`
- `docs/IDENTITY_AND_TENANT_SECURITY_EVALUATION.md`
- `docs/contracts/CONTRACT_VALIDATION_RUNBOOK.md`
- `docs/IMPLEMENTATION_GATE_BLOCKERS.md`
