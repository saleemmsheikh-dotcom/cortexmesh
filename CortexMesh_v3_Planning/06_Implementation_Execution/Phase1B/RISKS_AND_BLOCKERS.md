# Phase 1B Risks and Blockers

## Status

ACTIVE

## Risks

| ID | Risk | Impact | Mitigation |
| -- | ---- | ------ | ---------- |
| P1B-R001 | Provider-specific behavior leaks outside adapters. | Future providers require duplicated or conflicting logic. | Enforce provider interface boundary before runtime integration. |
| P1B-R002 | Ollama and LM Studio response formats diverge. | Shared callers may become provider-aware. | Normalize all responses through provider adapters. |
| P1B-R003 | Provider identity is mistaken for reliability or confidence. | Violates architecture and verification constraints. | Treat provider identity as provenance only. |
| P1B-R004 | Local endpoint availability varies by developer environment. | Connection verification may be non-reproducible. | Record endpoint, model, timing, diagnostics, and failure reasons. Observed again in `PHASE1B-VE-005` when `localhost:11434` refused connection. |
| P1B-R005 | Runtime integration may require LOCKED component changes. | Governance violation if modified without authorization. | Defer integration into LOCKED components until explicit Board authorization. |
| P1B-R006 | Local AI integration through `engine/model_router.py` may lose provider provenance if reduced to a plain string response. | Evidence and traceability may be weaker than the Phase 1B provider contract requires. | Prefer `agents/local_solver.py` or equivalent non-LOCKED agent glue that preserves provider/model/request metadata as candidate provenance. |
| P1B-R007 | Auto-selection could be mistaken for provider authority. | Provider availability might be confused with quality, confidence, or governance status. | Record provider choice as provenance only; do not map provider identity into scoring, confidence, authority, rank, or vote weight. |
| P1B-R008 | LocalAIManager could accumulate provider-specific logic. | Manager may become a hidden provider adapter or violate provider-neutral design. | Keep provider-specific transport and response parsing inside adapters; manager may coordinate selection, health checks, diagnostics, and provenance only. Initial skeleton verified by `PHASE1B-VE-007`. |
| P1B-R009 | Health diagnostics could be mistaken for provider quality ranking. | Availability data may be misused as confidence, score, authority, rank, or vote weight. | M4.3 hardening records diagnostics as operational evidence only and explicitly marks `ranking_used: false`. |
| P1B-R010 | Capability declarations could be mistaken for provider quality or authority. | Capability metadata may be misused as confidence, score, authority, rank, vote weight, or governance status. | Treat capabilities as provenance-only operational metadata. Manager discovery exposes support without ranking providers or affecting scoring/authority paths. |
| P1B-R011 | Stabilisation refactors could accidentally change provider behavior. | Runtime behavior might drift before integration authorization. | M6 limits changes to review documentation and focused tests unless a low-risk simplification is clearly justified. |
| P1B-R012 | SAFE bridge may diverge from LocalAIManager as the subsystem matures. | Future runtime integration could duplicate manager behavior or weaken diagnostics consistency. | M7B review recommends deciding in M8 whether SAFE runtime wiring should converge on `LocalAIManager` as the primary coordination API. |
| P1B-R013 | Runtime callers may bypass LocalAIManager and call registries or adapters directly. | Provider details could leak into runtime callers and weaken subsystem boundaries. | M8.0 establishes `LocalAIManager` as the sole public runtime entry point. Registries, capabilities, telemetry buffers, and adapters remain internal subsystem details. |

## Outstanding Blockers

| ID | Blocker | Status | Required Resolution |
| -- | ------- | ------ | ------------------- |
| P1B-B001 | No live Ollama endpoint has been verified in this session. | CLOSED | Verified by `PHASE1B-VE-002` against `http://localhost:11434` using `qwen2.5-coder:7b`. |
| P1B-B002 | Runtime integration path may touch LOCKED components. | CLOSED FOR REVIEW | `LOCKED_COMPONENT_BOUNDARY_REVIEW.md` identifies SAFE non-LOCKED paths and marks direct orchestration/scoring/authority/ExternalRunner/snapshot changes as requiring Board authorization. |
| P1B-B003 | LM Studio compatibility remains design-level only. | CLOSED FOR DESIGN | `LM_STUDIO_COMPATIBILITY_REVIEW.md` finds no provider interface changes are required. Implementation has not started and should proceed only through a non-LOCKED adapter if authorized. |
| P1B-B004 | Runtime implementation has not yet been performed through the recommended SAFE path. | CLOSED | SAFE local solver integration implemented through `agents/local_solver.py` and `agents/local_ai_bridge.py`; verified by `PHASE1B-VE-004`. |
| P1B-B005 | Broader runtime testing with Local AI enabled has not yet been performed. | CLOSED | Closed by `PHASE1B-VE-005`. Non-LOCKED dev-mode runtime plumbing was verified with Local AI enabled and `LocalSolverAgent` in execution. Live endpoint availability remains an environment risk under `P1B-R004`. |
| P1B-B006 | Provider selection is hard-coded to a single provider. | CLOSED | Closed by `PHASE1B-VE-006`. Provider-neutral registry and configuration-driven selection are implemented through the SAFE non-LOCKED path. |
| P1B-B007 | LocalAIManager architecture has not been defined. | CLOSED FOR DESIGN | Closed by `LOCAL_AI_MANAGER_ARCHITECTURE.md`. Implementation has not started and requires separate authorization. |
| P1B-B008 | LocalAIManager skeleton has not been implemented. | CLOSED | Closed by `PHASE1B-VE-007`. Skeleton is implemented in the non-LOCKED Local AI subsystem and is not yet wired into runtime solver execution. |
| P1B-B009 | LocalAIManager health and diagnostics behavior has not been hardened. | CLOSED | Closed by `PHASE1B-VE-008`. Structured health diagnostics, clean provider failure, auto-selection fallback, and non-ranking diagnostics are verified. |
| P1B-B010 | Provider-neutral capability discovery has not been defined or implemented. | CLOSED | Closed by `PHASE1B-VE-009`. Capability discovery is provider-neutral, placeholder support is opt-in, and discovery does not affect scoring, authority, confidence, rank, vote weight, or governance decisions. |
| P1B-B011 | Local AI subsystem has not been reviewed for stabilisation before runtime integration. | CLOSED | Closed by `PHASE1B-VE-010`. Review completed with no behavior-changing refactor; focused stabilisation tests passed. |
| P1B-B012 | Local AI subsystem has not received a formal architecture review. | CLOSED | Closed by `PHASE1B-VE-012`. Formal review recommends `READY FOR M8`. |
| P1B-B013 | LM Studio adapter implementation lacks a pre-implementation design. | CLOSED FOR DESIGN | Closed by `LM_STUDIO_ADAPTER_DESIGN.md`. Design is `READY FOR IMPLEMENTATION`; implementation has not started. |

## Next Milestone

Review `VERIFICATION_EVIDENCE_008_HEALTH_DIAGNOSTICS.md` and decide whether to authorize wiring the manager into the SAFE local solver bridge. Repeat live endpoint runtime testing after local Ollama availability is confirmed.
