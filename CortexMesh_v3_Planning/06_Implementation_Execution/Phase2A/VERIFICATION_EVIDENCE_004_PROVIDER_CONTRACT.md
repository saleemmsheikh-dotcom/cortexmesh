# Verification Evidence 004 - Provider Contract

## Scope

Phase 2A M3 shared provider contract test suite.

## Date

2026-07-09

## Objective

Create provider-independent contract tests that every `LocalAIProvider` implementation must satisfy.

## Files Created

- `tests/provider_contract.py`
- `tests/test_phase2a_provider_contract.py`
- `PROVIDER_CONTRACT.md`
- `VERIFICATION_EVIDENCE_004_PROVIDER_CONTRACT.md`

## Files Modified

- `PHASE2A_STATUS.md`
- `RISKS_AND_BLOCKERS.md`

## Contract Coverage

The shared contract verifies:

- initialization;
- health checks;
- model discovery diagnostics;
- request validation;
- response normalization;
- diagnostics;
- error handling;
- capability declaration;
- provenance fields.

## Providers Covered

Both providers run through the same contract harness:

- Ollama;
- LM Studio.

No provider-specific exceptions are used.

## Constraints Verified

- No `LocalAIProvider` interface changes.
- No `LocalAIManager` API changes.
- No LOCKED component modifications.
- No provider ranking.
- No runtime orchestration changes.
- No scoring, authority, confidence, rank, or vote-weight effects.

## Verification

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_phase2a_provider_contract -v
```

Result:

```text
test_lmstudio_satisfies_provider_contract ... ok
test_ollama_satisfies_provider_contract ... ok
test_registered_providers_declare_capabilities_without_authority_semantics ... ok

Ran 3 tests in 0.004s

OK
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover tests
```

Result:

```text
Ran 127 tests in 0.154s

OK
```

## LOCKED Component Check

No LOCKED components were modified.

LOCKED components remain:

- `orchestrator.py`
- `competition/scorer.py`
- `agents/authority.py`
- `core/contracts.py`
- `core/external_runner.py`
- `governance/snapshot.py`

## Status

PASS
