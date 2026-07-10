# Capability Routing Architecture

## Status

PROPOSED

## Purpose

Define how Phase 2C routes work from structured intent to agent execution using capabilities rather than provider identity.

This document complements `INTENT_DRIVEN_ORCHESTRATION.md`.

## Routing Rule

Capabilities drive agent selection.

Providers never drive orchestration decisions.

Provider identity remains provenance only.

Providers execute work. Agents solve problems. Orchestration coordinates agents. Governance constrains orchestration.

```text
Governance
      |
      v
Orchestration
      |
      v
Agents
      |
      v
Providers
```

## Routing Inputs

Capability routing may consider:

- structured intent;
- required capabilities;
- optional capabilities;
- agent role suitability;
- task constraints;
- evidence requirements;
- fallback needs;
- available approved subsystem entry points.

Capability routing must not consider:

- provider brand;
- model brand as a ranking signal;
- provider popularity;
- provider speed as an authority signal;
- confidence changes based on provider identity;
- vote weight changes based on provider identity.

## Routing Stages

### Stage 1 - Intent Capability Extraction

Extract capability requirements from structured intent.

Output:

- required capabilities;
- optional capabilities;
- ambiguity notes;
- evidence requirements.

### Stage 2 - Capability Resolution

Resolve capability requirements against known agent and subsystem capability declarations.

Output:

- candidate agent roles;
- missing capability notes;
- fallback constraints.

### Stage 3 - Agent Selection

Select agents based on capability fit and execution requirements.

Output:

- selected agents;
- selection rationale;
- rejected candidates where relevant;
- evidence requirements.

### Stage 4 - Execution Planning

Construct an execution plan for selected agents.

Output:

- execution sequence;
- dependencies;
- fallback behavior;
- evidence collection points.

### Stage 5 - Local AI Invocation Boundary

When Local AI execution is required, the execution coordinator calls `LocalAIManager`.

`LocalAIManager` owns provider selection and provider invocation.

The routing layer does not call:

- provider registry;
- capability registry;
- telemetry buffers;
- provider adapters;
- provider-specific APIs.

### Stage 6 - Evidence Collection

Collect outputs, diagnostics, provenance, and reasoning evidence.

Provider/model identity is recorded as provenance only.

## Component Responsibilities

### Intent Analyzer

Produces structured intent and capability hints.

### Capability Resolver

Maps intent to provider-neutral capability requirements.

### Agent Planner

Maps capability requirements to agent roles and execution plan candidates.

### Execution Coordinator

Executes the plan through agents and approved subsystem entry points.

### LocalAIManager

Owns provider selection, health checks, capability discovery, diagnostics, telemetry, and provider invocation inside the Local AI subsystem.

### Provider

Executes provider-specific requests behind the Local AI subsystem boundary.

Providers do not influence orchestration decisions.

## Governance Boundaries

- GG-02 remains in force.
- LOCKED component modification requires future explicit authorization.
- Capability routing does not modify scoring.
- Capability routing does not modify authority.
- Capability routing does not modify confidence.
- Capability routing does not modify rank or vote weight.

## Risks

| Risk | Mitigation |
| ---- | ---------- |
| Capability routing becomes provider ranking. | Record provider identity as provenance only. |
| Routing touches LOCKED orchestration code. | Require boundary review before implementation. |
| Evidence is interpreted as authority. | Preserve governance review and authority separation. |
| Consensus is interpreted as voting. | Define consensus as future evidence synthesis only. |

## Architecture Decision

Capability routing is approved as the Phase 2C M1 architectural direction.

Implementation must begin with boundary review and verification evidence.

## Recommendation

READY FOR IMPLEMENTATION, subject to milestone-specific implementation planning and LOCKED component authorization review.
