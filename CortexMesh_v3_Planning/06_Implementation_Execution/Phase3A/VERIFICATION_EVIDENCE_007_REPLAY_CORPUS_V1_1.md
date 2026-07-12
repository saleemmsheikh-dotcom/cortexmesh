# Verification Evidence 007 - Replay Corpus v1.1 Remediation

## Release

- Corpus: 1.1.0
- Parent: 1.0.0 unchanged
- Schema: 1.1
- Cases/scenarios: 24/12
- Hash: `20e4b446097db5b3dcaa6fbf214218038c9c297d2e60bbbc57b9d24bc1e59788`
- Status: CERTIFIED

## Remediation Evidence

v1.1 adds executable payload modes, negative inputs, alias/conflict policies, minority/divergence claims, sealed-engine planning bindings, and statement-level synthesis/diagnostic expectations.

## Repeated Baseline - Metric Deltas Only

| Metric | v1.0 | v1.1 | Delta |
| --- | ---: | ---: | ---: |
| Determinism | 100% | 100% | 0 pp |
| Replay reproducibility | 100% | 100% | 0 pp |
| Pipeline stability | 100% | 100% | 0 pp |
| Consensus correctness | 50% | 100% | +50 pp |
| Executable minority scenarios | Not measurable | 100% | Now measurable |
| Executable negative scenarios | Descriptive only | 5/5 | Now executable |
| Median latency | 0.463 ms | 0.546 ms | +0.083 ms |
| P95 latency | 0.766 ms | 0.642 ms | -0.124 ms |
| Maximum latency | 1.637 ms | 0.684 ms | -0.953 ms |

Latency is descriptive; the short run is not a performance conclusion.

## Boundary Confirmation

- No engine behavior changed.
- No runtime behavior changed.
- No Local AI behavior changed.
- No provider behavior changed.
- No LOCKED file changed.

## Verification

- Manifest/file hashes: PASS.
- Schema/order/reference checks: PASS.
- 24/24 consensus outcomes: PASS.
- 24/24 deterministic: PASS.
- Full regression: 219/219 PASS.

## Recommendation

**READY FOR REPLAY REGRESSION PROGRAM**
