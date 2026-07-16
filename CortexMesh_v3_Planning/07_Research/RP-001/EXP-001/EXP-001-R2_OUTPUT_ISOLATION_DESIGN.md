# EXP-001-R2 Output Isolation Design

## Identity

| Field | Value |
| --- | --- |
| Research program | RP-001 |
| Reproduction | EXP-001-R2 |
| Milestone | Output Isolation Design |
| Date | 2026-07-17 |
| Status | DESIGN VERIFIED — EXECUTION NOT AUTHORIZED |
| Observation | OBS-INF-001 - OPEN |

## Purpose

Permit a future, separately authorized EXP-001-R2 reproduction to write evidence into an isolated package without reading from, deleting, moving, renaming, or overwriting the published EXP-001 `raw/` or `analysis/` directories.

This milestone changes evidence-destination infrastructure only. It does not authorize reproduction, validate repository portability, change the experiment, or create results.

## Interfaces

Collection selects a reproduction package root:

```bash
python3 CortexMesh_v3_Planning/07_Research/RP-001/EXP-001/harness/exp001_runner.py \
  --output-root reproduction/EXP-001-R2
```

Analysis selects the corresponding raw input and analysis output:

```bash
python3 CortexMesh_v3_Planning/07_Research/RP-001/EXP-001/harness/exp001_analyze.py \
  --input-root reproduction/EXP-001-R2/raw \
  --output-root reproduction/EXP-001-R2/analysis
```

All supplied paths are interpreted relative to `RP-001/EXP-001`. Absolute paths and resolved paths outside `EXP-001/reproduction/` are rejected. Analyzer input and output must belong to the same reproduction package.

## Default and Reproduction Behavior

With no arguments, the runner and analyzer retain their published paths:

- runner: `EXP-001/raw/`;
- analyzer input: `EXP-001/raw/`;
- analyzer output: `EXP-001/analysis/`.

The existing non-empty-directory refusal remains active, so the published evidence prevents a default rerun.

With an explicit runner output root, the harness creates only these isolated directories beneath the selected package:

- `raw/`;
- `analysis/`;
- `logs/`;
- `environment/`;
- `hashes/`.

Collection refuses to start if the selected package's `raw/` or `analysis/` tree contains a file. Analysis refuses to start if its selected analysis directory is non-empty and verifies the selected raw package manifest before calculating results.

## Integrity Boundaries

- Published EXP-001 evidence remains immutable.
- Reproduction paths cannot resolve to published `raw/` or `analysis/` locations.
- Path traversal outside reproduction space is rejected after canonical resolution.
- The runner resolves the repository from its own source location; it does not depend on a workstation-specific absolute path.
- Engine identity, corpus identity and hash, validation identity, repetitions, case order, simulated evidence, consensus policy, metrics, and analysis calculations are unchanged.
- No runtime, Local AI, provider, governance, or LOCKED component participates.

## Verification Scope

Focused infrastructure tests cover default selection, published-output protection, clean isolation, non-empty isolation refusal, traversal rejection, runner/analyzer path agreement, and frozen scientific constants. Full regression and artifact hashing are recorded in the milestone report; they do not constitute EXP-001-R2 execution.

## Verification Record

| Check | Result |
| --- | --- |
| `py_compile` | PASS |
| Focused output-isolation tests | 7/7 PASS |
| Full regression | 226/226 PASS |
| `git diff --check` | PASS |
| Runtime, Local AI, provider, and LOCKED changes | None |
| EXP-001-R2 execution | Not run |

Published artifact hashes matched the pre-change baseline:

| Artifact | SHA-256 |
| --- | --- |
| `raw/PACKAGE_MANIFEST.json` | `8ad3780feffd63c46d6a09183105bab0cda81912407632e89c00faf98c0c4651` |
| `raw/RUN_MANIFEST.json` | `b54cae14f689c7764678d63c984c1654ef2499b1a4527966e711cc2d5f162ab3` |
| `raw/exp001_runner.py` | `885248766376d4d80c4f14c34077c4fe043879e2243e3b2fa3981a802290ec23` |
| `raw/observations.jsonl` | `6551e6d6fd0ca6f661221a9be793802ddba1c301de0c44f07c5b1842ad6b962e` |
| `analysis/ANALYSIS_MANIFEST.json` | `60e2f9c1ac66d414d611f7a81f3640b39a0fa714c74dc63a03b1f8916de7b646` |
| `analysis/case_results.json` | `c29fdebfffd83cf40ff7ddb9073b4cf6ab1d84a23d85b2eee5df149e90f685d4` |
| `analysis/differences.json` | `10dd87be746433bcc64bc3bdd12ae7cf15a58f85f72b75a484ed3016d4cf552e` |
| `analysis/metrics.json` | `30ff1aabb777e4d7c7eda53363c7715f35cab3bf439b03fc63e8a37c631460a6` |

## Authorization Boundary

Review and authorization must occur after this design is verified. A separate authorization record and commit are required before any of the 240 planned executions may begin.
