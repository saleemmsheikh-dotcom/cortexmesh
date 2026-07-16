# EXP-001-R2 - Ubuntu Reproduction

## Status

**REPRODUCED**

## Identity

| Field | Value |
| --- | --- |
| Experiment | RP-001/EXP-001 |
| Reproduction identifier | EXP-001-R2 |
| Date | 2026-07-17 |
| Repository commit | `4dcba31` |
| Output-isolation commit | `09b4455` |
| Engine | `phase2c-complete` / `a72d11fe57f9026ab307efeaf962b97095527039` |
| Validation framework | `phase3a-complete` / `6c41364c56883043c20d237d37b8fcd83ec02547` |
| Replay corpus | Certified v1.1.0 / `20e4b446097db5b3dcaa6fbf214218038c9c297d2e60bbbc57b9d24bc1e59788` |
| Planned executions | 240 |
| Recorded executions | 240 |

## Ubuntu Environment

| Field | Value |
| --- | --- |
| Distribution | Ubuntu 26.04 LTS (Resolute Raccoon) |
| Kernel | Linux 7.0.0-27-generic x86_64 |
| Python | CPython 3.14.4 (`/usr/bin/python3`) |
| Locale | `C.UTF-8` categories |
| Timezone | AEST / AEDT |
| Dependency boundary | Standard library only |
| Dependency manifest SHA-256 | `66d71ed42383d5a322464862fd102e4bbbdaeb588f7d8c7f7d84859a6ee7b383` |
| Configuration SHA-256 | `299927eb372b86f2d82070749b957ef2faccce4ac41859f927d5632018f16f21` |

The complete experiment environment and orchestration-module hashes are recorded in `raw/RUN_MANIFEST.json`. Collection required no network, provider, Local AI, runtime invocation, randomness, or external dependency.

## Authorized Commands

```text
PYTHONDONTWRITEBYTECODE=1 python3 CortexMesh_v3_Planning/07_Research/RP-001/EXP-001/harness/exp001_runner.py --output-root reproduction/EXP-001-R2
PYTHONDONTWRITEBYTECODE=1 python3 CortexMesh_v3_Planning/07_Research/RP-001/EXP-001/harness/exp001_analyze.py --input-root reproduction/EXP-001-R2/raw --output-root reproduction/EXP-001-R2/analysis
```

Each command executed once. No retry, expectation change, or experiment-logic modification occurred.

## Results

| Measurement | Result |
| --- | ---: |
| Executions | 240/240 |
| Canonical matches with EXP-001 | 240/240 |
| Canonical matches with EXP-001-R1 | 240/240 |
| Status matches with both prior runs | 240/240 |
| Statement expectations | 220/260 |
| Diagnostic expectations | 100/100 |
| Evidence completeness | 450/450 |
| Evidence traceability | 450/450 |
| Deterministic cases | 24/24 |
| Replay-reproducible cases | 24/24 |
| Pipeline-stable executions | 240/240 |
| Consensus-certified cases | 24/24 |
| Minority preservation | 3/3 |
| Material-divergence preservation | 4/4 |
| Synthesis-stable cases | 24/24 |
| Preserved differences | 4 |

All registered non-latency metrics reproduced exactly. The four published statement-presentation differences remained visible.

## Descriptive Latency

| Statistic | EXP-001-R2 |
| --- | ---: |
| Minimum | 0.008302 ms |
| Median | 0.544225 ms |
| P95 nearest rank | 0.872810 ms |
| Maximum | 3.077545 ms |
| Mean | 0.529636 ms |
| Population standard deviation | 0.266673 ms |
| Coefficient of variation | 0.503503 |

Latency remains environment-specific and descriptive. It is not a performance, learning, or reproduction gate.

## Artifact Integrity

| Artifact | SHA-256 |
| --- | --- |
| `raw/observations.jsonl` | `24e1e95253c0c77e182bf62aed2e05552852229bcb4c0f401b7f3ea305f70677` |
| `raw/RUN_MANIFEST.json` | `543208c52db09012f85308b3c8474efee98f0903546e56ac520786837aa64e75` |
| `raw/PACKAGE_MANIFEST.json` | `d491e22dfa1e7a3a5be6626eb0f6c71dccb5000effdade66f8756b353b6ee193` |
| `raw/exp001_runner.py` | `f1e60a02916d8b57016fac13d150bdf35aa3083edaa2af364c32a070ec4b909f` |
| `analysis/metrics.json` | `935a9e077207cb7fbcaccef1ac60005d32aece50795b47eb98232ac33d3b54eb` |
| `analysis/case_results.json` | `c29fdebfffd83cf40ff7ddb9073b4cf6ab1d84a23d85b2eee5df149e90f685d4` |
| `analysis/differences.json` | `10dd87be746433bcc64bc3bdd12ae7cf15a58f85f72b75a484ed3016d4cf552e` |
| `analysis/ANALYSIS_MANIFEST.json` | `a49eeebba16881e6e8a5db0c3f066242eb1dfceb89d1bcb5eb1dc17298a84d47` |

Published EXP-001 raw and analysis artifacts were verified before and after execution and remained byte-for-byte unchanged. The post-execution full regression passed 226/226. No runtime, Local AI, provider, governance, or LOCKED file changed.

## Conclusion

EXP-001-R2 reproduced the published behavioral results on Ubuntu using repository-relative isolated output paths. This supplies the required closure evidence for OBS-INF-001 and validates repository-portable execution under the declared environment.
