# Verification Evidence 006 - Provider-Neutral Local AI Selection

## Verification ID

PHASE1B-VE-006

## Date

2026-07-07

## Purpose

Record Phase 1B M3 verification for provider-neutral Local AI selection.

## Objective

Create a provider-neutral selection layer that can choose from available Local AI providers without hard-coding a single provider as the phase objective.

## Scope

In scope:

- Provider registry
- Provider option list
- Explicit provider selection by configuration
- Auto-selection from configured provider options
- Placeholder support for future providers
- Provenance-only provider identity

Out of scope:

- LM Studio adapter implementation
- LOCKED component modification
- Scoring changes
- Authority changes
- Confidence changes
- Vote-weight changes

## Files Added

```text
CortexMesh_v3_Planning/06_Implementation_Execution/Phase1B/local_ai/registry.py
tests/test_phase1b_provider_selection.py
CortexMesh_v3_Planning/06_Implementation_Execution/Phase1B/VERIFICATION_EVIDENCE_006_PROVIDER_NEUTRAL_SELECTION.md
```

## Files Modified

```text
CortexMesh_v3_Planning/06_Implementation_Execution/Phase1B/local_ai/__init__.py
agents/local_ai_bridge.py
CortexMesh_v3_Planning/06_Implementation_Execution/Phase1B/PHASE1B_STATUS.md
CortexMesh_v3_Planning/06_Implementation_Execution/Phase1B/RISKS_AND_BLOCKERS.md
```

## Provider Registry

The provider registry records:

```text
ollama    implemented
lmstudio  placeholder
```

Ollama remains an available provider.

It is no longer treated as the only Phase 1B objective.

## Configuration

Provider selection is controlled by environment configuration:

```text
CORTEX_LOCAL_AI_PROVIDER=ollama
CORTEX_LOCAL_AI_PROVIDER=auto
CORTEX_LOCAL_AI_PROVIDER_OPTIONS=ollama,lmstudio
```

Current defaults preserve existing behavior:

```text
CORTEX_LOCAL_AI_PROVIDER=ollama
CORTEX_LOCAL_AI_PROVIDER_OPTIONS=ollama
```

## Auto-Selection

When configured with:

```text
CORTEX_LOCAL_AI_PROVIDER=auto
```

the selection layer evaluates configured provider options and selects the first implemented provider whose connection check succeeds.

Unavailable or placeholder providers fail cleanly and do not become authoritative.

## Unknown Provider Behavior

Unknown providers fail cleanly with:

```text
unknown Local AI provider
```

Registered but unimplemented providers fail cleanly with:

```text
Local AI provider is registered but not implemented
```

## Provenance

Provider selection metadata is recorded only as provenance:

```text
provider
model
selected_provider
provider_selection
provider_options
```

Provider identity does not affect:

- confidence
- scoring
- authority
- rank
- vote weight
- governance status

## Tests Run

Compile check:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile agents/local_ai_bridge.py CortexMesh_v3_Planning/06_Implementation_Execution/Phase1B/local_ai/__init__.py CortexMesh_v3_Planning/06_Implementation_Execution/Phase1B/local_ai/registry.py tests/test_phase1b_provider_selection.py
```

Result: PASS

Focused provider-selection tests:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_phase1b_provider_selection -v
```

Observed result:

```text
Ran 4 tests in 0.201s
OK
```

Full existing test suite:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover tests
```

Observed result:

```text
Ran 84 tests in 0.164s
OK
```

## LOCKED Component Check

No LOCKED component modification is required or performed.

LOCKED components remain out of scope:

- `orchestrator.py`
- `competition/scorer.py`
- `agents/authority.py`
- `core/contracts.py`
- `core/external_runner.py`
- `governance/snapshot.py`

## Result

PASS

Phase 1B M3 provider-neutral Local AI selection is implemented through the SAFE non-LOCKED path.
