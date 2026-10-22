# Engineering and Code-Commenting Standard

**Applies to:** all 33 Aether AI repositories and any later Aether integration code. This is a documentation standard; it does not authorize implementation by itself.

## Comments should explain why

Comments must explain intent, invariants, constraints, security decisions, non-obvious tradeoffs, or why a seemingly simpler alternative is unsafe. Do not narrate obvious syntax line by line.

### Required comment/docstring locations

- Public package exports and public API functions: document purpose, inputs, outputs, errors, side effects, cancellation, and compatibility expectations.
- Security-sensitive code: explain the trust boundary, authorization assumption, validation, redaction, and why a control is required.
- Retry/cancellation/idempotency code: document what is safe to retry, what side effects may have happened, and how duplicates are prevented.
- State machines and concurrency code: document valid transitions, invariants, ownership/lease rules, and recovery behavior.
- Provider/MCP/integration adapters: document upstream quirks, capability differences, timeouts, and how errors are normalized.
- Data migrations: document purpose, compatibility window, backfill, rollback limits, and retention implications.
- Non-obvious configuration: explain safe defaults and operational consequences.

## Example

Good:

```ts
// Do not retry this tool call unless its idempotency key is preserved:
// the remote action may have succeeded even if the response was lost.
await invokeRemoteAction(request, { idempotencyKey });
```

Avoid:

```ts
// Call the function.
await invokeRemoteAction(request);
```

These are illustrative examples only; no application code is being added in the documentation phase.

## TODO and FIXME policy

- Every TODO/FIXME must explain what is missing and, once issue tracking exists, include a ticket/issue link.
- Never leave TODOs for security controls, authorization checks, tenant isolation, secret handling, or validation in a release path.
- Temporary compatibility code must include removal criteria and an owner.

## Cross-repository connection comments

When code calls another Aether component, docs/comments should identify the public contract or package boundary used, not merely the target repository name. The canonical dependency graph lives in [REPOSITORY_CATALOG.md](REPOSITORY_CATALOG.md). Update it when a dependency edge changes.

## Documentation update rule

A change to API shape, events, state transitions, permissions, data retention, configuration, or deployment behavior must update the corresponding specification, contract, test plan, and work log in the same change.

## Code review checklist

- [ ] Does the code respect the repository's ownership boundary?
- [ ] Are public interfaces and error cases documented?
- [ ] Do comments explain why rather than restate what?
- [ ] Are security/permission checks explicit and tested?
- [ ] Are retries, timeouts, cancellation, and idempotency safe?
- [ ] Are logs redacted and correlated?
- [ ] Are dependencies/licenses and cross-repo contracts updated?
- [ ] Do tests prove behavior, including failure paths?
