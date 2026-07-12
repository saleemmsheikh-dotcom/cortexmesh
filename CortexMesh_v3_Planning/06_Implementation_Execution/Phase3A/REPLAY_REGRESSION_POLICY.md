# Replay Regression Policy

## Classification

ENGINEERING VALIDATION POLICY - NON-AUTHORITATIVE

## Scope

Applies to isolated replay regression using certified Phase 3A corpora and identified reference component baselines.

## Execution Policy

- Run the complete certified corpus.
- Verify certification and hashes before execution.
- Use the declared schema/adapter/comparator versions.
- Use no network, provider, Local AI, runtime memory, agent invocation, or LOCKED component.
- Record environment and repetitions.
- Retain case-level artifacts and failures.
- Do not alter expectations after observing results within the same corpus version.

## Baseline Comparison Rules

1. Identify left and right engine, corpus, schema, adapter, framework, and environment versions.
2. Prefer the same immutable corpus version.
3. If corpus versions differ, use an explicit certified delta/migration and distinguish corpus-fidelity deltas from engine-behavior deltas.
4. Compare case-level metrics before aggregation.
5. Report unavailable/non-measurable values; never coerce them to pass or zero.
6. Do not compare subjective prose as a metric.
7. Do not claim engine improvement from corpus remediation.
8. Do not use provider/model identity as a grouping or explanatory variable.

## Metric Rules and Gates

| Metric | Required record | Release gate |
| --- | --- | --- |
| Determinism | Identical executions / repetitions | No regression; target 100% |
| Replay reproducibility | Reproduced cases / cases | No regression; target 100% |
| Pipeline stability | Successful complete runs / runs | No regression; target 100% |
| Planning completeness | Complete planning artifacts / cases | Required; failure must be dispositioned |
| Evidence completeness | Required evidence fields / applicable fields | No regression; target 100% |
| Traceability | Resolvable attributed items / attributable items | No regression; target 100% |
| Consensus correctness | Correct declared categories/signals / applicable cases | Required; failure blocks unless corpus defect proven |
| Minority preservation | Preserved minority items / expected minority items | No regression; target 100% |
| Diagnostic completeness | Satisfied declared diagnostic contracts / applicable contracts | Required; failure must be dispositioned |
| Latency | count, median, p95, maximum, environment | Observational only |

Metrics are independent. No weighted or aggregate score is permitted.

## Failure Classification

- `ENGINE_REGRESSION`: sealed/candidate component behavior differs unexpectedly.
- `CORPUS_DEFECT`: fixture or expectation is incomplete, inconsistent, or non-executable.
- `ADAPTER_DEFECT`: replay resolution changes case meaning or fails schema rules.
- `ENVIRONMENT_VARIANCE`: reproducible environment-specific difference.
- `INFRASTRUCTURE_FAILURE`: test/host failure prevents a valid observation.
- `INCONCLUSIVE`: evidence cannot establish cause.

All classes remain visible. Only a new certified corpus version may correct corpus content.

## Release Decision

- `PASS`: all non-regression gates pass and required metrics are satisfied.
- `FAIL`: any protected metric regresses or a blocking finding remains.
- `INCONCLUSIVE`: required evidence is unavailable; release certification prohibited.

## Certification Policy

- Certification is version-specific and append-only.
- A new engine or corpus version requires a new regression certification.
- Certification records exact hashes and metric results.
- Review evidence must disclose corpus changes and role overlap.
- Certification does not authorize runtime integration or governance action.

## Governance and Boundary

GG-02 remains authoritative. This policy modifies no runtime, Local AI, provider, engine, or LOCKED component. Any future integration remains separately assessed and authorized.
