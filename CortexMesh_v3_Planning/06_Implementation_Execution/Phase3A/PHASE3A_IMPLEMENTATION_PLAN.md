# Phase 3A Implementation Plan

## Objective

Produce reproducible validation evidence for the isolated Phase 2C reference orchestration subsystem without changing runtime behavior.

## Milestone Plan

### M1 - Commencement and Validation Framework

Outputs:

- Phase 3A architecture and status;
- validation principles, metrics, and gates;
- commencement evidence;
- risk and blocker register.

### M2 - Replay Corpus Design

Define the case schema, taxonomy, source rules, expected outcomes, versioning, sanitization, and integrity checks.

Required case families:

- deterministic planning;
- exact and compatible agreement;
- partial agreement and minority evidence;
- material divergence;
- insufficient evidence;
- missing or malformed simulated outputs;
- assumptions, limitations, diagnostics, provenance, and traceability;
- prohibited semantic and identity inputs.

No corpus implementation begins until the schema and expected-outcome review are complete.

### M3 - Baseline Measurement

Execute or specify a versioned baseline against `phase2c-complete`. Record raw case results, metric results, environment, limitations, and failures.

### M4 - Determinism and Reproducibility Validation

Repeat cases within and across clean runs. Compare canonical artifacts, intermediate objects, diagnostics, and final synthesis sections.

### M5 - Evidence and Traceability Validation

Measure required-field completeness, record-to-section mappings, provenance retention, trace/correlation preservation, and unresolved-question coverage.

### M6 - Consensus and Minority Preservation Validation

Verify expected category classification, precedence, minority preservation, material divergence visibility, and absence of vote/authority semantics.

### M7 - Diagnostic and Latency Characterization

Assess diagnostic specificity, actionability, source attribution, planning latency distribution, and measurement noise. Performance work remains prohibited unless reproducible evidence identifies a material issue.

### M8 - Stability Assessment and Integration Recommendation

Summarize metric results, deviations, regression stability, limitations, and whether evidence supports another runtime integration assessment. This milestone cannot authorize integration.

## Verification Requirements

Documentation-only milestones verify:

- documentation-only changed paths;
- no LOCKED component changes;
- `git diff --check`;
- governance and runtime boundary language.

Any future validation code milestone must additionally run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile ...
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover tests
```

Validation code must remain isolated from live runtime imports and persistent state.

## Measurement Discipline

- Define expectation before observing the result.
- Retain raw case-level artifacts.
- Version all schemas, policies, cases, and metric formulas.
- Separate correctness gates from descriptive latency.
- Report failures and minority cases without aggregate suppression.
- Do not change thresholds after observation without a versioned rationale.

## Acceptance Criteria

Runtime integration shall not be considered until measurable improvements are demonstrated against the validation metrics in `VALIDATION_FRAMEWORK.md`.

At minimum, a future consideration requires:

- all correctness and preservation gates satisfied;
- replay reproducibility demonstrated;
- stable regression baseline;
- a declared comparator and statistically or operationally meaningful improvement;
- no runtime, governance, Local AI, provider-selection, or LOCKED-boundary leakage;
- limitations and failure cases explicitly dispositioned.

Passing these criteria permits a new assessment milestone only.

## Exit Criteria

Phase 3A exits when all validation milestones are complete or explicitly deferred, evidence is indexed, risks are dispositioned, and Product Owner acceptance is recorded.

## Recommendation

**READY FOR REPLAY CORPUS DESIGN**
