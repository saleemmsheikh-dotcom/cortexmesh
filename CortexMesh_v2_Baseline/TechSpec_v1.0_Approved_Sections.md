# CortexMesh Technical Specification v1.0

## Approved Sections
Section 2 is approved for the v2 certified baseline.

## Approved Technical Points
- Scoring consumes structured, validated evidence flags.
- `competition.scorer.compute_total_score(...)` is the canonical scoring path.
- Repetition penalties are applied once in Authority, not in the base scorer.
- Specialist boost is fixed and bounded.
- Entropy is retained for orchestration use only.
- External execution uses Docker-backed `ExternalRunner` isolation.

## Remaining Work
The full technical specification remains partially complete and is carried forward into v3 planning.
