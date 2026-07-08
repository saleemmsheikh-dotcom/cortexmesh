# Phase 2A Implementation Plan

## Objective

Consolidate the Local AI subsystem while preserving all Phase 1B public contracts and governance boundaries.

## Milestone Plan

### M1 - SAFE Bridge Convergence Assessment

Assess and, if appropriate, converge `agents/local_ai_bridge.py` on `LocalAIManager`.

Constraints:

- no orchestrator change;
- no scoring change;
- no authority change;
- no confidence or vote-weight change.

### M2 - SAFE Bridge Convergence Implementation

If M1 confirms the path is safe, update the bridge to use `LocalAIManager` as the only Local AI subsystem entry point.

Expected output:

- implementation change limited to non-LOCKED files;
- tests proving behavior unchanged;
- evidence record.

### M3 - Provider Adapter Contract Tests

Create a reusable provider adapter test contract that Ollama and LM Studio can satisfy.

Expected coverage:

- config validation;
- health check normalization;
- request mapping;
- response normalization;
- clean failure behavior;
- provenance-only diagnostics.

### M4 - Provider Adapter Utility Review

Review adapter duplication and extract shared utilities only if it reduces complexity without weakening provider boundaries.

Potential areas:

- endpoint path validation;
- HTTP JSON request handling;
- elapsed timing calculation;
- error normalization.

### M5 - Provider Lifecycle Improvements

Improve lifecycle diagnostics and evidence where useful.

No provider ranking may be introduced.

### M6 - Phase 2A Review and Closeout

Produce Phase 2A closeout evidence and Product Owner review packet.

## Verification Requirements

Every implementation milestone must run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile ...
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover tests
```

## Non-Goals

- Cloud provider implementation.
- MCP implementation.
- LOCKED runtime integration.
- Scoring or authority changes.
- Provider ranking.

## Exit Criteria

Phase 2A exits when:

- SAFE bridge convergence decision is complete;
- provider adapter contract tests exist;
- any utility extraction is completed or explicitly rejected;
- regression suite is green;
- evidence records are complete;
- no governance boundaries were crossed.
