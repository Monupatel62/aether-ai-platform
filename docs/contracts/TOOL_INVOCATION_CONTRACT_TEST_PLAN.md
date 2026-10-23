# Tool Invocation Contract Test Plan — Draft

**Status:** Proposed acceptance criteria only. No validator or runtime tests have been run.  
**Scope:** `docs/contracts/tool-invocation.schema.json` and the server-side execution boundary.  
**Approval:** Not approved for production implementation.

## Contract rule

The invocation envelope is an untrusted request, not an authorization grant. Fields such as `requested_by`, `tenant_id`, `resource_refs`, and `approval_ref` are selectors or claims until the server resolves them against authenticated identity, canonical tenant membership, registered tool metadata, authoritative resource state, and a trusted approval record.

Before executing a tool, the server must validate the registered tool-version input schema, establish the effective principal and tenant from trusted sources, resolve the exact resource/action set, evaluate current policy, validate any required approval against the exact action and argument fingerprint, and enforce idempotency. If required authority, approval, schema, or resource state cannot be established, execution must fail closed.

## Schema-level positive and negative cases

| ID | Input | Expected result |
|---|---|---|
| TINV-001 | Valid envelope with all required fields and a valid date-time | Schema accepts; this does not authorize execution |
| TINV-002 | Missing `invocation_id`, `tool_id`, `arguments`, `requested_by`, or `idempotency_key` | Reject |
| TINV-003 | Unknown top-level property | Reject |
| TINV-004 | `arguments` with more than 100 direct properties | Reject |
| TINV-005 | `resource_refs` with more than 100 entries | Reject |
| TINV-006 | Resource reference missing `resource_type`, `resource_id`, or `action` | Reject |
| TINV-007 | Resource reference contains an unknown property | Reject |
| TINV-008 | Malformed `requested_at` timestamp with format assertions enabled | Reject |
| TINV-009 | Nested argument exceeds configured transport byte or parser-depth limits | Reject before tool execution |
| TINV-010 | Arguments do not conform to the registered schema for the exact `tool_id` + `tool_version` | Reject before tool execution |

## Execution-boundary security cases

| ID | Scenario | Expected result |
|---|---|---|
| TINV-011 | Caller forges `requested_by` to another principal | Ignore as authority; bind authenticated principal or reject mismatch |
| TINV-012 | Caller supplies another tenant's `tenant_id` | Resolve membership server-side; deny if not authorized |
| TINV-013 | Resource ID belongs to another tenant or is not visible to caller | Deny without leaking protected resource details |
| TINV-014 | High-risk tool requires approval but `approval_ref` is absent | Deny; do not execute |
| TINV-015 | Approval is expired, revoked, already consumed, or belongs to another principal/tenant | Deny |
| TINV-016 | Approval matches a different tool, tool version, action, resource, or canonical argument fingerprint | Deny |
| TINV-017 | Resource ACL, membership, tool policy, or resource version changes after enqueue and before execution | Re-authorize against current authority; deny or require fresh approval |
| TINV-018 | Authorization or approval service is unavailable or returns an indeterminate result | Fail closed |
| TINV-019 | Same idempotency key is replayed with the same canonical request fingerprint | Return the recorded outcome or safe in-progress status; do not repeat side effects |
| TINV-020 | Same idempotency key is reused with a different fingerprint | Reject conflict; do not execute |
| TINV-021 | Tool output or arguments contain secrets | Apply data-minimization/redaction policy to logs, traces and user-visible errors |
| TINV-022 | Tool attempts an action outside its declared scope or approved resource/action set | Deny at the execution boundary |

## Required binding for approvals

The eventual approval contract should bind, at minimum, the approval ID to the authenticated requester or approved delegate, tenant, tool ID and version, action, resource references, canonical argument fingerprint, policy/risk version, expiry, and single-use or replay semantics. The exact approval authority, signature/integrity mechanism, fingerprint canonicalization, and consumption transaction remain architecture decisions; this plan does not choose them.

## Limits and implementation evidence

- The schema's `maxProperties: 100` is not a byte-size, nesting-depth, execution-time, or output-size limit.
- Per-tool input schemas must reject unknown fields unless a specific versioned contract explicitly allows them.
- Resource references in the request do not prove resource ownership or permission.
- Schema validation cannot establish identity, approval authenticity, current membership, or authorization.
- Execution must re-check policy immediately before side effects and must use idempotency/reconciliation for non-transactional external actions.
- The test runner must report each fixture's actual validator/runtime result; do not mark a case passed from manual inspection alone.

## Exit criteria

1. Product/security owners approve risk tiers and which tools require approval.
2. Owners decide the authoritative sources for membership, resource ACL/version, tool registration/version and approval records.
3. The contract uses a selected Draft 2020-12 validator with `format` assertions; schema cases execute in CI.
4. Execution-boundary cases run against a non-production test harness with synthetic tenants and tools.
5. Negative cases prove there are no side effects on deny, timeout, stale approval, invalid schema, or idempotency conflict.
6. Findings and test evidence are recorded in the master work log and cross-repository contract audit.

Until these criteria are accepted and evidenced, this remains a proposed plan and the Phase 0 implementation gate stays open.
