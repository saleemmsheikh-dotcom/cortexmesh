# CA002 — gstack Comparison

## Classification

PROPOSED COMPARATIVE ARCHITECTURE NOTE

## System

gstack

## Primary Observation

gstack is relevant to CortexMesh because it appears to include cross-model review and adversarial challenge patterns.

It is not a CortexMesh analogue.

It operates primarily at the coding-agent and content-generation layer.

CortexMesh operates as a decision-governance shell.

## Architectural Contrast

| Dimension | gstack | CortexMesh |
|---|---|---|
| Primary objective | Coding throughput and review velocity | Governed decision process |
| Core mechanism | Multi-model coding/review workflows | Intent gating and decision lifecycle governance |
| Cross-model review | Present as second-opinion/challenge pattern | Deferred in Section 4.2 |
| Aggregate metrics | Uses or implies scoring/trending patterns | Prohibited by Section 7 |
| Human role | Developer/operator | Decision authority |
| Output | Code review, coding assistance, findings | Governed decision lifecycle |
| Governance posture | Throughput-oriented | Accountability-oriented |
| Speed posture | Optimized for velocity | Deliberately not optimized for speed |

## Section 4.2 Relevance

gstack's cross-model review pattern may be useful as a candidate input for the deferred CortexMesh multi-agent consensus work.

Potential design ideas:

- Independent second opinion
- Adversarial challenge mode
- Open consultation mode
- Overlap/divergence report
- Unique findings surfaced separately

These are candidate inputs only.

They are not approved CortexMesh mechanisms.

## Section 7 Relevance

gstack-style scoring or trend tracking is a contrast case for CortexMesh.

CortexMesh should not import:

- standing weighted scores
- agent performance trends
- leaderboards
- aggregate quality metrics

Any cross-model review design must preserve CortexMesh's no-aggregate-metrics rule.

## Section 4.11 Relevance

gstack's layered defense approach may be useful as a design reference for CortexMesh failure handling.

Relevant pattern:

- Multiple independent checks before blocking or escalating
- Avoid trusting a single model's judgment on security-relevant decisions
- Surface failures rather than silently route around them

This may inform future DEBT-011 or agent-failure design work.

## Preliminary Conclusion

gstack is useful as a comparative case for:

1. Section 4.2 multi-agent consensus design.
2. Section 4.11 failure escalation design.
3. Section 7 aggregate-metric boundary defense.

It should not be treated as a model for CortexMesh overall.
