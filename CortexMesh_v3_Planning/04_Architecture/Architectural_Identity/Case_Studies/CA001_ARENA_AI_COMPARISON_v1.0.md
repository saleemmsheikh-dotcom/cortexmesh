# CA001 — Arena.ai / LMArena Comparison

## Classification

PROPOSED COMPARATIVE ARCHITECTURE NOTE

## System

Arena.ai / LMArena

## Primary Observation

Arena.ai is a model-evaluation platform.

CortexMesh is a decision-governance shell.

These systems solve different problems.

## Architectural Contrast

| Dimension | Arena.ai / LMArena | CortexMesh |
|---|---|---|
| Primary objective | Compare and rank AI models | Govern AI-assisted decision process |
| Core mechanism | Battle mode, voting, leaderboard | Intent confirmation, draft-final lifecycle, audit trail |
| Aggregate metrics | Central feature | Explicitly prohibited |
| Ranking | Core function | Refused function |
| Human role | Voter/evaluator | Decision authority |
| Output | Model ranking / comparative result | Governed decision lifecycle |
| Authority | Community/aggregate preference | Human decision authority |
| Retention posture | Public evaluation data may be retained/shared | Rejected drafts deleted; no aggregate metrics |

## Relevance to CortexMesh

Arena.ai is useful as a negative boundary example.

It illustrates what CortexMesh deliberately refuses to become:

- A model leaderboard
- A ranking system
- A voting platform
- An aggregate benchmark layer

## Section 7 Relevance

Arena.ai demonstrates the design pattern that CortexMesh Section 7 rejects:

standing visible aggregate metrics.

CortexMesh does not claim that aggregate benchmarking is invalid.

CortexMesh claims it is inappropriate for its own governance-shell purpose because visible aggregate metrics create optimization pressure.

## Section 4.2 Relevance

Arena.ai's battle mode may be useful as an external comparison when designing the separate multi-agent consensus document.

However, CortexMesh must not silently import voting, ranking, or leaderboard mechanics.

## Preliminary Conclusion

Arena.ai is not a direct competitor.

It is an architectural contrast case.

It helps clarify that CortexMesh is not an evaluation platform.
