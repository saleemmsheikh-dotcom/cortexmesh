# RP-001 Success Criteria

## Purpose

Define in advance what constitutes a valid study, a supported research finding, and an impermissible conclusion. These criteria are independent; no aggregate score or compensating average is allowed.

## A. Research Integrity Gates

All are mandatory before results may be characterized as valid RP-001 findings.

| Criterion | Required result |
| --- | --- |
| Preregistration | Question, hypotheses, corpus, protocol, metrics, thresholds, exclusions, and analysis frozen before observation |
| Authorization | All required engineering, provider, cost, privacy, ethics, Product Owner, and governance dispositions recorded |
| Baseline integrity | Foundation, code, corpus, schema, and policy versions pinned and hash-verifiable |
| Condition equivalence | Comparable source information, constraints, and declared resource budgets |
| Complete reporting | All registered metrics, failures, exclusions, deviations, nulls, and adverse results retained |
| Reproducibility | Exact artifacts and commands reproduce registered results in the declared environment |
| Independent reproduction | At least one separately declared environment or reviewer reproduces primary findings before confirmatory publication |
| Auditability | Claims trace to cases, evidence identifiers, measurements, and provenance |
| Ethical compliance | No unauthorized human, personal, secret, production, or proprietary data use |
| Governance compliance | No authority leakage; GG-02 and LOCKED boundaries preserved |

## B. Protected Engineering Gates

The experimental condition must not regress any of the following relative to the control or certified baseline, according to the preregistered comparator:

- determinism;
- replay reproducibility;
- pipeline stability;
- evidence provenance and traceability;
- minority evidence preservation;
- unresolved divergence visibility;
- prohibited-semantic rejection;
- runtime, governance, and LOCKED-boundary compliance.

Any regression blocks a positive integration recommendation, regardless of improvements elsewhere.

## C. Evidence of Research Value

The primary hypothesis is supported only when:

1. at least one preregistered primary evidence-quality metric improves by its preregistered material engineering threshold;
2. its uncertainty and paired case evidence are reported;
3. the result is not explained by corpus, harness, rubric, budget, or environment differences;
4. every research-integrity and protected engineering gate passes;
5. the finding reproduces as required;
6. no unreported primary metric or adverse result contradicts the recommendation.

Statistical significance alone is insufficient. A favorable average cannot compensate for a protected-gate failure.

## D. Required Threshold Registration

Before execution, the protocol must define numerical or categorical materiality thresholds for:

- evidence completeness;
- claim traceability;
- minority and divergence preservation;
- synthesis completeness;
- diagnostic completeness/actionability;
- reviewer agreement where human coding is used;
- acceptable missingness and exclusions;
- latency reporting precision and environment variance.

This charter does not invent those values. They require corpus-specific pilot evidence or an explicit exploratory designation before confirmatory use.

## E. Outcome Categories

### SUPPORTED FOR SEPARATE DESIGN REVIEW

All mandatory gates pass and the primary research-value criteria are satisfied. This permits preparation of a separate design or integration-assessment milestone only.

### INCONCLUSIVE - ADDITIONAL RESEARCH REQUIRED

The study is valid but effect estimates, sample coverage, reproduction, or engineering materiality are insufficient to support or reject further design work.

### NOT SUPPORTED

Valid evidence shows no material improvement, an adverse hypothesis is supported, or protected engineering gates regress. The negative result is published and preserved.

### INVALID STUDY

Integrity, authorization, control, auditability, ethics, or reproducibility gates fail. Observations may be retained as diagnostic evidence but cannot support an effectiveness claim.

## F. Publication Acceptance

A publication is complete only when it includes:

- registered and actual methods;
- all independent metric tables;
- effect estimates and uncertainty where applicable;
- per-case traceability;
- anomalies, exclusions, protocol deviations, and failed runs;
- negative, null, minority, and adverse findings;
- validity threats, limitations, and unresolved questions;
- exact reproducibility manifest and verification status;
- authorship, review roles, and conflicts where applicable;
- the explicit statement: **RP-001 findings are advisory research evidence and confer no implementation, runtime, certification, governance, or LOCKED-component authority.**

## Current Disposition

**READY FOR PREREGISTERED EXPERIMENT DESIGN**

This disposition authorizes no execution, provider invocation, runtime integration, implementation change, or LOCKED modification.
