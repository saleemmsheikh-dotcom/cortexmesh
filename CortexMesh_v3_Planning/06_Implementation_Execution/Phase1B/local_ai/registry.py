"""Provider registry and selection helpers for Phase 1B Local AI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .capabilities import DEFAULT_PROVIDER_CAPABILITIES
from .config import LocalAIConfig
from .provider import LocalAIProvider


ProviderFactory = Callable[[], LocalAIProvider]


@dataclass(frozen=True)
class ProviderRegistration:
    """Local AI provider registration metadata."""

    name: str
    factory: ProviderFactory | None
    default_base_url: str
    default_model: str
    status: str = "available"
    notes: str = ""
    capabilities: tuple[str, ...] = DEFAULT_PROVIDER_CAPABILITIES

    @property
    def implemented(self) -> bool:
        return self.factory is not None


def _ollama_factory() -> LocalAIProvider:
    from .ollama import OllamaProvider

    return OllamaProvider()


PROVIDER_REGISTRY: dict[str, ProviderRegistration] = {
    "ollama": ProviderRegistration(
        name="ollama",
        factory=_ollama_factory,
        default_base_url="http://localhost:11434",
        default_model="qwen2.5-coder:7b",
        notes="Implemented Phase 1B adapter.",
        capabilities=("text_generation", "health_check"),
    ),
    "lmstudio": ProviderRegistration(
        name="lmstudio",
        factory=None,
        default_base_url="http://localhost:1234",
        default_model="local-model",
        status="placeholder",
        notes="Future OpenAI-compatible local adapter placeholder.",
        capabilities=("chat_completion", "text_generation", "health_check"),
    ),
}


def registered_provider_names(include_placeholders: bool = True) -> list[str]:
    """Return known provider names in registry order."""

    return [
        name
        for name, registration in PROVIDER_REGISTRY.items()
        if include_placeholders or registration.implemented
    ]


def implemented_provider_names() -> list[str]:
    """Return provider names with implemented factories."""

    return registered_provider_names(include_placeholders=False)


def provider_options(raw_options: str | None = None) -> list[str]:
    """Parse a comma-separated provider option list."""

    if not raw_options:
        return implemented_provider_names()

    options = [item.strip().lower() for item in raw_options.split(",") if item.strip()]
    return options or implemented_provider_names()


def get_registration(provider_name: str) -> ProviderRegistration:
    """Return registration or fail cleanly for unknown providers."""

    normalized = provider_name.strip().lower()
    try:
        return PROVIDER_REGISTRY[normalized]
    except KeyError as exc:
        known = ", ".join(registered_provider_names())
        raise ValueError(f"unknown Local AI provider: {provider_name}; known providers: {known}") from exc


def create_provider(provider_name: str) -> LocalAIProvider:
    """Create an implemented provider adapter or fail cleanly."""

    registration = get_registration(provider_name)
    if registration.factory is None:
        raise ValueError(
            f"Local AI provider is registered but not implemented: {provider_name}"
        )
    return registration.factory()


def select_provider(provider_name: str, options: list[str]) -> tuple[str, LocalAIProvider]:
    """Select a provider by explicit name or by the first configured option."""

    normalized = provider_name.strip().lower()

    if normalized and normalized != "auto":
        return normalized, create_provider(normalized)

    errors: list[str] = []
    for option in options:
        try:
            return option, create_provider(option)
        except ValueError as exc:
            errors.append(str(exc))

    if not options:
        raise ValueError("no Local AI provider options configured")

    raise ValueError(
        "no implemented Local AI provider found in configured options: "
        + ", ".join(options)
        + (f"; errors: {' | '.join(errors)}" if errors else "")
    )


def auto_select_available_provider(
    options: list[str],
    config_factory: Callable[[str], LocalAIConfig],
) -> tuple[str, LocalAIProvider, LocalAIConfig]:
    """Select the first provider whose connection check succeeds."""

    diagnostics: list[str] = []

    for option in options:
        try:
            provider = create_provider(option)
            config = config_factory(option)
            check = provider.check_connection(config)
            if check.ok:
                return option, provider, config
            diagnostics.append(f"{option}: {check.status} {check.error or check.diagnostics}")
        except Exception as exc:  # pragma: no cover - live endpoint dependent
            diagnostics.append(f"{option}: {exc}")

    raise RuntimeError(
        "no available Local AI provider passed connection check: "
        + "; ".join(diagnostics)
    )
