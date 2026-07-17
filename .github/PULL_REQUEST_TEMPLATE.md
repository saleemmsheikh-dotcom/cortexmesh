## Summary

Describe the problem, the bounded change, and the outcome.

## Scope

- Files or components changed:
- Explicitly out of scope:
- Related issue or evidence:

## Boundary Impact

Mark each item and explain every non-`None` answer.

| Boundary | Impact |
| --- | --- |
| Runtime | None / Describe |
| Reference orchestration | None / Describe |
| Local AI | None / Describe |
| Provider layer | None / Describe |
| Validation or replay | None / Describe |
| Research evidence | None / Describe |
| Governance | None / Describe |
| LOCKED components | None / Describe |

## Verification

List exact commands and results.

```text
Focused tests:
Full regression:
git diff --check:
```

## Evidence Integrity

- [ ] I did not overwrite sealed, certified, published, or historical evidence.
- [ ] Generated artifacts are identified and reproducible.
- [ ] Minority evidence, unresolved divergence, failures, and limitations remain visible.
- [ ] Expected outcomes were not changed after observing results without an explicit version or deviation record.

## Contribution Checks

- [ ] The change is focused and contains no unrelated modifications.
- [ ] Documentation and tests are updated in proportion to risk.
- [ ] No secrets, credentials, personal data, or sensitive vulnerability details are included.
- [ ] I have read `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.
- [ ] I have the right to submit this contribution under Apache-2.0.

## Risks and Rollback

Describe remaining risks, limitations, and rollback. Write `Not applicable` only when genuinely unnecessary.

## Authority

Pull-request approval does not itself supersede GG-02, authorize protected implementation, certify results, or permit LOCKED-component modification.
