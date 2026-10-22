# Aether AI Gateway Architecture Evaluation

**Status:** Exploratory design note; no external gateway has been accepted as a dependency.

## Goal

Choose a gateway implementation strategy for Aether AI while keeping Aether-owned contracts, authorization, tenant isolation, quotas, observability, and provider compatibility tests authoritative.

## Options

### Option A — Native Aether gateway

Implement the gateway contract within Aether AI using the chosen runtime and provider adapters. This keeps behavior and release ownership within the project, but requires Aether to implement and test streaming, timeouts, retries, cancellation, normalized errors, usage reporting, and provider capabilities.

### Option B — Optional external gateway adapter

A future architecture decision may evaluate an external gateway such as AI DIAL Core behind an Aether-owned adapter. This is not a current dependency or commitment. Any evaluation must cover deployment, authentication, tenant policy, provider coverage, failure semantics, license, security, and operational cost.

## Decision gates

1. Define the Aether gateway contract and conformance tests first.
2. Build a small native proof of concept with mock provider responses.
3. Evaluate external options only if a concrete requirement justifies them.
4. Do not add an external runtime until compatibility, security, licensing, and operational ownership are reviewed and explicitly approved.

## Required evidence

- Versioned provider capability schema and normalized error mapping.
- Streaming frame, cancellation, timeout, retry, and fallback tests.
- Tenant authorization and quota enforcement tests.
- Load, latency, cost, and operational complexity comparison.
- Explicit decision record before accepting any external dependency.
