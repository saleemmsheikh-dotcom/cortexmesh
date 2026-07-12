# Phase 3A M4 - Replay Authoring Guide

## Purpose

Define the controlled workflow for authoring, reviewing, publishing, and certifying replay datasets for the isolated CortexMesh Reference Orchestration Engine.

## Authoring Principles

1. Expectations are written before implementation output is observed.
2. Scenario rationale is independent from executable fixture encoding.
3. Synthetic cases are preferred; derived cases require sanitization review.
4. Every expected artifact is attributable to a validation principle or metric.
5. Minority, divergence, diagnostics, provenance, and traceability are case-level obligations.
6. Compatibility rules are explicit and narrow.
7. Published corpus content is immutable.
8. Certification binds one exact release and creates no governance authority.
9. Runtime, Local AI, provider invocation, and orchestration execution remain outside authoring.

## Replay Author Workflow

### 1. Propose Scenario

Create a stable scenario identifier and record:

- purpose and category;
- source description;
- independent expected-behavior rationale;
- metric coverage;
- assumptions and limitations;
- sensitivity and sanitization status;
- proposed derived cases.

### 2. Review Expectation Basis

An expectation reviewer confirms that the rationale follows the published architecture and policies rather than copied implementation output. Ambiguous consensus or compatibility expectations are rejected or marked for domain review.

### 3. Author Cases

Use `REPLAY_CASE_TEMPLATE.md`. Each case must include original/normalized intent, expected planning artifacts, simulated outputs, evidence expectations, consensus expectations, synthesis expectations, diagnostics, comparator rules, metadata, and prohibited semantics.

### 4. Validate Schema and References

Run the reusable certification mixin and dataset-specific tests. Confirm canonical ordering, unique identifiers, scenario/case references, semantic version, metadata, content hashes, comparator coverage, and prohibited-field rules.

### 5. Review Coverage

Map every case to scenario family and Phase 3A metrics. A corpus release must not claim coverage for an unrepresented category. Aggregate coverage never waives minority or material-divergence cases.

### 6. Build Manifest

Generate the manifest from canonically ordered scenarios and cases. Record schema version, corpus version, content hashes, comparator coverage, and dataset identifier. Recompute and verify the manifest hash independently.

### 7. Certify Release

Complete `REPLAY_CERTIFICATION_CHECKLIST.md`. Certification binds exact version, schema, hash, counts, comparator coverage, evidence, approval date, and reviewer. Any mismatch blocks publication.

### 8. Publish Immutably

Publish the certified dataset as a new version. Do not edit files in place. Corrections require a new semantic version under the architecture rules, with historical releases retained.

## Minimum Metadata

Every case and scenario includes:

- Phase version;
- architecture version;
- replay corpus version;
- validation framework version;
- component versions and repository baseline;
- schema version;
- UTC timestamp;
- source scenario;
- descriptive provenance;
- canonicalization/hash context;
- author and expectation-review record in the publication package.

Metadata cannot contain provider/model preference, score, confidence, rank, authority, vote weight, or governance approval semantics.

## Comparator Requirements

### Exact

Use when all included canonical paths must match. Exclusions are limited to schema-declared run identifiers or timestamps.

### Compatible

Use only with reviewed field-level equivalence rules. It cannot exclude evidence identifiers, minority evidence, unresolved divergence, required diagnostics, traceability, or advisory markers.

### Regression

Use for two identified component baselines against the same immutable corpus version. Report every degradation separately; improvements cannot cancel failures.

### Future Runtime

Not available. Its presence in authoring content or comparator coverage fails certification until a separate design is authorized.

## Expected Evidence Characteristics

Each applicable case declares:

- expected record identifiers and count;
- source role and fulfilled capability;
- output/claim characteristics;
- assumptions and limitations, including explicit empty states;
- diagnostics by pipeline stage;
- descriptive provenance requirements;
- trace and correlation relationships;
- minority and unmatched record preservation;
- agreement and divergence signal relationships;
- synthesis section and evidence-reference coverage;
- prohibited semantics and identity decision use.

## Acceptance Criteria

A dataset is ready for certification only when:

- all scenarios and cases pass schema/reference validation;
- expectations have independent review evidence;
- required metadata is complete;
- ordering and hashes reproduce;
- manifest content matches the dataset;
- claimed comparator coverage is tested;
- every required scenario family is represented or explicitly excluded;
- no preservation-critical field is hidden by compatibility rules;
- no runtime, Local AI, provider invocation, or orchestration execution occurs;
- all focused and full regression tests pass.

## Recommendation

**READY FOR FIRST CERTIFIED REPLAY DATASET**
