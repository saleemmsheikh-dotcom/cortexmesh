# Replay Corpus Review Process

## Purpose

Define review roles, required evidence, decision states, and release gates for replay corpus authoring and certification.

## Roles

### Replay Author

Proposes scenarios and cases, completes metadata, documents rationale, and responds to findings. The author cannot certify a release solely from observed implementation output.

### Expectation Reviewer

Reviews expected planning, evidence, consensus, synthesis, and diagnostic behavior against architecture and validation principles. Confirms expectations have an independent rationale.

### Schema and Integrity Reviewer

Reviews schema validity, references, ordering, semantic versioning, canonical hashes, manifest construction, and immutable publication mechanics.

### Comparator Reviewer

Reviews comparator choice and exclusions. Ensures compatible rules cannot hide preservation, traceability, diagnostic, or advisory-boundary failures.

### Sensitivity Reviewer

Required for any non-synthetic source scenario. Confirms sanitization, provenance, retention, and absence of identity-bearing decision inputs.

### Release Certifier

Confirms checklist completion and signs the release-specific certification record. Certification is an engineering release status, not GG-02 governance authority.

Roles may be performed by the same person where staffing requires, but the record must identify each review function and explicitly disclose non-independent review.

## Review States

1. `DRAFT` - authoring incomplete; not valid for baseline use.
2. `EXPECTATION REVIEW` - rationale and expected outcomes under review.
3. `SCHEMA REVIEW` - fixture, metadata, references, and ordering under review.
4. `COMPARATOR REVIEW` - comparison rules and exclusions under review.
5. `APPROVED FOR CORPUS` - case may enter a proposed release.
6. `RELEASE CANDIDATE` - manifest and coverage frozen for certification testing.
7. `CERTIFIED` - exact release passed all gates and has approval record.
8. `FAILED` - blocking findings remain; publication prohibited.
9. `SUPERSEDED` - historical certified release retained but no longer current.

## Case Review Requirements

Every case review confirms:

- scenario reference and expectation rationale;
- original and normalized intent;
- expected capability, agent, and execution plans;
- simulated output provenance and no invocation;
- expected evidence characteristics and trace links;
- consensus category, precedence, minority, and divergence behavior;
- all synthesis sections and explicit empty states;
- diagnostics, assumptions, and limitations;
- comparator kind, included/excluded paths, and compatibility rules;
- minimum metadata and canonical ordering;
- prohibited semantics and identity boundaries.

A case with ambiguous correctness must be revised, split, or marked outside the release; observed engine behavior is not sufficient rationale.

## Dataset Review Requirements

- Scenario-family and metric coverage matrix is complete.
- Every claimed comparator is covered by tests.
- No aggregate claim hides a failed case.
- Case/scenario identifiers and references are unique and valid.
- Corpus version transition matches change content.
- Manifest and item hashes recompute.
- Known limitations and excluded domains are explicit.
- Historical corpus versions remain available.
- Certification data matches the exact release candidate.

## Finding Severity

| Severity | Meaning | Release effect |
| --- | --- | --- |
| Blocking | Hash/reference failure, missing required expectation, prohibited semantics, sensitive leakage, invalid version, untested comparator, or preservation gap | Certification prohibited |
| Material | Coverage, rationale, diagnostic, or compatibility weakness that may change validation meaning | Must resolve or explicitly remove affected claim/case from release |
| Editorial | Wording or presentation issue with no fixture, expectation, hash, or semantic effect | May be corrected before publication; post-publication correction requires version rules |

## Certification Process

1. Freeze a release candidate and compute hashes.
2. Run schema/manifest/certification mixin tests.
3. Run focused dataset tests and full regression.
4. Complete the certification checklist.
5. Resolve all blocking and material findings.
6. Recompute hashes after any change.
7. Verify version, schema, counts, and comparator coverage.
8. Record validation status, approver, approval timestamp, evidence references, and limitations.
9. Publish immutably only when status is `CERTIFIED`.

## Acceptance Criteria

A release is accepted only when every checklist item is satisfied, all tests pass, review evidence is complete, certification matches the manifest exactly, and no runtime/Local AI/LOCKED boundary is crossed.

Certification permits dataset use for isolated validation only. It does not authorize orchestration execution, runtime replay, integration, adaptation, optimization, or governance action.

## Recommendation

**READY FOR FIRST CERTIFIED REPLAY DATASET**
