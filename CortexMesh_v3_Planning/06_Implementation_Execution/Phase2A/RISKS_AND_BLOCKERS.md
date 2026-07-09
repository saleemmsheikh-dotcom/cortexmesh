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
| P2A-R008 | New provider developers may bypass provider-neutral contract requirements. | Future providers could weaken interchangeability. | M4 PDK requires shared contract tests and certification checklist before acceptance. |
| P2A-R009 | A reference adapter could accidentally enter runtime selection. | Example behavior could affect production execution. | Keep `ReferenceProvider` out of the runtime provider registry and verify this invariant. |

## Blockers

| ID | Blocker | Status | Required Resolution |
| -- | ------- | ------ | ------------------- |
| P2A-B001 | SAFE bridge still uses direct registry helpers instead of `LocalAIManager`. | CLOSED | M2 convergence implemented; bridge now uses `LocalAIManager` as the Local AI subsystem entry point. |
| P2A-B002 | Shared provider adapter contract tests do not yet exist. | CLOSED | M3 shared contract suite verifies Ollama and LM Studio through identical provider-neutral requirements. |
| P2A-B003 | Adapter utility extraction has not been assessed. | OPEN | Review duplication and decide whether extraction is beneficial. |
| P2A-B004 | Provider implementation process is not standardized. | CLOSED | M4 PDK standardizes provider implementation, testing, and certification. |
| P2A-B005 | PDK usability has not been demonstrated by an independent example provider. | CLOSED | M5 reference provider passes the shared contract suite and remains outside runtime registration. |

## M2 Risk Review

P2A-R001 and P2A-R007 remain monitored, but M2 verification confirms the solver schema, confidence behavior, provenance, disabled fallback behavior, and provider failure propagation expectations were preserved.

## Current Recommendation

M5 is complete. Proceed to shared provider adapter utility assessment.
