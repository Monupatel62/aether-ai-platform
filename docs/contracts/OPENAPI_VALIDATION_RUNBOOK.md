# OpenAPI 3.1 Validation Runbook

**Status:** Validation tooling proposal; passing structural validation does not approve this draft API for implementation.

## Run locally

From the repository root:

```sh
python -m pip install -r requirements-openapi-validation.txt
python scripts/validate_openapi.py
```

The validator requires the contract at `docs/contracts/openapi.v1.yaml` to declare OpenAPI `3.1.0` and checks it with `openapi-spec-validator`. The GitHub Actions workflow runs on relevant pull requests, pushes to the validation branch, and manual dispatch. Workflow actions are pinned to full commit SHAs.

## Acceptance criteria

- The YAML document loads as an object.
- The declared version is exactly OpenAPI 3.1.0.
- The OpenAPI validator exits successfully, including structural and reference validation supported by the selected validator.
- Invalid syntax, unresolved references, or invalid OpenAPI structures cause a non-zero exit.
- The workflow has read-only repository permissions.

## Limits

A passing result does not establish that endpoints are implemented, that security controls work at runtime, that authorization is correct, or that product decisions are approved. It does not replace semantic review, security tests, or contract tests against a running service.

The specification is explicitly a draft and retains unresolved authentication, tenant membership, streaming, limits, and endpoint semantics. ADR-0021 remains an owner decision.
