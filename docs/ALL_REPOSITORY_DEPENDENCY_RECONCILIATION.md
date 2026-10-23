# All-Repository Dependency Reconciliation — Focused Pass

**Date:** 2026-10-23  
**Status:** Documentation comparison; proposed follow-up actions, not runtime evidence.  
**Scope:** Catalog-derived 33 canonical repositories; each current-main `docs/REPOSITORY_SPECIFICATION.md` was fetched in three batches and its dependency section checked against the master dependency matrix. This pass compares declared dependency text, not every statement in every file.

## Inventory result

- Canonical repositories in catalog: 33.
- Repository specification files fetched successfully: 33/33.
- Dependency sections compared: 33/33.
- Application source/runtime imports: none claimed or checked by this document.

## Reconciliation findings

| ID | Repository | Comparison result | Required action |
|---|---|---|---|
| DEP-33-01 | `aether-ai-search` | Specification names `aether-ai-database` for neutral metadata contracts; matrix summarizes backend, neutral index/document metadata contract, and Security, but omits the explicit Database relationship. | Clarify whether the Database link is a package contract, generated/public artifact, or documentation-level contract. Add it to the matrix only if it is a real direct dependency; otherwise align the spec wording. |
| DEP-33-02 | `aether-ai-providers` | Specification describes the provider interface/capability contract as owned here and consumed by Gateway; matrix calls it a shared provider contract owned here. Direction is aligned, but artifact/import type is not finalized. | Decide whether the initial modular runtime uses a package interface, generated artifact, or another contract; preserve the no-provider-to-Gateway-import rule. |
| DEP-33-03 | `aether-ai-integrations` | Specification permits MCP only for integrations that explicitly use MCP; matrix similarly says MCP only where justified. | Keep this conditional dependency optional and ensure the generic integration package does not require MCP. |
| DEP-33-04 | `aether-ai-testing` | Specification and matrix both describe test-only fixtures/contracts and explicitly exclude production runtime dependency. | Preserve this boundary; CI should prevent production packages from importing the testing repository/package. |
| DEP-33-05 | `aether-ai-platform` and `aether-ai-docs` | Both define documentation-only relationships; matrix says no runtime dependencies/imports. | Preserve docs-only boundary and enforce it in any future package graph. |
| DEP-33-06 | `aether-ai-workflows`, `aether-ai-queue`, `aether-ai-database`, `aether-ai-security` | Their specs and matrix largely agree on dependency inversion and ownership direction; exact edge types remain incomplete or provisional. | Classify each connection using the edge-register vocabulary before implementation. Do not infer package imports from the word “depends.” |

## High-risk ownership invariants checked across all 33 dependency sections

- API delegates durable runs to Orchestration; no competing durable run state owner.
- Workflows owns schema/validation, not execution or durable persistence.
- Queue owns transport/delivery mechanics, not producer/consumer business logic.
- Database tooling does not import domain services; domain owners retain data semantics.
- Auth owns identity/session lifecycle; Security owns shared policy contracts; membership authority remains an open ADR.
- Knowledge owns source/collection ACL authority; RAG/Search consume contracts and cannot grant access from projection metadata.
- Provider adapters do not import Gateway implementation.
- UI components have no product-domain authorization logic; browser traffic goes through API.
- Testing is not a production runtime dependency.
- Deployment consumes Infrastructure modules; Infrastructure does not depend on product-domain runtime components.

## Limitations and status

This is a dependency-section reconciliation, not a full semantic re-audit of every repository specification. The prior focused audit identified unresolved membership authority, Security library-vs-service shape, migration composition, indexing/revocation propagation targets, and edge classification. Those remain open. No package-import graph, cycle detector, source import scan, build, or runtime test was run; all repositories remain documentation-only on the inspected main branches.

## Next acceptance gate

1. Resolve DEP-33-01 and classify the provider/interface edge.
2. Review the remaining ownership decisions in [Cross-Repository Ownership Consistency Follow-up](CROSS_REPOSITORY_OWNERSHIP_CONSISTENCY_FOLLOWUP.md).
3. Add machine-readable edge inventory and automated cycle detection after implementation languages/package boundaries are approved.
4. Keep Phase 0 open until P0 contracts are accepted or explicitly deferred and implementation is explicitly authorized.
