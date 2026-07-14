# Session 13 Evidence Index

## Purpose

Point reviewers to primary evidence without duplicating the underlying documents. Paths are relative to `CortexMesh_v3_Planning/` unless stated otherwise.

## Foundation and Governance

| Evidence | Review relevance |
| --- | --- |
| `FOUNDATION_BASELINE_v1.0.md` | Foundation identity, layers, assets, principles, tags, and boundaries |
| `00_Governance/GG-02_Board_Voting_and_Ratification_Rules_v1.0.md` | Active Board voting and ratification authority |
| `04_Architecture/LOCK_REGISTRY_v1.0.md` | Protected component boundary |
| `06_Implementation_Execution/IMPLEMENTATION_EXECUTION_TRACKER.md` | Phase closeouts and current lifecycle traceability |
| `06_Implementation_Execution/P2A_B003_LIFECYCLE_DISPOSITION.md` | Final Foundation-era deferred-item disposition |

## Published Phase Evidence

| Evidence | Review relevance |
| --- | --- |
| `06_Implementation_Execution/Phase1B/PHASE1B_CLOSEOUT_REPORT.md` | Local AI platform closeout |
| `06_Implementation_Execution/Phase2A/PHASE2A_CLOSEOUT_REPORT.md` | Platform consolidation closeout |
| `06_Implementation_Execution/Phase2C/PHASE2C_CLOSEOUT_REPORT.md` | Reference engine and isolation decision |
| `06_Implementation_Execution/Phase2C/RUNTIME_INTEGRATION_ASSESSMENT.md` | Evidence against current runtime integration |
| `06_Implementation_Execution/Phase3A/PHASE3A_CLOSEOUT_REPORT.md` | Permanent validation methodology adoption |
| `06_Implementation_Execution/Phase3A/VALIDATION_READINESS_ASSESSMENT.md` | Adoption rationale and remaining gaps |

## Research Methodology

| Evidence | Review relevance |
| --- | --- |
| `07_Research/CORTEXMESH_RESEARCH_PROGRAM.md` | Research lifecycle, validity, publication, ethics, and authorization rules |
| `07_Research/RP-001/RP-001_CHARTER.md` | RP-001 question, scope, hypotheses, and boundaries |
| `07_Research/RP-001/RP-001_RESEARCH_METHOD.md` | Controls, metrics, analysis, validity, and reproducibility method |
| `07_Research/RP-001/RP-001_SUCCESS_CRITERIA.md` | Independent gates and permissible outcomes |
| `07_Research/RP-001/RP-001_PREREGISTRATION.md` | Registered EXP-001 design and preserved revision history |

## EXP-001 and Reproduction

| Evidence | Review relevance |
| --- | --- |
| `07_Research/RP-001/EXP-001/EXP-001_PROTOCOL.md` | Authorized experiment procedure |
| `07_Research/RP-001/EXP-001/EXP-001_PROTOCOL_REVIEW.md` | Review record |
| `07_Research/RP-001/EXP-001/EXP-001_AUTHORIZATION.md` | State-only authorization and three gates |
| `07_Research/RP-001/EXP-001/EXP-001_DEVIATION_001.md` | Pre-collection harness-freeze deviation |
| `07_Research/RP-001/EXP-001/EXP-001_EXECUTION_LOG.md` | Environment, 240 executions, and raw freeze |
| `07_Research/RP-001/EXP-001/EXP-001_RESULTS.md` | Independent metrics and four anomalies |
| `07_Research/RP-001/EXP-001/EXP-001_DISCUSSION.md` | Bounded interpretation |
| `07_Research/RP-001/EXP-001/EXP-001_LIMITATIONS.md` | Registered and observed limitations |
| `07_Research/RP-001/EXP-001/EXP-001_REPRODUCIBILITY_PACKAGE.md` | Raw/analysis/reproduction integrity references |
| `07_Research/RP-001/EXP-001/reproduction/REPRODUCTION_REPORT.md` | EXP-001-R1 independent reproduction |
| `07_Research/RESEARCH_OBSERVATIONS.md` | OBS-000 permanent observation |

## Machine-Readable Evidence

Raw observations, manifests, per-case results, differences, metrics, and reproduction evidence are retained below `07_Research/RP-001/EXP-001/{raw,analysis,reproduction}/` and are available through GitHub.

## Review Sequence

```text
FOUNDATION_BASELINE_v1.0.md
  -> RP-001_CHARTER.md
  -> RP-001_PREREGISTRATION.md
  -> EXP-001_PROTOCOL.md
  -> EXP-001_RESULTS.md
  -> REPRODUCTION_REPORT.md
  -> RESEARCH_OBSERVATIONS.md
```
