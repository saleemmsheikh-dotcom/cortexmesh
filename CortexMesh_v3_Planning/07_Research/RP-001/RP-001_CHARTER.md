# RP-001 Research Charter

## Identity

| Field | Value |
| --- | --- |
| Program | RP-001 |
| Title | Evidence-Based Orchestration Effectiveness |
| Status | CHARTERED - EXECUTION NOT AUTHORIZED |
| Charter version | 1.0 |
| Established | 2026-07-13 |
| Research class | Controlled offline comparative study |

## Purpose

Determine whether the descriptive evidence, alignment, divergence-preservation, and synthesis structure of the CortexMesh reference orchestration approach can yield measurable engineering value when applied to genuinely independent candidate outputs.

The study exists to measure before integration. It is not intended to prove that more agents are inherently better or to justify runtime change by default.

## Primary Research Question

Under controlled, replayable conditions, does evidence-based multi-agent orchestration produce measurable improvements in solution completeness, evidence coverage, traceability, diagnostic usefulness, and divergence preservation compared with a controlled single-path baseline, without reducing determinism or causing authority leakage?

## Hypotheses

### Primary Hypothesis H1

For a preregistered corpus containing complementary and conflicting evidence, the orchestration condition will improve at least one declared evidence-quality metric by its material threshold while preserving every protected Foundation 1.0 gate.

### Secondary Hypotheses

- H2: orchestration will preserve more relevant minority and divergent evidence than the single-path control.
- H3: orchestration will improve evidence-to-claim traceability and diagnostic actionability.
- H4: improvements, if observed, will reproduce across repeated executions and at least one separately declared environment.
- H5: any additional planning latency will remain measurable and descriptively attributable.

### Null Hypothesis H0

The orchestration condition produces no material improvement over the single-path control on the preregistered primary engineering metrics.

### Adverse Hypotheses

- HA1: orchestration reduces determinism or replay reproducibility.
- HA2: orchestration erases minority evidence or unresolved divergence.
- HA3: provider/model identity, confidence, score, rank, vote, majority, or authority semantics affect the result.
- HA4: additional complexity or diagnostic noise outweighs observed benefits.

## Experimental Conditions

- **Control:** one preregistered candidate output is processed through an equivalent descriptive evidence and response structure, without cross-output alignment.
- **Experimental:** multiple independently prepared candidate outputs are collected, assessed for non-voting alignment/divergence, and synthesized through the isolated reference approach.
- **Negative controls:** insufficient, duplicate, malformed, provenance-only, minority, and materially divergent evidence cases.
- **Boundary controls:** inputs containing prohibited authority, scoring, confidence, rank, voting, governance, or provider-identity decision semantics must be rejected or remain non-decision provenance.

Input budgets, source material, task information, formatting constraints, and evaluation rules must be matched between comparable conditions. A later protocol must define how candidate outputs are obtained without contaminating independence.

## In Scope

- offline replay and controlled synthetic or approved benchmark inputs;
- sealed reference components or a separately versioned research harness;
- independent evidence-quality and preservation metrics;
- deterministic comparison and reproducibility analysis;
- qualitative error taxonomy supported by traceable evidence.

## Out of Scope

- live runtime integration;
- production traffic or decisions;
- modification of Phase 2C sealed behavior;
- adaptive routing or provider selection;
- Local AI or external provider invocation without separate authorization;
- governance, scoring, confidence, ranking, voting, or authority changes;
- human-subject or personal-data research;
- modification of LOCKED components.

## Decision Relevance

Possible results may justify one of three advisory conclusions:

1. evidence supports designing a separately authorized research implementation or integration assessment;
2. evidence is inconclusive and additional controlled research is required;
3. evidence does not support further orchestration integration work.

No result directly authorizes implementation.

## Governance and Ethics Boundaries

GG-02 remains the sole applicable governance authority. Product Owner acceptance of research artifacts does not replace Board approval where required. Research records must not imply governance ratification, runtime authority, or certification outside their declared scope.

No sensitive, personal, proprietary, production, or provider-bound data may be used without explicit approval and a recorded handling plan. Researchers shall disclose conflicts, preserve unfavorable evidence, and avoid presenting model/provider identity as a proxy for quality or authority.

## Deliverables Before Execution

- preregistered executable protocol;
- versioned and certified study corpus;
- frozen evaluation rubric and metric definitions;
- sample-size or exploratory-design justification;
- analysis plan and multiplicity treatment;
- immutable experiment preregistration;
- environment and dependency manifest;
- ethics, privacy, security, provider, and cost disposition;
- stop conditions and rollback/cleanup plan;
- authorization record.
