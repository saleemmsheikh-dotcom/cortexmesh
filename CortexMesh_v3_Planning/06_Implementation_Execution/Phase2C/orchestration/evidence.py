"""Descriptive, deterministic Phase 2C evidence collection.

This isolated reference module records execution results.  It does not assign
authority, score, confidence, rank, vote weight, or consensus meaning.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Iterable, Mapping


_AUTHORITY_KEYS = frozenset(
    {"authority", "authority_input", "score", "confidence", "rank", "vote", "vote_weight", "consensus"}
)
_IDENTITY_KEYS = frozenset({"provider", "provider_id", "model", "model_id", "model_name"})


@dataclass(frozen=True)
class EvidenceSource:
    """Descriptive source of an execution output."""

    agent_role: str
    capability_fulfilled: str
    provenance: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvidenceRecord:
    """One normalized execution output and its context."""

    record_id: str
    step_id: str
    source: EvidenceSource
    output: Any
    assumptions: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()
    trace_id: str | None = None
    correlation_id: str | None = None


@dataclass(frozen=True)
class EvidenceBundle:
    """Deterministically ordered descriptive evidence."""

    records: tuple[EvidenceRecord, ...]
    diagnostics: tuple[str, ...] = ()
    trace_id: str | None = None
    correlation_id: str | None = None
    descriptive_only: bool = True


class EvidenceCollector:
    """Normalize execution step outputs into an evidence bundle."""

    def collect(
        self,
        step_outputs: Iterable[EvidenceRecord | Mapping[str, Any]],
        *,
        diagnostics: Iterable[str] = (),
        trace_id: str | None = None,
        correlation_id: str | None = None,
        authority_input: Mapping[str, Any] | None = None,
    ) -> EvidenceBundle:
        if authority_input:
            keys = {str(key).strip().lower() for key in authority_input}
            identities = sorted(keys & _IDENTITY_KEYS)
            if identities:
                raise ValueError(
                    "provider/model identity cannot be used as authority input: "
                    + ", ".join(identities)
                )
            raise ValueError("authority input is not accepted by evidence collection")

        records = [
            self._record(item, trace_id=trace_id, correlation_id=correlation_id)
            for item in step_outputs
        ]
        records.sort(key=lambda record: (record.step_id, record.record_id, _stable(record.output)))
        if len({record.record_id for record in records}) != len(records):
            raise ValueError("evidence record identifiers must be unique")

        return EvidenceBundle(
            records=tuple(records),
            diagnostics=_strings(diagnostics),
            trace_id=_optional(trace_id),
            correlation_id=_optional(correlation_id),
        )

    def _record(
        self,
        item: EvidenceRecord | Mapping[str, Any],
        *,
        trace_id: str | None,
        correlation_id: str | None,
    ) -> EvidenceRecord:
        if isinstance(item, EvidenceRecord):
            self._validate_source(item.source)
            return EvidenceRecord(
                record_id=_required(item.record_id, "record_id"),
                step_id=_required(item.step_id, "step_id"),
                source=self._source(item.source),
                output=_normalize(item.output),
                assumptions=_strings(item.assumptions),
                limitations=_strings(item.limitations),
                diagnostics=_strings(item.diagnostics),
                trace_id=_optional(item.trace_id or trace_id),
                correlation_id=_optional(item.correlation_id or correlation_id),
            )
        if not isinstance(item, Mapping):
            raise TypeError("step outputs must be EvidenceRecord or mapping values")
        forbidden = sorted({str(key).lower() for key in item} & _AUTHORITY_KEYS)
        if forbidden:
            raise ValueError("authoritative evidence fields are not accepted: " + ", ".join(forbidden))
        source_value = item.get("source")
        if isinstance(source_value, EvidenceSource):
            source = source_value
        elif isinstance(source_value, Mapping):
            source = EvidenceSource(
                agent_role=source_value.get("agent_role", ""),
                capability_fulfilled=source_value.get("capability_fulfilled", ""),
                provenance=source_value.get("provenance", {}),
            )
        else:
            source = EvidenceSource(
                agent_role=item.get("agent_role", ""),
                capability_fulfilled=item.get("capability_fulfilled", ""),
                provenance=item.get("provenance", {}),
            )
        self._validate_source(source)
        return EvidenceRecord(
            record_id=_required(item.get("record_id"), "record_id"),
            step_id=_required(item.get("step_id"), "step_id"),
            source=self._source(source),
            output=_normalize(item.get("output")),
            assumptions=_strings(item.get("assumptions", ())),
            limitations=_strings(item.get("limitations", ())),
            diagnostics=_strings(item.get("diagnostics", ())),
            trace_id=_optional(item.get("trace_id") or trace_id),
            correlation_id=_optional(item.get("correlation_id") or correlation_id),
        )

    def _validate_source(self, source: EvidenceSource) -> None:
        if not isinstance(source.provenance, Mapping):
            raise TypeError("source provenance must be a mapping")
        forbidden = sorted({str(key).lower() for key in source.provenance} & _AUTHORITY_KEYS)
        if forbidden:
            raise ValueError("provenance cannot contain authority semantics: " + ", ".join(forbidden))

    def _source(self, source: EvidenceSource) -> EvidenceSource:
        return EvidenceSource(
            agent_role=_required(source.agent_role, "agent_role"),
            capability_fulfilled=_required(source.capability_fulfilled, "capability_fulfilled"),
            provenance=_normalize(source.provenance),
        )


def _required(value: Any, name: str) -> str:
    normalized = " ".join(str(value or "").strip().split())
    if not normalized:
        raise ValueError(f"{name} is required")
    return normalized


def _optional(value: Any) -> str | None:
    normalized = " ".join(str(value or "").strip().split())
    return normalized or None


def _strings(values: Iterable[Any]) -> tuple[str, ...]:
    return tuple(sorted({text for value in values if (text := _optional(value))}))


def _normalize(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _normalize(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, (list, tuple)):
        return tuple(_normalize(item) for item in value)
    if isinstance(value, (set, frozenset)):
        return tuple(sorted((_normalize(item) for item in value), key=_stable))
    return value


def _stable(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), default=repr)
    except (TypeError, ValueError):
        return repr(value)
