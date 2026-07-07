"""Provider-neutral observability primitives for Phase 1B Local AI."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from .provider import ConnectionCheck, LocalAIRequest, LocalAIResponse


EVENT_PROVIDER_LIFECYCLE = "provider_lifecycle"
EVENT_CAPABILITY_DISCOVERY = "capability_discovery"
EVENT_HEALTH_CHECK = "health_check"
EVENT_REQUEST_TIMING = "request_timing"
EVENT_RESPONSE_TIMING = "response_timing"

FORBIDDEN_TELEMETRY_KEYS = frozenset(
    {
        "authority",
        "confidence",
        "rank",
        "score",
        "vote_weight",
    }
)


def new_trace_id(prefix: str = "local-ai") -> str:
    """Return an opaque trace identifier."""

    safe_prefix = prefix.strip() or "local-ai"
    return f"{safe_prefix}-{uuid.uuid4().hex}"


def utc_timestamp() -> str:
    """Return a UTC timestamp suitable for diagnostics export."""

    return datetime.now(timezone.utc).isoformat()


def _clean_diagnostics(diagnostics: Mapping[str, Any] | None) -> dict[str, Any]:
    """Remove decision-affecting keys from telemetry diagnostics."""

    if not diagnostics:
        return {}
    return {
        key: value
        for key, value in diagnostics.items()
        if key not in FORBIDDEN_TELEMETRY_KEYS
    }


@dataclass(frozen=True)
class LocalAIEvent:
    """Structured Local AI telemetry event.

    Events are informational only. They must never influence authority,
    confidence, ranking, scoring, vote weight, or governance decisions.
    """

    event_type: str
    trace_id: str
    correlation_id: str
    timestamp_utc: str = field(default_factory=utc_timestamp)
    provider: str | None = None
    model: str | None = None
    capability: str | None = None
    request_id: str | None = None
    status: str | None = None
    latency_ms: int | None = None
    diagnostics: Mapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "trace_id": self.trace_id,
            "correlation_id": self.correlation_id,
            "timestamp_utc": self.timestamp_utc,
            "provider": self.provider,
            "model": self.model,
            "capability": self.capability,
            "request_id": self.request_id,
            "status": self.status,
            "latency_ms": self.latency_ms,
            "diagnostics": _clean_diagnostics(self.diagnostics),
            "informational_only": True,
            "ranking_used": False,
        }


def provider_lifecycle_event(
    provider: str,
    status: str,
    trace_id: str,
    correlation_id: str,
    diagnostics: Mapping[str, Any] | None = None,
) -> LocalAIEvent:
    """Create a provider lifecycle telemetry event."""

    return LocalAIEvent(
        event_type=EVENT_PROVIDER_LIFECYCLE,
        trace_id=trace_id,
        correlation_id=correlation_id,
        provider=provider,
        status=status,
        diagnostics=_clean_diagnostics(diagnostics),
    )


def capability_discovery_event(
    capabilities: Iterable[str],
    trace_id: str,
    correlation_id: str,
    provider: str | None = None,
) -> LocalAIEvent:
    """Create a capability discovery telemetry event."""

    declared = sorted({str(capability) for capability in capabilities})
    return LocalAIEvent(
        event_type=EVENT_CAPABILITY_DISCOVERY,
        trace_id=trace_id,
        correlation_id=correlation_id,
        provider=provider,
        status="observed",
        diagnostics={"capabilities": declared},
    )


def health_check_event(
    check: ConnectionCheck,
    trace_id: str,
    correlation_id: str,
) -> LocalAIEvent:
    """Create a health-check telemetry event."""

    return LocalAIEvent(
        event_type=EVENT_HEALTH_CHECK,
        trace_id=trace_id,
        correlation_id=correlation_id,
        provider=check.provider,
        model=check.model,
        status=check.status,
        latency_ms=check.latency_ms,
        diagnostics={
            **_clean_diagnostics(check.diagnostics),
            "endpoint_ref": check.endpoint_ref,
            "ok": check.ok,
            "error": check.error,
        },
    )


def request_timing_event(
    request: LocalAIRequest,
    provider: str,
    trace_id: str,
    correlation_id: str,
) -> LocalAIEvent:
    """Create a request timing telemetry event."""

    return LocalAIEvent(
        event_type=EVENT_REQUEST_TIMING,
        trace_id=trace_id,
        correlation_id=correlation_id,
        provider=provider,
        model=request.model,
        request_id=request.request_id,
        status="started",
        diagnostics=_clean_diagnostics(request.metadata),
    )


def response_timing_event(
    response: LocalAIResponse,
    trace_id: str,
    correlation_id: str,
) -> LocalAIEvent:
    """Create a response timing telemetry event."""

    return LocalAIEvent(
        event_type=EVENT_RESPONSE_TIMING,
        trace_id=trace_id,
        correlation_id=correlation_id,
        provider=response.provider,
        model=response.model,
        request_id=response.request_id,
        status=response.status,
        latency_ms=response.latency_ms,
        diagnostics={
            **_clean_diagnostics(response.diagnostics),
            "finish_reason": response.finish_reason,
        },
    )


class LocalAITelemetryBuffer:
    """In-memory telemetry collector for diagnostics export."""

    def __init__(self) -> None:
        self._events: list[LocalAIEvent] = []

    def record(self, event: LocalAIEvent) -> LocalAIEvent:
        self._events.append(event)
        return event

    def extend(self, events: Iterable[LocalAIEvent]) -> None:
        for event in events:
            self.record(event)

    def events(self) -> tuple[LocalAIEvent, ...]:
        return tuple(self._events)

    def export_diagnostics(self) -> dict[str, Any]:
        return {
            "events": [event.as_dict() for event in self._events],
            "event_count": len(self._events),
            "telemetry_is_informational_only": True,
            "ranking_used": False,
        }
