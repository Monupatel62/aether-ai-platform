# ADR Evidence and Status Consistency Audit

**Review date:** 2026-10-23  
**Scope:** Compare `ADR_INDEX.md` and `DECISION_LOG.md` against the supporting research and policy documents available in the documentation branch.  
**Type:** Documentation evidence audit only. This review does not accept decisions, close P0 blockers, or authorize implementation.

## Executive result

The inspected evidence supports keeping the technology and security ADRs unresolved or proposed. Research repeatedly states that candidates have not been selected and that POCs/tests have not run. The main actionable gaps are incomplete evidence pointers in the canonical index, the missing ADR-0017 record, and a need to distinguish the status of an ADR from the status of its supporting research.

## Findings

| ID | ADR(s) | Finding | Evidence observed | Recommended disposition |
|---|---|---|---|---|
| ADR-AUDIT-01 | ADR-0001–0004 | Statuses are explicitly Accepted in the decision log. | The canonical decision-log table records these four as Accepted. | Preserve these statuses; do not expand their scope beyond their stated decisions. |
| ADR-AUDIT-02 | ADR-0005 | Open status is supported. | `DIAL_ADOPTION_EVALUATION.md` says no external gateway is accepted; it requires a native POC, conformance tests, and explicit review before any external runtime. `OPEN_DECISIONS_RESEARCH.md` asks for a two-provider POC. | Keep Open. Add direct evidence links to the index; do not select native/DIAL based on research alone. |
| ADR-AUDIT-03 | ADR-0006 | Open status is supported, but evidence is thin in the inspected documents. | Decision log says DIAL Chat is a reference, not a binding stack. No accepted stack decision was found in the reviewed supporting docs. | Keep Open; define evaluation criteria and a decision owner before selecting a stack. |
| ADR-AUDIT-04 | ADR-0007 and ADR-0018 | Open/Proposed distinction is consistent. | `DATA_INFRASTRUCTURE_EVALUATION.md` explicitly says no vendor or database choice has been accepted. PostgreSQL + pgvector/full-text, BullMQ, and a Valkey-compatible cache are recommendations to evaluate, not final selections. | Keep ADR-0007 Open and ADR-0018 Proposed. Require measured backup/restore, tenancy/isolation, failure and workload evidence before acceptance. |
| ADR-AUDIT-05 | ADR-0008 | Open status is supported. | `IDENTITY_AND_TENANT_SECURITY_EVALUATION.md` says no identity provider or authorization implementation has been selected. `IDENTITY_PROVIDER_SHORTLIST_AND_SCORECARD.md` says no provider is selected and scores must be based on POC evidence. | Keep Open; do not convert a shortlist or scorecard into a vendor choice. |
| ADR-AUDIT-06 | ADR-0009 | Open status is supported; no provider/fallback decision evidenced. | The decision log requires comparison of capability, cost, privacy, streaming, tool calls and terms. The reviewed docs do not record an accepted model/provider policy. | Keep Open; attach a model capability, privacy, cost and fallback evaluation before decision. |
| ADR-AUDIT-07 | ADR-0010–0011 | Open statuses are supported; the reviewed evidence does not settle branding or packaging/CI strategy. | The decision log marks both Open. The CI/CD audit is an evidence inventory, not an accepted package/release policy. | Keep Open; require explicit owner and acceptance criteria. |
| ADR-AUDIT-08 | ADR-0012 and ADR-0015 | Open/Proposed states are consistent. | `DATA_RETENTION_DELETION_EXPORT_TELEMETRY_POLICY.md` explicitly says no numeric retention duration is approved and no compliance certification is claimed. It recommends raw content telemetry off by default. | Keep ADR-0012 Open and ADR-0015 Proposed. Numeric periods, legal holds, residency, export scope and observability redaction need review/approval. |
| ADR-AUDIT-09 | ADR-0013 | Proposed status is supported, not accepted. | `OPEN_DECISIONS_RESEARCH.md` proposes a protocol adapter/version matrix and lists unresolved transports, legacy compatibility, auth and upgrade questions. | Keep Proposed until protocol/SDK versions and support policy are approved with conformance tests. |
| ADR-AUDIT-10 | ADR-0014 | Proposed status is supported, not accepted. | `OPEN_DECISIONS_RESEARCH.md` proposes mapping the threat model to OWASP GenAI 2026 guidance and stresses that prompt wording is not a security control. | Keep Proposed; require Aether-specific threat scenarios, controls and executable tests. |
| ADR-AUDIT-11 | ADR-0016 | Proposed status is supported, not accepted. | Decision log contains a supply-chain policy proposal; inspected CI/CD audit reports evidence gaps and unknown branch-protection status. | Keep Proposed; do not claim branch protection or immutable action pinning is deployed until verified. |
| ADR-AUDIT-12 | ADR-0019 | Open status is supported. | `BROWSER_SESSION_AND_AUTHORIZATION_ARCHITECTURE.md` labels BFF/server-side sessions a candidate recommendation, not a final decision. | Keep Open; POC must test session revocation, CSRF, token handling and tenant resolution. |
| ADR-AUDIT-13 | ADR-0020–0024 | Open statuses are supported. | `AUTHORIZATION_POLICY_GAP_AUDIT.md`, `IDENTITY_AND_TENANT_SECURITY_EVALUATION.md`, and `DATA_RETENTION_DELETION_EXPORT_TELEMETRY_POLICY.md` identify policy/ownership gaps and state no implementation or POC has run. | Keep Open; resolve membership ownership, support access, role grants, workload identity, lifecycle/revocation targets and RLS rollout with approved contracts and tests. |
| ADR-AUDIT-14 | ADR-0017 | Missing record remains unresolved. | The inspected decision log contains no ADR-0017 occurrence; repository code search returned no match. | Keep “Needs reconciliation.” Ask the authorized decision owner whether this ID was reserved or omitted. Do not repurpose or renumber it without confirmation. |
| ADR-AUDIT-15 | All indexed ADRs | Canonical index does not yet consistently link to primary evidence for every row. | Several rows have a direct document link, while others only state a generic next action. | Add direct evidence links where documents exist; explicitly label “evidence not located” where no supporting artifact was found. |

## Evidence boundary

- This audit checked document content, not running services or deployed controls.
- No identity-provider POC, gateway POC, database benchmark, runtime security test, or retention-deletion test was executed as part of this audit.
- The presence of a research document is not proof of implementation, compliance, acceptance, or production readiness.
- This audit does not change the status of any ADR and does not close any P0 implementation blocker.

## Recommended next sequence

1. Obtain an explicit owner disposition for ADR-0017.
2. Add primary-document links and evidence labels to the canonical index.
3. Define decision owners and required evidence for ADR-0006, ADR-0009, ADR-0010 and ADR-0011.
4. Keep all P0-sensitive identity, authorization, data lifecycle and tool execution decisions gated on reviewed contracts and test evidence.
