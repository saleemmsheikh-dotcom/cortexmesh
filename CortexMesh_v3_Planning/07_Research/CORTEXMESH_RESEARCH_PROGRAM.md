# CortexMesh Research Program

## Status

ACTIVE FRAMEWORK - INDIVIDUAL STUDIES REQUIRE EXPLICIT AUTHORIZATION

## Mission

Produce reproducible evidence about CortexMesh capabilities, limitations, and future opportunities without converting research observations into runtime or governance authority.

## Research Lifecycle

1. Register a bounded question and falsifiable hypotheses.
2. Record prior evidence, assumptions, conflicts of interest, and foreseeable risks.
3. Freeze the protocol, controls, corpus, metrics, exclusions, and analysis plan.
4. Obtain required engineering, security, privacy, ethics, Product Owner, and GG-02 approvals.
5. Execute in an isolated, declared environment.
6. Preserve raw inputs, outputs, failures, provenance, hashes, and environment metadata.
7. Analyze using the preregistered method and report deviations.
8. Reproduce independently or in a separately declared environment where practicable.
9. Publish findings with limitations and non-claims.
10. Submit any proposed implementation as a separate milestone; research publication alone grants no authority.

## Identifier Convention

- Research programs use `RP-NNN`, allocated monotonically across CortexMesh research.
- Experiments use `EXP-NNN`, allocated monotonically within their research program.
- The canonical experiment identity is `RP-NNN/EXP-NNN`.
- Withdrawn, invalid, null, negative, and superseded identifiers are retained and never reused.
- Preregistrations, datasets, results, replications, corrections, and publications cite both identifiers.

An experiment preregistration becomes immutable when its status is `PREREGISTERED`. Any post-registration change must be recorded as a dated deviation or a new preregistration before additional data collection. It must never overwrite the registered design.

## Execution Authorization Principle

**Execution authorization is a governance event within the research methodology, not a data event. It changes experiment state but shall not alter the experiment design, hypotheses, metrics, comparators, or expected outcomes.**

Authorization must be separately attributable, dated, evidence-backed, and committed before collection begins. It neither records an observation nor grants runtime, implementation, provider, governance, or LOCKED-component authority.

## Required Program Artifacts

Every research program shall define:

- question, scope, and decision relevance;
- primary, secondary, null, and adverse hypotheses;
- experimental and control conditions;
- sampling unit, corpus, repetitions, and environment;
- independent metrics and measurement procedures;
- statistical and engineering validity rules;
- reproducibility package and retention policy;
- ethics, privacy, security, governance, and LOCKED boundaries;
- publication and review standards;
- success, failure, inconclusive, and stop conditions.

## Validity Standard

### Statistical Validity

- Define the unit of analysis before collection.
- Justify sample size or explicitly label exploratory work.
- Report effect sizes and uncertainty intervals where inference is made.
- Report all preregistered metrics; do not select only favorable outcomes.
- Correct or clearly limit families of multiple inferential comparisons.
- Treat missing, malformed, excluded, and failed observations explicitly.
- Do not treat repeated deterministic runs as independent samples.
- Do not infer practical value from statistical significance alone.

### Engineering Validity

- Pin code, corpus, schema, policy, dependency, and environment versions.
- Use immutable inputs and content hashes.
- Separate corpus defects, harness defects, environment variance, and system behavior.
- Compare equivalent inputs and conditions.
- Preserve determinism, traceability, diagnostics, minority evidence, and failure evidence.
- Require a material effect against a declared engineering threshold before recommending implementation.
- Keep latency descriptive unless an operational requirement and measurement protocol are approved.

## Publication Standard

Published research shall include:

- immutable question, protocol version, and preregistration timestamp;
- exact artifacts, commits, tags, hashes, environment, and execution dates;
- all primary and secondary results, including null and negative findings;
- deviations from protocol and their consequences;
- exclusions, missing data, anomalies, and failed runs;
- uncertainty, limitations, threats to validity, and unresolved questions;
- funding, authorship, reviewer roles, and conflicts of interest where applicable;
- a reproducibility manifest and verification status;
- a statement that findings are advisory and confer no runtime or governance authority.

Corrections create a new version and preserve the original publication. Retraction records remain visible.

## Ethics and Governance

- No human-subject or personal-data research without a separately approved ethics and privacy protocol.
- No secret, credential, production, or sensitive dataset may enter a corpus without authorization and controls.
- No provider or model may be invoked without explicit scope, data-handling review, and cost authorization.
- Provider/model identity must not become authority, confidence, rank, score, or vote weight.
- GG-02 remains authoritative for governed decisions.
- Research must not modify or bypass LOCKED components.
- A research result may recommend review; it may not authorize implementation or integration.

## Relationship to Validation

The Phase 3A validation methodology is the permanent certification baseline. Research uses it for reproducibility, immutable evidence, independent gates, and historical integrity. Research questions may introduce study-specific metrics, but may not weaken Foundation 1.0 release gates or replace them with an aggregate score.
