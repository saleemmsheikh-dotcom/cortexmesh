# Phase 3A M8 - Replay Regression Program

## Purpose

Establish continuous, evidence-based regression validation of the sealed CortexMesh Reference Orchestration Engine using Certified Replay Corpus v1.1.

The program observes isolated reference behavior. It does not change the engine, runtime, Local AI, provider behavior, LOCKED components, or governance authority.

## Current Baseline

- Reference engine: `phase2c-complete` / `a72d11f`
- Replay corpus: 1.1.0
- Schema: 1.1
- Corpus hash: `20e4b446097db5b3dcaa6fbf214218038c9c297d2e60bbbc57b9d24bc1e59788`
- Cases/scenarios: 24/12
- Certified comparators: exact, compatible, regression
- Runtime replay: not certified

## Program Outputs

Each regression cycle produces:

1. execution identity and environment record;
2. corpus/engine/framework version bindings;
3. case-level results and artifact hashes;
4. independent metric table;
5. prior-baseline comparison matrix;
6. all deviations and minority-case failures;
7. release-gate decision;
8. certification or failure record;
9. append-only metric and certification history.

## Execution Cycle

1. Verify corpus certification and manifest hashes.
2. Verify sealed engine version and changed-path boundary.
3. Execute every certified case with the versioned v1.1 adapter semantics.
4. Repeat according to the determinism/reproducibility sampling policy.
5. Preserve raw case-level and canonical artifact evidence.
6. Calculate each metric independently.
7. Compare only with the identified certified baseline using regression comparator rules.
8. Apply non-compensating release gates.
9. Record pass, fail, or inconclusive status and findings.
10. Append history; never rewrite prior results.

## Required Metrics

- determinism;
- replay reproducibility;
- pipeline stability;
- planning completeness;
- evidence completeness;
- traceability;
- consensus correctness;
- minority preservation;
- diagnostic completeness;
- latency, descriptive only.

No overall score is calculated. A strength in one metric cannot offset a regression in another.

## Release Gates

No release may regress determinism, replay reproducibility, pipeline stability, evidence completeness, traceability, or minority preservation.

Planning completeness, consensus correctness, and diagnostic completeness must meet the certified case expectations or have an explicitly reviewed failure disposition; an undispositioned regression blocks certification.

Latency never blocks or approves a release by itself. It is reported with environment and variance context.

## Baseline Changes

A baseline changes only when:

- a new immutable corpus version is certified;
- the engine/component baseline is explicitly identified;
- both old and candidate baselines run against a valid comparison corpus or versioned migration;
- metric deltas and changed expectations are reviewed;
- release gates pass;
- history records the supersession without deleting the prior baseline.

Changing a corpus to make a failing engine result pass is prohibited. Corpus corrections require independent rationale, a new version, and certification.

## Failure Handling

On regression:

1. freeze the result and raw evidence;
2. identify affected cases, metrics, stages, and hashes;
3. classify engine regression, corpus defect, adapter defect, environment variance, or inconclusive;
4. reproduce in a clean run;
5. prohibit release certification while blocking findings remain;
6. correct the responsible validation asset or component only under separate scope;
7. rerun the complete corpus, not only failed cases;
8. retain the failed history record.

The sealed Phase 2C engine is not changed under Phase 3A. An apparent engine defect is reported for a separately authorized decision.

## Certification Workflow

Every regression record binds corpus certification, engine commit/tag, framework version, adapter/schema version, environment, repetitions, metric results, gate decision, reviewer, timestamp, and limitations.

A passing regression certification means only that the identified reference baseline satisfied the certified replay policy. It creates no runtime, release, authority, governance, or integration approval.

## Recommendation

**READY FOR LONGITUDINAL VALIDATION**
