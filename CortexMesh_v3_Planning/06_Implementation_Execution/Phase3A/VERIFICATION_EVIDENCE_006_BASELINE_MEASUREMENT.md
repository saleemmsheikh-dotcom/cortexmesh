# Verification Evidence 006 - Baseline Replay Measurement

## Evidence ID

VE-006

## Baselines

- Certified Replay Corpus: v1.0 / 1.0.0
- Content hash: `91c9b565bdfbf13d655dbe95dc3aa1c6db3666edc90e4bbe9cea6a5237de04d8`
- Reference engine: `phase2c-complete` / `a72d11f`
- Cases: 24
- Timed repetitions: 120

## Verified Results

- Determinism: 24/24 PASS.
- Pipeline completeness: 24/24 PASS.
- Capability expectation match: 13/24.
- Agent expectation match: 18/24.
- Execution-step-count match: 18/24.
- Consensus expectation match: 12/24.
- Evidence/traceability structural completeness: 24/24 PASS.
- Synthesis section completeness: 24/24 PASS.
- Replay reproducibility: 24/24 PASS.
- Pipeline stability: 120/120 PASS.
- Corpus-median per-case latency: 0.463 ms.

## Evidence Qualification

Minority preservation and declared diagnostic semantics could not be fully measured because v1.0 records characteristic expectations rather than executable case-specific simulated claims and failure inputs. This is reported as a baseline anomaly and v1.1 opportunity, not silently counted as passing.

## Regression

Full repository regression: **219/219 PASS**.

## Boundaries

Reference orchestration only. No live runtime, Local AI, provider/agent invocation, persistent mutation, or LOCKED modification occurred.

## Result

PASS - BASELINE ESTABLISHED WITH RECORDED ANOMALIES

## Recommendation

**READY FOR REPLAY REGRESSION PROGRAM**
