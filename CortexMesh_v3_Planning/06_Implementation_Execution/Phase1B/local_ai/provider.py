"""Provider-independent Local AI interface for Phase 1B."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol

from .config import LocalAIConfig


@dataclass(frozen=True)
class LocalAIRequest:
    """Provider-independent generation request."""

    prompt: str
    model: str
    request_id: str
    objective_ref: str
    system_prompt: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    timeout_seconds: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.prompt.strip():
            raise ValueError("prompt must be non-empty")
        if not self.model.strip():
            raise ValueError("model must be explicit")
        if not self.request_id.strip():
            raise ValueError("request_id must be explicit")
        if not self.objective_ref.strip():
            raise ValueError("objective_ref must be explicit")
        if self.max_tokens is not None and self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive when provided")
        if self.timeout_seconds is not None and self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive when provided")


@dataclass(frozen=True)
class LocalAIResponse:
    """Provider-independent generation response."""

    request_id: str
    provider: str
    model: str
    content: str
    status: str
    latency_ms: int
    usage: Mapping[str, Any] = field(default_factory=dict)
    finish_reason: str | None = None
    raw_response_ref: str | None = None
    diagnostics: Mapping[str, Any] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class ConnectionCheck:
    """Provider-independent connection check result."""

    provider: str
    model: str
    endpoint_ref: str
    ok: bool
    status: str
    latency_ms: int
    diagnostics: Mapping[str, Any] = field(default_factory=dict)
    error: str | None = None


class LocalAIProvider(Protocol):
    """Protocol every Local AI provider adapter must implement."""

    def name(self) -> str:
        """Return the provider adapter name."""

    def validate_config(self, config: LocalAIConfig) -> None:
        """Validate provider configuration."""

    def check_connection(self, config: LocalAIConfig) -> ConnectionCheck:
        """Run a non-destructive connection check."""

    def generate(self, request: LocalAIRequest, config: LocalAIConfig) -> LocalAIResponse:
        """Generate a response using provider-specific transport."""
