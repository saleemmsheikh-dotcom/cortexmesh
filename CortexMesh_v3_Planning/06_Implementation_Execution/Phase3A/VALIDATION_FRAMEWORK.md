# Phase 3A Validation Framework

## Purpose

Define measurable success metrics, collection rules, initial targets, and acceptance gates for the Phase 2C isolated reference orchestration subsystem.

## General Measurement Rules

- Measurements use versioned replay cases with declared expected outcomes.
- Correctness and preservation metrics are evaluated per case before aggregation.
- Every aggregate resolves to raw case-level evidence.
- A failed minority or material-divergence case remains visible.
- Provider/model identity cannot influence expectations, grouping, ordering, or results.
- Metrics are validation evidence, not runtime score, confidence, rank, authority, or vote weight.
- Latency is reported descriptively until a reproducible operational requirement is approved.

## Success Metrics

### 1. Determinism

Definition: proportion of repeated executions whose canonical intermediate and final artifacts exactly match the first execution for identical case, component, policy, and environment versions.

Formula: identical repeated executions / total repeated executions.

Initial gate: 100% across the required replay corpus and declared repetition count.

### 2. Evidence Completeness

Definition: proportion of required evidence fields present and valid for each expected record, including output, role, capability, provenance, assumptions, limitations, diagnostics, and identifiers or explicit allowed empty states.

Formula: satisfied required fields / applicable required fields.

Initial gate: 100%; no silently missing required field.

### 3. Evidence Traceability

Definition: proportion of synthesized material statements, agreement signals, divergence signals, minority records, and diagnostics that resolve to valid source evidence and trace/correlation identifiers where required.

Formula: resolvable attributable items / total attributable items.

Initial gate: 100%.

### 4. Minority Evidence Preservation

Definition: proportion of cases with declared minority or unmatched evidence in which every expected minority record and claim remains visible in assessment and synthesis output.

Formula: preserved expected minority items / total expected minority items.

Initial gate: 100%, with zero erased minority cases.

### 5. Consensus Correctness

Definition: proportion of replay cases whose categorical outcome and required agreement/divergence signals match the independently declared expectation.

Categories: exact agreement, compatible agreement, partial agreement, material divergence, and insufficient evidence.

Formula: correctly classified cases / total consensus cases.

Initial gate: 100% for the reviewed corpus. Material divergence precedence is mandatory.

### 6. Diagnostic Quality

Definition: case-level assessment of whether expected failures and boundary conditions produce stable, specific, attributable, non-authoritative diagnostics without leaking prohibited semantics.

Required attributes:

- stable diagnostic identifier or canonical text;
- correct triggering condition;
- relevant step, record, or stage attribution;
- no provider preference, score, confidence, authority, rank, vote, or governance effect;
- actionable description where action is possible.

Initial gate: 100% of declared diagnostic expectations satisfied. Qualitative limitations are reported separately.

### 7. Replay Reproducibility

Definition: proportion of cases that reproduce their canonical expected outcome and artifact hashes across clean validation runs under the same declared environment class.

Formula: reproducible cases / total replay cases.

Initial gate: 100% within a declared supported environment; cross-environment differences must be explained and versioned.

### 8. Planning Latency

Definition: elapsed monotonic time for capability resolution, agent planning, and execution planning, reported separately from evidence, consensus, and synthesis stages.

Report:

- sample count;
- median;
- 95th percentile;
- maximum;
- environment and measurement method;
- measurement noise and warm-up handling.

Initial target: establish a reproducible baseline. No optimization or integration claim may use latency until variance is characterized and an operational threshold is approved.

### 9. Pipeline Completeness

Definition: proportion of expected pipeline stages and required result sections represented for each case, including explicit empty states where content is unsupported.

Required stages: resolution, agent plan, execution plan, evidence, consensus, synthesis, orchestration result.

Required synthesis sections: all ten M9 sections.

Initial gate: 100%.

### 10. Reference Implementation Stability

Definition: preservation of the accepted Phase 2C public reference contracts and regression behavior throughout validation.

Evidence:

- full regression result;
- focused Phase 2C validation result;
- unchanged reference contract inventory or explicit reviewed change record;
- no runtime, Local AI, or LOCKED changes.

Initial gate: baseline 200/200 tests remain passing, with all new validation tests passing.

## Comparator Requirement

“Improvement” must name a comparator, metric, corpus version, environment, and practical significance threshold. A reference result cannot be declared improved merely because it passes its own tests.

Permitted future comparators may include:

- a prior reference-engine version;
- a deliberately reduced baseline lacking a validated feature;
- a read-only historical artifact mapping, if separately designed and sanitized.

The live runtime is not a comparator until a separate read-only measurement design is authorized.

## Acceptance Criteria

Runtime integration shall not be considered until:

1. all correctness, completeness, traceability, preservation, reproducibility, pipeline, and stability gates pass;
2. latency is reproducibly characterized;
3. measurable improvement is demonstrated against a declared comparator;
4. failures, limitations, and minority cases remain visible;
5. no metric changes runtime confidence, score, rank, authority, vote weight, provider selection, or governance;
6. a new evidence-driven runtime integration assessment is explicitly authorized.

These criteria are necessary but not sufficient for integration. Any LOCKED impact still requires prior Board authorization.

## Initial Recommendation

Design the replay corpus and expectation-review process before implementing metric automation.

**READY FOR REPLAY CORPUS DESIGN**
