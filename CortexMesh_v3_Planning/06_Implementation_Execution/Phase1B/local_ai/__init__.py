"""Phase 1B Local AI reference implementation.

This package is intentionally isolated from runtime integration points until
the required governance and LOCKED-component boundaries are cleared.
"""

from .capabilities import (
    CAPABILITY_REGISTRY,
    DEFAULT_PROVIDER_CAPABILITIES,
    Capability,
    get_capability,
    normalize_capability_name,
    registered_capability_names,
)
from .config import LocalAIConfig, LocalAIConfigError
from .manager import (
    LocalAIHealthResult,
    LocalAIManager,
    LocalAIManagerResult,
    LocalAIManagerSettings,
    LocalAISelection,
)
from .ollama import OllamaProvider
from .provider import LocalAIProvider, LocalAIRequest, LocalAIResponse
from .registry import (
    PROVIDER_REGISTRY,
    ProviderRegistration,
    auto_select_available_provider,
    create_provider,
    get_registration,
    implemented_provider_names,
    provider_options,
    registered_provider_names,
    select_provider,
)
from .telemetry import (
    EVENT_CAPABILITY_DISCOVERY,
    EVENT_HEALTH_CHECK,
    EVENT_PROVIDER_LIFECYCLE,
    EVENT_REQUEST_TIMING,
    EVENT_RESPONSE_TIMING,
    LocalAIEvent,
    LocalAITelemetryBuffer,
    capability_discovery_event,
    health_check_event,
    new_trace_id,
    provider_lifecycle_event,
    request_timing_event,
    response_timing_event,
)
from .verification import VerificationRecord, verify_connection

__all__ = [
    "LocalAIConfig",
    "LocalAIConfigError",
    "LocalAIHealthResult",
    "LocalAIManager",
    "LocalAIManagerResult",
    "LocalAIManagerSettings",
    "LocalAISelection",
    "LocalAIProvider",
    "LocalAIRequest",
    "LocalAIResponse",
    "OllamaProvider",
    "CAPABILITY_REGISTRY",
    "DEFAULT_PROVIDER_CAPABILITIES",
    "Capability",
    "PROVIDER_REGISTRY",
    "ProviderRegistration",
    "VerificationRecord",
    "LocalAIEvent",
    "LocalAITelemetryBuffer",
    "EVENT_CAPABILITY_DISCOVERY",
    "EVENT_HEALTH_CHECK",
    "EVENT_PROVIDER_LIFECYCLE",
    "EVENT_REQUEST_TIMING",
    "EVENT_RESPONSE_TIMING",
    "auto_select_available_provider",
    "capability_discovery_event",
    "create_provider",
    "get_capability",
    "get_registration",
    "health_check_event",
    "implemented_provider_names",
    "normalize_capability_name",
    "new_trace_id",
    "provider_options",
    "provider_lifecycle_event",
    "registered_capability_names",
    "registered_provider_names",
    "request_timing_event",
    "response_timing_event",
    "select_provider",
    "verify_connection",
]
