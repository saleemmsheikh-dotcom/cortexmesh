# Phase 2C Risks and Blockers

## Status

OPEN

## Purpose

Track risks, blockers, constraints, and deferred decisions for Phase 2C intelligent multi-agent orchestration.

## Active Risks

| ID | Risk | Impact | Mitigation | Status |
| -- | ---- | ------ | ---------- | ------ |
| P2C-R001 | Capability-driven routing may require changes near LOCKED orchestration surfaces. | Future authorization may be required before implementation. | Begin with design and impact assessment; do not modify LOCKED components without approval. | OPEN |
| P2C-R002 | Multi-agent collaboration may create convergence pressure that weakens independent reasoning. | Architectural integrity risk. | Preserve independent reasoning stages and record collaboration steps as evidence. | OPEN |
| P2C-R003 | Evidence-aware reasoning may overlap with scoring or authority semantics. | Governance and behavioral ambiguity. | Keep evidence handling separate from score, confidence, rank, vote weight, and authority unless future authorization is granted. | OPEN |
| P2C-R004 | Consensus layer may be mistaken for voting or authority. | Governance confusion. | Define consensus as evidence synthesis only; preserve human governance authority. | OPEN |
| P2C-R005 | Adaptive orchestration may accidentally introduce provider ranking. | Violates provider neutrality. | Adapt only on evidence, capability fit, and task context; provider identity remains provenance only. | OPEN |
| P2C-R006 | Intent and capability routing may be mistaken for scoring or authority logic. | Could blur governance and execution boundaries. | Keep intent, capability, evidence, scoring, confidence, and authority semantics explicitly separate. | OPEN |

## Blockers

| ID | Blocker | Impact | Disposition |
| -- | ------- | ------ | ----------- |
| None | No active blockers at commencement. | None | N/A |

## Deferred Items

| ID | Item | Target | Rationale |
| -- | ---- | ------ | --------- |
| P2C-D001 | LOCKED component implementation changes | Future Board authorization if needed | Phase 2C may identify useful integration points, but no LOCKED modification is authorized at commencement. |
| P2C-D002 | Runtime implementation of capability routing | M1 implementation planning | Architecture is ready, but implementation requires boundary review before any orchestration code change. |

## Governance Constraints

- GG-02 is ratified and in force.
- No LOCKED component modifications without future authorization.
- No Local AI platform redesign.
- No scoring, authority, confidence, rank, or vote-weight changes without future authorization.

## Current Recommendation

Phase 2C may proceed with design, evidence, and non-LOCKED implementation work while preserving all stated constraints.

M1 intent-driven orchestration architecture is ready for implementation planning.
