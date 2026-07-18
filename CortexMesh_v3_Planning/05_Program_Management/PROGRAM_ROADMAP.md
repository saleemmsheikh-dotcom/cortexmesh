# CortexMesh Program Roadmap

## Purpose

Provide a state-based view of CortexMesh progress.

This roadmap is status-oriented rather than date-oriented.

No timeline commitments are implied.

This is a living document and should be updated when board decisions, implementation-planning status, or active workstreams change.

## Status Vocabulary

Use these statuses consistently unless the board approves a new status:

| Status | Meaning |
|--------|---------|
| NOT STARTED | Work has not begun |
| IN PROGRESS | Work is actively underway |
| BLOCKED | Work cannot proceed until a blocker is removed |
| IN REVIEW | Work is under board, architecture, or technical review |
| AUTHORIZED | Work has been approved but may not have started |
| COMPLETE | Work is finished or accepted |
| MONITOR | No active work; condition is watched for re-entry |
| DEFERRED | Work is intentionally postponed |

## Governance Stream

| Item | Status |
|--------|--------|
| Governance Baseline | COMPLETE |
| Lock Registry | COMPLETE |
| Board History Summary | COMPLETE |
| Current Board State | COMPLETE |
| Policy Review | IN PROGRESS |

## Architecture Stream

| Item | Status |
|--------|--------|
| Architectural North Star | IN REVIEW |
| Four-Pool Architecture | IN REVIEW |
| Decision-Governance Shell Definition | IN REVIEW |
| v3 Architecture Principles | NOT STARTED |

## Debt Stream

| Debt | Severity | Status |
|--------|--------|--------|
| DEBT-001 | MEDIUM | MONITOR |
| DEBT-010 | HIGH | MONITOR |
| DEBT-011 | MEDIUM | IN PROGRESS |
| DEBT-008 | MEDIUM | DEFERRED |
| DEBT-007 | HIGH | IN REVIEW |

## Implementation Stream

| Item | Status |
|--------|--------|
| DEBT-011 Design Study | COMPLETE |
| DEBT-011 Implementation Plan | IN PROGRESS |
| DEBT-011 Board Review | NOT STARTED |
| DEBT-011 Implementation | NOT STARTED |

## Foundation 1.1 Repository Quality Stream

| Workstream | Status |
| --- | --- |
| F1.1-A Repository Identity | COMPLETE |
| F1.1-B Legal and Community | DEFERRED — INTERIM CORRECTION EFFECTIVE; FORMAL LEGAL REVIEW OUTSTANDING |
| F1.1-C Repository Hygiene | COMPLETE |
| F1.1-D CI/CD and Automation | COMPLETE |
| F1.1-E Packaging and Environment | IN REVIEW — PR ACCESS BLOCKED |

Foundation 1.1 remains IN PROGRESS because F1.1-B is paused and F1.1-E is not
complete. F1.1-C closed at merge commit `1004f7f`. F1.1-D closed following
Product Owner acceptance and pull request #2 merge at `ac14b74`; local and
`main` CI regression passed 250/250 and protected surfaces remained unchanged.
F1.1-E CP1–CP3 are complete on
`foundation-1.1e-environment-contract` at `6735bf6`. The default and optional
OpenAI profiles passed direct Ubuntu/CPython 3.14.4 validation, and the expanded
local regression passed 279/279 under both unittest and pytest. Pull-request
creation is blocked by GitHub access, so CP4, implementation acceptance, merge,
and closeout remain pending.

## Roadmap Relationships

| Document | Role |
|----------|------|
| `CURRENT_BOARD_STATE.md` | Where the program is now |
| `BOARD_HISTORY_SUMMARY.md` | How the program reached the current state |
| `PROGRAM_ROADMAP.md` | Where the program is trying to go |

## Governance Notes

- This roadmap does not authorize implementation.
- LOCKED component changes still require explicit board authorization.
- DEBT-011 implementation remains unauthorized until the board approves an implementation plan.
- Status changes should be evidence-backed and reflected in the relevant board or planning artifact.
- Foundation 1.1 status is maintained in
  `../06_Implementation_Execution/Foundation_1_1/FOUNDATION_1_1_STATUS.md`.
- F1.1-E implementation is authorized and ready for Product Owner review.
  Merge remains unauthorized, and CP4 is blocked until pull-request access is
  restored.
