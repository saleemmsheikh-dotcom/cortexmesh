# Gate T0: Architectural Inventory

## Status
COMPLETE

## Date
2026-06-11

## Board
- Kimi
- DeepSeek
- ChatGPT

## Purpose
Gate T0 records the first v3 planning inventory after the CortexMesh v2 certified baseline was archived and frozen. This document identifies the current module surface, runtime path, dead-code candidates, risk register, and board recommendations for the next planning gates.

## Scope
This inventory excludes:
- `CortexMesh_v2_Baseline/`
- `.git/`
- `__pycache__/`
- test harness and research-only artifacts unless they affect architecture decisions

The board summary records 55 catalogued architecture modules. Static filesystem inspection also shows two additional legacy/helper modules that should be handled during cleanup review.

## Certified vs Implemented Matrix
| Area | Status | Notes |
|------|--------|-------|
| CONTRACTS_v2 | CERTIFIED | Boundary and trust enforcement archived in v2 baseline. |
| GOVERNANCE_v2 | CERTIFIED | Tamper detection, recovery, freeze, and rollback accepted for v2. |
| CORE_v2 | CERTIFIED | Scoring, authority, memory, and orchestration paths accepted for v2. |
| ExternalRunner | IMPLEMENTED | Docker-backed execution with audit trail and timeout kill path. |
| Docker Isolation | IMPLEMENTED | Network disabled, read-only filesystem, memory and CPU caps. |
| Entropy Monitoring | IMPLEMENTED | Orchestration-only, not authority scoring. |
| v3 Planning | OPEN | Architecture debt review may proceed. |

## Module Inventory Summary
Primary runtime areas:
- `agents/`
- `competition/`
- `config/`
- `core/`
- `cost/`
- `engine/`
- `evolution/`
- `governance/`
- `ledger/`
- `memory/`
- `main.py`
- `orchestrator.py`

Additional non-runtime or helper areas:
- `audit/`
- `capabilities/`
- `research/`
- `testing/`
- `tests/`
- `external_runner_local.py`

## Runtime Execution Path
```text
main.py
  -> engine.runner.run_task(task)
    -> memory.memory_store.load_memory()
    -> orchestrator.orchestrate(task, memory)
      -> cleanup_knowledge_memory()
      -> classify_task()
      -> Ledger()
      -> enforce_governance()
      -> spawn_successors()
      -> build_solvers()
      -> select_unique_agents()
      -> solver.act()
      -> record_solution_structure()
      -> detect_conflict()
      -> critic.review()
      -> score_solution()
      -> AuthorityAgent.decide()
      -> record_lesson()
      -> update_used_lessons()
      -> update_used_negative_lessons()
      -> update_active_conflicts()
      -> record_negative_lesson()
      -> decay_lessons()
      -> prune_memory()
      -> log_confidence()
      -> record_failure()
      -> update_role_weights()
      -> TaskTrustLedger reward/penalize
      -> run_evolution()
      -> entropy_correction()
      -> compute_rebalance()
      -> enforce_governance()
      -> update_governance_stability()
      -> create_governance_snapshot()
```

## Import Dependency Highlights
Core runtime path:
- `orchestrator.py` imports agents, selection, scoring, governance, memory, evolution, entropy correction, and rebalancing.
- `engine/runner.py` wraps orchestration with memory persistence and report generation.
- `agents/authority.py` consumes scorer output and applies diversity, repetition, trust, calibration, and specialist boost.
- `competition/scorer.py` is the canonical scoring path.
- `core/external_runner.py` is the only approved external capability boundary.
- `memory/memory_store.py` owns persistent schema creation, migration, load, save, and report shaping.

## Dead Code Candidates
| Candidate | Evidence | Recommendation |
|-----------|----------|----------------|
| `competition/selector.py` | No runtime references found; signature appears stale against current scorer API. | Deprecate or remove in T1. |
| `engine/agent_weights.py` | No references found. | Review for deletion. |
| `engine/structure_memory.repetition_penalty()` | `structure_hash()` is used; repetition function is superseded by `core/repetition.py`. | Split or remove unused function. |
| `core/capability_sandbox.py` | Deprecated D+ hard-fail shim; no runtime references found. | Keep only if compatibility warning is required. |
| `external_runner_local.py` | Manual Docker IPC smoke-test helper; no runtime references found. | Move to tools or archive. |
| `memory/trust_ledger.py` | No references found; active trust path uses `memory/task_trust.py`. | Review for deletion or migration. |

## Risk Register
| Risk | Severity | Notes |
|------|----------|-------|
| Legacy selector drift | Medium | `competition/selector.py` may mislead future agents. |
| Duplicate repetition logic | Medium | Two repetition functions exist with different semantics. |
| Deprecated sandbox naming | Medium | `capability_sandbox.py` may confuse boundary model. |
| Docker daemon trust | High | Accepted v2 limitation; should be revisited for v3. |
| Memory schema sprawl | Medium | Persistent memory has many evolving top-level keys. |
| Research/testing overlap | Low | Research and testing harnesses are useful but not clearly separated from runtime. |
| Archive/tag drift | Medium | Certified tag has moved several times as archive artifacts were added. |

## Board Recommendations
### T1: Dead Code Review
- Decide whether to remove or archive `competition/selector.py`.
- Decide whether to remove `engine/agent_weights.py`.
- Consolidate repetition logic.
- Decide whether `core/capability_sandbox.py` remains as a compatibility shim.

### T2: Memory Architecture Review
- Document persistent memory schema.
- Split operational memory, governance memory, and research artifacts.
- Define migration rules for v3.

### Phase B: Isolation Roadmap
- Evaluate rootless Docker.
- Evaluate VM-backed isolation.
- Define ExternalRunner backend interface if multi-backend support is needed.

### Phase C: Runtime Surface Cleanup
- Separate runtime, audit, research, and testing modules.
- Move manual helper scripts out of production root.
- Create explicit module ownership map.

## Gate T0 Result
Gate T0 is complete.

Proceed to T1 only after board acknowledgement.
