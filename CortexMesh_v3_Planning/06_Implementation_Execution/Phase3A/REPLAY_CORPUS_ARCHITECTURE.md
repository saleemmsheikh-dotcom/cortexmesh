# Phase 3A M2 - Replay Corpus Architecture

## 1. Purpose

Define the versioned canonical validation dataset for the isolated CortexMesh Reference Orchestration Engine.

The replay corpus supplies reviewed inputs and independently declared expectations. It does not invoke live agents or providers, modify runtime state, create authority, or authorize integration.

## 2. Architectural Goals

- Make validation cases explicit, reviewable, immutable, and reproducible.
- Separate source scenarios from executable cases and observed results.
- Cover the complete Phase 2C planning, evidence, consensus, synthesis, and orchestration pipeline.
- Preserve minority evidence, material divergence, diagnostics, provenance, and traceability.
- Support exact, compatible, regression, and future runtime comparisons without conflating their semantics.
- Bind every published dataset to component and framework versions.

## 3. Canonical Model

### 3.1 ReplayScenario

`ReplayScenario` is the human-reviewed validation proposition from which one or more replay cases are derived. It contains:

- stable scenario identifier;
- title, purpose, and category;
- source scenario description;
- validation principle and metric coverage;
- rationale for expected behavior;
- declared assumptions and limitations;
- sensitivity classification and sanitization record;
- reviewer and approval state for expectation publication;
- links to derived case identifiers.

A scenario is not directly executed. It prevents executable fixtures from becoming unexplained implementation snapshots.

### 3.2 ReplayCase

`ReplayCase` is one deterministic executable validation fixture. Each case records:

- original intent;
- normalized intent;
- expected capability requirements;
- expected agent plan;
- expected execution plan;
- simulated execution inputs;
- expected evidence characteristics;
- expected consensus classification;
- expected synthesis characteristics;
- expected diagnostics;
- case-level metadata and integrity hash.

Expectations are declared before baseline execution. They describe observable contracts, not private implementation steps beyond those intentionally exposed by the Phase 2C reference models.

### 3.3 ReplayDataset

`ReplayDataset` is the complete published corpus for one `ReplayVersion`. It contains:

- dataset identifier and description;
- replay version;
- ordered scenario manifest;
- ordered case manifest;
- coverage matrix;
- validation-framework mapping;
- component compatibility declaration;
- dataset integrity manifest and hash;
- publication record;
- known limitations and excluded domains.

Case ordering is canonical by stable case identifier. Ordering has no priority, rank, or authority meaning.

### 3.4 ReplayVersion

`ReplayVersion` identifies an immutable published corpus release. It contains:

- corpus semantic version;
- schema version;
- parent version, if any;
- publication timestamp;
- change classification and rationale;
- added, retired, or superseded case references;
- manifest hash;
- compatibility notes.

A version identifies content, not validation quality. Later versions do not retroactively change earlier results.

### 3.5 ReplayMetadata

`ReplayMetadata` binds a scenario, case, dataset, or result to reproducibility context. Required metadata includes:

- Phase version;
- architecture version;
- replay corpus version;
- validation framework version;
- component versions;
- timestamp;
- source scenario.

It also records schema version, repository commit/tag, environment class where applicable, provenance, authorship/review roles, and integrity hashes. Provider/model identity is prohibited as an expectation or comparator input; if present in a future sanitized source record, it remains descriptive provenance only.

### 3.6 ReplayResult

`ReplayResult` records one execution of one case against an identified reference baseline. It contains:

- result and case identifiers;
- replay and component versions;
- canonical intermediate artifacts;
- final orchestration result;
- actual diagnostics;
- observed trace/correlation relationships;
- artifact hashes;
- metric observations;
- deviation records;
- execution environment metadata;
- comparator outcome references;
- explicit pass, fail, or inconclusive state per metric.

The result never modifies the case expectation. A mismatch creates evidence; it does not rewrite the corpus.

### 3.7 ReplayComparator

`ReplayComparator` applies a named, versioned comparison contract to expected and observed artifacts. It produces structured differences without scoring, confidence adjustment, ranking, voting, provider preference, authority, or governance meaning.

Comparator output includes compared identifiers, comparator kind/version, matched fields, differences, excluded fields, rationale, and reproducibility hashes.

### 3.8 ReplayCertification

`ReplayCertification` is the release record for one immutable published corpus. It records:

- replay corpus and schema versions;
- dataset manifest/content hash;
- replay case and scenario counts;
- comparator coverage;
- validation status;
- certification timestamp and approval record;
- known limitations and evidence references.

Certification behaves like a software release attestation: it identifies exactly what was reviewed. It creates no governance authority and cannot be transferred to changed corpus content. Any new corpus version requires its own certification record.

## 4. Corpus Layers

The corpus is separated into:

1. `scenarios` - human rationale and expectation basis;
2. `cases` - canonical executable fixtures;
3. `manifests` - version, ordering, hashes, and coverage;
4. `expected` - reviewed expected artifacts or characteristics;
5. `results` - generated run evidence stored outside immutable published content;
6. `comparisons` - generated difference evidence stored outside immutable published content.

Results and comparisons reference a corpus version but do not alter it.

## 5. Required Scenario Families

The canonical dataset must cover:

- intent normalization and fallback behavior;
- capability resolution and missing coverage;
- agent-role planning;
- independent and dependent execution planning;
- exact agreement;
- compatible agreement;
- partial agreement;
- material divergence with precedence;
- insufficient evidence;
- minority and unmatched evidence preservation;
- assumptions, limitations, and diagnostics;
- provenance and trace/correlation preservation;
- missing, extra, or malformed simulated outputs;
- prohibited provider/model decision inputs;
- prohibited authority, score, confidence, rank, vote, vote-weight, and governance inputs;
- all ten synthesis sections and explicit empty states;
- full pipeline result preservation.

## 6. Publication Workflow

1. Propose scenario with rationale and metric coverage.
2. Review expected behavior independently of observed engine output.
3. Derive one or more cases using the current schema.
4. Validate schema, identifiers, references, prohibited fields, and canonicalization.
5. Review coverage and known exclusions.
6. Generate case and manifest hashes.
7. Publish a new immutable replay corpus version.
8. Issue a version-specific replay certification after manifest, schema, hash, coverage, and validation checks pass.
9. Execute validation results separately against that version.

Failed expectations are corrected only in a new version with an explicit rationale; the historical version remains available.

## 7. Versioning Model

Replay corpus versions use `major.minor.patch`:

- major: incompatible schema or expectation-semantics change;
- minor: one or more new, retired, or materially changed cases/scenarios;
- patch: metadata or documentation correction that cannot change executable inputs, expected outcomes, ordering, or hashes of existing cases.

Any new case requires at least a minor version. Any change to a published case input or expected outcome requires a new version and a new case hash. Published versions are immutable.

Historical datasets, schemas, manifests, and compatible component baselines remain addressable so their results can be reproduced.

Every published release has a distinct certification. Certification is invalid if its version, schema, manifest hash, case count, scenario count, or comparator coverage differs from the dataset.

## 8. Integrity and Reproducibility

- Each case has a canonical serialized representation and content hash.
- Each dataset manifest hashes the ordered scenario/case entries and referenced schema versions.
- Validation records bind commit, tag, corpus version, framework version, component versions, and environment.
- Timestamps are metadata and excluded from deterministic artifact equality where specified by schema.
- Generated results never overwrite prior results; repetitions receive distinct result identifiers.
- Canonicalization rules are versioned and cannot silently change.

## 9. Comparator Architecture

### Exact Replay

Compares canonical expected and actual artifacts for equality after only schema-declared exclusions. Used for determinism, exact contract, and artifact-hash validation.

### Compatible Replay

Applies explicit compatibility rules where multiple representations preserve the same declared semantics. Every allowed difference must be named and versioned. Compatibility cannot hide minority evidence, material divergence, missing traceability, or prohibited semantics.

### Regression Replay

Compares results from two identified reference component baselines against the same immutable corpus version. It reports preserved, improved, degraded, added, and removed behavior per metric. It does not rank providers/models or convert metrics into runtime authority.

### Future Runtime Replay

Reserved for a future separately authorized, read-only mapping of sanitized live artifacts into the replay schema. It is not implemented or authorized in Phase 3A M2. It must not invoke live agents, mutate runtime state, or treat runtime authority output as the replay expectation. A separate design, privacy/security review, and LOCKED-boundary assessment are required.

## 10. Governance and Runtime Boundary

- Replay expectations do not create governance policy.
- Comparator pass/fail states do not create authority or approval.
- GG-02 remains exclusively authoritative for Board decisions.
- Runtime remains unchanged.
- No Local AI, provider, agent, scoring, confidence, ranking, voting, authority, or governance behavior enters corpus execution.
- Any future runtime comparator remains deferred and separately governed.

## 11. Architecture Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Expected artifacts are copied from current output. | Corpus validates implementation against itself. | Require scenario rationale and expectation review before baseline execution. |
| Version proliferation obscures canonical status. | Users replay the wrong dataset. | Maintain one explicit current manifest while retaining immutable historical versions. |
| Patch releases change behavior. | Historical result meaning becomes unstable. | Prohibit case/input/expectation/hash changes in patch releases. |
| Compatibility rules are too broad. | Regressions or missing evidence are hidden. | Require named field-level rules and zero tolerance for preservation/traceability loss. |
| Future runtime artifacts contaminate canonical expectations. | Live authority behavior becomes an implicit oracle. | Keep runtime replay separate, read-only, deferred, and non-authoritative. |

## 12. Recommendation

**READY FOR REPLAY CORPUS IMPLEMENTATION**
