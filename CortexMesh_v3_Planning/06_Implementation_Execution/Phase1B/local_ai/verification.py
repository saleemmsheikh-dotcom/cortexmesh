"""Connection verification support for Phase 1B Local AI providers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

from .config import LocalAIConfig
from .provider import LocalAIProvider


@dataclass(frozen=True)
class VerificationRecord:
    """Traceable Local AI connection verification record."""

    verification_id: str
    timestamp_utc: str
    provider: str
    model: str
    endpoint_ref: str
    result: str
    latency_ms: int
    diagnostics: Mapping[str, Any] = field(default_factory=dict)
    failure_reason: str | None = None


def verify_connection(
    provider: LocalAIProvider,
    config: LocalAIConfig,
    verification_id: str,
) -> VerificationRecord:
    """Run provider connection verification and normalize the evidence record."""

    checked = provider.check_connection(config)
    return VerificationRecord(
        verification_id=verification_id,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        provider=checked.provider,
        model=checked.model,
        endpoint_ref=checked.endpoint_ref,
        result="PASS" if checked.ok else "FAIL",
        latency_ms=checked.latency_ms,
        diagnostics=checked.diagnostics,
        failure_reason=checked.error,
    )
