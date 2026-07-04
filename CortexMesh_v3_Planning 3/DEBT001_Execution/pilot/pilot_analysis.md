# DEBT-001 Pilot Analysis

## Classification
OBSERVED evidence summary. No severity interpretation is made in this document.

## Run Summary
- Total planned runs: 100
- Completed rows: 100
- Successful rows: 100
- Error rows: 0

## Winner Reproducibility

| Winner | Count | Rate |
|---|---:|---:|
| Architect_v2 | 80 | 80.0% |
| Engineer_v2 | 10 | 10.0% |
| Researcher_v2 | 10 | 10.0% |

## Agent Selection Reproducibility
- Unique agent-selection patterns: 6

| Agent Selection | Count |
|---|---:|
| `Architect_v2,Engineer_v2,Researcher_v2` | 64 |
| `Researcher_v2,Architect_v2,Engineer_v2` | 23 |
| `Researcher_v2,Engineer_v2,Architect_v2` | 5 |
| `Engineer_v2,Architect_v2,Researcher_v2` | 3 |
| `Architect_v2,Researcher_v2,Engineer_v2` | 3 |
| `Engineer_v2,Researcher_v2,Architect_v2` | 2 |

## Score Variance
- Scores observed: 100
- Mean winner score: 6.5879
- Population standard deviation: 0.2736
- Minimum winner score: 5.8764
- Maximum winner score: 6.8400

## Seed Sensitivity

| Seed Type | Seed | Runs | Winner Counts | Selection Patterns | Score Mean | Score StdDev |
|---|---|---:|---|---:|---:|---:|
| fixed | 10 | 20 | `{"Architect_v2": 16, "Engineer_v2": 2, "Researcher_v2": 2}` | 1 | 6.6860 | 0.3199 |
| fixed | 123 | 20 | `{"Architect_v2": 16, "Engineer_v2": 2, "Researcher_v2": 2}` | 1 | 6.4840 | 0.1381 |
| fixed | 42 | 20 | `{"Architect_v2": 16, "Engineer_v2": 2, "Researcher_v2": 2}` | 1 | 6.6860 | 0.3199 |
| fixed | 999 | 20 | `{"Architect_v2": 16, "Engineer_v2": 2, "Researcher_v2": 2}` | 1 | 6.4840 | 0.1381 |
| random | system | 20 | `{"Architect_v2": 16, "Engineer_v2": 2, "Researcher_v2": 2}` | 6 | 6.5994 | 0.3008 |

## Task-Level Winner Stability

| Task | Runs | Unique Winners | Top Winner | Top Winner Rate | Winner Counts |
|---|---:|---:|---|---:|---|
| E1 | 10 | 1 | Architect_v2 | 100.0% | `{"Architect_v2": 10}` |
| E2 | 10 | 1 | Architect_v2 | 100.0% | `{"Architect_v2": 10}` |
| E3 | 10 | 1 | Engineer_v2 | 100.0% | `{"Engineer_v2": 10}` |
| E4 | 10 | 1 | Architect_v2 | 100.0% | `{"Architect_v2": 10}` |
| R1 | 10 | 1 | Architect_v2 | 100.0% | `{"Architect_v2": 10}` |
| R2 | 10 | 1 | Architect_v2 | 100.0% | `{"Architect_v2": 10}` |
| R3 | 10 | 1 | Architect_v2 | 100.0% | `{"Architect_v2": 10}` |
| S1 | 10 | 1 | Architect_v2 | 100.0% | `{"Architect_v2": 10}` |
| S2 | 10 | 1 | Architect_v2 | 100.0% | `{"Architect_v2": 10}` |
| S3 | 10 | 1 | Researcher_v2 | 100.0% | `{"Researcher_v2": 10}` |

## Ledger Consistency
- Unique normalized ledger hashes: 20

## Governance Inconsistencies
- No conflict/action governance inconsistencies observed in pilot outputs.

## Execution Anomalies
- No execution anomalies observed in pilot run logs.

## Evidence Boundary
This report records pilot evidence only. Severity interpretation and board recommendations belong in a later severity review or board submission.
