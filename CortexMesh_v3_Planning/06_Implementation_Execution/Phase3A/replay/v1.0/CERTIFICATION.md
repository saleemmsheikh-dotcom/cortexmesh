# Replay Corpus v1.0 Certification

## Release

- Replay Corpus Version: 1.0.0 (v1.0)
- Schema Version: 1.0
- Content Hash: `91c9b565bdfbf13d655dbe95dc3aa1c6db3666edc90e4bbe9cea6a5237de04d8`
- Replay Cases: 24
- Replay Scenarios: 12
- Comparator Coverage: Exact, Compatible, Regression
- Runtime Replay: NOT CERTIFIED
- Validation Status: CERTIFIED
- Approved: 2026-07-12
- Approved By: Product Owner
- Certification ID: `phase3a-replay-v1.0`

## Certification Evidence

- Schema and manifest integrity validated.
- Dataset file hashes and aggregate content hash validated.
- Case and scenario identifiers are deterministically ordered and unique.
- All scenario-to-case references resolve.
- Every case contains metadata context, normalized intent, capabilities, agent plan, execution plan, evidence characteristics, consensus category, synthesis characteristics, comparator, and validation expectations.
- Exact, compatible, and regression comparator contracts are present.
- Future runtime replay is explicitly not certified.
- Full regression and focused certification results are recorded in VE-005.

## Boundaries

This certification applies only to the exact v1.0 manifest and content hash. It certifies an isolated synthetic dataset, not runtime integration, orchestration execution, provider/model performance, governance authority, scoring, confidence, ranking, voting, or agent invocation.

Any content change requires a new corpus version and certification.
