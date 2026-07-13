# RP-001 Preregistration

## Registration Record

| Field | Value |
| --- | --- |
| Registered | 2026-07-13 |
| Research program | RP-001 |
| Experiment | EXP-001 |
| Experiment title | Single-Path Versus Evidence-Based Orchestration |
| Preregistration version | 1.0 |
| Status | PREREGISTERED - EXECUTION NOT AUTHORIZED |
| Data collected before registration | None |
| Supersedes | None |
| Amendment rule | This registered version is immutable after data collection begins; changes require a preserved deviation record or a new preregistration before further collection |

## Research Question

Under controlled, replayable conditions, does evidence-based multi-agent orchestration produce measurable improvements in solution completeness, evidence coverage, traceability, diagnostic usefulness, and divergence preservation compared with a controlled single-path baseline, without reducing determinism or causing authority leakage?

## Registered Hypotheses

### H1 - Primary

On the registered eligible cases, the evidence-based orchestration condition will improve at least one primary evidence-quality metric by its registered material threshold while every protected engineering gate remains satisfied.

### H2 - Minority and Divergence Preservation

The experimental condition will preserve at least as much relevant minority evidence and unresolved material divergence as the control and will improve preservation where the control omits such evidence.

### H3 - Traceability and Diagnostics

The experimental condition will improve evidence-to-claim traceability or diagnostic actionability without increasing false provenance links or prohibited decision semantics.

### H4 - Reproducibility

Any supported primary finding will reproduce under the declared environment and one separately declared reproduction context before confirmatory publication.

### H0 - Null

The experimental condition will produce no material improvement over the control on any registered primary evidence-quality metric.

### Adverse Hypotheses

- HA1: the experimental condition reduces determinism, reproducibility, or pipeline stability;
- HA2: it erases or obscures minority evidence or unresolved divergence;
- HA3: provider/model identity or confidence, score, rank, vote, majority, authority, or governance semantics affect output decisions;
- HA4: added orchestration creates diagnostic noise or complexity that prevents a material engineering benefit.

## Registered Baselines

| Baseline | Registered version |
| --- | --- |
| Foundation baseline | `FOUNDATION_BASELINE_v1.0.md`, version 1.0 |
| Reference engine | `phase2c-complete`, commit `a72d11f` |
| Replay corpus | Certified Replay Corpus v1.1 / manifest version 1.1.0, schema 1.1, content hash `20e4b446097db5b3dcaa6fbf214218038c9c297d2e60bbbc57b9d24bc1e59788` |
| Validation framework | `phase3a-complete`, commit `6c41364` |
| Research charter | RP-001 Charter v1.0 |
| Research method | RP-001 Research Method as committed with this registration |
| Success criteria | RP-001 Success Criteria as committed with this registration |

The Phase 2C engine remains sealed. A research corpus release may extend Replay Corpus v1.1 through a separately versioned, immutable derivative; it may not edit v1.1. If an executable adapter is required, it must be separately reviewed, versioned as research infrastructure, and must not change sealed engine behavior.

## Experimental Conditions

### Control Comparator: SPB-1

`SPB-1` is the single-path baseline. For each paired case, one registered candidate output is converted into the same descriptive evidence and response section vocabulary used for evaluation, but no cross-candidate agreement, divergence, minority, or synthesis operation is performed.

### Experimental Comparator: EBO-1

`EBO-1` is evidence-based orchestration. For the paired case, two or more independently prepared candidate outputs are represented as step-keyed evidence, evaluated for non-voting alignment/divergence, and synthesized through the isolated Phase 2C reference approach.

### Equivalence Controls

Comparable conditions must use the same:

- original and normalized task intent;
- source material and allowed contextual facts;
- case-level constraints and output schema;
- aggregate declared input/output resource budget;
- evaluation rubric and case expectations;
- corpus, component, policy, and environment versions.

Candidate-output generation is not authorized by this preregistration. A later execution protocol must freeze how independence and resource equivalence are achieved before any candidate data are collected.

## Inclusion Criteria

A case is included only when it:

- belongs to the preregistered immutable research corpus;
- has a unique identifier, content hash, declared stratum, and complete metadata;
- provides executable step-keyed evidence expectations;
- defines control and experimental inputs without using observed outcomes;
- defines statement-level evidence, synthesis, and diagnostic expectations;
- declares expected agreement/divergence and minority-evidence behavior where applicable;
- passes schema, manifest, provenance, and comparator validation;
- uses no unauthorized personal, secret, production, proprietary, or provider-bound data.

## Exclusion Criteria

A case is excluded from confirmatory analysis only when, before outcome inspection where practicable:

- its hash, schema, manifest, or registered baseline cannot be verified;
- required paired inputs or metadata are missing or corrupted;
- the two conditions are not information- or resource-equivalent;
- corpus leakage or candidate dependence is demonstrated;
- the environment or harness fails before a valid pipeline observation exists;
- authorization, privacy, security, ethics, provider, or cost boundaries are violated.

Excluded cases, reasons, timing, and any observed data remain reported. Semantic difficulty, unfavorable outcomes, null results, malformed inputs intentionally included as negative controls, and valid pipeline failures are not exclusion grounds.

## Registered Case Strata

The confirmatory corpus must include cases covering:

- complementary evidence;
- exact agreement;
- compatible agreement;
- partial agreement;
- material divergence;
- minority evidence;
- insufficient evidence;
- malformed inputs;
- prohibited authority/governance semantics;
- architecture, implementation, risk, and diagnostic tasks.

The count per stratum and total sample-size justification must be frozen in a separately approved execution protocol before data collection. Until those values are registered, EXP-001 may not execute and no confirmatory statistical claim may be made.

## Registered Metrics

### Primary Evidence-Quality Metrics

- evidence completeness;
- evidence-to-claim traceability;
- minority evidence preservation;
- unresolved divergence preservation;
- synthesis completeness;
- diagnostic completeness and actionability.

### Protected Engineering Metrics

- determinism;
- replay reproducibility;
- pipeline stability;
- provenance preservation;
- prohibited-semantic rejection;
- GG-02 compliance;
- LOCKED-boundary preservation;
- absence of runtime authority leakage.

### Secondary Descriptive Metrics

- planning and pipeline latency;
- output size;
- diagnostic volume;
- unresolved-question count;
- case failures and exclusions.

No composite or overall score is permitted. Latency is observational and cannot compensate for another metric.

## Materiality and Success Thresholds

Protected engineering metrics must not regress. Determinism, replay reproducibility, evidence completeness, traceability, minority preservation, prohibited-semantic rejection, GG-02 compliance, LOCKED preservation, and absence of authority leakage require 100% on applicable registered cases unless the execution protocol explicitly identifies a metric as not measurable before data collection and explains why.

Confirmatory effect thresholds for judgment-dependent primary metrics are not invented in this registration. They must be derived from a separately labeled, non-confirmatory pilot or an external engineering requirement, then frozen in a new preregistration before confirmatory collection. Data used to set a threshold cannot also serve as confirmatory evidence.

Therefore, the current registration authorizes protocol completion only. EXP-001 is not ready to collect confirmatory data.

## Registered Statistical Methods

- The case is the unit of analysis; deterministic reruns are stability observations, not independent samples.
- Report counts, denominators, rates, and paired case-level differences for every registered metric.
- For paired binary outcomes, use an exact two-sided McNemar test only if the frozen sample size supplies sufficient discordant pairs; otherwise report exact paired counts and uncertainty without a significance claim.
- For paired ordinal or continuous rubric outcomes, report median paired difference and a distribution-free paired confidence interval; use a two-sided paired permutation test if exchangeability is justified and frozen before collection.
- Report effect sizes and 95% uncertainty intervals for all confirmatory comparisons.
- Define one primary comparison family in the execution protocol and control its family-wise error rate at 0.05 using Holm adjustment when more than one inferential primary metric is tested.
- Treat secondary and stratum analyses as descriptive unless separately powered and registered.
- Report reviewer agreement for human-coded fields using raw agreement and an appropriate chance-corrected coefficient selected before annotation; adjudication results remain separate.
- Analyze missingness, exclusions, invalid runs, and protocol deviations explicitly; do not impute primary outcomes unless a method is registered before collection.
- Do not interpret statistical significance as engineering materiality.

## Planned Analyses

1. Validate baseline, corpus, manifest, environment, and authorization integrity.
2. Produce a complete case-flow table: registered, included, excluded, invalid, and analyzed.
3. Verify protected metrics before testing benefit hypotheses.
4. Compare paired primary metrics overall using the registered method.
5. Report paired differences by registered case stratum descriptively.
6. Analyze minority, material-divergence, insufficient-evidence, malformed, and prohibited-semantic cases explicitly.
7. Classify failures as system, corpus, harness, rubric, authorization, or environment issues.
8. Reproduce any supported primary finding in the separately declared context.
9. Publish all results, including null, negative, adverse, invalid, and inconclusive findings.

No unregistered subgroup or alternative metric may be presented as confirmatory. Exploratory analyses must be labeled and cannot change the registered outcome.

## Outcome Rules

### SUPPORTED FOR SEPARATE DESIGN REVIEW

All research-integrity and protected engineering gates pass; at least one registered primary metric exceeds its preregistered material threshold with the registered uncertainty analysis; the effect is not attributable to corpus, harness, rubric, budget, or environment differences; and the primary finding reproduces.

This outcome permits only a separate design or integration-assessment proposal.

### NOT SUPPORTED

A valid study finds no registered materially beneficial primary effect, supports an adverse hypothesis, or records a protected-gate regression. The result is published and preserved.

### INCONCLUSIVE

The study is valid but sample coverage, effect precision, threshold registration, reproduction, or engineering materiality is insufficient to support or reject further design work.

### INVALID STUDY

Authorization, integrity, equivalence, auditability, ethics, or reproducibility gates fail. Observations remain diagnostic evidence but cannot support an effectiveness claim.

## Reproducibility and Publication Requirements

Execution must produce the complete reproducibility package defined in `RP-001_RESEARCH_METHOD.md`, including immutable inputs, hashes, exact commands, raw and derived outputs, environment metadata, failures, exclusions, reviewer records, and replication status.

The publication must distinguish preregistered and exploratory analysis; disclose every deviation; preserve null, negative, adverse, minority, and failed evidence; and include this statement:

**RP-001 findings are advisory research evidence and confer no implementation, runtime, certification, governance, or LOCKED-component authority.**

## Ethics and Governance Freeze

- No human-subject, personal-data, secret, production, proprietary, or provider-bound research is authorized.
- No Local AI or external provider invocation is authorized.
- No live agent invocation, runtime integration, adaptive behavior, or provider selection is authorized.
- No Phase 2C engine, Local AI, provider, governance, or LOCKED modification is authorized.
- Provider/model identity remains descriptive provenance only.
- GG-02 remains authoritative for governed decisions.

## Immutability Declaration

This preregistration records the design state before data collection. Once EXP-001 data collection begins, this file must not be edited. Deviations must be appended through a separately dated deviation record, and material design changes require a new preserved preregistration before additional collection.
