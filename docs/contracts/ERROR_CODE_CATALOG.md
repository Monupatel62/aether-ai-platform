# Public Error Code Catalog — Draft

**Status:** Draft proposal only. Codes are not approved, implemented, or guaranteed to be returned by any running service.

## Contract rules

- The envelope shape is defined in error.schema.json.
- Codes are stable machine-readable identifiers; clients must not branch on human-readable message text.
- Messages must be safe for the caller and must not expose stack traces, provider payloads, SQL, filesystem paths, credentials, or internal topology.
- HTTP status, retryability, and code must agree. A retryable error is not permission to retry a non-idempotent side effect without an idempotency key.
- Do not reveal whether another tenant's resource exists. Use the same externally visible response for unauthorized and non-existent resources where enumeration risk exists.
- Unknown codes must be handled as a generic failure by clients.
- Request IDs are correlation identifiers, not credentials. Never place secrets or personal data in them.

## Proposed code registry

| Code | Intended meaning | Suggested HTTP status | Retryable | Notes |
|---|---|---:|---|---|
| INVALID_ARGUMENT | Request fields or values are invalid | 400 | No | Field-level safe details may be included |
| UNAUTHENTICATED | Authentication is absent, invalid, or expired | 401 | No | Do not include credential validation details |
| PERMISSION_DENIED | Caller is not authorized for the action | 403 | No | Avoid cross-tenant existence leaks |
| RESOURCE_NOT_FOUND | Resource is absent or intentionally concealed | 404 | No | May also represent concealed unauthorized resources |
| CONFLICT | Request conflicts with current state or version | 409 | No | Client may need to refresh state |
| PRECONDITION_FAILED | Required precondition or version check failed | 412 | No | Include safe version hints only if policy permits |
| RATE_LIMITED | Caller or tenant exceeded a rate limit | 429 | Yes | Include Retry-After at HTTP layer when known |
| QUOTA_EXCEEDED | Entitlement or usage quota prevents operation | 429 | No | Retry only after quota/entitlement changes |
| PAYLOAD_TOO_LARGE | Request exceeds a documented size limit | 413 | No | Do not echo the submitted payload |
| UNSUPPORTED_MEDIA_TYPE | Content type or encoding is unsupported | 415 | No | |
| DEPENDENCY_UNAVAILABLE | Required internal or external dependency is unavailable | 503 | Yes | Do not disclose dependency hostnames or raw upstream response |
| DEPENDENCY_TIMEOUT | A dependency did not respond within the deadline | 504 | Yes | Retry within a bounded deadline and only when safe |
| TEMPORARY_UNAVAILABLE | Service cannot currently complete the request | 503 | Yes | Use when a more specific safe code is not appropriate |
| IDEMPOTENCY_KEY_REUSED | Key was reused with a different request fingerprint | 409 | No | Never execute the second differing request |
| APPROVAL_REQUIRED | Action requires approval before execution | 403 | No | A supplied approval reference must be verified |
| APPROVAL_INVALID | Approval is missing, expired, revoked, or not bound to this action | 403 | No | Avoid disclosing approval internals |
| RUN_NOT_CANCELLABLE | Run is in a state that cannot be cancelled | 409 | No | State-specific behavior must be documented |
| RUN_FAILED | A durable run failed with a safe public failure summary | 500 | No | Internal cause belongs in access-controlled telemetry |
| INTERNAL_ERROR | Unexpected failure without a safer public classification | 500 | No | Generic message; log with request ID after redaction |

## Decisions still required

1. Confirm whether HTTP status mapping is uniform across API and gateway boundaries.
2. Decide whether quota exhaustion is 429 or 403 for entitlement-denied cases.
3. Define whether details.field uses JSON Pointer, dotted paths, or a constrained field-name vocabulary.
4. Decide if retry delay metadata belongs in the envelope or only standard HTTP headers.
5. Add owners, deprecation rules, and compatibility tests before treating this registry as stable.

## Acceptance gate

Before approval, compare every code with endpoint semantics, authorization concealment policy, retry/idempotency behavior, observability redaction, and generated client behavior. No service should emit these codes solely because this draft exists.
