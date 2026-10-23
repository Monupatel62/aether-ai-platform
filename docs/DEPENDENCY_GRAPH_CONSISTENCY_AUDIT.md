# Dependency Graph Consistency Audit

**Audit date:** 2026-10-23  
**Status:** Static validation of the proposed graph only. Not source-import analysis, build validation, or approval to implement.  
**Inputs:** `docs/dependency-package-graph.json`, `docs/DEPENDENCY_EDGE_REGISTER.md`, `docs/DEPENDENCY_MATRIX.md`, and the current tenant-membership decision documents.

## Executive result

The machine-readable candidate package-import graph parses as JSON and passes these structural checks:

| Check | Result |
|---|---:|
| Declared repository nodes | 33 |
| Package-import edges | 61 |
| Edges with an endpoint missing from the node list | 0 |
| Duplicate package-import edges | 0 |
| Directed cycles found by graph traversal | 0 |
| Edge types represented in this JSON graph | `package_import` only |

These results confirm the graph is structurally consistent as a proposed package-import graph. They do not prove that code imports match it, that interfaces compile, or that network/event relationships are safe. No repository builds or tests were run.

## Review findings

### DG-01 — Tenant-membership owner is still unresolved

The dependency matrix and tenant/ACL decision documents explicitly leave the canonical membership owner open. The new `TENANT_MEMBERSHIP_OWNER_DECISION_BRIEF.md` recommends `aether-ai-enterprise` only as a proposal, conditional on its being the universal tenancy domain.

**Required action:** Do not add an `aether-ai-enterprise` dependency to runtime contracts or freeze authorization schemas until the product owner accepts the tenancy model. If Option A is accepted, update the dependency matrix, edge register, graph, and affected repository specs together. If a new repository is preferred, explicitly revise the accepted 33-repository plan before creating it.

### DG-02 — Six nodes have no package-import edges in the current graph

The current candidate graph has no incoming or outgoing package-import edge for:
- `aether-ai-platform`
- `aether-ai-sdk`
- `aether-ai-deployment`
- `aether-ai-docs`
- `aether-ai-cache`
- `aether-ai-infrastructure`

This is not automatically an error: the platform and docs repositories are control/documentation areas, the SDK is represented as a generated/public artifact, and deployment/infrastructure may use provisioning relationships. Cache may be reached through an infrastructure adapter or an abstraction not represented in this package graph. However, the edge register and master catalog must make each node's intended connection type explicit and consistent. Do not invent package imports solely to remove isolated nodes.

### DG-03 — The JSON graph deliberately excludes non-package relationships

The graph's own metadata says network APIs, events/queues, generated artifacts, infrastructure provisioning and documentation-only relationships are excluded. Therefore, zero cycles applies only to the proposed package-import edges. It is not a claim that the complete runtime interaction graph is cycle-free.

**Required action:** Keep the typed edge register as the source for cross-boundary relationships and review request/event directions, especially trusted usage events, authorization checks, deletion/revocation events and job reauthorization. Do not merge every edge type into a single package-cycle graph.

### DG-04 — No source code exists in the audited tree baseline

The previous recursive-tree audit found documentation-only content across all 33 canonical repositories and no conventional source, test or CI paths in the returned trees. Consequently, this pass could not compare declared package imports against real source imports.

**Required action:** When the implementation gate is approved, create one minimal vertical slice and add automated checks that compare actual workspace/package imports with the accepted graph. Until then, label this result as design validation only.

## Acceptance checklist before the first vertical slice

- [ ] Accept the canonical tenant/workspace membership owner.
- [ ] Resolve the P0 identity/session and authorization-context trust blockers.
- [ ] Confirm every repository's direct dependencies against the typed edge register.
- [ ] Confirm package imports, synchronous APIs, asynchronous events, generated artifacts and infrastructure edges remain separately classified.
- [ ] Validate OpenAPI and JSON Schema with dedicated validators and run the contract fixtures.
- [ ] Approve the documentation gate explicitly before application coding.
- [ ] After coding is authorized, enforce dependency direction and cycle checks in CI against actual source imports.

## Related documents

- [Dependency matrix](DEPENDENCY_MATRIX.md)
- [Dependency edge register](DEPENDENCY_EDGE_REGISTER.md)
- [Machine-readable package graph](dependency-package-graph.json)
- [Cross-repository contract audit](CROSS_REPOSITORY_CONTRACT_AUDIT.md)
- [Tenant membership ownership decision brief](TENANT_MEMBERSHIP_OWNER_DECISION_BRIEF.md)
- [Implementation gate blockers](IMPLEMENTATION_GATE_BLOCKERS.md)
- [Identity and authorization POC test matrix](IDENTITY_AUTHORIZATION_POC_TEST_MATRIX.md)
