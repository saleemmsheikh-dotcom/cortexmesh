# ADR-004 Single Authority Score

## Status
Accepted (v2 certification)

## Context
P0 Scoring Specification review revealed two competing scoring paths: competition/scorer.py and agents/authority.py. Both computed weighted totals with different weight sources. This created ambiguity about which score was authoritative.

## Decision
Single source of truth for scoring. competition/scorer.py::compute_total_score() is canonical. agents/authority.py consumes its output directly. No recalculation of weights or totals in authority path.

## Consequences
- get_weights(task_type) removed from agents/authority.py
- score_solution() returns complete breakdown including weighted_total
- competition/selector.py deprecated (legacy only)

## Alternatives Considered
- Keep dual paths with reconciliation: REJECTED — complexity, potential divergence
- Move all scoring to authority: REJECTED — breaks separation of concerns

## References
- TechSpec §2 (Scoring Specification)
- P0 Scoring Specification remediation
