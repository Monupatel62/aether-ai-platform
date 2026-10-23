# Dependency Direction Audit — 2026-10-23

**Status:** Documentation-only findings and proposed corrections. No source import graph, build, CI, or runtime behavior was tested.

## Summary

A targeted comparison of the master `DEPENDENCY_MATRIX.md` with the repository-level `docs/DEPENDENCIES_AND_CONTRACTS.md` files found three direct-dependency statements that contradicted the proposed master ownership direction. Corrected each component contract on a review branch and fetched the files back for verification.

## Findings and corrections

| ID | Repository | Previous declaration | Why it conflicted | Correction |
|---|---|---|---|---|
| DEP-DIR-01 | `aether-ai-providers` | Provider adapters depend on gateway public contracts | The master matrix assigns ownership of the provider interface/capability registry to providers and says gateway consumes it. A provider→gateway package edge reverses ownership and can create a cycle if gateway also imports providers. | Vendor SDKs are optional reviewed dependencies; gateway consumes the provider contract. Provider adapters do not import gateway implementation. |
| DEP-DIR-02 | `aether-ai-agents` | Agents depend on orchestration through versioned contracts | The master matrix assigns durable run state to orchestration, which consumes the agent runtime. A direct agents→orchestration package dependency would reverse the edge and create a potential package cycle. | Orchestration consumes the agent runtime contract. Agents do not import orchestration implementation. Any shared run/event schema must be lower-level and independently versioned. |
| DEP-DIR-03 | `aether-ai-files` | API listed as a direct dependency | The master matrix makes API a consumer of the files public contract; the file component should not depend on the product API. | Direct dependencies now list persistence contracts, security policy, observability and a future object-storage adapter. API is explicitly described as a consumer. |

## Changed artifacts

- `aether-ai-providers/docs/DEPENDENCIES_AND_CONTRACTS.md`
- `aether-ai-agents/docs/DEPENDENCIES_AND_CONTRACTS.md`
- `aether-ai-files/docs/DEPENDENCIES_AND_CONTRACTS.md`

The changes are proposed documentation corrections only. They do not prove that actual source imports match the contracts, nor that the full 33-repository graph is cycle-free.

## Remaining verification

1. Review the three component-repository pull requests and the master audit pull request.
2. Compare all repository-level direct-dependency declarations against the typed edge register and machine-readable graph.
3. Normalize dependency edges by type (package import, synchronous API, event/queue, generated artifact, infrastructure, documentation) before any automated cycle claim.
4. Keep implementation blocked until P0 identity/tenant/ACL, tool-policy, durable-run and data-deletion contracts are accepted and the user explicitly approves the transition.


## Second targeted pass — additional findings

| ID | Repository | Previous declaration | Why it conflicted | Correction |
|---|---|---|---|---|
| DEP-DIR-04 | `aether-ai-cache` | Cache depended on API, gateway, search and database | The master matrix defines cache as a low-level adapter/key/TTL capability. Application components consume cache; cache should not import consumers or require database as an inherent dependency. | Direct dependencies narrowed to selected cache adapter and neutral key/TTL/value-format contracts. |
| DEP-DIR-05 | `aether-ai-plugins` | Plugins depended on the admin application | The master matrix makes plugins a capability/policy subsystem. Admin may consume plugin-management contracts, but plugin runtime must not import the admin app. | Removed admin from plugin direct dependencies and documented the consumer direction. |
| DEP-DIR-06 | `aether-ai-deployment` | Deployment depended on “platform” and services being deployed | The platform repository is docs/control plane only; the generic declaration did not distinguish build/release artifacts from runtime/package dependencies. | Deployment consumes infrastructure modules and versioned component release artifacts/manifests; platform is not a runtime dependency. |

The six findings are proposed dependency-contract corrections only. No source imports or runtime dependency graph was inspected.
