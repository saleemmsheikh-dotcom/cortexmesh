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
| P2C-R007 | Capability resolver diagnostics may be misinterpreted as routing authority. | Could lead to silent policy drift in later planner work. | Treat diagnostics as informational only and verify planner design preserves this boundary. | OPEN |
| P2C-R008 | Agent planner output may be mistaken for final runtime execution authorization. | Could blur planning and execution boundaries. | Treat AgentPlan as reference planning output only until execution plan design and boundary review are complete. | OPEN |
| P2C-R009 | Execution plan output may be mistaken for agent invocation. | Could blur planning and runtime execution boundaries. | Treat ExecutionPlan as deterministic planning output only; no agents or providers are invoked. | OPEN |
| P2C-R010 | Descriptive evidence may be mistaken for authority or quality judgment. | Could introduce implicit scoring or provider/model preference. | Mark bundles descriptive-only, reject authoritative fields, and keep identity in provenance only. | MITIGATED |

## Blockers

| ID | Blocker | Impact | Disposition |
| -- | ------- | ------ | ----------- |
| None | No active blockers at commencement. | None | N/A |

## Deferred Items

| ID | Item | Target | Rationale |
| -- | ---- | ------ | --------- |
| P2C-D001 | LOCKED component implementation changes | Future Board authorization if needed | Phase 2C may identify useful integration points, but no LOCKED modification is authorized at commencement. |
| P2C-D002 | Runtime implementation of capability routing | M1 implementation planning | Architecture is ready, but implementation requires boundary review before any orchestration code change. |
| P2C-D003 | Agent planner design | Phase 2C next milestone | Capability resolver is complete; next work should map capability requirements to candidate agent responsibilities without provider selection. |
| P2C-D004 | Execution plan design | Phase 2C next milestone | Agent planner is complete; next work should define execution sequencing without provider invocation or LOCKED runtime changes. |
| P2C-D005 | Evidence collection design | Phase 2C next milestone | Execution planner is complete; next work should define evidence capture without authority, scoring, or consensus effects. |
| P2C-D006 | Consensus design | Phase 2C next milestone | Evidence collection is complete; synthesis semantics require a separate design and governance boundary. |

## Governance Constraints

- GG-02 is ratified and in force.
- No LOCKED component modifications without future authorization.
- No Local AI platform redesign.
- No scoring, authority, confidence, rank, or vote-weight changes without future authorization.

## Current Recommendation

Phase 2C may proceed with design, evidence, and non-LOCKED implementation work while preserving all stated constraints.

M1 intent-driven orchestration architecture is ready for implementation planning.

M2 capability resolver reference implementation is complete and ready for agent planner design.

M3 agent planner reference implementation is complete and ready for execution plan design.

M4 execution planner reference implementation is complete and ready for evidence collection design.

M5 evidence collection reference implementation is complete and ready for consensus design.
