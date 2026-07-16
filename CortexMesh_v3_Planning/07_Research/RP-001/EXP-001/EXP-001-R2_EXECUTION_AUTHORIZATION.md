# EXP-001-R2 Execution Authorization

## Status

**DESIGN VERIFIED — EXECUTION NOT AUTHORIZED**

| Field | Value |
| --- | --- |
| Research program | RP-001 |
| Reproduction | EXP-001-R2 |
| Date | 2026-07-17 |
| Planned executions | 240 |
| OBS-INF-001 | OPEN |
| Authorization commit | Not issued |
| Data collection | Prohibited |

## Preconditions for Future Authorization

Authorization requires a separate review confirming:

1. the output-isolation design and focused tests pass;
2. the full established regression baseline passes;
3. published EXP-001 `raw/` and `analysis/` hashes are unchanged;
4. the selected destination is an empty `reproduction/EXP-001-R2/` package;
5. engine, certified corpus, validation framework, and protocol identities remain frozen;
6. no runtime, Local AI, provider, governance, or LOCKED file changed.

Authorization changes reproduction state only. It must not alter hypotheses, protocol, corpus inputs, metrics, comparators, analysis, or expected outcomes.

## Prohibited by This Record

This record does not authorize running the collection harness, analyzing R2 data, creating or claiming R2 results, validating Ubuntu portability, or closing OBS-INF-001.
