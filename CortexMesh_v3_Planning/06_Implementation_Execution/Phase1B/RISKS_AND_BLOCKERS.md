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

## Outstanding Blockers

| ID | Blocker | Status | Required Resolution |
| -- | ------- | ------ | ------------------- |
| P1B-B001 | No live Ollama endpoint has been verified in this session. | CLOSED | Verified by `PHASE1B-VE-002` against `http://localhost:11434` using `qwen2.5-coder:7b`. |
| P1B-B002 | Runtime integration path may touch LOCKED components. | CLOSED FOR REVIEW | `LOCKED_COMPONENT_BOUNDARY_REVIEW.md` identifies SAFE non-LOCKED paths and marks direct orchestration/scoring/authority/ExternalRunner/snapshot changes as requiring Board authorization. |
| P1B-B003 | LM Studio compatibility remains design-level only. | CLOSED FOR DESIGN | `LM_STUDIO_COMPATIBILITY_REVIEW.md` finds no provider interface changes are required. Implementation has not started and should proceed only through a non-LOCKED adapter if authorized. |
| P1B-B004 | Runtime implementation has not yet been performed through the recommended SAFE path. | CLOSED | SAFE local solver integration implemented through `agents/local_solver.py` and `agents/local_ai_bridge.py`; verified by `PHASE1B-VE-004`. |
| P1B-B005 | Broader runtime testing with Local AI enabled has not yet been performed. | CLOSED | Closed by `PHASE1B-VE-005`. Non-LOCKED dev-mode runtime plumbing was verified with Local AI enabled and `LocalSolverAgent` in execution. Live endpoint availability remains an environment risk under `P1B-R004`. |

## Next Milestone

Review `LM_STUDIO_COMPATIBILITY_REVIEW.md` and decide whether to authorize non-LOCKED LM Studio adapter implementation. Repeat live endpoint runtime testing after local Ollama availability is confirmed.
