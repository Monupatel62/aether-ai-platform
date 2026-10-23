# Canonical Architecture Decision Record (ADR) Index

**Updated:** 2026-10-23  
**Authority:** `DECISION_LOG.md` contains the decision history; this index normalizes the latest explicitly documented state. If an entry's state is uncertain, it is marked **Needs reconciliation**, never inferred as accepted.

## Controlled status vocabulary

- **Accepted:** Explicitly accepted in the decision log.
- **Open:** Decision is unresolved.
- **Proposed:** Candidate guidance exists but is not accepted.
- **Needs reconciliation:** The source log does not provide a reliable canonical row/status, or duplicate rows conflict.

## Canonical index

| ADR | Decision | Canonical status | Evidence / next action |
|---|---|---|---|
| ADR-0001 | Aether AI is standalone | Accepted | Keep architecture and product decisions owned by Aether AI. |
| ADR-0002 | No assumed external runtime dependencies | Accepted | External runtime dependencies require explicit review. |
| ADR-0003 | Plan 33 canonical repositories | Accepted | Repository organization does not imply 33 deployable services. Duplicate source row noted in [ADR Log Integrity Audit](ADR_LOG_INTEGRITY_AUDIT.md); consolidate source log without losing history. |
| ADR-0004 | Repository boundaries vs deployable-service boundaries | Accepted | Prefer smallest viable modular runtime; topology remains undecided. Duplicate source row noted in audit. |
| ADR-0005 | Gateway strategy: native, adapter, or external DIAL | Open | [Gateway evaluation](DIAL_ADOPTION_EVALUATION.md); no external runtime selected. Duplicate source row noted in audit. |
| ADR-0006 | Frontend/backend technology stack | Open | Compare maintainability, compatibility, security and operations before selection. |
| ADR-0007 | Database, queue, cache, vector/search technology | Open | [Data infrastructure evaluation](DATA_INFRASTRUCTURE_EVALUATION.md); candidates remain unselected. Duplicate source row noted in audit. |
| ADR-0008 | Identity provider and session model | Open | Threat model, requirements, and synthetic-identity POC required. |
| ADR-0009 | Provider/model catalog and fallback policy | Open | Compare capability, cost, privacy, streaming, tool calls, and model terms. |
| ADR-0010 | Product name and public branding | Open | Verify naming/domain/trademark availability before launch. |
| ADR-0011 | Package/repository/CI strategy | Open | Choose versioning and cross-repository release model before implementation. |
| ADR-0012 | Prompt/file/memory retention and telemetry | Open | Product/privacy/legal review required; numeric periods remain open. |
| ADR-0013 | MCP protocol and SDK compatibility | Proposed | Pin supported protocol revision and validate implementation conformance. |
| ADR-0014 | AI security baseline | Proposed | Map threat model to selected guidance and executable abuse-case tests. |
| ADR-0015 | GenAI observability and privacy | Proposed | Raw prompt/completion capture disabled by default until retention/redaction are approved. |
| ADR-0016 | CI action and release supply-chain policy | Proposed | Pin actions immutably, least-privilege tokens, and protect releases. |
| ADR-0017 | Unknown / unrecorded in inspected decision log | Needs reconciliation | Determine whether the ID was reserved or an ADR record was omitted. Do not silently assign or renumber. |
| ADR-0018 | Data-layer ownership and source-of-truth rules | Proposed | Validate transaction source, rebuildable projections, opaque queue references, durable orchestration state, and reconstructible cache with tests. |
| ADR-0019 | Browser session architecture | Open | Research describes BFF/server-side session as candidate only. |
| ADR-0020 | Authorization model and policy-engine scope | Open | Permission matrix and policy gaps require product/security approval. |
| ADR-0021 | Tenant hierarchy and support access | Open | Tenant membership/support-access decisions remain unresolved. |
| ADR-0022 | API-key and workload identity | Open | Define lifecycle, audience, scope, rotation and revocation. |
| ADR-0023 | MFA, recovery, session and revocation SLOs | Open | Define measurable targets and test evidence. |
| ADR-0024 | Tenant isolation and row-level security rollout | Open | Define rollout, enforcement boundaries, migration and negative tests. |

## Governance rules

1. Never infer an accepted decision from a recommendation, research note, test plan, or candidate scorecard.
2. Each ADR must include context, options, chosen option (if accepted), rationale, consequences, security/license implications, migration plan, affected repositories, date, reviewer, and evidence.
3. Every change in status must update this index and the decision log in the same pull request.
4. Accepted decisions are not silently rewritten; supersede them with a new ADR and preserve the historical record.
5. The validator detects duplicate ADR IDs in the canonical table and invalid status labels. It does not decide architecture, approve an ADR, or infer missing decisions.
6. ADR-0017 remains **Needs reconciliation** until an authorized owner confirms whether it is reserved or missing.

## Evidence boundary

This index is normalized from the inspected `DECISION_LOG.md` text. ADR-0019 through ADR-0024 are marked Open because the log explicitly says they remain open. ADR-0017 has no recorded occurrence in the inspected source. No P0 blocker is closed by this index.
