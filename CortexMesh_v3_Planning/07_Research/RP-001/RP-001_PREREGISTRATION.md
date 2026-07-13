# RP-001 Preregistration

## Registration Record

| Field | Value |
| --- | --- |
| Registered | 2026-07-13 |
| Research program | RP-001 |
| Experiment | EXP-001 |
| Experiment title | Baseline Characterization of the Phase 2C Reference Orchestration Engine |
| Preregistration version | 1.1 |
| Status | PREREGISTERED - EXECUTION NOT AUTHORIZED |
| Data collected | None |
| Supersedes | Version 1.0, before data collection |
| Reason for revision | Replace the proposed comparative-effectiveness experiment with conservative baseline characterization |
| Amendment rule | After authorization and collection begin, this version is immutable; deviations require a separate dated record and material redesign requires a new preregistration |

Version 1.0 remains preserved in repository history at commit `42453be`. No EXP-001 data were collected under version 1.0, and no result was inspected before this revision.

## Objective

Establish the first fully reproducible research characterization of the sealed Phase 2C Reference Orchestration Engine using Certified Replay Corpus v1.1 and the permanently adopted Phase 3A validation framework.

EXP-001 observes the existing baseline. It does not attempt to improve, optimize, outperform, adapt, or prove the engine.

## Registered Experimental Questions

1. Is the reference engine completely deterministic under repeated replay?
2. Are all replay outcomes reproducible across executions?
3. Are all evidence artifacts fully traceable?
4. Are consensus classifications stable?
5. Are synthesis outputs stable?
6. Does latency remain observationally stable in the declared environment?

## Registered Expectations and Anomaly Conditions

EXP-001 is descriptive. It does not register an improvement hypothesis.

| Question | Registered expectation | Anomaly condition |
| --- | --- | --- |
| Determinism | Canonical outputs are identical for every repeated execution of each case. | Any canonical output difference for an identical case and environment. |
| Replay reproducibility | Every eligible case completes with the same replay result on every execution. | Any outcome, status, or validation difference. |
| Evidence traceability | Every required evidence identifier and trace/correlation relationship remains present and resolvable. | Any missing, altered, duplicate, or unresolved required reference. |
| Consensus stability | Every case retains its certified consensus category and registered divergence/minority representation. | Any category or preservation difference. |
| Synthesis stability | Canonical synthesis sections, referenced evidence, diagnostics, and unresolved questions remain identical. | Any canonical synthesis difference. |
| Latency stability | Latency distributions can be described reproducibly enough to form an observational reference. | Measurement failure, unexplained environment discontinuity, or insufficient metadata. Latency variance alone is not a correctness failure. |

An anomaly is a finding, not an automatic engine defect. It must be classified as engine, corpus, harness, environment, measurement, or unresolved before interpretation.

## Registered Baselines

| Baseline | Registered version |
| --- | --- |
| Foundation baseline | `FOUNDATION_BASELINE_v1.0.md`, version 1.0 |
| Reference engine | `phase2c-complete`, commit `a72d11f` |
| Replay corpus | Certified Replay Corpus v1.1 / manifest version 1.1.0 / schema 1.1 / content hash `20e4b446097db5b3dcaa6fbf214218038c9c297d2e60bbbc57b9d24bc1e59788` |
| Validation framework | `phase3a-complete`, commit `6c41364` |
| Research charter | RP-001 Charter v1.0 |
| Preregistration | RP-001 Preregistration v1.1 |

The engine, corpus, and validation framework are fixed research objects. EXP-001 may not modify them.

## Experimental Design

### Unit of Analysis

The replay case is the unit of analysis. Repeated executions are repeated observations of the same case and are not independent samples.

### Execution Set

The experiment shall execute every valid case in Certified Replay Corpus v1.1 in deterministic manifest order for ten complete repetitions in one declared environment.

The first repetition establishes the experiment-local reference observation. Repetitions 2-10 are compared with repetition 1 and with the certified v1.1 expectations. No warm-up execution may be discarded. If a warm-up is operationally necessary, it must be separately logged and excluded by protocol before authorization.

### Comparator Definitions

- **Certified expectation comparator:** compares each observed case outcome with its immutable Replay Corpus v1.1 expectation using that case's certified comparator selection.
- **Exact repetition comparator:** compares canonicalized artifacts from repetitions 2-10 with repetition 1, excluding only fields explicitly registered as observational environment metadata.
- **Traceability comparator:** verifies evidence, provenance, trace, correlation, minority, divergence, and synthesis references against certified case expectations.
- **Latency observation comparator:** reports distributions by repetition and case without a release gate or performance ranking.

No single-path, alternative planner, provider, model, adaptive, or runtime condition is part of EXP-001.

## Inclusion Criteria

A replay case is included when it:

- is listed in the Certified Replay Corpus v1.1 manifest;
- passes corpus hash, schema, manifest, and certification validation;
- has complete executable inputs and registered expectations;
- is supported by the sealed reference-engine adapter used by the certified baseline;
- contains no unauthorized personal, secret, production, proprietary, or provider-bound data.

## Exclusion Criteria

A case may be excluded only when:

- corpus integrity cannot be verified before execution;
- required executable data are missing or corrupted;
- the declared environment or harness cannot produce a valid observation;
- an authorization, privacy, security, ethics, or boundary violation is detected.

Every exclusion and its timing must be recorded. A malformed negative-control input, insufficient-evidence result, divergence, failure produced by valid execution, unexpected outcome, or unfavorable observation is not an exclusion ground.

## Registered Metrics

| Metric | Measurement | Required reporting |
| --- | --- | --- |
| Determinism | Cases with identical canonical artifacts across all repetitions / eligible cases | Count, denominator, percentage, per-case differences |
| Replay reproducibility | Cases with identical replay status and outcome across all repetitions / eligible cases | Count, denominator, percentage |
| Pipeline stability | Successful valid pipeline executions / planned executions | Count by case and repetition, failure taxonomy |
| Evidence completeness | Required evidence characteristics present / required characteristics | Count and percentage per case and aggregate |
| Evidence traceability | Required identifiers and relationships resolvable / required references | Count and percentage per case and aggregate |
| Consensus stability | Cases with invariant certified classification and preserved divergence/minority state / applicable cases | Count, denominator, percentage |
| Minority preservation | Applicable cases preserving all registered minority evidence on every repetition / applicable cases | Count, denominator, percentage |
| Synthesis stability | Cases with identical canonical synthesis artifacts across repetitions / eligible cases | Count, denominator, percentage, section-level differences |
| Diagnostic completeness | Required diagnostics present / required diagnostics | Count and percentage per case and aggregate |
| Latency | Per-execution elapsed time | Count, minimum, median, p95, maximum, mean, standard deviation, coefficient of variation; descriptive only |

No overall or composite score is permitted. One metric may not compensate for another.

## Registered Analysis

1. Verify commit, tag, corpus, manifest, schema, content hash, environment, and authorization before collection.
2. Record the complete planned and observed execution flow.
3. Compare each case with its certified expectation for every repetition.
4. Compare canonical artifacts from repetitions 2-10 with repetition 1.
5. Report each registered metric independently, with counts and denominators.
6. Produce per-case and per-repetition difference tables for every anomaly.
7. Classify anomalies without changing the engine, corpus, expectations, or registered method.
8. Report latency distributions descriptively overall and by repetition; inspect run-order patterns without an optimization claim.
9. Preserve all results, including null, negative, failed, and unexpected observations.

EXP-001 makes no inferential population claim. No significance test, multiple-comparison correction, improvement effect, or causal claim is planned. Exact binomial intervals may be reported descriptively for bounded proportions, but the certified corpus is treated as the complete registered study set rather than a random sample of all possible tasks.

## Outcome Definitions

### BASELINE CHARACTERIZED

All planned executions and registered measurements are complete, artifacts are auditable, and every observation or anomaly is reported and classified. This status does not require the engine to match prior expectations.

### BASELINE CHARACTERIZED WITH ANOMALIES

The study is complete and reproducible, but one or more observations differ from the certified expectation or across repetitions. Anomalies remain visible and are attributed where evidence permits.

### INCONCLUSIVE

The study remains valid but missing executions, unresolved environment variance, inadequate metadata, or measurement limitations prevent one or more experimental questions from being answered.

### INVALID EXPERIMENT

Authorization, baseline integrity, protocol adherence, auditability, ethics, or reproducibility-package requirements fail. Observations remain retained but cannot establish the RP-001 baseline.

There is no `SUPPORTED` or `NOT SUPPORTED` effectiveness outcome in EXP-001 because no improvement claim is tested.

## Reproducibility Requirements

The experiment must preserve:

- this preregistration and the authorized protocol;
- exact code, tag, corpus, schema, manifest, and content hashes;
- operating system, architecture, interpreter, dependency, configuration, and environment metadata;
- exact commands and execution order;
- raw inputs, outputs, diagnostics, timings, failures, and exit states;
- canonicalization rules and comparator versions;
- per-case and aggregate measurements;
- anomaly classifications and review records;
- a content-hashed reproducibility manifest.

## Ethics and Governance Freeze

- No Board update is required for this documentation and isolated research preparation.
- No human subjects, personal data, secrets, production data, or proprietary provider data are authorized.
- No Local AI, external provider, live agent, or runtime invocation is authorized.
- No provider selection, adaptation, optimization, or alternative planner is authorized.
- No engine, corpus, validation framework, runtime, governance, or LOCKED modification is authorized.
- No authority, scoring, voting, ranking, confidence, or governance semantics may be introduced.
- GG-02 remains authoritative for any later governed decision.

## Authorization Boundary

This preregistration does not authorize data collection. EXP-001 may begin only after `EXP-001_PROTOCOL.md` is reviewed against this preregistration and its status is explicitly changed to:

**EXP-001 AUTHORIZED FOR EXECUTION**

The authorization record must identify the approver and date. That record is the immutable start point for data collection.
