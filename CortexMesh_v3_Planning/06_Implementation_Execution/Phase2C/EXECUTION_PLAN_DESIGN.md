# Execution Plan Design

## Status

PROPOSED

## Purpose

Define the Phase 2C Execution Planner that converts `AgentPlan` output into deterministic ordered execution steps.

The planner is a reference implementation under the Phase 2C planning area. It is not runtime orchestration integration.

## Objective

Transform `AgentPlan` into an `ExecutionPlan` without performing:

- agent invocation;
- provider selection;
- provider invocation;
- runtime orchestration;
- scoring;
- confidence changes;
- authority decisions;
- ranking;
- vote-weight changes;
- consensus.

## Model Definitions

### ExecutionStep

Single planned execution step.

Fields:

- step identifier;
- role;
- capability requirements;
- dependencies;
- parallel group;
- parallelizable flag.

### ExecutionDependency

Explicit dependency relationship between planned agent roles.

Fields:

- before role;
- after role;
- reason.

### ExecutionPlan

Planner output containing:

- deterministic ordered steps;
- valid dependencies;
- explicit diagnostics;
- provenance metadata.

### ExecutionPlanner

Deterministic planner that maps agent requirements to execution steps.

The planner does not invoke agents or providers.

## Planning Flow

```text
AgentPlan
    |
    v
Reject Provider/Model Identity
    |
    v
Normalize Agent Requirements
    |
    v
Validate Dependencies
    |
    v
Detect Missing, Invalid, or Cyclic Dependencies
    |
    v
Topologically Order Steps
    |
    v
Emit ExecutionPlan
```

## Dependency Rules

Independent steps have no dependencies and share the same parallel group.

Dependent steps record their prerequisite roles.

Steps in the same parallel group are explicitly marked as parallelizable when the group contains more than one step.

Missing, invalid, or cyclic dependencies produce diagnostics.

Diagnostics are informational only.

## Boundary Rules

- No runtime orchestration changes.
- No agent invocation.
- No provider selection.
- No `LocalAIManager` changes.
- No `LocalAIProvider` changes.
- No LOCKED component modifications.
- No scoring, confidence, authority, rank, vote-weight, or consensus effects.
- Implementation remains isolated under `Phase2C/orchestration/`.

## Provenance Rules

Provenance is informational metadata only.

Provider/model identity is not accepted by the planner.

Planner provenance identifies the reference execution planner and does not influence orchestration decisions.

## Recommendation

The reference Execution Planner is ready for evidence collection design after verification passes.
