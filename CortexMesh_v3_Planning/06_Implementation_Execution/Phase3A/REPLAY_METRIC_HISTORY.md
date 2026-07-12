# Replay Metric and Certification History

## Format

Each row records date, engine baseline, corpus/schema, content hash, environment class, repetitions, independent metrics, certification state, and evidence reference. Historical rows are append-only.

`NM` means not measurable. Latency is descriptive only.

## Historical Metric Table

| Evidence | Engine | Corpus | Determinism | Reproducibility | Stability | Planning complete | Evidence complete | Traceability | Consensus correct | Minority preserved | Diagnostics complete | Median / p95 / max ms |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| VE-006 | `phase2c-complete` | 1.0.0 | 100% | 100% | 100% | 100% | 100% | 100% | 50% | NM | Generated adapter diagnostics only | 0.463 / 0.766 / 1.637 |
| VE-007 | `phase2c-complete` | 1.1.0 | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% executable contracts | 0.546 / 0.642 / 0.684 |

## Regression History

| Date | Comparison | Classification | Protected metric regression | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-07-12 | Corpus 1.0.0 initial baseline | BASELINE | N/A | Established with anomalies | VE-006 |
| 2026-07-12 | Corpus 1.0.0 to 1.1.0 on unchanged engine | CORPUS FIDELITY REMEDIATION | None | PASS; engine unchanged | VE-007 |

## Certification History

| Release | Schema | Content hash | Status | Scope |
| --- | --- | --- | --- | --- |
| Replay Corpus 1.0.0 | 1.0 | `91c9b565bdfbf13d655dbe95dc3aa1c6db3666edc90e4bbe9cea6a5237de04d8` | CERTIFIED | Structural canonical baseline; runtime replay not certified |
| Replay Corpus 1.1.0 | 1.1 | `20e4b446097db5b3dcaa6fbf214218038c9c297d2e60bbbc57b9d24bc1e59788` | CERTIFIED | Executable semantic baseline; runtime replay not certified |

## Version Comparison Matrix

| Dimension | v1.0 | v1.1 | Classification |
| --- | --- | --- | --- |
| Engine | `phase2c-complete` | unchanged | No engine change |
| Cases/scenarios | 24/12 | 24/12 | Metadata continuity |
| Executable payloads | Characteristic-level | Role/step-resolved profiles | Executable semantics addition |
| Negative cases | Descriptive | Executable | Executable semantics addition |
| Alias/conflict policy | Incomplete | Per-case | Fidelity correction |
| Planning expectations | Drift observed | Sealed-contract bound | Expectation correction |
| Minority/divergence | Not fully measurable | Executable | Fidelity correction |
| Runtime replay | Not certified | Not certified | No boundary change |

## Next History Entry Requirements

The next entry must identify the exact certified baseline, retain all failed cases, apply release gates independently, and link raw case-level evidence. No row may replace or edit an earlier record.
