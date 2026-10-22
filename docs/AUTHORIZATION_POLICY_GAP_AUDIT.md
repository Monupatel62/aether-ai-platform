# Authorization Policy Gap Audit

**Review date:** 2026-10-22  
**Status:** Documentation audit; proposed corrections require product-owner review.  
**Scope:** Semantic consistency of `AUTHORIZATION_PERMISSION_MATRIX.md` and its relationship to tenant/ACL consistency, identity, data lifecycle, and repository boundaries.  
**Implementation status:** No code or tests were run.

## 1. Executive result

The authorization matrix is a useful deny-by-default baseline, but it is not yet ready to be treated as an implementation contract. Several rows are ambiguous or internally inconsistent, and multiple high-risk product policies remain undecided. This audit distinguishes clear document defects from choices that require product-owner approval.

## Follow-up contract artifact — 2026-10-22

Added [Tenant Context Resolution Contract](contracts/TENANT_CONTEXT_RESOLUTION_CONTRACT.md) to translate the audit's tenant authority, stale membership/ACL, and fail-closed concerns into a reviewable request-processing sequence and 12 proposed acceptance cases. This does not resolve the canonical membership-owner decision, approve cache/revocation thresholds, or demonstrate runtime enforcement. No implementation or tests were run.

## 2. Findings

| ID | Severity | Finding | Why it matters | Proposed disposition |
|---|---|---|---|---|
| AUTH-GAP-01 | High | Workspace creation row grants Member `A**`, while its footnote says creation should default to denied until tenant policy enables it. | Readers or implementers may treat the table cell as permission to create by default. | Change the cell to “Configurable; default deny” and define who can enable it. |
| AUTH-GAP-02 | High | Support Operator is defined as a principal, but the role matrix has no Support Operator column. The support-content row instead grants conditional access to Platform Operator. | Support access may be accidentally inherited by all platform operators, or the separate support identity may be ignored. | Model support as a distinct, separately authorized identity/workflow; default deny; ticket/reason, approval, expiry, least scope and immutable audit. Confirm emergency-access design. |
| AUTH-GAP-03 | High | “Read/run own conversations” gives Owner and Tenant Admin `A`, but the word “own” conflicts with broad tenant-wide access implied by `A`. AI memory has similar ambiguity. | Conversation and memory contents can be sensitive; tenant administration must not silently mean content surveillance. | Decide whether admins can read only metadata, their own content, explicitly shared content, or all tenant content through an approved exceptional workflow. Default to no implicit content access. |
| AUTH-GAP-04 | High | Role/ownership changes use `A*` for Owner and `J` for Admin, but the matrix does not define the grant ceiling, dual control, last-owner protection or exact ownership-transfer workflow. | Role escalation, lockout, or self-promotion risks. | Define explicit grant-ceiling rules; forbid self-elevation; require re-authentication and audit for ownership transfer; decide whether dual approval is needed. |
| AUTH-GAP-05 | High | “Access assigned files” and “Access AI memory” compress read, write, share, delete, execute and export into one cell. | Least privilege cannot be reliably implemented from a broad “access” permission. | Split by action for first-launch resource classes; use a common action vocabulary and explicit resource-scoped grants. |
| AUTH-GAP-06 | High | Export, destructive actions, bulk operations and support access refer to approval/step-up, but no common risk tiers, approval authority, expiry, or failed-approval semantics are defined. | High-impact actions could receive inconsistent safeguards across repositories. | Define action risk tiers and policy obligations in ADR-0020/0023; fail closed when required approval or step-up is missing. |
| AUTH-GAP-07 | High | Membership revocation and resource ACL revocation are described across several domains, but the canonical membership owner remains open and the policy matrix does not define a version/conflict model. | Consumers may make decisions from stale or conflicting membership and ACL state. | Resolve ADR-0021; version membership/ACL state; require current authorization for protected operations. Follow the separate consistency decision. |
| AUTH-GAP-08 | Medium | Service-principal permissions mix tenant-wide, resource-granted and credential-rotation concepts; expiry, audience, owner, scope, rotation and revocation are not uniformly mandatory in the matrix. | Workload credentials may gain excessive scope or persist after the owner/resource is removed. | Resolve ADR-0022; define a standard workload-identity record and minimum lifetime, audience, scope, rotation, owner and audit requirements. |
| AUTH-GAP-09 | Medium | Billing permissions group usage viewing, invoice viewing, plan changes, payment method changes, refunds, credits and spending limits. The detail notes recognize these should be separate, but the matrix does not encode that separation. | A role may see financial data or change spending when it only needs usage visibility. | Split billing permissions by action and sensitive data category before billing implementation. |
| AUTH-GAP-10 | Medium | The matrix states policy-service failure must fail closed, but does not distinguish protected data/actions from availability-safe public operations or define user-visible error and retry behavior. | Teams may either fail open unsafely or make unrelated low-risk functions unavailable. | Define protected operation categories, safe denial/error behavior, timeout budget, audit event and retry policy. |
| AUTH-GAP-11 | Medium | “Audit events for privileged action/denial” does not define which denied attempts are recorded, retention, tamper resistance, tenant visibility or separation of security events from product analytics. | Inconsistent detection and possible sensitive-data exposure through logs. | Resolve retention/telemetry ADRs; define mandatory event fields, access controls, redaction, retention and export scope. |
| AUTH-GAP-12 | Medium | Resource Manager `G` and service-principal `G` mean “granted/assigned resources,” but no common grant representation or rule for inheritance, sharing, delegation and revocation is specified. | Two repositories may interpret the same grant differently. | Define a versioned grant contract with subject, resource, actions, tenant, issuer, expiry, delegation ceiling and revocation/version state. |
| AUTH-GAP-13 | Medium | Tenant Admin access to provider/model policy, tenant keys, usage, audit and resource content is not consistently distinguished between configuration, metadata and secret/content access. | Admin rights may be interpreted more broadly than intended. | Split configure/read-secret/read-content/manage-grant actions and explicitly deny raw secrets. |
| AUTH-GAP-14 | Medium | The table does not explicitly cover tenant suspension, workspace suspension, legal hold, retention expiry or deleted-resource restoration, although related docs mention them. | A deleted or suspended resource may remain available through queues, caches, indexes, exports or restoration. | Define lifecycle states and ensure authorization checks include resource state; keep retention/legal hold separate from access revocation. |

## 3. Proposed baseline clarifications

These are recommendations for review, not accepted policy:

1. **Deny by default:** every unlisted action is denied. “Configurable” permissions remain denied until an authorized tenant policy explicitly enables them.
2. **Separate identity from content access:** tenant administration, platform operations, and customer-content access are different grants.
3. **Use action-level permissions:** read, list/search, create, update, delete, share/invite, execute, configure, approve and export are distinct.
4. **No self-elevation:** a principal cannot grant itself a role or permission it does not already have authority to delegate; protect last-owner and ownership-transfer flows.
5. **Re-authorize at execution time:** delayed jobs, tool calls, streaming, retrieval and exports check current membership, resource state and policy before protected work.
6. **No stale projection as authority:** caches/indexes can accelerate filtering but cannot grant access. Revocation denies protected access before asynchronous cleanup finishes.
7. **Fail closed for protected operations:** if authorization or required approval cannot be established, do not return protected data or perform the action.
8. **Separate policy from commercial entitlement:** a paid plan may permit a feature, but does not authorize access to another user's resource.
9. **Auditable high-risk actions:** ownership transfer, privilege changes, bulk export, destructive operations and exceptional support access need explicit policy, step-up/approval where chosen, and redacted audit.
10. **Do not imply tests passed:** the matrix is a plan only; every invariant needs automated positive and negative tests in a later approved implementation phase.

## 4. Decisions required from product owner

Before this matrix can become an implementation contract, decide:

- First-launch roles and whether “Owner,” “Tenant Admin,” “Member,” “Viewer,” and “Resource Manager” are all needed.
- Whether tenant admins can read conversation or memory content; proposed safe default is no implicit access.
- Whether member workspace creation is allowed by tenant policy; default proposed as deny.
- Which roles can invite/remove users, assign roles, manage API keys, configure providers, view audit, export data and manage billing.
- Whether support access exists at launch; if yes, approval model, ticket/reason, scope, expiry, emergency process and audit retention.
- Ownership transfer and last-owner rules, including whether dual approval is required.
- Workload identity/API-key scope, expiry and rotation.
- Data categories, retention, deletion, export and legal-hold rules.
- Risk tiers, step-up authentication, approval requirements and numeric session/revocation targets.
- Tenant isolation/RLS rollout and the failure behavior when policy dependencies are unavailable.

## 5. Related open decisions

- ADR-0012: prompt/file/memory retention and telemetry policy.
- ADR-0015: GenAI observability and privacy.
- ADR-0020: authorization model and policy engine scope.
- ADR-0021: tenant/workspace hierarchy and support access.
- ADR-0022: API-key and workload identity.
- ADR-0023: MFA, recovery, session and revocation targets.
- ADR-0024: tenant isolation and RLS rollout.
- ADR-0008 / ADR-0019: identity provider and browser session model.

## 6. Next gate

1. Review the high-severity findings and explicitly accept/reject the proposed clarifications.
2. Correct the permission matrix and update repository contracts only after the policy decisions are approved.
3. Finalize data retention/deletion and audit policy.
4. Convert each accepted rule into policy contract cases and negative tests.
5. Run the identity/authorization POC only after explicit approval.

No application code, tests, identity-provider selection, or repository creation was performed during this audit.
