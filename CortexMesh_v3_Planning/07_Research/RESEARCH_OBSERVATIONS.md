# CortexMesh Research Observations

## Purpose

Maintain an append-only register of durable observations supported by completed CortexMesh research evidence.

An observation describes what was measured under declared conditions. It is not a hypothesis, implementation decision, runtime authority, certification transfer, governance decision, or permission to modify a LOCKED component.

## Observation Register

### OBS-000 - Reference Engine Reproducibility

| Field | Value |
| --- | --- |
| Status | OBSERVED AND REPRODUCED |
| Date | 2026-07-13 |
| Research program | RP-001 |
| Original experiment | EXP-001 |
| Independent reproduction | EXP-001-R1 |
| Engine | `phase2c-complete` / `a72d11fe57f9026ab307efeaf962b97095527039` |
| Corpus | Certified Replay Corpus v1.1.0 |
| Original executions | 240 |
| Reproduction executions | 240 |
| Canonical matches | 240/240 |
| Behavioral differences | 0 |

**The sealed Phase 2C Reference Orchestration Engine reproduced identical canonical outputs across independent executions of the certified replay corpus. No behavioral drift or evidence mutation was observed.**

Latency differed descriptively between the two collections while canonical behavior remained identical. This supports the established separation between behavioral reproducibility and observational performance measurements.

OBS-000 provides no evidence of learning. The reference engine is stateless within the experiment and has no persistent memory, training loop, parameter update, or adaptive policy.

Primary evidence:

- `RP-001/EXP-001/EXP-001_RESULTS.md`;
- `RP-001/EXP-001/raw/`;
- `RP-001/EXP-001/analysis/`;
- `RP-001/EXP-001/reproduction/REPRODUCTION_REPORT.md`;
- `RP-001/EXP-001/reproduction/run-001/`.

Boundary: OBS-000 does not authorize learning, adaptation, runtime integration, provider invocation, engine modification, or LOCKED modification.

### OBS-INF-001 - External Reproduction Output Isolation Gap

| Field | Value |
| --- | --- |
| Status | CLOSED |
| Date opened | 2026-07-17 |
| Date closed | 2026-07-17 |
| Research program | RP-001 |
| Reproduction | EXP-001-R2 |
| Category | Research infrastructure / lifecycle traceability |

An external Ubuntu verification reached the immutable-output gate and correctly refused to overwrite published EXP-001 evidence. The event exposed that the harness and analyzer lacked an explicit isolated destination for a second reproduction package.

The separately authorized EXP-001-R2 reproduction completed on Ubuntu using the isolated output mechanism. It recorded 240/240 executions, 240/240 canonical matches with both EXP-001 and EXP-001-R1, and the published 220/260 statement-expectation result. All other registered non-latency metrics reproduced exactly. Latency remains descriptive.

Raw and analysis manifests verified, the published EXP-001 artifacts remained byte-for-byte unchanged, and the post-execution regression passed 226/226. Repository-relative execution under the declared Ubuntu environment is therefore validated for this experiment.

Primary evidence:

- `RP-001/EXP-001/EXP-001-R2_OUTPUT_ISOLATION_DESIGN.md`;
- `RP-001/EXP-001/EXP-001-R2_EXECUTION_AUTHORIZATION.md`;
- `RP-001/EXP-001/reproduction/EXP-001-R2/`.

OBS-INF-001 is closed because the authorized Ubuntu execution, isolated evidence package, manifest verification, canonical comparisons, and regression evidence satisfy its closure criteria. Closure does not generalize portability beyond the declared Ubuntu environment or authorize runtime, provider, Local AI, engine, governance, or LOCKED changes.
