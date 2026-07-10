# Intent-Driven Orchestration

## Status

PROPOSED

## Purpose

Define the Phase 2C orchestration pipeline that transforms user intent into coordinated agent execution while preserving provider neutrality, evidence traceability, and governance constraints.

This is an architecture milestone only. It does not authorize implementation.

## Core Principle

User intent drives orchestration.

Capabilities drive agent selection.

Agents own execution.

`LocalAIManager` owns provider selection.

Providers never influence orchestration decisions.

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

## Orchestration Pipeline

```text
User Request
        |
        v
Intent Analysis
        |
        v
Capability Resolution
        |
        v
Agent Selection
        |
        v
Execution Planning
        |
        v
LocalAIManager
        |
        v
Provider
        |
        v
Evidence Collection
        |
        v
Consensus (future)
        |
        v
Final Response
```

## Definitions

### Intent

Intent is the structured interpretation of the user's objective, constraints, requested outcome, and relevant context.

Intent is not a provider instruction.

Intent is not a score.

### Capability

A capability is a provider-neutral description of what an agent or subsystem can support.

Capabilities guide routing and planning.

Capabilities do not rank providers.

### Agent

An agent is an execution participant responsible for reasoning or producing an output within its assigned role.

Agents own execution behavior within the constraints of the execution plan.

### Execution Plan

An execution plan is the structured assignment of tasks, agents, dependencies, evidence requirements, and fallback behavior.

An execution plan does not modify scoring, confidence, authority, rank, or vote weight.

### Evidence

Evidence is the recorded material produced or referenced during orchestration.

Evidence may include observations, assumptions, reasoning, diagnostics, provenance, and outputs.

Evidence is not authority.

### Provenance

Provenance records where outputs, diagnostics, or evidence came from.

Provider and model identity are provenance only.

Provenance does not affect scoring, confidence, authority, rank, or vote weight.

### Consensus

Consensus is a future evidence synthesis layer.

Consensus is not voting.

Consensus does not transfer authority to the system.

## Responsibilities

### Intent Analyzer

The Intent Analyzer transforms the user request into structured intent.

Responsibilities:

- identify objective;
- identify constraints;
- identify requested output form;
- identify ambiguity;
- identify required capability categories;
- preserve user-facing context.

Non-responsibilities:

- provider selection;
- scoring;
- authority decisions;
- confidence modification.

### Capability Resolver

The Capability Resolver maps structured intent to required capabilities.

Responsibilities:

- derive required capabilities from intent;
- identify optional capabilities;
- preserve provider neutrality;
- produce capability requirements for agent planning.

Non-responsibilities:

- provider ranking;
- model preference;
- authority decisions.

### Agent Planner

The Agent Planner selects agent roles and prepares an execution plan.

Responsibilities:

- map capability requirements to agent responsibilities;
- preserve schema compatibility;
- define evidence requirements;
- define fallback behavior;
- define execution sequence.

Non-responsibilities:

- direct provider calls;
- Local AI provider selection;
- score or authority changes.

### Execution Coordinator

The Execution Coordinator runs the execution plan through agents and approved subsystem entry points.

Responsibilities:

- coordinate agent execution;
- call `LocalAIManager` where Local AI execution is required;
- collect execution evidence;
- preserve provenance;
- record diagnostics.

Non-responsibilities:

- direct provider adapter access;
- provider registry access;
- capability registry mutation;
- authority changes.

### Future Consensus Layer

The future Consensus Layer synthesizes evidence across agent outputs.

Responsibilities:

- identify agreement;
- identify disagreement;
- preserve minority findings;
- prepare evidence synthesis.

Non-responsibilities:

- voting;
- final authority;
- scoring changes.

### Future Adaptive Layer

The future Adaptive Layer may adjust orchestration behavior based on evidence, capability fit, diagnostics, and task context.

Responsibilities:

- recommend orchestration adjustments;
- preserve rollback paths;
- preserve traceability.

Non-responsibilities:

- provider ranking;
- hidden confidence changes;
- authority changes.

## Design Constraints

- Architecture only.
- No implementation.
- No runtime changes.
- No `LocalAIManager` changes.
- No `LocalAIProvider` changes.
- No LOCKED component modifications.
- Provider identity remains provenance only.
- Confidence semantics remain unchanged.

## Architecture Decision

Phase 2C orchestration shall be intent-first and capability-driven.

Provider access remains encapsulated behind `LocalAIManager`.

Provider implementations remain invisible to orchestration decisions.

## Recommendation

READY FOR IMPLEMENTATION, subject to future milestone-specific boundary checks and any required authorization for LOCKED component impact.
