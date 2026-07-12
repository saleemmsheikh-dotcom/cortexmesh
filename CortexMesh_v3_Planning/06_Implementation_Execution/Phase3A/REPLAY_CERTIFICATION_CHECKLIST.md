# Replay Dataset Certification Checklist

## Release Identity

- Dataset ID:
- Replay corpus version:
- Schema version:
- Parent corpus version:
- Change class: major / minor / patch
- Manifest/content hash:
- Scenario count:
- Case count:
- Comparator coverage:
- Validation framework version:
- Component baseline/tag:

## Version and Immutability

- [ ] Semantic-version transition is valid.
- [ ] New or changed cases use at least a minor release.
- [ ] Patch release changes no executable input, expectation, ordering, or case hash.
- [ ] Dataset content is canonically ordered.
- [ ] Historical version remains retained and addressable.
- [ ] Publication target is immutable.

## Scenario and Case Review

- [ ] Every scenario has purpose, category, source, metric coverage, and independent expectation rationale.
- [ ] Every case resolves to one scenario.
- [ ] Every scenario case reference resolves.
- [ ] Identifiers are unique and stable.
- [ ] Expected outcomes were reviewed before baseline observation.
- [ ] Synthetic cases are preferred.
- [ ] Derived cases have sensitivity and sanitization approval.
- [ ] Known exclusions and limitations are explicit.

## Metadata

- [ ] Phase version present.
- [ ] Architecture version present.
- [ ] Replay corpus version present.
- [ ] Validation framework version present.
- [ ] Component versions and repository baseline present.
- [ ] Schema version present.
- [ ] UTC timestamp present.
- [ ] Source scenario present.
- [ ] Provenance and integrity context present.

## Expected Pipeline Coverage

- [ ] Original and normalized intent recorded.
- [ ] Expected capabilities recorded.
- [ ] Expected agent plan recorded.
- [ ] Expected execution plan recorded.
- [ ] Simulated outputs recorded.
- [ ] Evidence characteristics recorded.
- [ ] Consensus category and signals recorded.
- [ ] Minority and unresolved divergence expectations recorded where applicable.
- [ ] All ten synthesis section expectations recorded.
- [ ] Diagnostics recorded by stage.
- [ ] Traceability requirements recorded.

## Comparator Certification

- [ ] Exact comparator behavior tested if claimed.
- [ ] Compatible comparator rules are field-level, reviewed, and tested if claimed.
- [ ] Regression comparator behavior tested if claimed.
- [ ] Compatibility rules cannot hide evidence, minority, divergence, diagnostics, traceability, or advisory markers.
- [ ] Future runtime comparator is absent.

## Integrity Validation

- [ ] Every scenario content hash recomputes.
- [ ] Every case content hash recomputes.
- [ ] Manifest hash recomputes.
- [ ] Manifest dataset identifier and versions match.
- [ ] Manifest scenario/case counts match content.
- [ ] Manifest comparator coverage matches tested coverage.
- [ ] Replay certification fields exactly match the manifest.

## Boundary Verification

- [ ] No runtime changes.
- [ ] No Local AI changes or imports.
- [ ] No provider or agent invocation.
- [ ] No orchestration execution during authoring/certification tests.
- [ ] No LOCKED component changes.
- [ ] No provider/model decision use.
- [ ] No score, confidence, rank, authority, voting, or governance semantics.

## Test Evidence

- Focused certification tests:
- Full regression result:
- Whitespace result:
- Changed-path/LOCKED audit:
- Evidence record:

## Certification Decision

- Validation status: DRAFT / FAILED / CERTIFIED
- Approved by:
- Approved at:
- Certification ID:
- Evidence references:
- Known limitations:

A certified decision applies only to the exact version, schema, manifest hash, counts, and comparator coverage above. Any content change requires a new release and certification.
