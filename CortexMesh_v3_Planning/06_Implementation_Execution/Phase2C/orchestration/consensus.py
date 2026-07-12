"""Deterministic, non-voting Phase 2C evidence alignment assessment.

The evaluator consumes EvidenceBundle-like records and produces descriptive,
advisory classifications.  It assigns no authority, score, confidence, rank,
vote weight, winning position, or governance meaning.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from typing import Any, Iterable, Mapping


EXACT_AGREEMENT = "exact agreement"
COMPATIBLE_AGREEMENT = "compatible agreement"
PARTIAL_AGREEMENT = "partial agreement"
MATERIAL_DIVERGENCE = "material divergence"
INSUFFICIENT_EVIDENCE = "insufficient evidence"

_IDENTITY_KEYS = frozenset({"provider", "provider_id", "model", "model_id", "model_name"})
_PROHIBITED_KEYS = frozenset(
    {
        "authority", "authority_input", "score", "confidence", "rank", "vote",
        "vote_weight", "consensus", "governance", "approval", "decision_state",
    }
) | _IDENTITY_KEYS


@dataclass(frozen=True)
class ConsensusInput:
    """Identity-neutral projection of one descriptive evidence record."""

    scope: str
    evidence_record_id: str
    agent_role: str
    capability_fulfilled: str
    claims: tuple[str, ...]
    supporting_context: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()
    trace_id: str | None = None
    correlation_id: str | None = None


@dataclass(frozen=True)
class AgreementSignal:
    """Descriptive agreement relationship among evidence records."""

    signal_id: str
    scope: str
    evidence_record_ids: tuple[str, ...]
    alignment_kind: str
    aligned_claims: tuple[str, ...]
    rationale: str


@dataclass(frozen=True)
class DivergenceSignal:
    """Visible, preserved divergence among evidence records."""

    signal_id: str
    scope: str
    evidence_record_ids: tuple[str, ...]
    divergence_kind: str
    conflicting_claims: tuple[str, ...]
    material: bool
    resolution_state: str
    rationale: str


@dataclass(frozen=True)
class ConsensusAssessment:
    """Advisory-only result for a future synthesis layer."""

    assessment_id: str
    scope: str
    outcome: str
    evidence_record_ids: tuple[str, ...]
    agreement_signals: tuple[AgreementSignal, ...] = ()
    divergence_signals: tuple[DivergenceSignal, ...] = ()
    unresolved_divergences: tuple[DivergenceSignal, ...] = ()
    minority_evidence_record_ids: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    correlation_ids: tuple[str, ...] = ()
    rationale: str = ""
    advisory_to_synthesis_only: bool = True


@dataclass(frozen=True)
class ConsensusPolicy:
    """Categorical comparison rules; never a scoring or voting policy."""

    name: str = "phase2c.default.consensus"
    version: str = "1"
    scope: str = "evidence synthesis"
    minimum_records: int = 2
    compatible_claims: Mapping[str, str] = field(default_factory=dict)
    material_conflicts: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if self.minimum_records < 2:
            raise ValueError("consensus assessment requires at least two evidence records")
        _reject_prohibited(self.compatible_claims, "consensus policy")


class ConsensusEvaluator:
    """Evaluate evidence alignment without votes, weights, or authority."""

    def evaluate(
        self,
        evidence_bundle: Any,
        policy: ConsensusPolicy | None = None,
        *,
        scope: str | None = None,
    ) -> ConsensusAssessment:
        policy = policy or ConsensusPolicy(scope=scope or "evidence synthesis")
        assessment_scope = _required(scope or policy.scope, "scope")
        inputs = tuple(
            sorted(
                (self._project(record, assessment_scope) for record in self._records(evidence_bundle)),
                key=lambda item: item.evidence_record_id,
            )
        )
        record_ids = tuple(item.evidence_record_id for item in inputs)
        if len(set(record_ids)) != len(record_ids):
            raise ValueError("evidence record identifiers must be unique")

        diagnostics = _strings(getattr(evidence_bundle, "diagnostics", ()))
        common = self._common_fields(inputs)
        assessment_id = f"consensus:{_token(policy.name)}:{_token(policy.version)}:{_token(assessment_scope)}"

        if len(inputs) < policy.minimum_records or any(not item.claims for item in inputs):
            return self._assessment(
                assessment_id, assessment_scope, INSUFFICIENT_EVIDENCE, inputs,
                diagnostics=diagnostics + ("insufficient_comparable_evidence",),
                rationale="Policy-required comparable evidence is absent.",
            )

        agreements: list[AgreementSignal] = []
        divergences: list[DivergenceSignal] = []
        canonical = {
            item.evidence_record_id: frozenset(self._canonical(claim, policy) for claim in item.claims)
            for item in inputs
        }
        raw = {item.evidence_record_id: frozenset(item.claims) for item in inputs}

        for left, right in combinations(inputs, 2):
            ids = (left.evidence_record_id, right.evidence_record_id)
            conflict_claims = self._conflicts(left.claims, right.claims, policy)
            if conflict_claims:
                divergences.append(
                    DivergenceSignal(
                        signal_id=self._signal_id("divergence", ids), scope=assessment_scope,
                        evidence_record_ids=ids, divergence_kind="contradiction",
                        conflicting_claims=conflict_claims, material=True,
                        resolution_state="unresolved",
                        rationale="Policy identifies materially incompatible claims.",
                    )
                )
                continue
            intersection = canonical[ids[0]] & canonical[ids[1]]
            if raw[ids[0]] == raw[ids[1]]:
                kind = "exact"
            elif canonical[ids[0]] == canonical[ids[1]]:
                kind = "compatible"
            elif intersection:
                kind = "partial"
            else:
                divergences.append(
                    DivergenceSignal(
                        signal_id=self._signal_id("divergence", ids), scope=assessment_scope,
                        evidence_record_ids=ids, divergence_kind="unsupported claim",
                        conflicting_claims=tuple(sorted(raw[ids[0]] | raw[ids[1]])),
                        material=False, resolution_state="unresolved",
                        rationale="Claims are unmatched but not declared materially incompatible.",
                    )
                )
                continue
            agreements.append(
                AgreementSignal(
                    signal_id=self._signal_id(f"agreement-{kind}", ids), scope=assessment_scope,
                    evidence_record_ids=ids, alignment_kind=kind,
                    aligned_claims=tuple(sorted(intersection or canonical[ids[0]])),
                    rationale=f"Evidence claims have {kind} categorical alignment.",
                )
            )

        material = tuple(signal for signal in divergences if signal.material and signal.resolution_state == "unresolved")
        kinds = {signal.alignment_kind for signal in agreements}
        if material:
            outcome = MATERIAL_DIVERGENCE
            rationale = "At least one unresolved material divergence must remain visible."
        elif "partial" in kinds or divergences:
            outcome = PARTIAL_AGREEMENT
            rationale = "Aligned and unmatched evidence coexist and are preserved."
        elif "compatible" in kinds:
            outcome = COMPATIBLE_AGREEMENT
            rationale = "All material claims are compatible but not textually equivalent."
        elif agreements and kinds == {"exact"}:
            outcome = EXACT_AGREEMENT
            rationale = "All comparable material claims are equivalent."
        else:
            outcome = INSUFFICIENT_EVIDENCE
            rationale = "No meaningful alignment relationship can be established."

        minority = self._minority_records(inputs, canonical)
        return self._assessment(
            assessment_id, assessment_scope, outcome, inputs,
            agreements=tuple(sorted(agreements, key=lambda signal: signal.signal_id)),
            divergences=tuple(sorted(divergences, key=lambda signal: signal.signal_id)),
            unresolved=material, minority=minority, diagnostics=diagnostics,
            rationale=rationale, common=common,
        )

    def _records(self, bundle: Any) -> tuple[Any, ...]:
        if isinstance(bundle, Mapping) or not hasattr(bundle, "records"):
            raise TypeError("consensus input must be an EvidenceBundle-like object with records")
        records = tuple(bundle.records)
        if any(not hasattr(record, "record_id") or not hasattr(record, "output") for record in records):
            raise TypeError("consensus input records must be EvidenceRecord-like values")
        return records

    def _project(self, record: Any, scope: str) -> ConsensusInput:
        source = getattr(record, "source", None)
        if source is None:
            raise TypeError("evidence record source is required")
        provenance = getattr(source, "provenance", {})
        if isinstance(provenance, Mapping):
            identities = sorted({str(key).lower() for key in provenance} & _IDENTITY_KEYS)
            if identities:
                raise ValueError(
                    "provider/model identity is prohibited as consensus input: " + ", ".join(identities)
                )
            _reject_prohibited(provenance, "evidence provenance")
        output = record.output
        _reject_prohibited(output, "evidence output")
        claims, context = self._claims(output)
        return ConsensusInput(
            scope=scope,
            evidence_record_id=_required(record.record_id, "evidence_record_id"),
            agent_role=_required(getattr(source, "agent_role", ""), "agent_role"),
            capability_fulfilled=_required(
                getattr(source, "capability_fulfilled", ""), "capability_fulfilled"
            ),
            claims=claims, supporting_context=context,
            assumptions=_strings(getattr(record, "assumptions", ())),
            limitations=_strings(getattr(record, "limitations", ())),
            diagnostics=_strings(getattr(record, "diagnostics", ())),
            trace_id=_optional(getattr(record, "trace_id", None)),
            correlation_id=_optional(getattr(record, "correlation_id", None)),
        )

    def _claims(self, output: Any) -> tuple[tuple[str, ...], tuple[str, ...]]:
        if isinstance(output, Mapping):
            values = output.get("claims", output.get("claim", output.get("finding", ())))
            context = output.get("supporting_context", output.get("observations", ()))
        else:
            values, context = output, ()
        return _claim_strings(values), _claim_strings(context)

    def _canonical(self, claim: str, policy: ConsensusPolicy) -> str:
        normalized = _claim(claim)
        aliases = {_claim(key): _claim(value) for key, value in policy.compatible_claims.items()}
        return aliases.get(normalized, normalized)

    def _conflicts(
        self, left: tuple[str, ...], right: tuple[str, ...], policy: ConsensusPolicy
    ) -> tuple[str, ...]:
        left_set = {_claim(value) for value in left}
        right_set = {_claim(value) for value in right}
        conflicts = []
        for first, second in policy.material_conflicts:
            first, second = _claim(first), _claim(second)
            if (first in left_set and second in right_set) or (second in left_set and first in right_set):
                conflicts.extend((first, second))
        return tuple(sorted(set(conflicts)))

    def _minority_records(
        self, inputs: tuple[ConsensusInput, ...], canonical: Mapping[str, frozenset[str]]
    ) -> tuple[str, ...]:
        # "Minority" is descriptive: records with a unique claim set. It never affects outcome.
        sets = tuple(canonical.values())
        return tuple(
            item.evidence_record_id
            for item in inputs
            if sets.count(canonical[item.evidence_record_id]) == 1 and len(inputs) > 1
        )

    def _common_fields(self, inputs: tuple[ConsensusInput, ...]) -> dict[str, tuple[str, ...]]:
        return {
            "assumptions": _strings(value for item in inputs for value in item.assumptions),
            "limitations": _strings(value for item in inputs for value in item.limitations),
            "traces": _strings(item.trace_id for item in inputs if item.trace_id),
            "correlations": _strings(item.correlation_id for item in inputs if item.correlation_id),
        }

    def _signal_id(self, kind: str, ids: tuple[str, ...]) -> str:
        return f"{kind}:{'|'.join(ids)}"

    def _assessment(
        self, assessment_id: str, scope: str, outcome: str, inputs: tuple[ConsensusInput, ...],
        *, agreements: tuple[AgreementSignal, ...] = (),
        divergences: tuple[DivergenceSignal, ...] = (),
        unresolved: tuple[DivergenceSignal, ...] = (), minority: tuple[str, ...] = (),
        diagnostics: tuple[str, ...] = (), rationale: str,
        common: Mapping[str, tuple[str, ...]] | None = None,
    ) -> ConsensusAssessment:
        common = common or self._common_fields(inputs)
        return ConsensusAssessment(
            assessment_id=assessment_id, scope=scope, outcome=outcome,
            evidence_record_ids=tuple(item.evidence_record_id for item in inputs),
            agreement_signals=agreements, divergence_signals=divergences,
            unresolved_divergences=unresolved, minority_evidence_record_ids=minority,
            assumptions=common["assumptions"], limitations=common["limitations"],
            diagnostics=_strings(diagnostics), trace_ids=common["traces"],
            correlation_ids=common["correlations"], rationale=rationale,
        )


def _reject_prohibited(value: Any, location: str) -> None:
    if isinstance(value, Mapping):
        keys = {str(key).strip().lower() for key in value}
        forbidden = sorted(keys & _PROHIBITED_KEYS)
        if forbidden:
            raise ValueError(f"prohibited consensus input in {location}: " + ", ".join(forbidden))
        for nested in value.values():
            _reject_prohibited(nested, location)
    elif isinstance(value, (tuple, list, set, frozenset)):
        for nested in value:
            _reject_prohibited(nested, location)


def _claim_strings(values: Any) -> tuple[str, ...]:
    if values is None:
        return ()
    if isinstance(values, str) or not isinstance(values, Iterable):
        values = (values,)
    return tuple(sorted({_claim(value) for value in values if _optional(value)}))


def _claim(value: Any) -> str:
    return " ".join(str(value).strip().lower().split())


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


def _token(value: str) -> str:
    return _claim(value).replace(" ", "-")
