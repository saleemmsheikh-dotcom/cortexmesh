# Phase 3A M6 - Baseline Replay Measurement Plan

## Objective

Execute Certified Replay Corpus v1.0 against the sealed `phase2c-complete` reference orchestration components and establish independent baseline metrics without runtime integration.

## Baselines

- Replay corpus: 1.0.0 / schema 1.0
- Corpus hash: `91c9b565bdfbf13d655dbe95dc3aa1c6db3666edc90e4bbe9cea6a5237de04d8`
- Reference engine: `phase2c-complete`, closeout commit `a72d11f`
- Cases: 24
- Repetitions: 5 timed executions per case, plus deterministic result comparison
- Environment: local Python process, no network/provider/runtime access

## Method

1. Read each immutable case.
2. Form provider-neutral resolver input from original intent plus declared normalized task type/domain.
3. Run capability resolver, agent planner, and execution planner.
4. Adapt characteristic-level v1.0 evidence into step-keyed synthetic outputs using one stable claim and limitation per actual step.
5. Run evidence, consensus, synthesis, and orchestration result stages through the isolated reference engine.
6. Repeat five times and compare complete result representations.
7. Compare observed planning and consensus outcomes with declared case expectations.
8. Record latency with monotonic nanosecond timing.

## Metric Rules

Metrics remain separate. No overall score is calculated.

- Accuracy metrics use exact set equality or declared categorical equality.
- Completeness measures required artifact presence, not correctness.
- Reproducibility means equal complete outputs under identical inputs.
- Latency is descriptive and not a quality score.
- Non-executable corpus characteristics are reported as measurement limitations.

## Boundary

No live runtime, Local AI, agent/provider invocation, persistent state, LOCKED component, authority, score, confidence, ranking, voting, or governance behavior is used.
