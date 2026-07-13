# RP-001 Research Method

## Method Status

DESIGN ONLY - EXECUTION REQUIRES A PREREGISTERED PROTOCOL

## Study Design

RP-001 is a paired, controlled, offline comparison. Each eligible research case is evaluated under a single-path control and an evidence-based orchestration condition using the same source information, constraints, and declared resource budget.

The unit of analysis is the replay case, not an individual deterministic rerun. Repetitions test determinism and measurement stability; they do not inflate statistical sample size.

## Case Design and Sampling

Before execution, the study shall publish a new immutable research corpus version derived from, but not editing, certified Phase 3A assets. Cases shall be stratified across:

- complementary evidence;
- exact and compatible agreement;
- partial agreement;
- material divergence;
- minority evidence;
- insufficient evidence;
- malformed and prohibited semantic inputs;
- architecture, implementation, risk, governance-boundary, and diagnostic tasks.

Case inclusion, exclusion, stratification, and minimum sample size must be frozen before results are observed. Exploratory cases must be labeled and analyzed separately.

## Controls

| Control | Purpose |
| --- | --- |
| Paired task/source input | Prevent task difficulty or information differences from explaining effects |
| Fixed input and output budgets | Prevent resource imbalance |
| Frozen corpus and rubric | Prevent expectation drift |
| Sealed component versions | Prevent implementation drift |
| Deterministic ordering and identifiers | Preserve repeatability and traceability |
| Blinded or independent expectation review where practicable | Reduce evaluator allegiance bias |
| Negative and malformed cases | Verify rejection and diagnostic behavior |
| Authority-leakage probes | Verify prohibited semantics cannot affect decisions |
| Separate environment reproduction | Identify environment-specific variance |

## Measurements

Primary engineering metrics:

- evidence completeness;
- evidence-to-claim traceability;
- minority evidence preservation;
- unresolved divergence preservation;
- synthesis completeness;
- diagnostic completeness and actionability.

Protected metrics:

- determinism;
- replay reproducibility;
- pipeline stability;
- provenance preservation;
- prohibited-semantic rejection;
- GG-02 and LOCKED-boundary compliance.

Secondary descriptive metrics:

- planning and pipeline latency;
- output size;
- diagnostic volume;
- unresolved-question count;
- failure and exclusion counts.

Each metric requires a machine-checkable definition where possible, a statement-level rubric where judgment is necessary, and an inter-reviewer agreement method for subjective annotations. No overall score is permitted.

## Analysis Plan

- Report each metric independently by condition and case stratum.
- For paired quantitative outcomes, report paired differences, effect sizes, and uncertainty intervals.
- Use a preregistered paired test only where its assumptions and sample size are justified.
- For bounded pass rates, report counts, denominators, rates, and suitable intervals.
- For human-coded results, report reviewer agreement and adjudication separately from system performance.
- Declare and control families of multiple inferential comparisons or label them exploratory.
- Report malformed, missing, excluded, and failed cases; do not silently remove them.
- Separate system defects, corpus defects, harness defects, rubric ambiguity, and environment variance.
- Do not claim improvement when any protected metric regresses.

## Statistical Validity Threats

- non-independent repeated runs;
- small or unrepresentative corpus;
- post hoc metric selection;
- multiple comparisons;
- ceiling effects from synthetic cases;
- evaluator and author overlap;
- ambiguous ground truth;
- model/provider variability if later authorized.

Mitigation requires preregistration, stratification, immutable inputs, independent review where practicable, complete reporting, uncertainty estimates, and explicit exploratory labels.

## Engineering Validity Threats

- mismatched budgets or source context;
- changing sealed components;
- corpus leakage into candidate construction;
- hidden provider/model effects;
- environment or dependency drift;
- conflating better formatting with better evidence;
- treating advisory consensus as correctness or authority.

Mitigation requires paired controls, pinned versions, content hashes, provenance, environment manifests, boundary probes, statement-level evaluation, and reruns in a separately declared environment.

## Reproducibility Package

Every executed release shall retain:

- charter, protocol, hypotheses, analysis plan, and authorization;
- corpus, schema, manifest, certification, and content hashes;
- code commit/tag and component versions;
- environment, dependencies, configuration, seed, and timestamps;
- raw inputs, outputs, diagnostics, failures, exclusions, and logs;
- derived measurements and analysis artifacts;
- reviewer annotations and adjudication records;
- exact commands and a reproduction guide;
- publication, corrections, and replication status.

Secrets and prohibited data must never be committed. Approved sensitive artifacts require a separately governed retention location and a reproducible non-sensitive manifest.

## Stop Conditions

Execution stops and results remain preserved if:

- a LOCKED or runtime modification becomes necessary;
- authority, scoring, confidence, ranking, voting, or governance leakage is detected;
- personal, secret, or unauthorized data is encountered;
- corpus, protocol, or baseline integrity cannot be verified;
- conditions are not resource-equivalent;
- required authorization is missing;
- a safety, cost, or provider boundary is exceeded.

## Publication Method

The final report shall distinguish preregistered from exploratory analysis and observation from inference. It shall publish null, negative, adverse, and inconclusive results; disclose deviations; state limitations and non-claims; and link the reproducibility manifest. Any later implementation recommendation must be a separate proposal.
