# Phase 2A Risks and Blockers

## Status

ACTIVE

## Risks

| ID | Risk | Impact | Mitigation |
| -- | ---- | ------ | ---------- |
| P2A-R001 | SAFE bridge convergence could accidentally change solver output schema. | Orchestrator-facing behavior may change. | Preserve existing `agent`, `base_agent`, `confidence`, `solution`, and provenance structure; add regression tests. |
| P2A-R002 | LocalAIManager could become provider-specific. | Provider neutrality could weaken. | Keep provider-specific logic inside adapters only. |
| P2A-R003 | Shared adapter utilities could over-abstract provider differences. | Adapter clarity may decrease. | Extract utilities only when they reduce meaningful duplication and preserve adapter boundaries. |
| P2A-R004 | Capability checks could be mistaken for ranking or authority. | Governance semantics could be blurred. | Capabilities remain metadata and diagnostics only. |
| P2A-R005 | Telemetry could leak decision-affecting semantics. | Confidence, score, authority, rank, or vote-weight leakage. | Continue filtering and testing telemetry diagnostics. |
| P2A-R006 | Phase 2A may drift into runtime integration. | LOCKED components could be implicated. | Keep Phase 2A limited to SAFE path consolidation and non-LOCKED files. |
| P2A-R007 | Bridge convergence could change fallback/error behavior. | Local AI disabled or provider failure behavior may change. | M1 design requires disabled path to return `None` and enabled provider failures to propagate compatibly. |

## Blockers

| ID | Blocker | Status | Required Resolution |
| -- | ------- | ------ | ------------------- |
| P2A-B001 | SAFE bridge still uses direct registry helpers instead of `LocalAIManager`. | CLOSED | M2 convergence implemented; bridge now uses `LocalAIManager` as the Local AI subsystem entry point. |
| P2A-B002 | Shared provider adapter contract tests do not yet exist. | OPEN | Create reusable tests for local provider adapters. |
| P2A-B003 | Adapter utility extraction has not been assessed. | OPEN | Review duplication and decide whether extraction is beneficial. |

## M2 Risk Review

P2A-R001 and P2A-R007 remain monitored, but M2 verification confirms the solver schema, confidence behavior, provenance, disabled fallback behavior, and provider failure propagation expectations were preserved.

## Current Recommendation

Proceed to Phase 2A M3 planning for shared adapter utilities and adapter contract tests.
