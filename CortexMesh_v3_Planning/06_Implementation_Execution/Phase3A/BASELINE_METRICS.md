# Phase 3A Baseline Metrics

## Independent Metric Scorecard

| Metric | Result | Observation |
| --- | ---: | --- |
| Replay determinism | 100% (24/24) | Complete result representation identical across repetitions. |
| Planning completeness | 100% (24/24) | Resolution, agent plan, and execution plan produced for every case. |
| Capability resolution accuracy | 54.2% (13/24) | Declared capability sets differed in 11 cases. |
| Agent planning accuracy | 75.0% (18/24) | Declared role sets differed in 6 cases. |
| Execution planning accuracy | 75.0% (18/24) | Declared step counts differed in 6 cases. |
| Evidence completeness | 100% (24/24 runs) | Generated evidence contained required source/output/qualification fields. |
| Evidence traceability | 100% (24/24 runs) | Generated records retained step, trace, and correlation identifiers. |
| Consensus classification correctness | 50.0% (12/24) | Characteristic-only fixtures could not reproduce several compatible/partial/divergent expectations. |
| Minority evidence preservation | Not measurable for intended cases | v1.0 lacks executable per-step claim payloads needed to create declared minority relationships. |
| Synthesis completeness | 100% (24/24) | All ten required sections were present, including empty states. |
| Diagnostic completeness | 100% for generated adapter/run diagnostics | Declared case diagnostics are characteristics, not executable trigger contracts; semantic correctness remains unmeasured. |
| Replay reproducibility | 100% (24/24) | Identical case adapter and environment reproduced results. |
| Pipeline stability | 100% (120/120 timed executions) | No exception or incomplete orchestration result. |

## Latency Statistics

The following describes full isolated pipeline execution, not only planning:

| Statistic | Milliseconds |
| --- | ---: |
| Per-case median of five runs, corpus median | 0.463 |
| 95th percentile of per-case medians | 0.766 |
| Maximum observed single run | 1.637 |

Latency is environment-specific and not an optimization or integration claim.

## Interpretation

Structural pipeline metrics are strong: deterministic execution, artifact completeness, traceability, synthesis sections, reproducibility, and stability all reached 100% in this measurement environment.

Expectation correctness is not yet certification-grade. The gaps indicate corpus authoring/adapter mismatches, not evidence that the engine should be integrated or optimized. v1.0 remains immutable; improvements require v1.1.
