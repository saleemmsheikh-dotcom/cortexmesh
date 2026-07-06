"""Configuration model for Phase 1B Local AI providers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


class LocalAIConfigError(ValueError):
    """Raised when Local AI configuration is invalid."""


@dataclass(frozen=True)
class LocalAIConfig:
    """Provider-independent Local AI configuration."""

    provider: str
    base_url: str
    model: str
    timeout_seconds: float = 30.0
    temperature: float | None = None
    max_tokens: int | None = None
    system_prompt: str | None = None
    provider_options: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self, registered_providers: set[str] | None = None) -> None:
        provider = self.provider.strip()
        if not provider:
            raise LocalAIConfigError("provider must be explicit")
        if registered_providers is not None and provider not in registered_providers:
            raise LocalAIConfigError(f"provider is not registered: {provider}")
        if not self.base_url.strip():
            raise LocalAIConfigError("base_url must be explicit")
        if not self.model.strip():
            raise LocalAIConfigError("model must be explicit")
        if self.timeout_seconds <= 0:
            raise LocalAIConfigError("timeout_seconds must be positive")
        if self.temperature is not None and self.temperature < 0:
            raise LocalAIConfigError("temperature must not be negative")
        if self.max_tokens is not None and self.max_tokens <= 0:
            raise LocalAIConfigError("max_tokens must be positive when provided")

    @property
    def normalized_base_url(self) -> str:
        return self.base_url.rstrip("/")
