# EXP-001 Protocol Review

## Review Record

| Field | Value |
| --- | --- |
| Research program | RP-001 |
| Experiment | EXP-001 |
| Protocol | EXP-001 Protocol v1.0 |
| Preregistration | RP-001 Preregistration v1.1 |
| Reviewer role | Product Owner |
| Review date | 2026-07-13 |
| Decision | EXP-001 PROTOCOL APPROVED |
| Execution authorization | NOT GRANTED BY THIS REVIEW |
| Data collected at review | None |

## Review Assessment

| Area | Status |
| --- | --- |
| Research integrity | PASS |
| Experimental design | PASS |
| Preregistration | PASS |
| Comparator selection | PASS |
| Metric design | PASS |
| Statistical validity | PASS |
| Governance compliance | PASS |
| LOCKED boundary | PASS |

## Review Findings

- The revised baseline-characterization design precedes all data collection.
- Preregistration v1.0 remains preserved at commit `42453be`.
- Preregistration v1.1 records the material design change before execution.
- The 24-case, ten-repetition design is proportionate for characterization.
- Exact repetition and certified expectation comparators are sufficient and appropriately bounded.
- Independent metrics prevent a composite score from masking an anomaly.
- No runtime, provider, adaptive, authority, scoring, voting, confidence, governance, or LOCKED change is proposed.

## Required Administrative Addition

The execution log records an environment fingerprint containing:

- engine commit;
- replay corpus hash;
- validation framework version;
- Python version;
- operating system;
- CPU and architecture;
- timestamp;
- random seed, if applicable;
- locale;
- timezone;
- dependency and configuration hashes.

## Authorization Preconditions

Before execution authorization is recorded, verify exactly:

1. the protocol hash is recorded;
2. Replay Corpus v1.1 certification and content hash are valid;
3. `phase2c-complete` resolves to commit `a72d11f`.

If all three gates pass, authorization may be recorded in a separate commit using the exact statement:

**EXP-001 AUTHORIZED FOR EXECUTION**

## Decision Boundary

This review approves the protocol for the authorization check. It does not authorize execution, data collection, provider invocation, runtime integration, engine modification, or LOCKED modification.
