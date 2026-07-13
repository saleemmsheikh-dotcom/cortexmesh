# EXP-001 Reproducibility Package

## Status

SPECIFICATION COMPLETE - PACKAGE NOT YET PRODUCED

## Package Identity

| Field | Value |
| --- | --- |
| Experiment | RP-001/EXP-001 |
| Package version | PENDING |
| Manifest hash | PENDING |
| Collection status | NOT STARTED |
| Reproduction status | NOT ATTEMPTED |

## Required Contents

### Registered Design

- RP-001 charter, method, and success criteria;
- RP-001 Preregistration v1.1;
- authorized EXP-001 Protocol v1.0 and its hash;
- authorization identity and date;
- all deviation records.

### Immutable Baselines

- repository commit and registered tag resolutions;
- engine component versions;
- Replay Corpus v1.1 manifest, schema, certification, cases, and content hash;
- validation framework version;
- comparator and canonicalization definitions.

### Environment

- operating system and architecture;
- interpreter and dependency versions;
- locale, timezone, relevant environment variables, and configuration;
- clock and timing method;
- environment manifest hash.

### Execution Evidence

- exact commands and execution order;
- raw inputs and outputs for every case and repetition;
- diagnostics, timings, exit states, failures, and exclusions;
- execution log and machine-readable run manifest;
- canonical artifacts and comparison records.

### Analysis and Publication

- per-case measurements and aggregate independent metrics;
- latency observations;
- anomaly classifications and review evidence;
- results, discussion, and limitations;
- reproduction instructions and reproduction result;
- corrections or retractions, if any.

## Integrity Rules

- Every package file must appear in a deterministic manifest with path, size, and cryptographic content hash.
- Raw evidence is immutable after collection.
- Corrections and derived reanalysis create new versions without overwriting prior records.
- Secrets and unauthorized data must never be included.
- Missing artifacts must be reported; placeholders must not be represented as evidence.
- A reproduction must use a new run identifier and preserve differences from the original.

## Reproduction Procedure

After the original package is complete, a reproducer shall:

1. verify every manifest hash;
2. reconstruct the declared environment or record unavoidable variance;
3. execute the exact authorized commands in the registered order;
4. compare all canonical outputs and independent metrics;
5. record raw differences and classify environment variance separately;
6. publish `REPRODUCED`, `REPRODUCED WITH DECLARED VARIANCE`, `NOT REPRODUCED`, or `INVALID REPRODUCTION` with evidence.

No reproduction has been attempted because EXP-001 is not authorized or executed.
