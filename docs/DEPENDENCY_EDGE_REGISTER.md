# Aether AI — Dependency Edge Register

**Date:** 2026-10-22  
**Status:** Proposed logical edge classification for architecture review. This register does not select a 33-service deployment topology. A package contract may be used in-process in the initial modular runtime; a network boundary is required only if a separate service is later justified.

## Edge types

- **Package import:** one repository imports a versioned public library/interface from another. It must not import private implementation internals.
- **Synchronous network API:** request/response contract between runtime components; does not imply separate deployment until topology is approved.
- **Asynchronous event/queue:** producer/consumer relationship using versioned envelopes and idempotent handlers.
- **Generated/public artifact:** generated SDK, schemas, release artifact, or other versioned output.
- **Infrastructure provisioning:** IaC/module relationship, not an application runtime dependency.
- **Documentation-only:** published documentation, catalog, or control-plane reference; no runtime edge.

Where the same logical relationship could be either a package import or network API, the table selects the **initial modular-runtime package contract** unless an event or artifact is more appropriate. Revisit the type if a service boundary is accepted. All edges remain proposed until reviewed. Package-import rows targeting external libraries/backends or generic test fixtures are listed for visibility but are excluded from the internal 33-repository package graph.

## Classified edges

| From | To | Proposed edge type | Contract / direction constraint |
|---|---|---|---|
| aether-ai-platform | all Aether repositories | Documentation-only | Catalog, ADRs and specs only; no runtime imports. |
| aether-ai-web | aether-ai-api | Synchronous network API | Browser-facing product API/BFF; no provider credentials in browser. |
| aether-ai-web | aether-ai-ui-components | Package import | Presentation primitives only; no product authorization logic. |
| aether-ai-web | aether-ai-sdk | Generated/public artifact | Consume generated public types/client; API must not import its own SDK. |
| aether-ai-admin | aether-ai-api | Synchronous network API | Privileged actions authorized and audited server-side. |
| aether-ai-admin | aether-ai-auth | Package import | Public principal/session types only; no identity bypass. |
| aether-ai-admin | aether-ai-ui-components | Package import | Shared presentation only. |
| aether-ai-api | aether-ai-auth | Package import | Authentication/session/principal contract; does not imply authorization grant. |
| aether-ai-auth | aether-ai-security | Package import | Shared principal/policy primitives only; identity/session lifecycle remains in Auth. |
| aether-ai-api | aether-ai-gateway | Synchronous network API | Bounded synchronous model requests only; durable run lifecycle is not owned here. |
| aether-ai-api | aether-ai-orchestration | Synchronous network API | Durable run submit/status/cancel; orchestration is sole run-state owner. |
| aether-ai-api | aether-ai-files | Synchronous network API | File lifecycle/download authorization contract. |
| aether-ai-api | aether-ai-knowledge | Synchronous network API | Collection/source metadata and ACL references. |
| aether-ai-api | aether-ai-billing | Package import | Read-only entitlement contract; billing does not call API back to validate usage. |
| aether-ai-api | aether-ai-security | Package import | Shared policy request/decision contract; API enforces each resource/action. |
| aether-ai-api | aether-ai-observability | Package import | Redacted telemetry interfaces; sensitive payload capture off by default. |
| aether-ai-gateway | aether-ai-providers | Package import | Provider interface/capability registry; provider adapters never import gateway implementation. |
| aether-ai-gateway | aether-ai-security | Package import | Policy and secret-handling primitives. |
| aether-ai-gateway | aether-ai-observability | Package import | Redacted tracing/metrics interface. |
| aether-ai-providers | WoHo AI DevKit provider packages | Package import | Optional only after exact version/export/license and contract tests. |
| aether-ai-agents | aether-ai-gateway | Package import | Stable model request contract; no provider-specific wire details. |
| aether-ai-agents | aether-ai-tools | Package import | All tool invocation goes through policy boundary. |
| aether-ai-agents | aether-ai-memory | Package import | Scoped memory retrieval and retention contract. |
| aether-ai-agents | aether-ai-security | Package import | Risk policy and principal/resource context. |
| aether-ai-agents | aether-ai-observability | Package import | Lifecycle telemetry with redaction. |
| aether-ai-workflows | shared schema utility, if selected | Package import | Optional minimal utility only; no imports of orchestration, agents or database. |
| aether-ai-orchestration | aether-ai-workflows | Package import | Consume versioned workflow schema/validation contract. |
| aether-ai-orchestration | aether-ai-agents | Package import | Invoke bounded agent runtime; orchestration owns durable state. |
| aether-ai-orchestration | aether-ai-queue | Package import | Neutral queue producer/consumer contract; queue must not import orchestration. |
| aether-ai-orchestration | aether-ai-database | Package import | Persistence tooling/contracts; domain state semantics remain with orchestration. |
| aether-ai-orchestration | aether-ai-security | Package import | Policy contract for protected steps/actions. |
| aether-ai-orchestration | aether-ai-observability | Package import | Run/step lifecycle telemetry. |
| aether-ai-tools | aether-ai-security | Package import | Policy decision and tool risk contract. |
| aether-ai-tools | aether-ai-observability | Package import | Redacted tool lifecycle telemetry. |
| aether-ai-mcp | aether-ai-tools | Package import | MCP adapters register through public tool manifest/invocation contract; tools never import MCP. |
| aether-ai-mcp | aether-ai-security | Package import | Server allowlist, auth and invocation policy. |
| aether-ai-mcp | aether-ai-observability | Package import | Redacted MCP lifecycle telemetry. |
| aether-ai-memory | aether-ai-database | Package import | Persistence tooling; tenant/user/session scoping remains mandatory. |
| aether-ai-memory | aether-ai-security | Package import | Retention and access policy contract. |
| aether-ai-rag | aether-ai-files | Package import | File lifecycle/ingestion contract. |
| aether-ai-rag | aether-ai-knowledge | Package import | Consume authoritative source metadata, ACL version and deletion contracts. |
| aether-ai-rag | aether-ai-search | Package import | Index/query contract; search remains a rebuildable projection. |
| aether-ai-rag | aether-ai-providers | Package import | Embedding capability contract. |
| aether-ai-rag | aether-ai-security | Package import | Policy contract; final authorization is not inferred from vector metadata. |
| aether-ai-files | aether-ai-database | Package import | Persistence tooling; file lifecycle/ACL semantics remain in Files. |
| aether-ai-files | aether-ai-security | Package import | Upload/download policy and scanning boundaries. |
| aether-ai-files | aether-ai-observability | Package import | Redacted lifecycle telemetry. |
| aether-ai-knowledge | aether-ai-files | Package import | Consume public file lifecycle contract; no private table access. |
| aether-ai-knowledge | aether-ai-database | Package import | Persistence tooling; knowledge owns its data semantics. |
| aether-ai-knowledge | aether-ai-auth | Package import | Principal/session contract only. |
| aether-ai-knowledge | aether-ai-security | Package import | Shared policy contract. |
| aether-ai-billing | aether-ai-database | Package import | Billing-owned persistence via shared tooling. |
| aether-ai-billing | aether-ai-queue | Package import | Consume trusted usage events and publish entitlement events/contracts. |
| aether-ai-billing | aether-ai-security | Package import | Billing/administrative policy contract. |
| aether-ai-billing | aether-ai-api | Asynchronous event/queue | Trusted usage events flow API → billing; no billing → API synchronous callback. |
| aether-ai-billing | aether-ai-gateway | Asynchronous event/queue | Trusted server-side usage events flow gateway → billing. |
| aether-ai-sdk | aether-ai-api | Generated/public artifact | SDK schemas/client generated from versioned API contract. |
| aether-ai-evaluations | aether-ai-agents | Package import | Evaluate agent contracts using synthetic/sanitized datasets by default. |
| aether-ai-evaluations | aether-ai-gateway | Package import | Evaluate normalized model behavior. |
| aether-ai-evaluations | aether-ai-testing | Package import | Shared fixtures and harness. |
| aether-ai-evaluations | aether-ai-observability | Package import | Evaluation telemetry contract. |
| aether-ai-deployment | aether-ai-infrastructure | Infrastructure provisioning | Consume reviewed IaC modules; no domain logic. |
| aether-ai-deployment | Aether release artifacts | Generated/public artifact | Deploy versioned, reviewed artifacts. |
| aether-ai-docs | all Aether repositories | Documentation-only | Publish versioned documentation; no runtime dependency. |
| aether-ai-cache | selected cache backend | Package import | Reconstructible data only; never authoritative permissions/billing/run state. |
| aether-ai-search | selected search/vector backend | Package import | Backend adapter; exact backend remains undecided. |
| aether-ai-search | aether-ai-database | Package import | Neutral metadata/migration contract only; not domain-private tables. |
| aether-ai-search | aether-ai-security | Package import | Query policy/filter contract; fresh authorization still required by caller. |
| aether-ai-plugins | aether-ai-tools | Package import | Tool manifest/policy contract; plugins cannot self-authorize. |
| aether-ai-plugins | aether-ai-auth | Package import | Principal and plugin enablement context. |
| aether-ai-plugins | aether-ai-security | Package import | Capability grants and policy contract. |
| aether-ai-integrations | aether-ai-tools | Package import | Connector calls pass through tool policy. |
| aether-ai-integrations | aether-ai-auth | Package import | Narrow credential/principal contract. |
| aether-ai-integrations | aether-ai-security | Package import | Outbound network and scope policy. |
| aether-ai-integrations | aether-ai-mcp | Package import | Only for integrations that actually use MCP; no forced protocol coupling. |
| aether-ai-testing | shared test fixtures/contracts | Package import | Test-only; no production runtime dependency. |
| aether-ai-enterprise | aether-ai-auth | Package import | Principal/session contract; no duplicate identity authority. |
| aether-ai-enterprise | aether-ai-security | Package import | Enterprise policy configuration contract. |
| aether-ai-enterprise | aether-ai-billing | Package import | Enterprise entitlement contract. |
| aether-ai-enterprise | aether-ai-observability | Package import | Auditable configuration and export telemetry. |
| aether-ai-infrastructure | selected infrastructure providers | Infrastructure provisioning | Provider modules and environment foundations. |
| aether-ai-ui-components | none | Documentation-only | UI primitives must not depend on product API/domain packages. |

## Candidate package-import graph used for cycle review

This is a proposed package graph extracted from the package-import rows above. Network API, asynchronous event/queue, generated-artifact, infrastructure and documentation-only edges are excluded from package cycle detection.

```text
web -> ui-components
web -> sdk (generated artifact; excluded from package graph)
admin -> auth, ui-components
api -> auth, billing, security, observability
gateway -> providers, security, observability
agents -> gateway, tools, memory, security, observability
orchestration -> workflows, agents, queue, database, security, observability
tools -> security, observability
mcp -> tools, security, observability
memory -> database, security
rag -> files, knowledge, search, providers, security
files -> database, security, observability
knowledge -> files, database, auth, security
billing -> database, queue, security
evaluations -> agents, gateway, testing, observability
deployment -> infrastructure (infrastructure edge; excluded)
search -> database, security
plugins -> tools, auth, security
integrations -> tools, auth, security, mcp
enterprise -> auth, security, billing, observability
```

## Explicit exclusions / non-edges

- `aether-ai-workflows` does **not** import orchestration, agents or database.
- `aether-ai-knowledge` does **not** import RAG or Search implementation.
- `aether-ai-api` does **not** import agents for durable execution.
- `aether-ai-queue` does **not** import orchestration, workflows, billing or observability consumers.
- `aether-ai-database` and `aether-ai-security` do not import their domain/runtime consumers.
- `aether-ai-tools` does **not** import MCP; the composition root registers MCP-backed tools.

## Machine-readable package graph and cycle check

The candidate package-import graph is stored in [dependency-package-graph.json](dependency-package-graph.json). The JSON file was fetched back from GitHub, parsed, validated for known nodes and `package_import` edge types, and passed to a depth-first-search cycle detector.

**Result:** 33 nodes, 61 directed package-import edges, **0 cycles reported**.

**Limitations:** the JSON graph is still a human-authored proposed design, not extracted from actual source imports or build manifests. This verifies only that the candidate graph encoded in the JSON file contains no directed cycles. It does not prove that implementation imports match the proposal, that every Markdown relationship was classified correctly, or that runtime synchronous-call/event loops are absent. Re-run the check whenever the JSON graph changes and separately review runtime call/event loops.

## Open items

- Confirm whether logical API relationships become package calls or network APIs in the initial deployment.
- Confirm the tenant/workspace membership and role-grant source of truth (ADR-0021).
- Define ACL revocation/deletion consistency targets and the canonical authorization check (ADR-0020/0024).
- Validate external package imports, versioned contracts and licenses before implementation.
- Compare the JSON edge inventory against every typed relationship in this register; retain a review record for any intentional mismatch.


## Register-to-graph reconciliation — 2026-10-22

A comparison script fetched both this register and `dependency-package-graph.json`, matched every internal package-import row whose source and target are among the 33 Aether nodes, and compared the resulting edge set. **Result: 61 internal package-import rows, 61 JSON edges, no duplicates, no missing edges, and no extra edges.** Five package-import rows target external backends/libraries or generic test fixtures and are intentionally excluded from the internal 33-repository graph. The JSON graph was then fetched again and cycle detection rerun: **0 cycles reported**.

This establishes consistency between the current human-authored register and the candidate JSON edge set, not consistency with source code. Both remain proposed architecture artifacts.
