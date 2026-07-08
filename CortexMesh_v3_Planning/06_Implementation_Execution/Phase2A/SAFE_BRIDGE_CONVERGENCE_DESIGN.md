# SAFE Bridge Convergence Design

## Milestone

Phase 2A M1 - SAFE Bridge Convergence Design

## Status

READY FOR IMPLEMENTATION

---

## Purpose

Design the convergence of `agents/local_ai_bridge.py` onto `LocalAIManager` before making runtime code changes.

This design preserves the SAFE `LocalSolverAgent` integration path and avoids LOCKED component modification.

---

## Current State

Current SAFE path:

```text
LocalSolverAgent
    -> agents/local_ai_bridge.py
        -> provider registry helpers
        -> provider adapter
```

The bridge currently performs provider selection by calling registry helpers directly.

Phase 2A should converge this to:

```text
LocalSolverAgent
    -> agents/local_ai_bridge.py
        -> LocalAIManager
            -> provider registry
            -> provider adapter
```

---

## Required Design Outcome

`LocalAIManager` becomes the Local AI subsystem entry point used by the SAFE bridge.

The bridge remains a thin compatibility layer for `LocalSolverAgent`.

---

## Preserved Contracts

### LocalSolverAgent Output Schema

The solver-facing output must remain unchanged:

```text
agent
base_agent
confidence
solution
provenance
```

### Confidence

Confidence remains unchanged.

The SAFE LocalSolver path continues to use the existing static local solver default:

```text
0.5
```

Provider, model, capability, telemetry, or health metadata must not alter confidence.

### Provenance

Provider/model metadata remains provenance only.

The returned provenance must remain non-authoritative:

```text
authoritative: false
```

### Provider Identity

Provider identity must not influence:

- scoring;
- authority;
- confidence;
- rank;
- vote weight;
- governance decisions.

---

## Proposed Bridge Shape

The bridge should:

1. Load existing environment configuration.
2. Convert bridge configuration into `LocalAIManagerSettings`.
3. Create a `LocalAIRequest` using the existing prompt and request ID logic.
4. Call `LocalAIManager.generate(request)`.
5. Convert `LocalAIManagerResult` into the existing bridge return shape.
6. Preserve current failure behavior.

The bridge should not call provider registry helpers directly after convergence.

---

## Fallback and Error Behavior

Current compatibility expectations:

- If Local AI is disabled, `generate_local_solution()` returns `None`.
- If Local AI is enabled but provider selection or generation fails, the error propagates as it does today.
- `LocalSolverAgent` behavior remains unchanged for disabled Local AI.
- No orchestrator fallback behavior is modified.

The convergence implementation must preserve these expectations.

---

## LOCKED Component Boundary

The design does not require changes to:

- `orchestrator.py`
- `competition/scorer.py`
- `agents/authority.py`
- `core/contracts.py`
- `core/external_runner.py`
- `governance/snapshot.py`

No runtime orchestration changes are proposed.

---

## Verification Plan

Implementation should verify:

1. Local AI disabled path still returns `None`.
2. Explicit provider selection still works.
3. Auto provider selection still works through `LocalAIManager`.
4. Returned solution string is unchanged in shape.
5. Provenance remains non-authoritative.
6. Confidence source remains static local solver default.
7. No provider metadata affects score, authority, confidence, rank, or vote weight.
8. Full regression suite passes.

Expected commands:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile agents/local_ai_bridge.py agents/local_solver.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_phase1b_provider_selection -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover tests
```

---

## Design Conclusion

The SAFE bridge can converge on `LocalAIManager` without changing public contracts, solver schema, confidence behavior, provenance semantics, or LOCKED components.

Conclusion:

```text
READY FOR IMPLEMENTATION
```
