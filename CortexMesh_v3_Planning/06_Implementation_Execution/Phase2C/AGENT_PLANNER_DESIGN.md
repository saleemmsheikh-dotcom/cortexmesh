# Agent Planner Design

## Status

PROPOSED

## Purpose

Define the Phase 2C Agent Planner that maps capability requirements to eligible agent roles.

The planner is a reference implementation under the Phase 2C planning area. It is not runtime orchestration integration.

## Objective

Transform `CapabilityResolution` into deterministic agent role requirements without performing:

- provider selection;
- provider invocation;
- runtime orchestration;
- scoring;
- authority decisions;
- consensus;
- confidence changes;
- ranking;
- vote-weight changes.

## Model Definitions

### AgentDescriptor

Provider-neutral description of an eligible agent role and the capabilities it can cover.

Fields:

- role;
- capabilities;
- description.

### AgentRequirement

Planned agent role required by one or more distinct capability requirements.

Fields:

- role;
- covered capabilities;
- reason;
- required flag.

### AgentPlan

Planner output containing:

- deterministic agent requirements;
- explicit diagnostics;
- provenance metadata.

### AgentPlanner

Deterministic planner that maps capability requirements to eligible agent roles.

The planner does not select providers, invoke providers, score agents, or perform authority decisions.

## Planning Flow

```text
CapabilityResolution
    |
    v
Reject Provider/Model Identity
    |
    v
Extract Capability Names
    |
    v
Resolve Eligible Agent Roles
    |
    v
Emit Missing Coverage Diagnostics
    |
    v
Emit AgentPlan
```

## Eligibility Rule

Capabilities determine agent eligibility.

An agent role is included only when it covers at least one required capability.

Multiple agents may be included only when distinct capabilities require distinct roles.

Agent order is deterministic and lexical. This order is not a quality ranking.

## Diagnostic Rules

Missing capability coverage produces explicit diagnostics.

Diagnostics are informational only.

Diagnostics do not affect confidence, score, authority, rank, or vote weight.

## Provenance Rules

Provenance is informational metadata only.

Provider/model identity is not accepted by the planner.

Planner provenance identifies the reference planner and does not influence orchestration decisions.

## Boundary Rules

- No runtime orchestration changes.
- No provider selection.
- No consensus logic.
- No `LocalAIManager` changes.
- No `LocalAIProvider` changes.
- No LOCKED component modifications.
- Implementation remains isolated under `Phase2C/orchestration/`.

## Recommendation

The reference Agent Planner is ready for execution plan design after verification passes.
