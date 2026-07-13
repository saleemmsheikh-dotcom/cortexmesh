# EXP-001 Deviation 001

## Record

| Field | Value |
| --- | --- |
| Recorded | 2026-07-13, before data collection |
| Classification | Administrative reproducibility correction |
| Collection affected | None at time of record |
| Design impact | None |
| Authorization impact | Authorization retained |

## Condition

EXP-001 Protocol v1.0 required the exact collection command and harness to be frozen before authorization. The protocol review and authorization commits froze the scientific procedure but did not contain the executable command or harness content hash.

No replay execution or EXP-001 observation occurred before this condition was identified.

## Correction

The isolated, standard-library-only research harness was syntax-validated and frozen before first execution.

```text
Harness: CortexMesh_v3_Planning/07_Research/RP-001/EXP-001/harness/exp001_runner.py
SHA-256: 885248766376d4d80c4f14c34077c4fe043879e2243e3b2fa3981a802290ec23
Command: PYTHONDONTWRITEBYTECODE=1 python3 CortexMesh_v3_Planning/07_Research/RP-001/EXP-001/harness/exp001_runner.py
```

The harness copies its exact source into the raw reproducibility package and records its own hash. It validates corpus integrity, loads only isolated Phase 2C reference components, processes all 24 cases in manifest order for ten repetitions, preserves raw outputs and timings, and performs no result interpretation.

## Scientific Design Check

Unchanged:

- research questions and registered expectations;
- 24 certified cases and their order;
- ten repetitions and 240 planned executions;
- engine, corpus, and validation baselines;
- comparators and canonical exclusions;
- metrics and planned analysis;
- inclusion, exclusion, stop, ethics, governance, and LOCKED rules.

## Boundary Check

The harness uses no network, provider, Local AI, live agent, runtime orchestration, adaptation, randomness, governance process, or LOCKED component. It writes only experiment evidence under `RP-001/EXP-001/raw/`.

## Disposition

**CORRECTED BEFORE DATA COLLECTION**

This deviation remains visible in the experiment record and must be included in publication and reproducibility evidence.
