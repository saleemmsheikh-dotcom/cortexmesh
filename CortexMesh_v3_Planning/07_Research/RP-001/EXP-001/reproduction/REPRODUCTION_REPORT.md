# EXP-001-R1 - Independent Reproduction

## Status

**REPRODUCED**

## Identity

| Field | Value |
| --- | --- |
| Experiment | RP-001/EXP-001 |
| Reproduction identifier | EXP-001-R1 |
| Classification | Independent reproduction appendix |
| Date | 2026-07-13 |
| Engine | `phase2c-complete` / `a72d11fe57f9026ab307efeaf962b97095527039` |
| Collection harness SHA-256 | `885248766376d4d80c4f14c34077c4fe043879e2243e3b2fa3981a802290ec23` |
| Replay corpus | Certified v1.1.0 |
| Planned executions | 240 |
| Recorded executions | 240 |

## Integrity

| Artifact | SHA-256 / result |
| --- | --- |
| Reproduction observations | `936439d85d5a3c36a8616449597e2957144e81c6d9337c315a6dfe94f8cc870d` |
| Reproduction package manifest | `1c3512f634898130f3ccc535e7f2d94e5f69d9bddd9688c1a6222c798b5d8727` |
| Package verification | PASS |

## Behavioral Comparison

| Measurement | Result |
| --- | ---: |
| Canonical output matches | 240/240 |
| Canonical output differences | 0 |
| Status differences | 0 |
| Behavioral reproduction | 100% |

Every case/repetition pair produced the same registered canonical output hash as the original EXP-001 collection.

Outcome:

**100% REPRODUCTION - NO BEHAVIORAL DRIFT OBSERVED**

## Descriptive Latency

| Statistic | Run 001 |
| --- | ---: |
| Minimum | 0.010727 ms |
| Median | 0.764332 ms |
| P95 nearest rank | 1.406319 ms |
| Maximum | 4.705332 ms |
| Mean | 0.797575 ms |
| Population standard deviation | 0.480831 ms |

Latency differs from the original observation and remains environment-specific and descriptive. It does not affect behavioral reproduction and is not a learning or performance gate.

## Interpretation

The sealed Phase 2C reference engine reproduced exactly on the registered behavioral artifacts. This provides no evidence that the system learned between runs.

That result is architecturally expected: the reference engine has no persistent memory, parameter update, adaptive policy, training loop, or state mutation in EXP-001. A system capable of learning would require a separately defined experiment with an authorized learning mechanism, pre/post measurements, and controls against ordinary environment variance.

## Boundaries

- No engine, corpus, expectation, protocol, provider, runtime, Local AI, governance, or LOCKED modification occurred.
- No raw EXP-001 artifact was overwritten.
- This reproduction assesses deterministic behavior, not learning effectiveness.
