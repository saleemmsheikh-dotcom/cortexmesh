# Capability Resolver Design

## Status

PROPOSED

## Purpose

Define the Phase 2C capability resolver that maps normalized user intent to required provider-neutral capabilities.

This resolver is a reference implementation under the Phase 2C planning area. It is not runtime orchestration integration.

## Objective

Transform normalized intent into capability requirements without performing:

- agent selection;
- provider selection;
- scoring;
- authority decisions;
- confidence changes;
- ranking;
- vote-weight changes.

## Model Definitions

### IntentDescriptor

Provider-neutral description of user intent.

Fields:

- objective;
- task type;
- domain;
- constraints;
- context terms;
- provenance metadata.

Provider and model identity are not accepted as intent input.

### CapabilityRequirement

Provider-neutral capability required by the normalized intent.

Fields:

- capability name;
- reason;
- required flag;
- source terms.

### CapabilityResolution

Resolver output containing:

- normalized intent;
- deterministic capability requirements;
- explicit diagnostics;
- provenance metadata.

### CapabilityResolver

Deterministic resolver that maps intent to capability requirements.

The resolver does not select agents or providers.

## Resolution Flow

```text
Raw Intent
    |
    v
Normalize IntentDescriptor
    |
    v
Reject Provider/Model Identity
    |
    v
Resolve Task Capabilities
    |
    v
Resolve Domain Capabilities
    |
    v
Resolve Intent Terms
    |
    v
Emit CapabilityResolution
```

## Diagnostic Rules

Unknown elements produce explicit diagnostics rather than silent guessing.

Diagnostics include:

- unknown task type;
- unknown domain;
- unresolved intent terms;
- no capabilities resolved.

Diagnostics are informational only.

Diagnostics do not affect confidence, score, authority, rank, or vote weight.

## Provenance Rules

Provenance is informational metadata only.

Provider/model identity is not accepted by the resolver.

Resolver provenance identifies the reference resolver and does not influence orchestration decisions.

## Boundary Rules

- No runtime orchestration changes.
- No `LocalAIManager` changes.
- No `LocalAIProvider` changes.
- No LOCKED component modifications.
- Implementation remains isolated under `Phase2C/orchestration/`.

## Recommendation

The reference capability resolver is ready for agent planner design after verification passes.
