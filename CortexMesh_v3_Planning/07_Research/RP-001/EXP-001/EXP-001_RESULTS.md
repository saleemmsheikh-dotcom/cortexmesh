# EXP-001 Results

## Status

REGISTERED ANALYSIS COMPLETE - RESULTS READY FOR REVIEW

## Result Integrity

These results derive from the frozen EXP-001 raw dataset with SHA-256 `6551e6d6fd0ca6f661221a9be793802ddba1c301de0c44f07c5b1842ad6b962e`.

Outcome:

**BASELINE CHARACTERIZED WITH ANOMALIES**

## Execution Flow

| Item | Value |
| --- | ---: |
| Registered cases | 24 |
| Planned repetitions | 10 |
| Planned case executions | 240 |
| Executed | 240 |
| Included | 240 |
| Excluded | 0 |
| Failed | 0 |

## Independent Metrics

| Metric | Result | Denominator | Status |
| --- | ---: | ---: | --- |
| Determinism | 24/24 (100%) | 24 cases | PASS |
| Replay reproducibility | 24/24 (100%) | 24 cases | PASS |
| Pipeline stability | 240/240 (100%) | 240 executions | PASS |
| Evidence completeness | 450/450 (100%) | 450 evidence records | PASS |
| Evidence traceability | 450/450 (100%) | 450 evidence records | PASS |
| Consensus certified match | 24/24 (100%) | 24 cases | PASS |
| Minority preservation | 3/3 (100%) | Applicable cases | PASS |
| Material-divergence preservation | 4/4 (100%) | Applicable cases | PASS |
| Synthesis stability | 24/24 (100%) | 24 cases | PASS |
| Diagnostic completeness | 24/24 cases; 100/100 expectations (100%) | Registered expectations | PASS |
| Synthesis statement expectations | 220/260 (84.615%) | Statement observations | ANOMALY |

## Latency

| Statistic | Observation |
| --- | ---: |
| Count | 240 |
| Minimum | 0.009334 ms |
| Median | 0.647353 ms |
| P95 | 0.931067 ms (nearest rank) |
| Maximum | 3.465394 ms |
| Mean | 0.616510 ms |
| Standard deviation | 0.323932 ms (population) |
| Coefficient of variation | 0.525428 |

Latency is descriptive only. The 210 completed pipeline observations had median 0.688903 ms and p95 0.941303 ms. The 30 expected rejection observations had median 0.168195 ms and p95 0.259713 ms. This mixture explains part of the overall dispersion and is not a correctness gate.

## Per-Case Results and Anomalies

All case outputs and statuses were stable across ten repetitions. Certified consensus classifications matched for every case.

Four reproducible statement-level differences were observed:

| Case | Certified statement expectation | Observed synthesis behavior | Repetitions |
| --- | --- | --- | ---: |
| c02 | `safe`, `acceptable` | Compatible aliases canonicalized to `safe`; `acceptable` not repeated in synthesis | 10/10 |
| c05 | `refactor` | Insufficient-evidence synthesis withheld the lone claim and requested comparable evidence | 10/10 |
| c09 | `neutral` | Insufficient-evidence synthesis withheld the lone claim and requested comparable evidence | 10/10 |
| c17 | `bounded` | Compatible aliases canonicalized to `safe`; `bounded` not repeated in synthesis | 10/10 |

The differences are presentation-policy/expectation differences. Raw evidence remains preserved and traceable. They do not alter the 100% synthesis-stability measurement.

## Artifact References

- `raw/observations.jsonl`: all 240 observations;
- `analysis/case_results.json`: per-case registered measurements;
- `analysis/differences.json`: four classified differences;
- `analysis/metrics.json`: independent aggregate measurements;
- `analysis/ANALYSIS_MANIFEST.json`: analysis integrity record.

No overall score was calculated.
