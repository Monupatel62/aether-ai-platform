# Event Envelope and Resource Revocation Test Plan — Draft

**Status:** Proposed contract and consumer acceptance criteria only. No validator or runtime tests have been run.  
**Scope:** `event-envelope.schema.json`, `resource-change-event.schema.json`, and consumers that update ACL, lifecycle, cache, search, retrieval, and queued-work projections.  
**Approval:** Not approved for production implementation.

## Trust boundary

An event envelope is untrusted input until the transport authenticates the producer and the consumer verifies that the producer is authorized to emit that event type for the named aggregate/tenant. `producer`, `tenant_id`, `principal_id`, `aggregate`, timestamps, and payload fields are claims, not proof of identity, ownership, authorization, or freshness.

Consumers must validate the envelope and event-type-specific payload schema, authenticate the producer through an approved service-to-service mechanism, deduplicate delivery, and apply state transitions only when event identity and version semantics pass. An event is a notification, not the authoritative source for current membership or ACL decisions.

## Envelope contract cases

| ID | Scenario | Expected result |
|---|---|---|
| EVT-001 | Valid envelope from an authenticated, authorized producer and registered event type | Accept for event-specific validation and policy checks |
| EVT-002 | Missing required envelope field or unknown top-level property | Reject |
| EVT-003 | Invalid `occurred_at` timestamp with format assertions enabled | Reject |
| EVT-004 | Payload violates the registered schema for `event_type` | Reject before consumer side effects |
| EVT-005 | Payload exceeds the schema property limit or transport byte/depth limit | Reject before side effects |
| EVT-006 | `producer` string is syntactically valid but producer authentication fails | Reject; never trust the string as identity |
| EVT-007 | Authenticated producer is not authorized to publish the event type or tenant/aggregate | Reject and emit safe security telemetry |
| EVT-008 | Client-supplied tenant/principal fields disagree with trusted event context | Reject or quarantine according to the approved policy; never grant access from payload claims |
| EVT-009 | Duplicate `event_id` delivery | Deduplicate; do not repeat side effects |
| EVT-010 | Event arrives with an older aggregate version than already applied | Ignore/reject as stale without rolling state back |
| EVT-011 | Same aggregate version arrives with conflicting payload/change identity | Treat as integrity/consistency conflict; do not silently overwrite |
| EVT-012 | Event arrives out of order with a version gap | Fetch/reconcile authoritative state or defer safely; do not infer missing changes |
| EVT-013 | Replay occurs outside the configured deduplication window | Apply approved replay controls and authoritative version checks; do not rely on the window alone |

## Resource-change and revocation cases

| ID | Scenario | Expected result |
|---|---|---|
| REV-001 | `resource.acl_changed` omits `acl_version` | Reject |
| REV-002 | `resource.access_revoked` omits `acl_version` | Reject |
| REV-003 | ACL version is lower than the authoritative or already applied version | Reject/ignore as stale; never restore prior access |
| REV-004 | ACL version skips a version or conflicts with the same version | Reconcile authoritative ACL state before applying the projection |
| REV-005 | Event says `resource.deletion_requested` | Record lifecycle request only; do not claim deletion completed |
| REV-006 | Event says `resource.deleted` but authoritative lifecycle state disagrees | Keep protected reads denied when current policy/lifecycle requires; reconcile authoritative state |
| REV-007 | Restore event arrives for a resource still deleted, suspended, or under legal hold | Do not restore access until authoritative lifecycle and policy checks permit it |
| REV-008 | Revocation event is delayed while a cached/search/vector result still exists | Protected read/search/retrieval must re-check current authorization and deny before returning content |
| REV-009 | Queued tool/agent job was authorized before ACL revocation but executes afterward | Re-authorize at execution time; deny or require fresh approval |
| REV-010 | Event consumer or authorization source is unavailable | Do not fail open; protected operations remain denied when current authorization cannot be established |
| REV-011 | Event has no `tenant_id` or `changed_by` | Apply the event-specific required-field policy; preserve authenticated producer identity in audit rather than inferring an actor |
| REV-012 | Event is syntactically valid but `change_id` is replayed with different content | Reject as an integrity conflict and alert through safe telemetry |

## Event-specific required-field decision table

The current resource-change schema only conditionally requires `acl_version` for ACL changes and access revocation. Before implementation, the contract owner must explicitly decide required tenant and actor/audit fields for each event type. At minimum:

- ACL changes and access revocation require an authoritative tenant/resource binding, monotonic ACL version, unique change identity, and authenticated actor or a clearly defined system actor.
- Deletion/restoration events require an authoritative lifecycle version/state and must distinguish requested, completed, and restored transitions.
- The producer's authenticated identity and authorization to publish must be recorded independently of self-asserted event fields.
- The exact fields, migration rules, and compatibility strategy must be approved before adding conditional schema requirements; this plan does not silently decide them.

## Consumer invariants

1. Current authorization state is authoritative; event payloads and cache/search/RAG projections cannot grant access.
2. Revocation must block protected reads and side effects at the authorization boundary before asynchronous cleanup completes.
3. Consumers must be idempotent and version-aware; duplicate or out-of-order delivery cannot restore stale access.
4. A lifecycle notification does not itself prove a transition completed unless authoritative state and the event contract say so.
5. Producer authentication, event-type authorization, tenant/aggregate binding, and replay handling are enforced outside JSON Schema.
6. Audit/telemetry excludes tokens, secrets, raw sensitive payloads, and unnecessary user content.

## Exit criteria

1. Owners approve producer authentication, event-type authorization, tenant/actor requirements, version ordering, deduplication, replay, and lifecycle transition semantics.
2. JSON Schema Draft 2020-12 validation runs with format assertions and positive/negative fixtures execute in CI.
3. Synthetic multi-tenant consumer tests prove stale, duplicate, forged, out-of-order, and conflicting events do not grant access or repeat side effects.
4. Revocation tests cover API reads, list/search, vector retrieval, caches, queued jobs, tool execution, and result retrieval.
5. Failure tests prove authorization or event-processing outages cannot turn stale projections into permission.
6. Results and unresolved decisions are recorded in the cross-repository audit and work log.

Until these criteria are accepted and evidenced, this remains a proposed plan; no runtime enforcement or implementation approval is implied.
