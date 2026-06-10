# P0 Remediation Record: Scoring Specification

## Status
COMPLETE

## Remediation
Scoring was refactored to consume structured evidence flags instead of keyword matching.

## Canonical Path
`competition.scorer.compute_total_score(...)` is the single source of truth for weighted base scoring.

## Authority Responsibilities
Authority applies:

- Diversity bonus.
- Repetition penalty.
- Trust multiplier.
- Calibration multiplier.
- Fixed specialist boost when eligible.

## Explicit Non-Responsibilities
The scorer does not apply repetition penalties.

Authority scoring does not use entropy. Entropy remains orchestration-only.

## Regression Coverage
`tests/test_scoring_regression.py` verifies:

- Same evidence produces same score.
- Keyword text does not change score when evidence is the same.
- Specialist boost is fixed and bounded.
- Repetition penalty is not part of base scoring.
- Authority applies repetition once.
