# ADR-003 Entropy Is Orchestration Only

## Status
Accepted (v2 certification)

## Context
During P0 Scoring Specification review, the board discovered that engine/entropy.py existed but was not integrated into the scoring pipeline. A proposal was made to integrate it as a modifier on authority_total.

## Decision
Entropy is an orchestration metric, not a scoring input. It monitors role weight distribution diversity but does not influence selection scores. Integration into authority scoring was explicitly rejected by unanimous board vote.

## Consequences
- compute_entropy() remains available for orchestration decisions
- authority_total formula excludes entropy
- Entropy's observable impact on selection is indirect

## Alternatives Considered
- Integrate as authority_total * entropy_modifier: REJECTED — board vote unanimous (Option B)
- Remove entirely: REJECTED — useful for orchestration monitoring

## References
- TechSpec §7 (Entropy Resolution)
- Board vote: Option B (unanimous)
- Governance Exception Record (override attempt, reverted)
