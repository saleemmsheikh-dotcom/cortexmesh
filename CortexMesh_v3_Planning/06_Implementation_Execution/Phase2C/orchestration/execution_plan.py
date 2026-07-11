"""Deterministic Phase 2C execution planner reference implementation.

The execution planner converts an AgentPlan-like object into ordered execution
steps. It does not invoke agents, providers, scoring, authority, consensus, or
runtime orchestration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


_FORBIDDEN_KEYS = frozenset({"provider", "provider_id", "model", "model_id", "model_name"})


@dataclass(frozen=True)
class ExecutionDependency:
    """Dependency relationship between planned agent roles."""

    before: str
    after: str
    reason: str = ""

    def normalized(self) -> "ExecutionDependency":
        return ExecutionDependency(
            before=_normalize_token(self.before),
            after=_normalize_token(self.after),
            reason=self.reason.strip(),
        )


@dataclass(frozen=True)
class ExecutionStep:
    """Single deterministic execution planning step."""

    step_id: str
    role: str
    capabilities: tuple[str, ...]
    depends_on: tuple[str, ...] = ()
    parallel_group: int = 0
    parallelizable: bool = False


@dataclass(frozen=True)
class ExecutionPlan:
    """Reference execution plan output."""

    steps: tuple[ExecutionStep, ...]
    dependencies: tuple[ExecutionDependency, ...] = ()
    diagnostics: tuple[str, ...] = ()
    provenance: Mapping[str, Any] = field(default_factory=dict)

    def step_ids(self) -> tuple[str, ...]:
        """Return planned step identifiers in deterministic order."""
        return tuple(step.step_id for step in self.steps)

    def role_names(self) -> tuple[str, ...]:
        """Return planned role names in execution order."""
        return tuple(step.role for step in self.steps)


class ExecutionPlanner:
    """Convert AgentPlan requirements into deterministic execution steps."""

    def plan(
        self,
        agent_plan: Any,
        dependencies: Iterable[ExecutionDependency] | None = None,
    ) -> ExecutionPlan:
        """Create an execution plan without invoking runtime behavior."""
        self._reject_forbidden_identity(agent_plan)

        requirements = tuple(sorted(self._agent_requirements(agent_plan), key=lambda req: req["role"]))
        dependency_list = tuple(
            dep.normalized() if isinstance(dep, ExecutionDependency) else dep
            for dep in (dependencies or ())
        )

        role_to_caps = {req["role"]: req["capabilities"] for req in requirements}
        role_names = set(role_to_caps)
        diagnostics: list[str] = []
        valid_dependencies: list[ExecutionDependency] = []

        for dep in dependency_list:
            if not isinstance(dep, ExecutionDependency):
                diagnostics.append("invalid_dependency_type")
                continue
            if dep.before == dep.after:
                diagnostics.append(f"invalid_dependency_self:{dep.before}")
                continue
            missing = [role for role in (dep.before, dep.after) if role not in role_names]
            if missing:
                diagnostics.append(
                    f"missing_dependency_role:{dep.before}->{dep.after}:"
                    + ",".join(sorted(missing))
                )
                continue
            valid_dependencies.append(dep)

        ordered_roles, cycle_diagnostics = self._topological_groups(
            tuple(sorted(role_names)),
            tuple(valid_dependencies),
        )
        diagnostics.extend(cycle_diagnostics)

        group_sizes: dict[int, int] = {}
        for _, group in ordered_roles:
            group_sizes[group] = group_sizes.get(group, 0) + 1

        steps = tuple(
            ExecutionStep(
                step_id=f"step-{index:03d}-{role}",
                role=role,
                capabilities=role_to_caps[role],
                depends_on=tuple(
                    sorted(dep.before for dep in valid_dependencies if dep.after == role)
                ),
                parallel_group=group,
                parallelizable=group_sizes[group] > 1,
            )
            for index, (role, group) in enumerate(ordered_roles, start=1)
        )

        if not steps:
            diagnostics.append("no_execution_steps_planned")

        return ExecutionPlan(
            steps=steps,
            dependencies=tuple(valid_dependencies),
            diagnostics=tuple(sorted(set(diagnostics))),
            provenance={
                "planner": "phase2c.reference.execution_planner",
                "provenance_only": True,
            },
        )

    def _agent_requirements(self, agent_plan: Any) -> tuple[dict[str, Any], ...]:
        requirements = []
        for requirement in getattr(agent_plan, "requirements", ()):
            role = _normalize_token(getattr(requirement, "role", ""))
            capabilities = tuple(
                sorted(
                    {
                        _normalize_token(capability)
                        for capability in getattr(requirement, "capabilities", ())
                        if capability
                    }
                )
            )
            if role:
                requirements.append({"role": role, "capabilities": capabilities})
        return tuple(requirements)

    def _reject_forbidden_identity(self, agent_plan: Any) -> None:
        mappings = []
        provenance = getattr(agent_plan, "provenance", None)
        if isinstance(provenance, Mapping):
            mappings.append(provenance)

        for mapping in mappings:
            forbidden_keys = sorted(k for k in mapping if str(k).lower() in _FORBIDDEN_KEYS)
            if forbidden_keys:
                raise ValueError(
                    "provider/model identity is not accepted by the execution planner: "
                    + ", ".join(forbidden_keys)
                )

    def _topological_groups(
        self,
        roles: tuple[str, ...],
        dependencies: tuple[ExecutionDependency, ...],
    ) -> tuple[tuple[tuple[str, int], ...], tuple[str, ...]]:
        remaining = set(roles)
        prerequisites: dict[str, set[str]] = {role: set() for role in roles}
        dependents: dict[str, set[str]] = {role: set() for role in roles}
        for dep in dependencies:
            prerequisites[dep.after].add(dep.before)
            dependents[dep.before].add(dep.after)

        ordered: list[tuple[str, int]] = []
        diagnostics: list[str] = []
        group = 0

        while remaining:
            ready = sorted(role for role in remaining if not prerequisites[role] & remaining)
            if not ready:
                diagnostics.append("cyclic_dependencies:" + ",".join(sorted(remaining)))
                ready = sorted(remaining)
            for role in ready:
                ordered.append((role, group))
                remaining.remove(role)
            group += 1

        return tuple(ordered), tuple(diagnostics)


def _normalize_token(value: str) -> str:
    return " ".join(str(value).strip().lower().split())
