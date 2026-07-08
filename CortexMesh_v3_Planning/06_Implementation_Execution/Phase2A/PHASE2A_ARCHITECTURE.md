# Phase 2A Architecture

## Purpose

Define the architecture posture for Phase 2A Local AI Platform Consolidation.

Phase 2A consolidates the Phase 1B Local AI subsystem without expanding governance scope or modifying LOCKED components.

## Architectural Baseline

Phase 2A inherits from Phase 1B:

- `LocalAIProvider` contract;
- `LocalAIManager`;
- provider registry;
- capability registry;
- telemetry and diagnostics;
- Ollama adapter;
- LM Studio adapter;
- SAFE `LocalSolverAgent` integration path.

## Primary Architectural Rule

`LocalAIManager` is the sole public runtime entry point into the Local AI subsystem.

Runtime callers must not call directly into:

- provider adapters;
- provider registry;
- capability registry;
- telemetry buffers;
- provider-specific utilities.

These remain internal subsystem details.

## SAFE Integration Boundary

The SAFE operational path remains:

```text
LocalSolverAgent
    -> local_ai_bridge
        -> LocalAIManager
            -> provider registry
            -> provider adapter
```

Phase 2A may refine the SAFE bridge, but it must not modify `orchestrator.py` or runtime orchestration.

## Provider Neutrality

Provider identity remains provenance only.

Provider metadata must not affect:

- scoring;
- authority;
- confidence;
- rank;
- vote weight;
- governance decisions.

## Capability-Centric Behavior

Capabilities describe provider functionality as metadata.

Capabilities may inform internal compatibility checks, diagnostics, and evidence, but not scoring, authority, or governance outcomes.

## Telemetry and Diagnostics

Telemetry remains informational only.

Diagnostics should remain structured, actionable, and scrubbed of decision-affecting semantics.

## Public Contracts

The following contracts are preserved:

- `LocalAIProvider`
- `LocalAIRequest`
- `LocalAIResponse`
- `ConnectionCheck`
- `LocalAIConfig`
- `LocalAIManager`

Any proposed change to public contracts requires separate review and explicit justification.

## LOCKED Boundary

No Phase 2A work may modify:

- `orchestrator.py`
- `competition/scorer.py`
- `agents/authority.py`
- `core/contracts.py`
- `core/external_runner.py`
- `governance/snapshot.py`

## Architecture Objective

By the end of Phase 2A, the Local AI subsystem should be easier to extend with future local providers while preserving the SAFE integration model and existing governance boundaries.
