# Data Retention, Deletion, Export and Telemetry Policy Proposal

**Research date:** 2026-10-22  
**Status:** Proposed baseline for product, privacy and legal review; no retention duration approved.  
**Phase:** Documentation/research only. No implementation or compliance certification.

## 1. Purpose and decision boundary

Every persisted data category must have a documented purpose, owner, tenant boundary, retention trigger, deletion behavior, export path, telemetry treatment and legal-hold exception before that category is implemented. This proposal establishes safe defaults and open decisions; it does not choose numeric retention periods or claim legal compliance.

Related decisions: ADR-0012 (retention/export/deletion/telemetry), ADR-0015 (observability/privacy), ADR-0021 (tenant hierarchy/support), ADR-0024 (tenant isolation/RLS), and the authorization policy gap audit.

## 2. Proposed default principles

1. **Minimize collection:** do not collect or persist data without a product purpose and owner.
2. **Default off for sensitive telemetry:** raw prompts, completions, retrieved passages, uploaded content, secrets and recovery material are not captured in ordinary logs/traces.
3. **Separate operational metadata from content:** use run IDs, event types, timing, token/cost counts, model/provider identifiers and stable error categories where possible; avoid content fields.
4. **Tenant scope everywhere:** persisted rows, object storage, caches, queues, traces, exports, indexes and backups need explicit tenant/data classification and access boundaries.
5. **Revocation is immediate; physical cleanup may be asynchronous:** deny access first, then remove or tombstone projections and storage according to the approved lifecycle policy.
6. **Delete from derived systems:** deletion/revocation workflows include chunks, embeddings, caches, search indexes, citations, queued jobs and materialized exports—not only the primary record.
7. **Backups need a documented expiry path:** deleted records may persist in immutable backups until expiry; restrict backup access and prevent restoration from silently reintroducing deleted data into active service.
8. **Legal hold is explicit and narrow:** a hold can delay physical destruction only under approved authority; it does not automatically grant ordinary product users access.
9. **Export is authorized and auditable:** verify requester scope, exclude secrets and other tenants' data, and apply expiry/access controls to generated export artifacts.
10. **No unsupported promises:** do not publish a numeric deletion SLA, retention period, residency claim or compliance claim until approved and tested.

## 3. Data inventory and proposed baseline

| Data category | Suggested owner | Proposed default | Deletion/export considerations |
|---|---|---|---|
| Account identity and profile | Auth/identity domain | Keep only attributes needed for account lifecycle; minimize provider claims | Account deletion must address mapping records, active sessions and recovery artifacts |
| Tenant/workspace/membership and role grants | Membership owner TBD | Keep authoritative lifecycle and audit state only as required | Removing a member revokes access immediately; retained audit records must not restore membership |
| Sessions, refresh tokens, API keys and workload credentials | Auth/security boundary | Never log raw secrets; store credentials securely or verifiers where appropriate; expiry/revocation required | Revoke before cleanup; never include secret values in exports |
| Conversations, prompts and completions | Conversation/run owner TBD | Content persistence should be an explicit feature with user-visible retention controls; avoid raw content in telemetry | User/tenant deletion, export, legal hold and derived-memory behavior must be specified |
| Uploaded files and extracted text | Files domain | Store only while needed for the feature and approved retention policy | Include object bytes, extracted text, temporary files, malware-scan artifacts and signed URLs |
| Knowledge sources, chunks and embeddings | Knowledge domain; RAG/Search are projections | Track source/version/ACL/deletion state; avoid orphaned derived content | Tombstone and deny access first; remove chunks/embeddings/indexes asynchronously and measure convergence |
| Agent runs, tool inputs/outputs and workflow state | Orchestration domain | Persist minimum required for recovery, safety, audit and user history | Separate durable execution state from optional full tool payload retention |
| Memory/profile summaries | Memory domain when created | Explicit opt-in/product behavior and scope; do not assume every chat becomes persistent memory | Provide deletion/update behavior for derived summaries and linked source records |
| Audit/security events | Security/observability domain | Record security-relevant metadata, not secrets or raw content by default | Define immutable/tamper-resistant handling, access policy, export and retention separately from product history |
| Logs, metrics and traces | Observability | Metadata-first; sensitive capture disabled by default | Redact at source; apply retention, tenant isolation, access controls and sampling rules |
| Usage/billing ledger and invoices | Billing domain | Preserve only required financial/operational records under approved policy | Product deletion does not necessarily imply ledger destruction; legal/accounting obligations need review |
| Evaluations and test datasets | Evaluations/testing | Synthetic or sanitized data by default | Real user content requires documented purpose, consent/authority, access controls and retention |
| Exports and generated reports | Resource owner plus export workflow | Time-limited artifacts; minimal content; restricted download access | Expire/revoke download access, clean temporary files and avoid long-lived public URLs |
| Backups and snapshots | Infrastructure/database owner | Encrypted, access-restricted, documented expiry and restore process | Define backup expiry, restore-time deletion replay/reconciliation and legal hold behavior |

Ownership names above are candidates aligned with current repository boundaries, not confirmation that the corresponding features or services are implemented.

## 4. Lifecycle contract

### 4.1 Delete and revoke are different
- **Revoke access:** changes authorization state so protected reads/actions are denied on the next required authoritative check.
- **Logical deletion/tombstone:** marks a source/resource as deleted so consumers suppress it even while cleanup is pending.
- **Physical deletion:** removes bytes/rows/index entries when allowed by retention, backup and legal-hold rules.
- **Retention expiry:** scheduled lifecycle action that applies the approved policy to eligible data.
- **Account/tenant closure:** orchestrated workflow spanning all owned categories, not a single-row delete.

The product must define which action is exposed to users and the expected behavior for each resource category.

### 4.2 Asynchronous derived data
Deletion/revocation events should include stable IDs, source/document version, tenant, event ID, lifecycle state, policy/ACL version and correlation ID. Consumers must be idempotent, handle duplicates/out-of-order delivery, and reconcile against authoritative source state. Event delivery is not the sole security control.

Search/RAG must not return protected snippets, derived content or citations after authoritative authorization denies access, even if physical index cleanup has not completed.

### 4.3 Backups and restoration
A restore must not silently resurrect deleted or revoked resources. Define a post-restore reconciliation process that replays tombstones or compares restored state with authoritative deletion records before restored data is exposed. Backup retention and restore access must be restricted and audited.

### 4.4 Legal hold and exceptional retention
Legal hold must have a documented basis, authorized approver, scope, start/end or review date, audit trail and release process. A hold must not grant extra read access to product users or support operators. Legal and jurisdictional review is required before defining implementation behavior.

## 5. Export contract

Before export is implemented, define:
- eligible roles and the exact data categories each can export;
- tenant/resource authorization and step-up/approval requirements for bulk or sensitive exports;
- formats, size limits, rate limits and partial-failure semantics;
- treatment of other users' content, shared resources, secrets, provider credentials, audit records and billing data;
- generated artifact encryption/access scope, expiry, download audit and deletion;
- notification and recovery behavior when export fails or is cancelled.

Do not export raw API keys, access tokens, session cookies, recovery codes or provider secrets. Exporting metadata about a credential is distinct from exporting its value.

## 6. Telemetry and observability contract

### Default allowed metadata (subject to privacy review)
- correlation/trace/run ID;
- event name and stable error category;
- timestamp and duration;
- service/component and version;
- model/provider identifier and capability;
- token counts, usage and cost estimates when available;
- authorization outcome/reason code in a safe, non-sensitive form;
- retry, queue, cancellation and dependency-health metadata.

### Default excluded unless separately approved
- raw prompt/completion and retrieved passages;
- uploaded document content or extracted text;
- access tokens, cookies, API keys, provider secrets, recovery codes;
- unnecessary email addresses, personal identifiers or free-form user content;
- unredacted tool arguments/results containing customer data.

Redact at the source before data leaves the process. Downstream redaction alone is insufficient if the original payload has already entered a log/trace. Sensitive capture, if ever needed, requires documented purpose, explicit access controls, sampling, redaction, short approved retention and audit.

## 7. Policy decisions and evidence still required

1. Data residency/jurisdictions and applicable legal/privacy obligations.
2. Numeric retention for each data category, audit/security events, traces, exports and backups.
3. User controls for chat history, memory, files, knowledge collections, run history and account/tenant deletion.
4. Whether prompts/completions are persisted by default, and for which features.
5. Hard-delete versus soft-delete behavior and retention/legal-hold exceptions.
6. Numeric projection-cleanup SLOs for search/RAG/cache/storage, based on workload and tests.
7. Backup/PITR duration, RPO/RTO, restore drills and deletion reconciliation.
8. Export entitlements, formats, size limits and artifact expiry.
9. Telemetry vendor/region, access control, redaction, retention, sampling and incident access.
10. Billing and audit record retention requirements reviewed by qualified legal/accounting owners.
11. How user/tenant deletion interacts with evaluation datasets, model-provider logs and third-party connectors; obtain vendor terms and capabilities rather than assume downstream deletion.
12. Operational owner and alerting for stuck deletion, failed tombstones, orphaned chunks and export cleanup.

## 8. Required acceptance tests

- Deleted or revoked source content is denied immediately by authoritative authorization, even while search/index/cache cleanup is delayed.
- Duplicate, missing and out-of-order lifecycle events converge without resurrecting data.
- A restored backup cannot expose deleted/revoked records before reconciliation.
- Export authorization blocks cross-tenant, out-of-scope and secret-bearing records.
- Expired export links stop working and artifacts are cleaned up according to approved policy.
- Default logs/traces contain no canary secrets, raw prompts, completions or retrieved content.
- Tenant context cannot leak through pooled database connections, queues, caches, object storage or observability.
- Legal hold affects physical deletion only as explicitly approved and audited.
- Failed deletion/export jobs alert an owner and can be safely retried without broadening access.
- Retention jobs are idempotent and do not delete records under a valid hold or outside their authorized tenant scope.

These are planned acceptance tests; none were run in this documentation step.

## 9. Next gate

Product/privacy/legal owners should review this proposal and choose retention, deletion, export and telemetry rules per data category. Then update ADR-0012/0015 and affected repository contracts. Do not claim compliance or implement irreversible deletion behavior until these decisions are approved and tested.

## References
- [Security Threat Model](SECURITY_THREAT_MODEL.md)
- [Data Infrastructure Evaluation](DATA_INFRASTRUCTURE_EVALUATION.md)
- [Tenant Membership and ACL Consistency Decision](TENANT_MEMBERSHIP_AND_ACL_CONSISTENCY_DECISION.md)
- [Authorization Policy Gap Audit](AUTHORIZATION_POLICY_GAP_AUDIT.md)
- [Decision Log](DECISION_LOG.md)
