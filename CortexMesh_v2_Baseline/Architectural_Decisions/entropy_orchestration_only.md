# Architectural Decision: Entropy Is Orchestration-Only

## Decision
Entropy monitoring remains available for orchestration decisions but is not part of authority scoring.

## Rationale
Authority scoring must remain auditable and deterministic over the scorer output, diversity, repetition, trust, calibration, and specialist boost.

## Consequence
`engine/entropy.py` remains in the codebase.

Authority output must not include entropy-derived score modifiers.

## Verification
The scoring regression suite passes without entropy in authority scoring output.
