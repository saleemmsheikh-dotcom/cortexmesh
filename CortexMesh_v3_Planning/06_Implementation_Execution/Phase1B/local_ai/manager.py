"""Provider-neutral Local AI manager skeleton for Phase 1B."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, replace
from typing import Any, Mapping

from .capabilities import CAPABILITY_REGISTRY, Capability, get_capability, normalize_capability_name
from .config import LocalAIConfig
from .provider import ConnectionCheck, LocalAIProvider, LocalAIRequest, LocalAIResponse
from .registry import PROVIDER_REGISTRY, ProviderRegistration, provider_options


@dataclass(frozen=True)
class LocalAIManagerSettings:
    """Provider-neutral manager settings."""

    enabled: bool = False
    provider: str = "ollama"
    provider_options: tuple[str, ...] = ("ollama",)
    base_url: str = ""
    model: str = ""
    timeout_seconds: float = 60.0
    temperature: float | None = 0.0
    max_tokens: int | None = 256
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "LocalAIManagerSettings":
        """Load manager settings from environment variables."""

        return cls(
            enabled=os.getenv("CORTEX_LOCAL_AI_ENABLED", "").lower()
            in {"1", "true", "yes"},
            provider=os.getenv("CORTEX_LOCAL_AI_PROVIDER", "ollama").strip().lower(),
            provider_options=tuple(
                provider_options(os.getenv("CORTEX_LOCAL_AI_PROVIDER_OPTIONS", "ollama"))
            ),
            base_url=os.getenv("CORTEX_LOCAL_AI_BASE_URL", ""),
            model=os.getenv("CORTEX_LOCAL_AI_MODEL", ""),
            timeout_seconds=float(os.getenv("CORTEX_LOCAL_AI_TIMEOUT", "60")),
            temperature=float(os.getenv("CORTEX_LOCAL_AI_TEMPERATURE", "0")),
            max_tokens=int(os.getenv("CORTEX_LOCAL_AI_MAX_TOKENS", "256")),
            metadata={"configuration_source": "environment"},
        )


@dataclass(frozen=True)
class LocalAIHealthResult:
    """Structured manager health-check result."""

    provider: str
    ok: bool
    status: str
    endpoint_ref: str
    latency_ms: int
    error: str | None = None
    diagnostics: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_check(cls, check: ConnectionCheck) -> "LocalAIHealthResult":
        return cls(
            provider=check.provider,
            ok=check.ok,
            status=check.status,
            endpoint_ref=check.endpoint_ref,
            latency_ms=check.latency_ms,
            error=check.error,
            diagnostics=check.diagnostics,
        )

    @classmethod
    def from_error(cls, provider: str, error: Exception) -> "LocalAIHealthResult":
        return cls(
            provider=provider,
            ok=False,
            status="failed",
            endpoint_ref="unavailable",
            latency_ms=0,
            error=str(error),
            diagnostics={},
        )

    def as_diagnostics(self) -> Mapping[str, Any]:
        return {
            "provider": self.provider,
            "ok": self.ok,
            "status": self.status,
            "endpoint_ref": self.endpoint_ref,
            "latency_ms": self.latency_ms,
            "error": self.error,
            "diagnostics": dict(self.diagnostics),
        }


@dataclass(frozen=True)
class LocalAISelection:
    """Selected provider and provider-neutral diagnostics."""

    provider_name: str
    provider: LocalAIProvider
    config: LocalAIConfig
    selection_mode: str
    diagnostics: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LocalAIManagerResult:
    """Provider-neutral generation result."""

    response: LocalAIResponse
    provenance: Mapping[str, Any]
    diagnostics: Mapping[str, Any]


class LocalAIManager:
    """Coordinate provider-neutral Local AI selection and diagnostics."""

    def __init__(
        self,
        settings: LocalAIManagerSettings | None = None,
        registry: Mapping[str, ProviderRegistration] | None = None,
    ):
        self.settings = settings or LocalAIManagerSettings.from_env()
        self.registry = dict(registry or PROVIDER_REGISTRY)

    def capabilities(self) -> Mapping[str, Any]:
        """Return provider capability metadata without ranking providers."""

        providers = {}
        for name, registration in self.registry.items():
            providers[name] = {
                "implemented": registration.implemented,
                "status": registration.status,
                "default_base_url": registration.default_base_url,
                "default_model": registration.default_model,
                "capabilities": list(registration.capabilities),
                "notes": registration.notes,
            }

        return {
            "providers": providers,
            "capability_registry": {
                name: capability.as_dict()
                for name, capability in CAPABILITY_REGISTRY.items()
            },
            "configured_provider": self.settings.provider,
            "configured_options": list(self.settings.provider_options),
            "capabilities_are_provenance_only": True,
            "ranking_used": False,
        }

    def list_capabilities(
        self,
        implemented_only: bool = True,
    ) -> list[Capability]:
        """List declared capabilities without ranking providers."""

        names: set[str] = set()
        for registration in self.registry.values():
            if implemented_only and not registration.implemented:
                continue
            names.update(normalize_capability_name(name) for name in registration.capabilities)

        return [get_capability(name) for name in CAPABILITY_REGISTRY if name in names]

    def supports(
        self,
        capability: str | Capability,
        implemented_only: bool = True,
    ) -> bool:
        """Return whether any registered provider declares a capability."""

        normalized = normalize_capability_name(capability)
        for registration in self.registry.values():
            if implemented_only and not registration.implemented:
                continue
            declared = {
                normalize_capability_name(name)
                for name in registration.capabilities
            }
            if normalized in declared:
                return True
        return False

    def build_config(self, provider_name: str) -> LocalAIConfig:
        """Build provider config from settings and registry defaults."""

        registration = self._registration(provider_name)
        return LocalAIConfig(
            provider=provider_name,
            base_url=self.settings.base_url or registration.default_base_url,
            model=self.settings.model or registration.default_model,
            timeout_seconds=self.settings.timeout_seconds,
            temperature=self.settings.temperature,
            max_tokens=self.settings.max_tokens,
            metadata={
                **dict(self.settings.metadata),
                "provider_selection": self.settings.provider,
                "provider_options": list(self.settings.provider_options),
            },
        )

    def select_provider(self) -> LocalAISelection:
        """Select explicit provider or auto-select by availability."""

        requested = self.settings.provider.strip().lower()
        if requested == "auto":
            return self._auto_select()

        provider = self._create_provider(requested)
        config = self.build_config(requested)
        provider.validate_config(config)
        health = self.health_result(requested)
        if not health.ok:
            raise RuntimeError(
                "selected Local AI provider is unavailable: "
                f"{requested}; status={health.status}; error={health.error}; "
                f"endpoint={health.endpoint_ref}"
            )
        return LocalAISelection(
            provider_name=requested,
            provider=provider,
            config=config,
            selection_mode="explicit",
            diagnostics={
                "provider_selection": requested,
                "provider_options": list(self.settings.provider_options),
                "ranking_used": False,
                "availability_checked": True,
                "health": health.as_diagnostics(),
            },
        )

    def check_health(self, provider_name: str | None = None) -> ConnectionCheck:
        """Run a non-destructive health check through a provider adapter."""

        selected = provider_name or self.settings.provider
        if selected == "auto":
            selection = self._auto_select()
            return selection.provider.check_connection(selection.config)

        provider = self._create_provider(selected)
        config = self.build_config(selected)
        return provider.check_connection(config)

    def health_result(self, provider_name: str) -> LocalAIHealthResult:
        """Return structured health diagnostics for a provider."""

        try:
            return LocalAIHealthResult.from_check(self.check_health(provider_name))
        except Exception as exc:
            return LocalAIHealthResult.from_error(provider_name, exc)

    def generate(self, request: LocalAIRequest) -> LocalAIManagerResult:
        """Generate through the selected provider and return provenance."""

        selection = self.select_provider()
        effective_request = request
        if not request.model.strip():
            effective_request = replace(request, model=selection.config.model)

        response = selection.provider.generate(effective_request, selection.config)
        provenance = {
            "provider": response.provider,
            "model": response.model,
            "selected_provider": selection.provider_name,
            "provider_selection": self.settings.provider,
            "provider_options": list(self.settings.provider_options),
            "request_id": response.request_id,
            "endpoint_ref": response.diagnostics.get("endpoint_ref"),
            "status": response.status,
            "latency_ms": response.latency_ms,
            "finish_reason": response.finish_reason,
            "authoritative": False,
        }
        diagnostics = {
            **dict(selection.diagnostics),
            "manager": "LocalAIManager",
            "ranking_used": False,
            "provider_identity_is_provenance_only": True,
        }
        return LocalAIManagerResult(
            response=response,
            provenance=provenance,
            diagnostics=diagnostics,
        )

    def _auto_select(self) -> LocalAISelection:
        diagnostics: list[Mapping[str, Any]] = []

        for option in self.settings.provider_options:
            try:
                provider = self._create_provider(option)
                config = self.build_config(option)
                health = LocalAIHealthResult.from_check(provider.check_connection(config))
            except Exception as exc:
                health = LocalAIHealthResult.from_error(option, exc)
                diagnostics.append(health.as_diagnostics())
                continue

            diagnostics.append(health.as_diagnostics())
            if health.ok:
                return LocalAISelection(
                    provider_name=option,
                    provider=provider,
                    config=config,
                    selection_mode="auto",
                    diagnostics={
                        "provider_selection": "auto",
                        "provider_options": list(self.settings.provider_options),
                        "availability_checked": True,
                        "ranking_used": False,
                        "selection_basis": "availability",
                        "health_checks": diagnostics,
                    },
                )

        raise RuntimeError(
            "no available Local AI provider passed manager health checks: "
            + str(diagnostics)
        )

    def _registration(self, provider_name: str) -> ProviderRegistration:
        normalized = provider_name.strip().lower()
        try:
            return self.registry[normalized]
        except KeyError as exc:
            known = ", ".join(self.registry)
            raise ValueError(
                f"unknown Local AI provider: {provider_name}; known providers: {known}"
            ) from exc

    def _create_provider(self, provider_name: str) -> LocalAIProvider:
        registration = self._registration(provider_name)
        if registration.factory is None:
            raise ValueError(
                f"Local AI provider is registered but not implemented: {provider_name}"
            )
        return registration.factory()
