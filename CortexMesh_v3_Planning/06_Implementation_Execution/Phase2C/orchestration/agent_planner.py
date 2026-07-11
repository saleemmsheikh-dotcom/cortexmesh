"""Deterministic Phase 2C agent planner reference implementation.

The planner maps capability requirements to eligible agent roles. It does not
invoke providers, runtime orchestration, scoring, authority, consensus, or
confidence logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


_PROVIDER_KEYS = frozenset({"provider", "provider_id", "model", "model_id", "model_name"})


@dataclass(frozen=True)
class AgentDescriptor:
    """Provider-neutral description of an eligible agent role."""

    role: str
    capabilities: tuple[str, ...]
    description: str = ""

    def normalized(self) -> "AgentDescriptor":
        return AgentDescriptor(
            role=_normalize_token(self.role),
            capabilities=tuple(sorted({_normalize_token(cap) for cap in self.capabilities if cap})),
            description=self.description.strip(),
        )


@dataclass(frozen=True)
class AgentRequirement:
    """Agent role required by one or more distinct capabilities."""

    role: str
    capabilities: tuple[str, ...]
    reason: str
    required: bool = True


@dataclass(frozen=True)
class AgentPlan:
    """Deterministic capability-to-agent planning output."""

    requirements: tuple[AgentRequirement, ...]
    diagnostics: tuple[str, ...] = ()
    provenance: Mapping[str, Any] = field(default_factory=dict)

    def role_names(self) -> tuple[str, ...]:
        """Return planned role names in deterministic order."""
        return tuple(requirement.role for requirement in self.requirements)


class AgentPlanner:
    """Map capability requirements to eligible agent roles."""

    _DEFAULT_AGENTS: tuple[AgentDescriptor, ...] = (
        AgentDescriptor(
            role="architect",
            capabilities=(
                "architecture.api_design",
                "capability.resolution",
                "evidence.synthesis",
                "orchestration.planning",
                "orchestration.routing",
                "reasoning.architecture",
                "reasoning.design",
                "reasoning.engineering",
                "reasoning.planning",
                "reasoning.systems",
            ),
            description="Architecture and orchestration planning role.",
        ),
        AgentDescriptor(
            role="governance_reviewer",
            capabilities=(
                "contract.review",
                "evidence.audit",
                "evidence.traceability",
                "governance.review",
            ),
            description="Governance and traceability review role.",
        ),
        AgentDescriptor(
            role="implementation_engineer",
            capabilities=(
                "code.generation",
                "code.reasoning",
                "code.refactoring",
                "code.review",
                "code.test_design",
            ),
            description="Implementation and test design role.",
        ),
        AgentDescriptor(
            role="risk_reviewer",
            capabilities=(
                "diagnostics.interpretation",
                "memory.integrity_review",
                "risk.assessment",
                "security.review",
            ),
            description="Risk, diagnostics, memory, and security review role.",
        ),
        AgentDescriptor(
            role="research_analyst",
            capabilities=(
                "evidence.collection",
                "evidence.consensus_synthesis",
                "evidence.summarization",
                "reasoning.analysis",
                "reasoning.comparison",
                "reasoning.general",
                "reasoning.review",
            ),
            description="Analysis, review, comparison, and evidence collection role.",
        ),
    )

    def __init__(self, agents: Iterable[AgentDescriptor] | None = None):
        descriptors = agents if agents is not None else self._DEFAULT_AGENTS
        self._agents = tuple(sorted((agent.normalized() for agent in descriptors), key=lambda a: a.role))
        self._capability_to_roles = self._build_capability_index(self._agents)

    def plan(self, capability_resolution: Any) -> AgentPlan:
        """Create an agent plan from a CapabilityResolution-like object."""
        self._reject_provider_identity(capability_resolution)

        capability_names = tuple(sorted(set(self._capability_names(capability_resolution))))
        role_to_capabilities: dict[str, set[str]] = {}
        diagnostics: list[str] = []

        for capability in capability_names:
            roles = self._capability_to_roles.get(capability, ())
            if not roles:
                diagnostics.append(f"missing_capability_coverage:{capability}")
                continue
            for role in roles:
                role_to_capabilities.setdefault(role, set()).add(capability)

        requirements = tuple(
            AgentRequirement(
                role=role,
                capabilities=tuple(sorted(capabilities)),
                reason="distinct capability coverage required",
                required=True,
            )
            for role, capabilities in sorted(role_to_capabilities.items())
        )

        if not requirements:
            diagnostics.append("no_agent_requirements_planned")

        return AgentPlan(
            requirements=requirements,
            diagnostics=tuple(sorted(set(diagnostics))),
            provenance={
                "planner": "phase2c.reference.agent_planner",
                "provenance_only": True,
            },
        )

    def _capability_names(self, capability_resolution: Any) -> tuple[str, ...]:
        if hasattr(capability_resolution, "capability_names"):
            return tuple(_normalize_token(cap) for cap in capability_resolution.capability_names())
        requirements = getattr(capability_resolution, "requirements", ())
        return tuple(_normalize_token(getattr(req, "capability", "")) for req in requirements if req)

    def _reject_provider_identity(self, capability_resolution: Any) -> None:
        mappings = []
        provenance = getattr(capability_resolution, "provenance", None)
        if isinstance(provenance, Mapping):
            mappings.append(provenance)
        intent = getattr(capability_resolution, "intent", None)
        intent_provenance = getattr(intent, "provenance", None)
        if isinstance(intent_provenance, Mapping):
            mappings.append(intent_provenance)

        for mapping in mappings:
            provider_keys = sorted(k for k in mapping if str(k).lower() in _PROVIDER_KEYS)
            if provider_keys:
                raise ValueError(
                    "provider/model identity is not accepted by the agent planner: "
                    + ", ".join(provider_keys)
                )

    def _build_capability_index(
        self, agents: tuple[AgentDescriptor, ...]
    ) -> Mapping[str, tuple[str, ...]]:
        capability_to_roles: dict[str, list[str]] = {}
        for agent in agents:
            for capability in agent.capabilities:
                capability_to_roles.setdefault(capability, []).append(agent.role)
        return {
            capability: tuple(sorted(roles))
            for capability, roles in sorted(capability_to_roles.items())
        }


def _normalize_token(value: str) -> str:
    return " ".join(str(value).strip().lower().split())
