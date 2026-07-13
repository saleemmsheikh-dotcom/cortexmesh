# EXP-001 Execution Log

## Status

DATA COLLECTION COMPLETE - EXECUTION LOG FROZEN - ANALYSIS NOT STARTED

## Authorization

| Field | Value |
| --- | --- |
| Protocol version | 1.0 |
| Authorization decision | AUTHORIZED |
| Authorized by | Product Owner |
| Authorization date | 2026-07-13 |
| Authorized protocol SHA-256 | `51d649de94b12eacb22c99b8efc343af42b6f250a5fe41b35337882a80194ff2` |
| Collection start | 2026-07-13T11:16:53.346126Z |
| Collection end | 2026-07-13T11:16:53.579461Z |
| Planned executions | 240 |
| Recorded executions | 240 |
| Raw package integrity | PASS |

## Environment Record

To be recorded after authorization and before the first execution:

| Field | Value |
| --- | --- |
| Run identifier | `RP-001/EXP-001@2026-07-13T11:16:53Z` |
| Environment fingerprint hash | `20a809335a76a9bdbf6125ec9b23bf13358c1646677bda31e37820226125a937` |
| Engine commit | `a72d11fe57f9026ab307efeaf962b97095527039` |
| Replay corpus hash | `20e4b446097db5b3dcaa6fbf214218038c9c297d2e60bbbc57b9d24bc1e59788` |
| Validation framework version | `phase3a-complete` / `6c41364c56883043c20d237d37b8fcd83ec02547` |
| Python version | CPython 3.14.5 |
| Operating system | Darwin 24.6.0 |
| CPU | Intel Core i5, 1.4 GHz, 4 cores |
| Architecture | x86_64 |
| Dependency manifest hash | `a22f5d7fd48e5383fce899fc84638e6727411d6d740e33a04c5871043bfda3e6` |
| Configuration hash | `299927eb372b86f2d82070749b957ef2faccce4ac41859f927d5632018f16f21` |
| Timestamp | 2026-07-13T11:16:53Z |
| Random seed | NOT APPLICABLE |
| Locale | `C/C.UTF-8/C/C/C/C` |
| Timezone | AEST / AEDT |

## Command Record

Executed exactly once:

```text
PYTHONDONTWRITEBYTECODE=1 python3 CortexMesh_v3_Planning/07_Research/RP-001/EXP-001/harness/exp001_runner.py
```

Harness SHA-256:

```text
885248766376d4d80c4f14c34077c4fe043879e2243e3b2fa3981a802290ec23
```

## Repetition Log

| Repetition | Planned cases | Started | Completed | Valid | Failed | Status |
| ---: | ---: | --- | --- | ---: | ---: | --- |
| 1 | 24 | Recorded | Recorded | 24 | 0 | COMPLETE |
| 2 | 24 | Recorded | Recorded | 24 | 0 | COMPLETE |
| 3 | 24 | Recorded | Recorded | 24 | 0 | COMPLETE |
| 4 | 24 | Recorded | Recorded | 24 | 0 | COMPLETE |
| 5 | 24 | Recorded | Recorded | 24 | 0 | COMPLETE |
| 6 | 24 | Recorded | Recorded | 24 | 0 | COMPLETE |
| 7 | 24 | Recorded | Recorded | 24 | 0 | COMPLETE |
| 8 | 24 | Recorded | Recorded | 24 | 0 | COMPLETE |
| 9 | 24 | Recorded | Recorded | 24 | 0 | COMPLETE |
| 10 | 24 | Recorded | Recorded | 24 | 0 | COMPLETE |

## Deviations, Stops, and Anomalies

Pre-collection deviation `EXP-001_DEVIATION_001.md` records that the exact command and harness hash were frozen after authorization but before collection. It changed no scientific design field.

No collection-time deviation, stop, exclusion, overwrite, or missing execution occurred.

## Raw Evidence Freeze

| Artifact | SHA-256 |
| --- | --- |
| `raw/RUN_MANIFEST.json` | `b54cae14f689c7764678d63c984c1654ef2499b1a4527966e711cc2d5f162ab3` |
| `raw/PACKAGE_MANIFEST.json` | `8ad3780feffd63c46d6a09183105bab0cda81912407632e89c00faf98c0c4651` |
| `raw/observations.jsonl` | `6551e6d6fd0ca6f661221a9be793802ddba1c301de0c44f07c5b1842ad6b962e` |
| `raw/exp001_runner.py` | `885248766376d4d80c4f14c34077c4fe043879e2243e3b2fa3981a802290ec23` |

Completeness verification confirmed 240 records, with 24 records in each repetition 1-10. Package manifest verification passed before analysis.

**EXECUTION LOG FROZEN - ANALYSIS MAY BEGIN**

Every future entry must include timestamp, affected cases/repetitions, evidence identifiers, classification, disposition, and reviewer.
