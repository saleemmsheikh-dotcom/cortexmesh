# Phase 2C M10 - Reference Orchestration Engine Architecture

## Purpose

Define the deterministic reference coordinator for the completed Phase 2C planning, evidence, consensus, and synthesis components. The engine demonstrates pipeline composition only. It is not the CortexMesh runtime orchestrator and does not invoke agents or providers.

## Pipeline

The engine coordinates this fixed sequence:

1. `CapabilityResolver.resolve(intent)`
2. `AgentPlanner.plan(capability_resolution)`
3. `ExecutionPlanner.plan(agent_plan, dependencies)`
4. Match caller-supplied simulated outputs to planned execution steps
5. `EvidenceCollector.collect(evidence_inputs)`
6. `ConsensusEvaluator.evaluate(evidence_bundle)`
7. `EvidenceSynthesizer.synthesize(evidence_bundle, consensus_assessment)`
8. Return `OrchestrationResult`

No stage selects a provider, invokes an agent, schedules runtime work, or mutates an existing runtime component.

## Model

### OrchestrationRequest

Contains a stable request identifier, provider-neutral intent, simulated output mappings keyed by planned step identifier, optional planning dependencies, consensus and synthesis policies, and assessment scope.

Simulated output mappings contain descriptive output, assumptions, limitations, and diagnostics. Provider/model identity, authority, score, confidence, rank, vote, vote weight, winning position, approval, and governance fields are prohibited recursively.

### OrchestrationContext

Preserves every intermediate artifact:

- capability resolution;
- agent plan;
- execution plan;
- evidence bundle;
- consensus assessment;
- synthesis result;
- aggregated diagnostics.

It is explicitly marked `simulated_only` and provides traceability rather than runtime state.

### OrchestrationResult

Contains the request identifier, full context, structured synthesis response, and aggregated diagnostics. It is explicitly deterministic, simulated-only, and advisory-only. It contains no provider, authority, score, confidence, rank, vote, governance, or invocation result.

### OrchestrationEngine

Receives all six pipeline components through constructor dependency injection. It has no hidden component registry, provider catalog, agent runtime, Local AI dependency, or global mutable state.

## Simulated Execution Boundary

The engine never manufactures agent reasoning and never calls a planned role. After planning, it matches supplied data to exact `ExecutionStep.step_id` values. Unplanned step identifiers are rejected. Missing step outputs produce explicit diagnostics and no evidence record.

For each supplied step, the engine records the planned role and a planned fulfilled capability, adds simulation provenance, and preserves assumptions, limitations, diagnostics, and trace/correlation identifiers. A supplied capability outside the planned step is rejected.

## Determinism

Determinism is provided by:

- deterministic injected Phase 2C components;
- fixed pipeline stage order;
- execution-step keyed simulation matching;
- stable evidence and diagnostic ordering;
- immutable request, context, and result models;
- no clock, randomness, network, runtime, provider, or mutable-global dependency.

For equal component implementations and equal requests, results are equal.

## Dependency Injection Contract

The engine requires explicit injection of:

- `CapabilityResolver`-like component;
- `AgentPlanner`-like component;
- `ExecutionPlanner`-like component;
- `EvidenceCollector`-like component;
- `ConsensusEvaluator`-like component;
- `EvidenceSynthesizer`-like component.

Missing components are rejected at construction. Injection enables isolated verification and does not authorize substituting runtime invokers or provider selectors.

## Prohibited Semantics

The reference engine must not:

- import or call the LOCKED runtime `orchestrator.py`;
- invoke an agent or provider;
- reference `LocalAIManager` or `LocalAIProvider`;
- select, prefer, rank, or weight providers/models;
- assign authority, score, confidence, rank, vote, or vote weight;
- declare a winner, approval, ratification, or governance outcome;
- alter GG-02 or Board process;
- treat consensus or synthesis output as runtime authorization.

## Diagnostics and Failure Behavior

- Invalid or prohibited request content is rejected before component coordination.
- Unplanned simulated outputs are rejected.
- Missing simulated outputs remain visible as diagnostics and lead naturally to insufficient evidence where applicable.
- Component validation errors propagate without being converted into apparent consensus or synthesis.
- Every successful result retains intermediate artifacts for audit and reproduction.

## LOCKED Boundary

The implementation is isolated in `Phase2C/orchestration/engine.py`. It changes no LOCKED component: `core/contracts.py`, `core/external_runner.py`, `competition/scorer.py`, `agents/authority.py`, `orchestrator.py`, or `governance/snapshot.py`.

This reference engine is not evidence that runtime integration is authorized. Runtime integration requires a separate impact and governance assessment.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Reference coordination is mistaken for runtime execution. | Unreviewed runtime integration may follow. | Mark all models simulated/advisory and keep implementation outside runtime surfaces. |
| Simulated outputs are mistaken for agent-produced results. | Evidence provenance could be misread. | Add explicit simulation provenance and missing-output diagnostics. |
| Injected component is replaced by a provider selector or invoker. | Reference boundary would be breached. | Define narrow component contracts and prohibit runtime/provider dependencies. |
| Aggregated diagnostics are treated as scores. | Descriptive state could gain authority. | Preserve string diagnostics only and expose no numeric quality semantics. |
| Successful end-to-end output is treated as governance approval. | GG-02 could be bypassed. | Keep result advisory-only and require separate runtime integration assessment. |

## Recommendation

READY FOR RUNTIME INTEGRATION ASSESSMENT
