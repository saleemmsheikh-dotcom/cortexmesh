# Phase 3A Replay Corpus Schema

## 1. Purpose

Define the architecture-level logical schema for versioned replay scenarios, cases, datasets, metadata, results, and comparisons.

This document does not select a storage format or implement serialization. A later implementation milestone may choose JSON or another deterministic format while preserving these contracts.

## 2. Common Conventions

- Identifiers are non-empty, stable, unique within their namespace, and never reused for changed content.
- Collections that have no semantic order use canonical identifier ordering.
- Required empty values are represented explicitly, not omitted.
- References must resolve within the declared dataset or an explicitly versioned external baseline.
- All timestamps use UTC ISO 8601 and are descriptive metadata.
- Content hashes use a declared algorithm over a versioned canonical representation.
- Unknown fields are rejected unless the schema version explicitly permits extensions.
- Provider/model identity is never a decision, expectation, grouping, or comparison key.

## 3. ReplayMetadata

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `phase_version` | string | Yes | Identifies Phase 3A validation record version. |
| `architecture_version` | string | Yes | Identifies replay architecture/schema baseline. |
| `replay_corpus_version` | string | Yes | Immutable corpus version. |
| `validation_framework_version` | string | Yes | Version of metric definitions and gates. |
| `component_versions` | mapping string to string | Yes | Includes relevant Phase 2C components and repository commit/tag. |
| `timestamp` | UTC timestamp | Yes | Descriptive creation/publication/execution time. |
| `source_scenario` | string | Yes | Stable `ReplayScenario` reference. |
| `schema_version` | string | Yes | Logical schema version. |
| `provenance` | mapping | Yes | Descriptive source and review provenance only. |
| `integrity` | mapping | Yes | Hash algorithm, canonicalization version, and content hash. |

Prohibited metadata semantics include authority, confidence, score, rank, vote, vote weight, governance approval, provider preference, and model preference.

## 4. ReplayScenario

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `scenario_id` | string | Yes | Stable unique identifier. |
| `title` | string | Yes | Human-readable scenario name. |
| `purpose` | string | Yes | Validation proposition. |
| `category` | enum | Yes | Declared scenario family. |
| `source_description` | string | Yes | Origin and context without sensitive live data. |
| `metric_coverage` | tuple of metric IDs | Yes | At least one Phase 3A metric. |
| `expected_behavior_rationale` | string | Yes | Independent basis for expected outcome. |
| `assumptions` | tuple of strings | Yes | Explicit, may be empty. |
| `limitations` | tuple of strings | Yes | Explicit, may be empty. |
| `sensitivity` | enum | Yes | Synthetic, sanitized, or restricted; restricted publication prohibited without review. |
| `sanitization_record` | mapping | Conditional | Required for non-synthetic source material. |
| `review` | mapping | Yes | Author, expectation reviewer, state, and review date. |
| `case_ids` | tuple of strings | Yes | Must resolve to derived cases. |
| `metadata` | ReplayMetadata | Yes | Version and integrity context. |

## 5. ReplayCase

### 5.1 Identity and Input

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `case_id` | string | Yes | Stable unique identifier tied to content hash. |
| `scenario_id` | string | Yes | Resolves to one scenario. |
| `title` | string | Yes | Concise case name. |
| `original_intent` | mapping or string | Yes | Original provider-neutral request input. |
| `normalized_intent` | mapping | Yes | Expected normalized objective, task type, domain, constraints, context terms, and permitted provenance. |
| `dependencies` | tuple | Yes | Expected role dependencies, may be empty. |
| `simulated_outputs` | mapping | Yes | Keyed by expected step identifier; contains descriptive outputs only. |

### 5.2 Expected Planning

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `expected_capability_requirements` | tuple | Yes | Canonically ordered capability, reason/characteristic, and required state. |
| `expected_agent_plan` | mapping | Yes | Expected roles, capability coverage, and allowed diagnostics. |
| `expected_execution_plan` | mapping | Yes | Expected steps, dependencies, ordering, parallel groups, and diagnostics. |

### 5.3 Expected Evidence and Output

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `expected_evidence_characteristics` | mapping | Yes | Record count/IDs, roles, capabilities, required fields, preservation rules, and trace relationships. |
| `expected_consensus_classification` | enum | Yes | Exact, compatible, partial, material divergence, or insufficient evidence. |
| `expected_consensus_characteristics` | mapping | Yes | Required agreement/divergence/minority/unresolved identifiers and advisory marker. |
| `expected_synthesis_characteristics` | mapping | Yes | Ten-section coverage, required statements/identifiers, empty states, and preservation rules. |
| `expected_diagnostics` | tuple | Yes | Required, permitted, and prohibited diagnostic patterns by stage. |

### 5.4 Validation Contract

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `comparator_kind` | enum | Yes | Exact or compatible for primary expected-result comparison. |
| `comparison_rules` | mapping | Yes | Explicit included/excluded paths and compatibility rules. |
| `metric_expectations` | mapping | Yes | Applicable metric IDs and case-level expected result. |
| `prohibited_semantics` | tuple | Yes | Includes authority, scoring, confidence, ranking, voting, governance, and provider/model decision use. |
| `metadata` | ReplayMetadata | Yes | Version, source, component, and integrity context. |

## 6. ReplayVersion

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `version` | semantic version | Yes | Immutable corpus release identifier. |
| `schema_version` | string | Yes | Schema used by every included item. |
| `parent_version` | semantic version or null | Yes | Null only for initial corpus. |
| `change_class` | enum | Yes | Major, minor, or patch. |
| `change_rationale` | string | Yes | Explains publication need. |
| `added_case_ids` | tuple | Yes | Explicit, may be empty. |
| `retired_case_ids` | tuple | Yes | Remain available historically. |
| `superseded_case_map` | mapping | Yes | Old-to-new references where applicable. |
| `publication_timestamp` | UTC timestamp | Yes | Descriptive. |
| `manifest_hash` | string | Yes | Hash of canonical dataset manifest. |
| `compatibility_notes` | tuple | Yes | Explicit, may be empty. |

Validation rules:

- new case means minor or major version;
- case input or expectation change means a new case hash and minor or major version;
- incompatible schema/meaning change means major version;
- patch cannot alter executable or expected behavior;
- published content cannot be overwritten.

## 7. ReplayDataset

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `dataset_id` | string | Yes | Stable corpus family identifier. |
| `name` | string | Yes | Human-readable name. |
| `description` | string | Yes | Scope and intended use. |
| `replay_version` | ReplayVersion | Yes | Published immutable version. |
| `scenario_ids` | tuple | Yes | Canonically ordered and resolvable. |
| `case_ids` | tuple | Yes | Canonically ordered and resolvable. |
| `coverage_matrix` | mapping | Yes | Scenario families and metrics to case IDs. |
| `framework_mapping` | mapping | Yes | Metric definition/version references. |
| `component_compatibility` | mapping | Yes | Supported reference baseline versions. |
| `known_limitations` | tuple | Yes | Explicit, may be empty. |
| `excluded_domains` | tuple | Yes | Explicit, may be empty. |
| `manifest_entries` | tuple | Yes | Path/reference, content hash, size, schema/version. |
| `metadata` | ReplayMetadata | Yes | Publication and integrity record. |

## 8. ReplayResult

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `result_id` | string | Yes | Unique run identifier. |
| `case_id` | string | Yes | Resolves to immutable case. |
| `dataset_version` | string | Yes | Exact corpus version. |
| `component_versions` | mapping | Yes | Exact evaluated baseline. |
| `environment` | mapping | Yes | Interpreter, platform class, and relevant settings. |
| `intermediate_artifacts` | mapping | Yes | Resolution, agent plan, execution plan, evidence, consensus, synthesis. |
| `orchestration_result` | mapping | Yes | Canonical final result. |
| `diagnostics` | tuple | Yes | Actual stage-attributed diagnostics. |
| `traceability` | mapping | Yes | Evidence, step, trace, correlation, and section links. |
| `artifact_hashes` | mapping | Yes | Canonical hashes by artifact. |
| `metric_observations` | mapping | Yes | Case-level raw observations, not authority scores. |
| `deviations` | tuple | Yes | Structured expected/actual differences. |
| `state` | enum | Yes | Pass, fail, or inconclusive per declared comparator. |
| `metadata` | ReplayMetadata | Yes | Run timestamp, provenance, and integrity. |

## 9. ReplayComparator

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `comparator_id` | string | Yes | Stable comparator contract identifier. |
| `kind` | enum | Yes | Exact, compatible, regression, or future runtime. |
| `version` | string | Yes | Comparator rule version. |
| `left_reference` | string | Yes | Expected result or baseline result identifier. |
| `right_reference` | string | Yes | Observed or comparison result identifier. |
| `included_paths` | tuple | Yes | Explicit comparison scope. |
| `excluded_paths` | tuple | Yes | Only schema-authorized nondeterministic/descriptive fields. |
| `compatibility_rules` | mapping | Conditional | Required for compatible/future mapping comparisons. |
| `matches` | tuple | Yes | Structured matched paths. |
| `differences` | tuple | Yes | Structured path, expected, actual, and rationale. |
| `outcome` | enum | Yes | Match, compatible, regression, improvement, inconclusive, or failure as allowed by kind. |
| `artifact_hash` | string | Yes | Integrity of comparison record. |

Comparator outcomes are descriptive validation states. They cannot determine live provider, agent, score, confidence, rank, authority, vote, or governance action.

## 10. ReplayCertification

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `certification_id` | string | Yes | Stable identifier unique to the corpus release. |
| `replay_corpus_version` | semantic version | Yes | Exact certified dataset version. |
| `schema_version` | string | Yes | Exact certified schema version. |
| `content_hash` | string | Yes | Must equal the published manifest hash. |
| `replay_case_count` | integer | Yes | Must equal manifest case count. |
| `replay_scenario_count` | integer | Yes | Must equal manifest scenario count. |
| `comparator_coverage` | tuple of enums | Yes | Exact, compatible, regression, and any separately authorized comparator. |
| `validation_status` | enum | Yes | Draft, failed, or certified. |
| `approved_at` | UTC timestamp or null | Conditional | Required only for certified status. |
| `approved_by` | string or null | Conditional | Recorded release reviewer; creates no governance authority. |
| `evidence_references` | tuple | Yes | Manifest, validation, and review records. |
| `known_limitations` | tuple | Yes | Explicit, may be empty. |

Certification validation fails if any bound version, hash, count, or comparator coverage differs from the dataset release. Changed content requires a new corpus version and certification.

## 11. Comparator Semantics

### Exact Replay

- Included canonical paths must be equal.
- Any undeclared difference fails comparison.
- Only schema-declared timestamps/run IDs may be excluded.

### Compatible Replay

- Exact equality is preferred.
- Every permitted difference requires a named rule and rationale.
- Evidence identifiers, minority evidence, unresolved divergence, diagnostics required by the case, and traceability cannot be excluded.

### Regression Replay

- Both results must reference the same immutable corpus version or an explicit migration mapping.
- Differences are reported per case and metric before aggregation.
- “Improvement” requires the validation framework comparator requirement and cannot hide a degradation.

### Future Runtime Replay

- Reserved and disabled in the initial schema implementation.
- Requires a separately versioned source mapping and sanitized read-only artifacts.
- Cannot use runtime winner, authority, confidence, score, rank, provider, or model identity as expected truth.

## 12. Schema Validation Failures

Publication must fail for:

- missing required fields or unresolved references;
- duplicate identifiers;
- noncanonical ordering where required;
- invalid version transition;
- hash mismatch;
- changed content under an existing published version;
- new case in a patch release;
- prohibited decision/governance semantics;
- provider/model identity used outside descriptive provenance;
- expected outcomes without rationale or review state;
- comparison exclusions that could hide evidence loss.
- certified release metadata that does not match its immutable manifest.

## 13. Recommendation

**READY FOR REPLAY CORPUS IMPLEMENTATION**
