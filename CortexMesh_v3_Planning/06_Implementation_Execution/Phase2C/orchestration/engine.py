"""Deterministic Phase 2C reference orchestration pipeline.

The engine coordinates planning components and caller-supplied simulated
outputs.  It never invokes an agent, provider, Local AI component, runtime
orchestrator, authority, scoring, confidence, ranking, voting, or governance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


_PROHIBITED_KEYS = frozenset(
    {
        "provider", "provider_id", "model", "model_id", "model_name", "authority",
        "score", "confidence", "rank", "ranking", "vote", "vote_weight", "winner",
        "governance", "approval", "ratification",
    }
)


@dataclass(frozen=True)
class OrchestrationRequest:
    """Intent plus externally supplied simulated execution outputs."""

    request_id: str
    intent: Any
    simulated_outputs: Mapping[str, Mapping[str, Any]]
    dependencies: tuple[Any, ...] = ()
    consensus_policy: Any = None
    synthesis_policy: Any = None
    scope: str = "reference orchestration"


@dataclass(frozen=True)
class OrchestrationContext:
    """Traceable intermediate artifacts from one reference pipeline run."""

    request_id: str
    capability_resolution: Any
    agent_plan: Any
    execution_plan: Any
    evidence_bundle: Any
    consensus_assessment: Any
    synthesis_result: Any
    diagnostics: tuple[str, ...] = ()
    simulated_only: bool = True


@dataclass(frozen=True)
class OrchestrationResult:
    """Final non-authoritative reference pipeline result."""

    request_id: str
    context: OrchestrationContext
    response: Any
    diagnostics: tuple[str, ...] = ()
    deterministic: bool = True
    simulated_only: bool = True
    advisory_only: bool = True


class OrchestrationEngine:
    """Coordinate injected Phase 2C components over simulated outputs only."""

    def __init__(
        self,
        *,
        capability_resolver: Any,
        agent_planner: Any,
        execution_planner: Any,
        evidence_collector: Any,
        consensus_evaluator: Any,
        evidence_synthesizer: Any,
    ) -> None:
        components = {
            "capability_resolver": capability_resolver,
            "agent_planner": agent_planner,
            "execution_planner": execution_planner,
            "evidence_collector": evidence_collector,
            "consensus_evaluator": consensus_evaluator,
            "evidence_synthesizer": evidence_synthesizer,
        }
        missing = tuple(sorted(name for name, component in components.items() if component is None))
        if missing:
            raise ValueError("all pipeline components must be injected: " + ", ".join(missing))
        self._resolver = capability_resolver
        self._agent_planner = agent_planner
        self._execution_planner = execution_planner
        self._evidence_collector = evidence_collector
        self._consensus_evaluator = consensus_evaluator
        self._synthesizer = evidence_synthesizer

    def run(self, request: OrchestrationRequest) -> OrchestrationResult:
        """Run the reference pipeline without runtime execution."""
        if not isinstance(request, OrchestrationRequest):
            raise TypeError("request must be OrchestrationRequest")
        request_id = _required(request.request_id, "request_id")
        scope = _required(request.scope, "scope")
        _reject_prohibited(request.intent, "intent")
        _reject_prohibited(request.simulated_outputs, "simulated outputs")

        resolution = self._resolver.resolve(request.intent)
        agent_plan = self._agent_planner.plan(resolution)
        execution_plan = self._execution_planner.plan(agent_plan, dependencies=request.dependencies)
        evidence_inputs, simulation_diagnostics = self._evidence_inputs(
            execution_plan, request.simulated_outputs, request_id
        )
        evidence_bundle = self._evidence_collector.collect(
            evidence_inputs,
            diagnostics=simulation_diagnostics,
            trace_id=f"trace:{request_id}",
            correlation_id=request_id,
        )
        consensus_assessment = self._consensus_evaluator.evaluate(
            evidence_bundle, request.consensus_policy, scope=scope
        )
        synthesis_result = self._synthesizer.synthesize(
            evidence_bundle,
            consensus_assessment,
            request.synthesis_policy,
            objective=getattr(getattr(resolution, "intent", None), "objective", "Present evidence"),
            scope=scope,
        )
        diagnostics = _strings(
            tuple(getattr(resolution, "diagnostics", ()))
            + tuple(getattr(agent_plan, "diagnostics", ()))
            + tuple(getattr(execution_plan, "diagnostics", ()))
            + tuple(getattr(evidence_bundle, "diagnostics", ()))
            + tuple(getattr(consensus_assessment, "diagnostics", ()))
            + tuple(getattr(synthesis_result, "diagnostics", ()))
        )
        context = OrchestrationContext(
            request_id=request_id,
            capability_resolution=resolution,
            agent_plan=agent_plan,
            execution_plan=execution_plan,
            evidence_bundle=evidence_bundle,
            consensus_assessment=consensus_assessment,
            synthesis_result=synthesis_result,
            diagnostics=diagnostics,
        )
        return OrchestrationResult(
            request_id=request_id,
            context=context,
            response=synthesis_result,
            diagnostics=diagnostics,
        )

    def _evidence_inputs(
        self,
        execution_plan: Any,
        simulated_outputs: Mapping[str, Mapping[str, Any]],
        request_id: str,
    ) -> tuple[tuple[Mapping[str, Any], ...], tuple[str, ...]]:
        if not isinstance(simulated_outputs, Mapping):
            raise TypeError("simulated_outputs must map step identifiers to output mappings")
        steps = tuple(getattr(execution_plan, "steps", ()))
        planned_ids = {step.step_id for step in steps}
        extra = tuple(sorted(str(key) for key in simulated_outputs if str(key) not in planned_ids))
        if extra:
            raise ValueError("simulated outputs reference unplanned steps: " + ", ".join(extra))

        records = []
        diagnostics = []
        for step in steps:
            supplied = simulated_outputs.get(step.step_id)
            if supplied is None:
                diagnostics.append(f"missing_simulated_output:{step.step_id}")
                continue
            if not isinstance(supplied, Mapping):
                raise TypeError(f"simulated output for {step.step_id} must be a mapping")
            capability = supplied.get("capability_fulfilled")
            if capability is None:
                capability = step.capabilities[0] if step.capabilities else "unspecified"
            if capability not in step.capabilities and step.capabilities:
                raise ValueError(
                    f"simulated output capability is not planned for {step.step_id}: {capability}"
                )
            records.append(
                {
                    "record_id": supplied.get("record_id", f"evidence:{step.step_id}"),
                    "step_id": step.step_id,
                    "agent_role": step.role,
                    "capability_fulfilled": capability,
                    "output": supplied.get("output"),
                    "provenance": {
                        "engine": "phase2c.reference.orchestration_engine",
                        "request_id": request_id,
                        "simulated": True,
                    },
                    "assumptions": supplied.get("assumptions", ()),
                    "limitations": supplied.get("limitations", ()),
                    "diagnostics": supplied.get("diagnostics", ()),
                    "trace_id": supplied.get("trace_id", f"trace:{request_id}:{step.step_id}"),
                    "correlation_id": supplied.get("correlation_id", request_id),
                }
            )
        return tuple(records), tuple(sorted(diagnostics))


def _reject_prohibited(value: Any, location: str) -> None:
    if isinstance(value, Mapping):
        keys = {str(key).strip().lower() for key in value}
        found = tuple(sorted(keys & _PROHIBITED_KEYS))
        if found:
            raise ValueError(f"prohibited orchestration input in {location}: " + ", ".join(found))
        for nested in value.values():
            _reject_prohibited(nested, location)
    elif isinstance(value, (tuple, list, set, frozenset)):
        for nested in value:
            _reject_prohibited(nested, location)


def _strings(values: tuple[Any, ...]) -> tuple[str, ...]:
    return tuple(sorted({text for value in values if (text := _optional(value))}))


def _required(value: Any, name: str) -> str:
    normalized = _optional(value)
    if not normalized:
        raise ValueError(f"{name} is required")
    return normalized


def _optional(value: Any) -> str | None:
    normalized = " ".join(str(value or "").strip().split())
    return normalized or None
