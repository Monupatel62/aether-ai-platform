# Architecture Decision Log Integrity Audit

**Date:** 2026-10-23  
**Scope:** Static review of ADR table rows in `docs/DECISION_LOG.md`.  
**Status:** Documentation consistency findings only. No decision is accepted, rejected, or changed by this audit.

## Findings

| ID | Severity | Finding | Required correction |
|---|---|---|---|
| ADRLOG-01 | High | ADR-0003 appears twice with slightly different rationale/status wording. | Keep one canonical row; preserve historical review notes below it without duplicating the active decision table. |
| ADRLOG-02 | High | ADR-0004 appears twice with wording variations. | Keep one canonical row and explicitly state that runtime topology remains undecided while the repository/service-boundary principle is accepted. |
| ADRLOG-03 | High | ADR-0005 appears twice: one row frames DIAL adoption/adapter/custom gateway; another frames native gateway vs optional external gateway. Both are open and overlap. | Consolidate into one ADR-0005 with a clear decision question and link the evaluation; do not infer adoption of DIAL or any external runtime. |
| ADRLOG-04 | High | ADR-0007 appears twice: a general open row and a later “Open; baseline proposed” row. | Keep one canonical status row and link the data-infrastructure evaluation. Candidate technologies remain candidates until evidence and review support acceptance. |
| ADRLOG-05 | Medium | Numbering moves from ADR-0016 to ADR-0018; ADR-0017 is not present in the active rows. | Determine whether ADR-0017 was intentionally reserved or omitted. Do not silently renumber existing ADRs; add a placeholder or record the reservation in the log. |
| ADRLOG-06 | Medium | ADR-0018 appears only in the later table and is not part of the initial top-level summary table. | Maintain a single canonical index for all ADR IDs, status, owner, affected repos, evidence link, and last-updated date. |
| ADRLOG-07 | Medium | The log uses statuses including Accepted, Open, Open; baseline proposed, and Proposed without a concise controlled vocabulary. | Define allowed statuses and distinguish a proposed baseline from an accepted architecture decision. |
| ADRLOG-08 | Medium | The log’s ADR format asks for reviewer and consequences, but active rows do not consistently provide owner, affected repositories, date, and evidence link. | Add those fields to the canonical ADR index; detailed decision records should contain alternatives, trade-offs, security/license implications and acceptance evidence. |

## Evidence and limitations

- The inspected decision-log content contains duplicate active table rows for ADR-0003, ADR-0004, ADR-0005, and ADR-0007.
- ADR-0018 is listed after ADR-0016; no ADR-0017 row appeared in the inspected table rows.
- This is a static document review. It does not establish whether ADR records exist in unlisted files, branches, or external discussions.
- No architecture choices were made during this audit. Open remains open; proposed remains proposed; accepted decisions are not changed.

## Safe remediation order

1. Create one canonical ADR index table with a stable ID and controlled status vocabulary.
2. Consolidate duplicate rows without erasing the review history or changing decision semantics.
3. Verify whether ADR-0017 is reserved or missing before adding any record.
4. Link every open/proposed ADR to its evidence and the P0 blocker(s) it affects.
5. Add a lightweight CI check that flags duplicate ADR IDs and malformed/missing status fields; do not make CI auto-accept decisions.
6. Fetch the revised log back and verify uniqueness, status preservation, and all relative links before proposing a merge.

## Relationship to the implementation gate

The duplicate rows do not justify treating any open architecture decision as accepted. Implementation remains blocked by the existing P0 gate until blockers are accepted or explicitly deferred, contract validation is evidenced, and the user authorizes implementation.
