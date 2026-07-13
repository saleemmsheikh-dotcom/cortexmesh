# RP-001 - Evidence-Based Orchestration Effectiveness

## Status

CHARTERED - EXECUTION NOT AUTHORIZED

## Research Question

Under controlled, replayable conditions, does evidence-based multi-agent orchestration produce measurable improvements in solution completeness, evidence coverage, traceability, diagnostic usefulness, and divergence preservation compared with a controlled single-path baseline, without reducing determinism or causing authority leakage?

## Scope

RP-001 defines the question, hypotheses, method, and success criteria for a future offline experiment. It does not execute agents or providers, change the sealed Phase 2C engine, integrate with runtime, or authorize adaptive orchestration.

## Documents

- `RP-001_CHARTER.md` defines purpose, scope, hypotheses, authority, and boundaries.
- `RP-001_RESEARCH_METHOD.md` defines design, controls, measurement, analysis, reproducibility, and publication.
- `RP-001_SUCCESS_CRITERIA.md` defines independent gates and permissible conclusions.
- `RP-001_PREREGISTRATION.md` freezes the first planned experiment before data collection.

## Experiment Register

| Experiment | Title | Status |
| --- | --- | --- |
| RP-001/EXP-001 | Baseline Characterization of the Phase 2C Reference Orchestration Engine | BASELINE CHARACTERIZED WITH ANOMALIES - REPRODUCED |

Future experiment identifiers are reserved only when their own charter or preregistration is published. Example research directions do not constitute approved experiments.

## Foundation Assets

The study is designed around:

- `phase2c-complete` as the sealed Reference Orchestration Engine baseline;
- Replay Corpus v1.1 as the initial certified validation baseline;
- the Phase 3A permanent validation methodology;
- GG-02 and the LOCKED registry as binding boundaries;
- `FOUNDATION_BASELINE_v1.0.md` as the architectural baseline record.

Any executable study protocol, corpus extension, agent/provider harness, or implementation proposal requires a later separately reviewed milestone.
