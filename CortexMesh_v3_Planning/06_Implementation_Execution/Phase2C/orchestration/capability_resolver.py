"""Deterministic Phase 2C capability resolver reference implementation.

The resolver maps normalized user intent to provider-neutral capability
requirements. It does not select agents, select providers, score outputs, alter
confidence, or participate in authority decisions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any, Iterable, Mapping


_TOKEN_RE = re.compile(r"[a-z0-9_+-]+")
_PROVIDER_KEYS = frozenset({"provider", "provider_id", "model", "model_id", "model_name"})


@dataclass(frozen=True)
class IntentDescriptor:
    """Provider-neutral description of normalized user intent."""

    objective: str
    task_type: str = "general"
    domain: str = "general"
    constraints: tuple[str, ...] = ()
    context_terms: tuple[str, ...] = ()
    provenance: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "IntentDescriptor":
        """Build a descriptor from raw input while rejecting provider identity."""
        provider_keys = sorted(k for k in data if k.lower() in _PROVIDER_KEYS)
        if provider_keys:
            raise ValueError(
                "provider/model identity is not accepted by the capability resolver: "
                + ", ".join(provider_keys)
            )

        return cls(
            objective=_normalize_text(str(data.get("objective", ""))),
            task_type=_normalize_text(str(data.get("task_type", "general"))) or "general",
            domain=_normalize_text(str(data.get("domain", "general"))) or "general",
            constraints=_normalize_terms(data.get("constraints", ())),
            context_terms=_normalize_terms(data.get("context_terms", ())),
            provenance=dict(data.get("provenance", {})),
        ).normalized()

    def normalized(self) -> "IntentDescriptor":
        """Return a normalized copy of this descriptor."""
        provenance = dict(self.provenance)
        provider_keys = sorted(k for k in provenance if k.lower() in _PROVIDER_KEYS)
        if provider_keys:
            raise ValueError(
                "provider/model identity is not accepted as resolver provenance: "
                + ", ".join(provider_keys)
            )

        return IntentDescriptor(
            objective=_normalize_text(self.objective),
            task_type=_normalize_text(self.task_type) or "general",
            domain=_normalize_text(self.domain) or "general",
            constraints=_normalize_terms(self.constraints),
            context_terms=_normalize_terms(self.context_terms),
            provenance=provenance,
        )


@dataclass(frozen=True)
class CapabilityRequirement:
    """Provider-neutral capability required by normalized intent."""

    capability: str
    reason: str
    required: bool = True
    source_terms: tuple[str, ...] = ()


@dataclass(frozen=True)
class CapabilityResolution:
    """Result of resolving normalized intent to capability requirements."""

    intent: IntentDescriptor
    requirements: tuple[CapabilityRequirement, ...]
    diagnostics: tuple[str, ...] = ()
    provenance: Mapping[str, Any] = field(default_factory=dict)

    def capability_names(self) -> tuple[str, ...]:
        """Return capability names in deterministic order."""
        return tuple(req.capability for req in self.requirements)


class CapabilityResolver:
    """Resolve normalized intent into provider-neutral capability requirements."""

    _TASK_CAPABILITIES: Mapping[str, tuple[str, ...]] = {
        "analysis": ("reasoning.analysis", "evidence.summarization"),
        "architecture": ("reasoning.architecture", "evidence.synthesis"),
        "comparison": ("reasoning.comparison", "evidence.synthesis"),
        "design": ("reasoning.design", "evidence.synthesis"),
        "implementation": ("code.generation", "code.review"),
        "planning": ("reasoning.planning", "evidence.synthesis"),
        "review": ("reasoning.review", "risk.assessment"),
        "test": ("code.test_design", "risk.assessment"),
    }

    _DOMAIN_CAPABILITIES: Mapping[str, tuple[str, ...]] = {
        "code": ("code.reasoning",),
        "engineering": ("reasoning.engineering",),
        "governance": ("governance.review", "evidence.traceability"),
        "security": ("risk.assessment", "security.review"),
        "systems": ("reasoning.systems", "risk.assessment"),
    }

    _TERM_CAPABILITIES: Mapping[str, str] = {
        "api": "architecture.api_design",
        "audit": "evidence.audit",
        "capability": "capability.resolution",
        "consensus": "evidence.consensus_synthesis",
        "contract": "contract.review",
        "diagnostic": "diagnostics.interpretation",
        "evidence": "evidence.collection",
        "governance": "governance.review",
        "memory": "memory.integrity_review",
        "orchestration": "orchestration.planning",
        "refactor": "code.refactoring",
        "risk": "risk.assessment",
        "routing": "orchestration.routing",
        "security": "security.review",
        "test": "code.test_design",
    }

    def resolve(self, intent: IntentDescriptor | Mapping[str, Any]) -> CapabilityResolution:
        """Resolve intent without selecting agents or providers."""
        descriptor = (
            IntentDescriptor.from_mapping(intent)
            if isinstance(intent, Mapping)
            else intent.normalized()
        )

        requirements: dict[str, CapabilityRequirement] = {}
        diagnostics: list[str] = []

        self._add_task_capabilities(descriptor, requirements, diagnostics)
        self._add_domain_capabilities(descriptor, requirements, diagnostics)
        self._add_term_capabilities(descriptor, requirements, diagnostics)

        if not requirements:
            diagnostics.append("no_capabilities_resolved")
            requirements["reasoning.general"] = CapabilityRequirement(
                capability="reasoning.general",
                reason="fallback capability for unresolved general intent",
                required=True,
                source_terms=("general",),
            )

        return CapabilityResolution(
            intent=descriptor,
            requirements=tuple(requirements[name] for name in sorted(requirements)),
            diagnostics=tuple(sorted(set(diagnostics))),
            provenance={
                "resolver": "phase2c.reference.capability_resolver",
                "provenance_only": True,
            },
        )

    def _add_task_capabilities(
        self,
        descriptor: IntentDescriptor,
        requirements: dict[str, CapabilityRequirement],
        diagnostics: list[str],
    ) -> None:
        task_caps = self._TASK_CAPABILITIES.get(descriptor.task_type)
        if not task_caps:
            diagnostics.append(f"unknown_task_type:{descriptor.task_type}")
            return
        for capability in task_caps:
            requirements.setdefault(
                capability,
                CapabilityRequirement(
                    capability=capability,
                    reason=f"required by task_type:{descriptor.task_type}",
                    source_terms=(descriptor.task_type,),
                ),
            )

    def _add_domain_capabilities(
        self,
        descriptor: IntentDescriptor,
        requirements: dict[str, CapabilityRequirement],
        diagnostics: list[str],
    ) -> None:
        domain_caps = self._DOMAIN_CAPABILITIES.get(descriptor.domain)
        if not domain_caps:
            diagnostics.append(f"unknown_domain:{descriptor.domain}")
            return
        for capability in domain_caps:
            requirements.setdefault(
                capability,
                CapabilityRequirement(
                    capability=capability,
                    reason=f"required by domain:{descriptor.domain}",
                    source_terms=(descriptor.domain,),
                ),
            )

    def _add_term_capabilities(
        self,
        descriptor: IntentDescriptor,
        requirements: dict[str, CapabilityRequirement],
        diagnostics: list[str],
    ) -> None:
        all_terms = set(_tokens(descriptor.objective))
        all_terms.update(descriptor.constraints)
        all_terms.update(descriptor.context_terms)

        unresolved = []
        for term in sorted(all_terms):
            capability = self._TERM_CAPABILITIES.get(term)
            if capability is None:
                unresolved.append(term)
                continue
            requirements.setdefault(
                capability,
                CapabilityRequirement(
                    capability=capability,
                    reason=f"derived from intent term:{term}",
                    source_terms=(term,),
                ),
            )

        if unresolved:
            diagnostics.append("unresolved_terms:" + ",".join(unresolved))


def _normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())


def _normalize_terms(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        terms: Iterable[Any] = (value,)
    else:
        terms = value
    normalized = {_normalize_text(str(term)) for term in terms if str(term).strip()}
    return tuple(sorted(normalized))


def _tokens(value: str) -> tuple[str, ...]:
    return tuple(_TOKEN_RE.findall(_normalize_text(value)))
