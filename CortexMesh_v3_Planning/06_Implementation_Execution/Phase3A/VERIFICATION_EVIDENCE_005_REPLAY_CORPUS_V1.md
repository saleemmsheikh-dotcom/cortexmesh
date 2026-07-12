# Verification Evidence 005 - Certified Replay Corpus v1.0

## Evidence ID

VE-005

## Scope

Certification evidence for the first canonical Phase 3A replay dataset.

## Release Statistics

| Field | Value |
| --- | --- |
| Release | v1.0 |
| Corpus version | 1.0.0 |
| Schema version | 1.0 |
| Scenarios | 12 |
| Cases | 24 |
| Comparator coverage | Exact, Compatible, Regression |
| Runtime replay | NOT CERTIFIED |
| Content hash | `91c9b565bdfbf13d655dbe95dc3aa1c6db3666edc90e4bbe9cea6a5237de04d8` |
| Certification status | CERTIFIED |

## Content Coverage

The corpus includes architecture design, implementation planning, refactoring, governance, provider integration, evidence collection, consensus, synthesis, risk assessment, insufficient evidence, conflicting evidence, and edge cases.

All five consensus categories are represented. Cases include metadata, normalized intent, expected capabilities, agent and execution plans, evidence characteristics, consensus category, synthesis characteristics, comparator selection, and validation expectations.

## Integrity Verification

- Scenario and case identifiers are sorted and unique.
- All references resolve.
- All required case fields are populated.
- Schema marker matches the manifest.
- Four payload file hashes recompute.
- Aggregate manifest content hash recomputes.
- Exact, compatible, and regression definitions are certified.
- Future runtime replay is present only as an uncertified reserved definition.

## Tests

- Focused corpus certification: 7/7 PASS.
- Full regression: 219/219 PASS.
- Whitespace: PASS.

## Boundary Verification

- Synthetic static dataset only.
- No orchestration execution.
- No runtime or Local AI access.
- No provider or agent invocation.
- No LOCKED changes.
- No scoring, confidence, ranking, authority, voting, or governance semantics.

## Result

**CERTIFIED REPLAY CORPUS v1.0**

## Recommendation

Proceed to baseline measurement against the certified immutable corpus.
