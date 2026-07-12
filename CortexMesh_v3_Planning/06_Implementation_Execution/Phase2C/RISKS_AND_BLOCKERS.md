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
| P2C-R011 | Evidence alignment may be implemented as majority voting or a winning position. | Minority evidence could be suppressed and consensus could acquire implicit authority. | Compare claims categorically, prohibit vote mechanics, and preserve every minority and unmatched claim. | MITIGATED IN ARCHITECTURE |
| P2C-R012 | Exact agreement may be mistaken for correctness. | Shared error could be amplified during synthesis. | Keep assessment advisory-only and retain supporting evidence, assumptions, limitations, and diagnostics. | OPEN |
| P2C-R013 | Consensus normalization may erase material semantic differences. | Divergence could be hidden from synthesis. | Use explicit versioned policies, categorical materiality rationales, and original-evidence traceability. | OPEN |
| P2C-R014 | Provider/model provenance may leak into consensus evaluation. | Provider preference or model reputation could become implicit weighting. | Project identity-neutral consensus inputs and reject provider/model fields at the evaluation boundary. | MITIGATED IN ARCHITECTURE |
| P2C-R015 | Advisory consensus output may be treated as governance approval. | GG-02 and Board process could be bypassed. | Mark output advisory to synthesis only and prohibit governance decision fields or effects. | MITIGATED IN ARCHITECTURE |
| P2C-R016 | Consensus policy aliases or conflict declarations may be incomplete for a domain. | Evidence could be classified as partial or insufficient rather than meaningfully comparable. | Keep policy rules explicit and versioned; preserve unmatched evidence and require domain review before broader use. | OPEN |
| P2C-R017 | A downstream synthesis layer may ignore preserved minority or divergence fields. | Synthesized output could overstate agreement. | Require synthesis design to consume original record identifiers, minority evidence, and unresolved divergences explicitly. | OPEN |
| P2C-R018 | A fluent synthesis summary may be mistaken for verified truth or authority. | Readers could over-trust aligned evidence or bypass independent judgment. | Qualify the consensus category, mark output descriptive/advisory, and prohibit authority or correctness claims. | MITIGATED IN ARCHITECTURE |
| P2C-R019 | Synthesis deduplication may erase attribution, qualifications, or minority evidence. | Traceability and material nuance could be lost. | Deduplicate presentation only; retain every source identifier, assumption, limitation, and unmatched record. | MITIGATED IN ARCHITECTURE |
| P2C-R020 | Material divergence may be buried in a polished summary. | Conflicting evidence could be missed by consumers. | Require divergence in the summary, dedicated divergent findings, and unresolved questions. | MITIGATED IN ARCHITECTURE |
| P2C-R021 | Provider/model provenance may influence synthesis prominence. | Descriptive identity could become implicit rank or authority. | Restrict identity to provenance output and prohibit identity-dependent policy, ordering, grouping, or wording. | MITIGATED IN ARCHITECTURE |
| P2C-R022 | Assessment-to-evidence reference drift may produce unsupported synthesis statements. | Result may misrepresent or omit source evidence. | Validate referential integrity and require every statement and record to remain traceable. | OPEN |
| P2C-R023 | Synthesis empty states may be ignored by a downstream renderer. | Missing findings could appear as silently omitted sections. | Keep every required section in the result and require explicit empty-state reasons. | OPEN |
| P2C-R024 | Evidence not referenced by an assessment may be mistaken for safely discardable input. | Source-of-record evidence could disappear from the response. | Preserve every bundle record in result, provenance, and traceability; emit an explicit omission diagnostic and unresolved question. | MITIGATED IN REFERENCE IMPLEMENTATION |
| P2C-R025 | Reference orchestration may be mistaken for runtime integration. | Runtime or LOCKED changes could proceed without assessment. | Mark engine results simulated/advisory and require a separate runtime integration assessment. | MITIGATED IN REFERENCE IMPLEMENTATION |
| P2C-R026 | Simulated outputs may be mistaken for invoked-agent results. | Evidence origin could be misrepresented. | Attach explicit simulation provenance and report missing simulations rather than invoking agents. | MITIGATED IN REFERENCE IMPLEMENTATION |
| P2C-R027 | A future injected component may introduce provider selection or runtime behavior. | Reference boundaries and provider neutrality could be breached. | Constrain injection contracts and assess all runtime adapters separately before integration. | OPEN |

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
| P2C-D007 | Consensus reference implementation | Phase 2C next milestone | M6 architecture is complete; implementation must remain isolated, deterministic, identity-neutral, and non-authoritative. |
| P2C-D008 | Synthesis design | Phase 2C next milestone | M7 consensus evaluation is complete; synthesis must preserve advisory boundaries, minority evidence, and unresolved divergence. |
| P2C-D009 | Evidence synthesis reference implementation | Phase 2C next milestone | M8 architecture is complete; implementation must validate references and preserve every required output section and boundary. |
| P2C-D010 | Adaptive orchestration design | Phase 2C next milestone | M9 synthesis is complete; adaptation must remain non-authoritative and must not become provider ranking or runtime integration without review. |
| P2C-D011 | Runtime integration assessment | Phase 2C next milestone | M10 proves reference composition only; any runtime connection requires impact, LOCKED-boundary, governance, and rollback assessment. |

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

M6 consensus architecture is complete and ready for an isolated reference implementation.

M7 consensus reference implementation is complete and ready for synthesis design.

M8 evidence synthesis architecture is complete and ready for an isolated reference implementation.

M9 evidence synthesis reference implementation is complete and ready for adaptive orchestration design.

M10 reference orchestration engine is complete and ready for runtime integration assessment.
