"""Provider-neutral Local AI capability declarations for Phase 1B."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class Capability:
    """Provider-neutral capability metadata.

    Capabilities describe what an adapter can expose. They are operational
    metadata only and must not be used for authority, scoring, ranking, vote
    weight, confidence, or governance decisions.
    """

    name: str
    description: str
    category: str = "generation"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        normalized = normalize_capability_name(self.name)
        if not normalized:
            raise ValueError("capability name is required")
        object.__setattr__(self, "name", normalized)

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "metadata": dict(self.metadata),
            "provenance_only": True,
        }


def normalize_capability_name(capability: str | Capability) -> str:
    """Normalize capability names for registry and manager lookup."""

    if isinstance(capability, Capability):
        return capability.name
    return str(capability).strip().lower().replace("-", "_").replace(" ", "_")


CAPABILITY_REGISTRY: dict[str, Capability] = {
    "text_generation": Capability(
        name="text_generation",
        description="Generate text from a prompt through a local provider.",
    ),
    "chat_completion": Capability(
        name="chat_completion",
        description="Generate chat-style completions through a local provider.",
    ),
    "health_check": Capability(
        name="health_check",
        description="Report local provider availability and diagnostics.",
        category="diagnostics",
    ),
}


DEFAULT_PROVIDER_CAPABILITIES: tuple[str, ...] = (
    "text_generation",
    "health_check",
)


def registered_capability_names() -> list[str]:
    """Return known capability names in registry order."""

    return list(CAPABILITY_REGISTRY)


def get_capability(capability: str | Capability) -> Capability:
    """Return a registered capability or fail cleanly."""

    normalized = normalize_capability_name(capability)
    try:
        return CAPABILITY_REGISTRY[normalized]
    except KeyError as exc:
        known = ", ".join(registered_capability_names())
        raise ValueError(f"unknown Local AI capability: {capability}; known capabilities: {known}") from exc
