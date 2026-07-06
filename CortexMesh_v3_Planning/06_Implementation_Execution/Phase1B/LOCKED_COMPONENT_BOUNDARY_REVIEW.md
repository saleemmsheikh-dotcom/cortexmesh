# Phase 1B LOCKED Component Boundary Review

## Review ID

PHASE1B-LCBR-001

## Date

2026-07-06

## Objective

Determine whether runtime integration of the Phase 1B Local AI provider requires modification of any LOCKED components.

## Scope

This review evaluates candidate integration paths only.

No runtime code was modified.

## Governing Boundary

Current LOCKED components are defined in:

```text
CortexMesh_v3_Planning/04_Architecture/LOCK_REGISTRY_v1.0.md
```

LOCKED components:

| Component | Path |
| --------- | ---- |
| Trust enforcement | `core/contracts.py` |
| ExternalRunner | `core/external_runner.py` |
| Scoring | `competition/scorer.py` |
| Authority | `agents/authority.py` |
| Orchestrator | `orchestrator.py` |
| Snapshots | `governance/snapshot.py` |

Current NOT LOCKED entries include:

| Component | Path |
| --------- | ---- |
| Memory | `memory/memory_store.py` |
| Entropy | `engine/entropy.py` |
| Evolution | `evolution/` |
| Ledger | `ledger/` |

Historical note: `memory/memory_store.py` appeared in the Session 09 retrospective ratification record, but the current explicit lock registry classifies Memory as NOT LOCKED. This review uses the current lock registry as controlling policy and records the historical ambiguity as a caution.

## Existing Runtime Path

The current runtime path is:

```text
main.py
  -> engine.runner.run_task(task)
    -> memory.memory_store.load_memory()
    -> orchestrator.orchestrate(task, memory)
      -> build_solvers(mode, memory)
      -> solver.act(task, ledger)
      -> competition.scorer.score_solution(...)
      -> agents.authority.AuthorityAgent.decide(...)
      -> governance.snapshot.create_governance_snapshot(...)
```

Relevant observations:

- `orchestrator.py` is LOCKED.
- `competition/scorer.py` is LOCKED.
- `agents/authority.py` is LOCKED.
- `governance/snapshot.py` is LOCKED.
- `core/external_runner.py` is LOCKED.
- `engine/runner.py`, `engine/model_router.py`, `agents/solver.py`, and `agents/local_solver.py` are not listed as LOCKED.
- `orchestrator.build_solvers()` already selects `LocalSolverAgent` in `dev` mode and `SolverAgent` otherwise.
- `engine.mode_manager.get_mode()` can select `dev` mode without modifying `orchestrator.py`.

## Candidate Integration Points

| ID | Candidate integration point | Required changes | LOCKED components affected | Classification |
| -- | --------------------------- | ---------------- | -------------------------- | -------------- |
| IP-01 | Modify `orchestrator.build_solvers()` to instantiate a Local AI solver or provider client directly. | Change `orchestrator.py` imports/selection logic. | `orchestrator.py` | REQUIRES_BOARD_AUTHORIZATION |
| IP-02 | Modify orchestration flow to add Local AI as an additional candidate, fallback path, or refinement pass. | Change solver loop, ledger flow, fallback handling, or refinement behavior in `orchestrator.py`. | `orchestrator.py` | REQUIRES_BOARD_AUTHORIZATION |
| IP-03 | Modify scoring to treat Local AI provenance, model identity, or provider metadata specially. | Change `competition/scorer.py`. | `competition/scorer.py` | REQUIRES_BOARD_AUTHORIZATION |
| IP-04 | Modify final decision logic to account for Local AI provider/model identity. | Change `agents/authority.py`. | `agents/authority.py` | REQUIRES_BOARD_AUTHORIZATION |
| IP-05 | Modify governance snapshots to include Local AI-specific runtime state. | Change `governance/snapshot.py`. | `governance/snapshot.py` | REQUIRES_BOARD_AUTHORIZATION |
| IP-06 | Execute Local AI as an external capability through the existing capability gateway and Docker isolation. | If using the existing gateway only for sidecar evidence, no locked change; if Local AI must become a solver candidate, `orchestrator.py` changes are required. Local Ollama access from isolated Docker may also require `core/external_runner.py` network policy changes. | Potentially `orchestrator.py`, `core/external_runner.py` | DEFERRED |
| IP-07 | Route `SolverAgent` model calls through `engine/model_router.py` to the Local AI provider when configured. | Change non-locked `engine/model_router.py` and configuration only. Preserve the existing `call_model(system_prompt, user_prompt)` contract. | None identified | SAFE |
| IP-08 | Replace or extend `agents/local_solver.py` so existing dev-mode `LocalSolverAgent` calls the Local AI provider and returns the current solver result schema. | Change non-locked `agents/local_solver.py` and/or add non-locked Local AI client glue. Uses existing dev-mode selection without changing `orchestrator.py`. | None identified | SAFE |
| IP-09 | Add a new non-locked Local AI agent module and invoke it from a new non-locked runner wrapper outside the current orchestrator path. | Add wrapper around or parallel to `engine.runner.run_task()` for evaluation/evidence only. Does not affect current orchestrator unless later wired in. | None identified for wrapper-only use | SAFE for wrapper-only evaluation; DEFERRED for production runtime |
| IP-10 | Persist Local AI configuration or verification evidence in memory/reporting. | May touch `memory/memory_store.py` or Phase 1B evidence files. Current registry says memory is NOT LOCKED, but historical Session 09 records create caution. | None under current registry | SAFE with caution |

## Classification Summary

### SAFE

- IP-07: Local AI via `engine/model_router.py`.
- IP-08: Local AI via existing `agents/local_solver.py` dev-mode solver path.
- IP-09: Non-locked wrapper-only evaluation path.
- IP-10: Memory/evidence persistence under current lock registry, with caution.

### REQUIRES_BOARD_AUTHORIZATION

- IP-01: Direct `orchestrator.py` solver construction changes.
- IP-02: Direct `orchestrator.py` runtime flow changes.
- IP-03: `competition/scorer.py` Local AI-aware scoring changes.
- IP-04: `agents/authority.py` Local AI-aware authority changes.
- IP-05: `governance/snapshot.py` Local AI-specific snapshot changes.

### DEFERRED

- IP-06: External capability gateway integration as a solver path.

Reason: sidecar capability execution may be possible with no runtime code changes, but using that result as an actual solver candidate would require locked orchestration changes. Local Ollama access from Docker isolation may also require changing `core/external_runner.py`, which is LOCKED and currently uses `--network=none`.

## Recommended Path

Recommended safest path: IP-08 first, with IP-07 as the secondary option.

Implementation shape:

1. Keep the Phase 1B Local AI provider implementation under the non-locked Phase 1B or agent/model adapter area.
2. Extend `agents/local_solver.py` or adjacent non-locked Local AI agent glue to call the provider-independent Local AI interface.
3. Preserve the existing solver output schema consumed by `orchestrator.py`:

```text
agent
base_agent
confidence
solution
```

4. Preserve provider provenance as candidate metadata only.
5. Do not derive confidence, score, rank, vote weight, or authority from provider identity.
6. Do not modify `orchestrator.py`, `competition/scorer.py`, `agents/authority.py`, `core/external_runner.py`, `core/contracts.py`, or `governance/snapshot.py`.

Rationale:

- The existing runtime already routes to `LocalSolverAgent` in `dev` mode.
- `agents/local_solver.py` is not listed as LOCKED.
- This path avoids changing solver selection, scoring, authority, trust enforcement, snapshotting, and external isolation boundaries.
- It validates Local AI as an agent output candidate, matching the Phase 1B architecture principle.

## Board Authorization Determination

Board authorization is not required before implementing the recommended IP-08 path, provided implementation remains limited to non-LOCKED files and preserves the existing orchestrator-facing solver contract.

Board authorization is required before implementing any path that modifies:

- `orchestrator.py`
- `core/external_runner.py`
- `competition/scorer.py`
- `agents/authority.py`
- `core/contracts.py`
- `governance/snapshot.py`

Board authorization is also required before treating provider identity as confidence, authority, rank, vote weight, or final-decision evidence.

## Result

LOCKED component boundary review complete.

Runtime integration can proceed only through the recommended non-locked path or another SAFE path. Any direct orchestration, scoring, authority, ExternalRunner, trust enforcement, or snapshot integration remains blocked until explicit unanimous Board authorization is recorded.
