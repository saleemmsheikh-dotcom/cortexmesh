# Phase 3A Baseline Results

## Overall Result

Baseline established with material corpus-executability anomalies. No aggregate score is assigned.

## Per-Case Measurements

Legend: C = capability expectation, A = agent expectation, E = execution-step count, D = deterministic, K = consensus category.

| Case | C | A | E | D | K | Median ms |
| --- | --- | --- | --- | --- | --- | ---: |
| c01 | PASS | PASS | PASS | PASS | PASS | 0.647 |
| c02 | FAIL | PASS | PASS | PASS | FAIL | 0.535 |
| c03 | PASS | PASS | PASS | PASS | PASS | 0.352 |
| c04 | PASS | PASS | PASS | PASS | FAIL | 0.462 |
| c05 | PASS | PASS | PASS | PASS | PASS | 0.422 |
| c06 | PASS | FAIL | FAIL | PASS | FAIL | 0.614 |
| c07 | FAIL | PASS | PASS | PASS | PASS | 0.766 |
| c08 | FAIL | PASS | PASS | PASS | FAIL | 0.800 |
| c09 | PASS | PASS | PASS | PASS | PASS | 0.450 |
| c10 | PASS | PASS | PASS | PASS | PASS | 0.544 |
| c11 | PASS | PASS | PASS | PASS | PASS | 0.383 |
| c12 | FAIL | PASS | PASS | PASS | PASS | 0.414 |
| c13 | FAIL | FAIL | FAIL | PASS | FAIL | 0.389 |
| c14 | PASS | PASS | PASS | PASS | FAIL | 0.658 |
| c15 | FAIL | FAIL | FAIL | PASS | FAIL | 0.580 |
| c16 | FAIL | FAIL | FAIL | PASS | FAIL | 0.448 |
| c17 | PASS | PASS | PASS | PASS | FAIL | 0.464 |
| c18 | PASS | PASS | PASS | PASS | FAIL | 0.545 |
| c19 | FAIL | PASS | PASS | PASS | PASS | 0.409 |
| c20 | FAIL | FAIL | FAIL | PASS | PASS | 0.388 |
| c21 | FAIL | FAIL | FAIL | PASS | FAIL | 0.634 |
| c22 | FAIL | PASS | PASS | PASS | FAIL | 0.575 |
| c23 | PASS | PASS | PASS | PASS | PASS | 0.403 |
| c24 | PASS | PASS | PASS | PASS | PASS | 0.359 |

## Observed Anomalies

### A1 - Characteristic-Level Simulated Evidence

v1.0 declares evidence characteristics but not executable step-keyed outputs with case-specific claims. The adapter therefore generated uniform claims for actual steps. This reliably exercises the pipeline but cannot realize declared compatible, partial, material-divergence, minority, missing-output, or rejection semantics.

Impact: consensus correctness 50%; minority preservation for intended minority cases not measurable.

### A2 - Expected Capability Drift

Eleven cases omit capabilities derived by the sealed resolver from objective terms or task/domain mappings, or declare capabilities the resolver does not derive from the supplied input.

Impact: capability accuracy 54.2%.

### A3 - Agent/Execution Expectation Drift

Six cases declare roles and step counts inconsistent with actual capability coverage.

Impact: agent and execution accuracy 75%.

### A4 - Error Cases Are Descriptive, Not Executable

Cases c10, c23, and c24 describe rejection behavior but do not encode prohibited input, empty required intent, or an unplanned step in an executable fixture field.

Impact: the baseline adapter executed ordinary valid requests; rejection semantics remain unmeasured.

## Improvement Opportunities

1. Publish v1.1 with explicit original intent mappings and exact normalized intent fields.
2. Add step-keyed simulated output templates or role-to-output mapping rules that resolve after planning.
3. Encode consensus policy aliases and material-conflict pairs per applicable case.
4. Encode executable missing, extra, malformed, and prohibited-input cases.
5. Generate expected capability/role/step contracts through independent architecture review, then lock them before execution.
6. Add statement-level evidence, minority, divergence, diagnostic, and synthesis expectations.
7. Preserve v1.0 and this baseline unchanged for regression comparison.

## Engineering Conclusion

The engine baseline is deterministic, reproducible, structurally complete, and stable. Corpus v1.0 is sufficient to establish those properties but insufficient for full semantic validation of consensus, minority preservation, diagnostics, and several planning expectations.

The next program should treat these failures as explicit regression/remediation targets, not change the engine to fit an under-specified corpus.

## Recommendation

**READY FOR REPLAY REGRESSION PROGRAM**
