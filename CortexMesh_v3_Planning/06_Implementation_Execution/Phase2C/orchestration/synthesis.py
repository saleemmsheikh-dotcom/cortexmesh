"""Deterministic, descriptive Phase 2C evidence synthesis.

This isolated reference implementation presents evidence and an advisory
consensus assessment.  It creates no authority, score, confidence, rank,
vote weight, winning position, or governance decision.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Iterable, Mapping


SECTION_ORDER = (
    "summary",
    "aligned findings",
    "divergent findings",
    "minority evidence",
    "assumptions",
    "limitations",
    "diagnostics",
    "provenance",
    "traceability",
    "unresolved questions",
)

_OUTCOMES = frozenset(
    {
        "exact agreement",
        "compatible agreement",
        "partial agreement",
        "material divergence",
        "insufficient evidence",
    }
)
_IDENTITY_KEYS = frozenset({"provider", "provider_id", "model", "model_id", "model_name"})
_PROHIBITED_KEYS = frozenset(
    {
        "authority", "authority_input", "score", "confidence", "confidence_adjustment",
        "rank", "ranking", "vote", "vote_weight", "winner", "approval", "ratification",
        "governance", "governance_decision",
    }
)


@dataclass(frozen=True)
class SynthesisInput:
    """Validated request containing evidence and an advisory assessment."""

    evidence_bundle: Any
    consensus_assessment: Any
    objective: str = "Present available evidence"
    scope: str | None = None


@dataclass(frozen=True)
class SynthesisSection:
    """One ordered, attributable part of a synthesis response."""

    name: str
    items: tuple[str, ...]
    evidence_record_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    correlation_ids: tuple[str, ...] = ()
    empty_reason: str | None = None


@dataclass(frozen=True)
class SynthesisResult:
    """Final descriptive and advisory structured response."""

    synthesis_id: str
    scope: str
    consensus_category: str
    sections: tuple[SynthesisSection, ...]
    evidence_record_ids: tuple[str, ...]
    policy_name: str
    policy_version: str
    diagnostics: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    correlation_ids: tuple[str, ...] = ()
    descriptive_only: bool = True
    advisory_output: bool = True
    governance_boundary: str = "Governance decisions remain outside synthesis under GG-02."

    def section(self, name: str) -> SynthesisSection:
        """Return a required section by its canonical name."""
        normalized = _text(name).lower()
        for section in self.sections:
            if section.name == normalized:
                return section
        raise KeyError(name)


@dataclass(frozen=True)
class SynthesisPolicy:
    """Deterministic presentation rules without decision semantics."""

    name: str = "phase2c.default.synthesis"
    version: str = "1"
    include_empty_sections: bool = True
    empty_section_text: str = "No supported content is available for this section."
    presentation_context: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _reject_prohibited(self.presentation_context, "synthesis policy", allow_identity=False)


class EvidenceSynthesizer:
    """Create a structured response without changing evidence semantics."""

    def synthesize(
        self,
        evidence_bundle: Any,
        consensus_assessment: Any,
        policy: SynthesisPolicy | None = None,
        *,
        objective: str = "Present available evidence",
        scope: str | None = None,
    ) -> SynthesisResult:
        policy = policy or SynthesisPolicy()
        request = SynthesisInput(evidence_bundle, consensus_assessment, _required(objective, "objective"), scope)
        records = self._records(request.evidence_bundle)
        assessment = request.consensus_assessment
        self._validate_assessment(assessment)
        record_by_id = {self._record_id(record): record for record in records}
        if len(record_by_id) != len(records):
            raise ValueError("evidence record identifiers must be unique")

        referenced = self._referenced_ids(assessment)
        missing = tuple(sorted(set(referenced) - set(record_by_id)))
        if missing:
            raise ValueError("consensus assessment references missing evidence: " + ", ".join(missing))

        assessment_ids = _strings(getattr(assessment, "evidence_record_ids", ()))
        extra = tuple(sorted(set(record_by_id) - set(assessment_ids)))
        result_scope = _required(scope or getattr(assessment, "scope", None), "scope")
        outcome = _text(getattr(assessment, "outcome", "")).lower()

        for record in records:
            _reject_prohibited(getattr(record, "output", None), "evidence output", allow_identity=False)
            source = getattr(record, "source", None)
            if source is None:
                raise TypeError("evidence record source is required")
            provenance = getattr(source, "provenance", {})
            _reject_prohibited(provenance, "evidence provenance", allow_identity=True)

        aligned = self._aligned_items(assessment)
        divergent = self._divergent_items(assessment)
        minority_ids = _strings(getattr(assessment, "minority_evidence_record_ids", ()))
        minority = tuple(
            f"{record_id}: {self._output_text(record_by_id[record_id])}" for record_id in minority_ids
        )
        assumptions = self._attributed(records, "assumptions")
        limitations = self._attributed(records, "limitations")
        diagnostics = _strings(
            tuple(getattr(evidence_bundle, "diagnostics", ()))
            + tuple(getattr(assessment, "diagnostics", ()))
            + tuple(value for record in records for value in getattr(record, "diagnostics", ()))
            + (("evidence_not_referenced_by_assessment:" + ",".join(extra),) if extra else ())
        )
        provenance = self._provenance_items(records)
        traceability = self._traceability_items(records)
        unresolved = self._unresolved_items(assessment, outcome, extra)
        summary = (self._summary(outcome, aligned, divergent, minority, assessment),)

        traces = _strings(getattr(record, "trace_id", None) for record in records)
        correlations = _strings(getattr(record, "correlation_id", None) for record in records)
        section_values = {
            "summary": (summary, tuple(record_by_id)),
            "aligned findings": (aligned, self._signal_ids(getattr(assessment, "agreement_signals", ())),),
            "divergent findings": (divergent, self._signal_ids(getattr(assessment, "divergence_signals", ())),),
            "minority evidence": (minority, minority_ids),
            "assumptions": (assumptions, tuple(record_by_id)),
            "limitations": (limitations, tuple(record_by_id)),
            "diagnostics": (diagnostics, tuple(record_by_id)),
            "provenance": (provenance, tuple(record_by_id)),
            "traceability": (traceability, tuple(record_by_id)),
            "unresolved questions": (unresolved, self._signal_ids(getattr(assessment, "unresolved_divergences", ())),),
        }
        sections = tuple(
            self._section(name, *section_values[name], traces=traces, correlations=correlations, policy=policy)
            for name in SECTION_ORDER
        )
        synthesis_id = "synthesis:" + ":".join(
            (_token(policy.name), _token(policy.version), _token(result_scope), _token(outcome))
        )
        return SynthesisResult(
            synthesis_id=synthesis_id,
            scope=result_scope,
            consensus_category=outcome,
            sections=sections,
            evidence_record_ids=tuple(sorted(record_by_id)),
            policy_name=_required(policy.name, "policy name"),
            policy_version=_required(policy.version, "policy version"),
            diagnostics=diagnostics,
            trace_ids=traces,
            correlation_ids=correlations,
        )

    def synthesize_input(
        self, synthesis_input: SynthesisInput, policy: SynthesisPolicy | None = None
    ) -> SynthesisResult:
        """Convenience entry point for the explicit input model."""
        if not isinstance(synthesis_input, SynthesisInput):
            raise TypeError("synthesis_input must be SynthesisInput")
        return self.synthesize(
            synthesis_input.evidence_bundle,
            synthesis_input.consensus_assessment,
            policy,
            objective=synthesis_input.objective,
            scope=synthesis_input.scope,
        )

    def _records(self, bundle: Any) -> tuple[Any, ...]:
        if isinstance(bundle, Mapping) or not hasattr(bundle, "records"):
            raise TypeError("synthesis requires an EvidenceBundle-like input")
        records = tuple(bundle.records)
        if any(not hasattr(record, "record_id") or not hasattr(record, "output") for record in records):
            raise TypeError("synthesis requires EvidenceRecord-like records")
        return tuple(sorted(records, key=self._record_id))

    def _validate_assessment(self, assessment: Any) -> None:
        if isinstance(assessment, Mapping) or not hasattr(assessment, "outcome"):
            raise TypeError("synthesis requires a ConsensusAssessment-like input")
        if getattr(assessment, "advisory_to_synthesis_only", None) is not True:
            raise ValueError("ConsensusAssessment must remain advisory to synthesis only")
        outcome = _text(assessment.outcome).lower()
        if outcome not in _OUTCOMES:
            raise ValueError("unsupported consensus assessment category: " + outcome)
        values = vars(assessment) if hasattr(assessment, "__dict__") else {}
        _reject_prohibited(values, "consensus assessment", allow_identity=False)

    def _referenced_ids(self, assessment: Any) -> tuple[str, ...]:
        ids = list(getattr(assessment, "evidence_record_ids", ()))
        ids.extend(getattr(assessment, "minority_evidence_record_ids", ()))
        for field_name in ("agreement_signals", "divergence_signals", "unresolved_divergences"):
            for signal in getattr(assessment, field_name, ()):
                ids.extend(getattr(signal, "evidence_record_ids", ()))
        return _strings(ids)

    def _aligned_items(self, assessment: Any) -> tuple[str, ...]:
        items = []
        for signal in sorted(getattr(assessment, "agreement_signals", ()), key=lambda item: item.signal_id):
            claims = ", ".join(signal.aligned_claims) or "aligned evidence"
            ids = ", ".join(signal.evidence_record_ids)
            items.append(f"{signal.alignment_kind}: {claims} [evidence: {ids}]")
        return tuple(items)

    def _divergent_items(self, assessment: Any) -> tuple[str, ...]:
        items = []
        unresolved_ids = {signal.signal_id for signal in getattr(assessment, "unresolved_divergences", ())}
        for signal in sorted(getattr(assessment, "divergence_signals", ()), key=lambda item: item.signal_id):
            claims = " | ".join(signal.conflicting_claims) or "unmatched evidence"
            ids = ", ".join(signal.evidence_record_ids)
            state = "unresolved" if signal.signal_id in unresolved_ids else signal.resolution_state
            items.append(
                f"{signal.divergence_kind} ({'material' if signal.material else 'non-material'}, "
                f"{state}): {claims} [evidence: {ids}]"
            )
        return tuple(items)

    def _attributed(self, records: tuple[Any, ...], field_name: str) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    f"{self._record_id(record)}: {_text(value)}"
                    for record in records
                    for value in getattr(record, field_name, ())
                    if _optional(value)
                }
            )
        )

    def _provenance_items(self, records: tuple[Any, ...]) -> tuple[str, ...]:
        items = []
        for record in records:
            source = record.source
            encoded = json.dumps(getattr(source, "provenance", {}), sort_keys=True, separators=(",", ":"), default=repr)
            items.append(
                f"{self._record_id(record)}: role={_text(source.agent_role)}; "
                f"capability={_text(source.capability_fulfilled)}; provenance={encoded}"
            )
        return tuple(items)

    def _traceability_items(self, records: tuple[Any, ...]) -> tuple[str, ...]:
        return tuple(
            f"{self._record_id(record)}: step={_text(getattr(record, 'step_id', ''))}; "
            f"trace={_optional(getattr(record, 'trace_id', None)) or 'none'}; "
            f"correlation={_optional(getattr(record, 'correlation_id', None)) or 'none'}"
            for record in records
        )

    def _unresolved_items(self, assessment: Any, outcome: str, extra: tuple[str, ...]) -> tuple[str, ...]:
        items = []
        for signal in sorted(getattr(assessment, "unresolved_divergences", ()), key=lambda item: item.signal_id):
            items.append(
                "What additional evidence would resolve " + signal.signal_id + " involving "
                + ", ".join(signal.evidence_record_ids) + "?"
            )
        if outcome == "partial agreement":
            items.append("What evidence is needed to reconcile the currently unmatched findings?")
        elif outcome == "insufficient evidence":
            items.append("What additional comparable evidence is required for synthesis?")
        if extra:
            items.append("How should evidence omitted from the assessment be evaluated: " + ", ".join(extra) + "?")
        return tuple(sorted(set(items)))

    def _summary(
        self, outcome: str, aligned: tuple[str, ...], divergent: tuple[str, ...],
        minority: tuple[str, ...], assessment: Any,
    ) -> str:
        if outcome == "exact agreement":
            lead = "Evidence is in exact categorical alignment; this does not establish correctness or authority."
        elif outcome == "compatible agreement":
            lead = "Evidence is materially compatible while retaining meaningful differences; this is advisory only."
        elif outcome == "partial agreement":
            lead = "Evidence is partially aligned, with unmatched or differing findings preserved below."
        elif outcome == "material divergence":
            lead = "Unresolved material divergence is present and no single conclusion is synthesized."
        else:
            lead = "Available evidence is insufficient for a complete synthesis or meaningful alignment conclusion."
        return (
            f"{lead} Aligned findings: {len(aligned)}; divergent findings: {len(divergent)}; "
            f"minority records: {len(minority)}. Assessment rationale: {_text(getattr(assessment, 'rationale', ''))}"
        )

    def _section(
        self, name: str, items: tuple[str, ...], record_ids: tuple[str, ...], *,
        traces: tuple[str, ...], correlations: tuple[str, ...], policy: SynthesisPolicy,
    ) -> SynthesisSection:
        values = tuple(sorted(set(items))) if name != "summary" else items
        empty_reason = None if values else _required(policy.empty_section_text, "empty section text")
        return SynthesisSection(
            name=name, items=values, evidence_record_ids=_strings(record_ids),
            trace_ids=traces, correlation_ids=correlations, empty_reason=empty_reason,
        )

    def _signal_ids(self, signals: Iterable[Any]) -> tuple[str, ...]:
        return _strings(value for signal in signals for value in signal.evidence_record_ids)

    def _record_id(self, record: Any) -> str:
        return _required(getattr(record, "record_id", None), "evidence record identifier")

    def _output_text(self, record: Any) -> str:
        return json.dumps(record.output, sort_keys=True, separators=(",", ":"), default=repr)


def _reject_prohibited(value: Any, location: str, *, allow_identity: bool) -> None:
    if isinstance(value, Mapping):
        keys = {str(key).strip().lower() for key in value}
        prohibited = _PROHIBITED_KEYS | (frozenset() if allow_identity else _IDENTITY_KEYS)
        found = sorted(keys & prohibited)
        if found:
            raise ValueError(f"prohibited synthesis semantics in {location}: " + ", ".join(found))
        for nested in value.values():
            _reject_prohibited(nested, location, allow_identity=allow_identity)
    elif isinstance(value, (tuple, list, set, frozenset)):
        for nested in value:
            _reject_prohibited(nested, location, allow_identity=allow_identity)


def _strings(values: Iterable[Any]) -> tuple[str, ...]:
    return tuple(sorted({text for value in values if (text := _optional(value))}))


def _required(value: Any, name: str) -> str:
    normalized = _optional(value)
    if not normalized:
        raise ValueError(f"{name} is required")
    return normalized


def _optional(value: Any) -> str | None:
    normalized = " ".join(str(value or "").strip().split())
    return normalized or None


def _text(value: Any) -> str:
    return _optional(value) or ""


def _token(value: str) -> str:
    return _text(value).lower().replace(" ", "-")
