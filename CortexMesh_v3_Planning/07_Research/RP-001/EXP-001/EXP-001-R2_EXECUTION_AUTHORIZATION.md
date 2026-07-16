# EXP-001-R2 Execution Authorization

## Status

**EXP-001-R2 AUTHORIZED FOR EXECUTION**

| Field | Value |
| --- | --- |
| Research program | RP-001 |
| Reproduction | EXP-001-R2 |
| Date | 2026-07-17 |
| Planned executions | 240 |
| OBS-INF-001 | OPEN |
| Infrastructure commit | `09b4455` |
| Engine | `phase2c-complete` / `a72d11fe57f9026ab307efeaf962b97095527039` |
| Replay Corpus | v1.1 / `20e4b446097db5b3dcaa6fbf214218038c9c297d2e60bbbc57b9d24bc1e59788` |
| Focused isolation tests | 7/7 PASS |
| Full regression | 226/226 PASS |
| Published evidence | `raw/` and `analysis/` unchanged |
| Fixed output destination | `reproduction/EXP-001-R2/` |
| Data collection | Authorized on the controlled Ubuntu environment |

## Authorization Basis

Independent review accepted the output-isolation design after confirming:

1. the output-isolation design and focused tests pass;
2. the full established regression baseline passes;
3. published EXP-001 `raw/` and `analysis/` hashes are unchanged;
4. the selected destination is an empty `reproduction/EXP-001-R2/` package;
5. engine, certified corpus, validation framework, and protocol identities remain frozen;
6. no runtime, Local AI, provider, governance, or LOCKED file changed.

Authorization changes reproduction state only. It must not alter hypotheses, protocol, corpus inputs, metrics, comparators, analysis, or expected outcomes.

## Authorized Procedure

The controlled Ubuntu environment may perform one clean collection into `reproduction/EXP-001-R2/raw/` and one registered analysis into `reproduction/EXP-001-R2/analysis/`. It must record the environment, generated artifacts and hashes, preserve divergent or partial results, and stop without retry or experimental alteration if any check fails.

## Continuing Boundaries

This authorization does not permit changing experiment logic, corpus inputs, expectations, metrics, published EXP-001 evidence, runtime, Local AI, providers, governance, or LOCKED components. It does not itself validate Ubuntu portability or close OBS-INF-001. Closure requires successful execution evidence and subsequent review.
