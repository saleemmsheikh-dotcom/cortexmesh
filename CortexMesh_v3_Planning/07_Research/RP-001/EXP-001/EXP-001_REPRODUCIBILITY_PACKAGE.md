# EXP-001 Reproducibility Package

## Status

PACKAGE PRODUCED - INDEPENDENT REPRODUCTION PENDING

## Package Identity

| Field | Value |
| --- | --- |
| Experiment | RP-001/EXP-001 |
| Package version | 1.0 |
| Raw package manifest hash | `8ad3780feffd63c46d6a09183105bab0cda81912407632e89c00faf98c0c4651` |
| Analysis manifest hash | `60e2f9c1ac66d414d611f7a81f3640b39a0fa714c74dc63a03b1f8916de7b646` |
| Collection status | COMPLETE - 240/240 |
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

## Produced Artifact Index

| Artifact | SHA-256 |
| --- | --- |
| Raw observations | `6551e6d6fd0ca6f661221a9be793802ddba1c301de0c44f07c5b1842ad6b962e` |
| Raw run manifest | `b54cae14f689c7764678d63c984c1654ef2499b1a4527966e711cc2d5f162ab3` |
| Raw package manifest | `8ad3780feffd63c46d6a09183105bab0cda81912407632e89c00faf98c0c4651` |
| Frozen collection harness | `885248766376d4d80c4f14c34077c4fe043879e2243e3b2fa3981a802290ec23` |
| Analysis metrics | `30ff1aabb777e4d7c7eda53363c7715f35cab3bf439b03fc63e8a37c631460a6` |
| Per-case results | `c29fdebfffd83cf40ff7ddb9073b4cf6ab1d84a23d85b2eee5df149e90f685d4` |
| Difference records | `10dd87be746433bcc64bc3bdd12ae7cf15a58f85f72b75a484ed3016d4cf552e` |
| Analysis manifest | `60e2f9c1ac66d414d611f7a81f3640b39a0fa714c74dc63a03b1f8916de7b646` |
| Analysis harness | `0c60efcbc4107ff1bfe40fb1ea108b88030f751005313ca43180fa44350d9d11` |

Raw artifacts are frozen. Analysis artifacts bind to the raw observations hash. No independent reproduction has yet been attempted.
