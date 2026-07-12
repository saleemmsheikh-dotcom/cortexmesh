"""Immutable logical models for Phase 3A replay validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


CONSENSUS_CATEGORIES = frozenset(
    {"exact agreement", "compatible agreement", "partial agreement", "material divergence", "insufficient evidence"}
)
_PROHIBITED_KEYS = frozenset(
    {"authority", "score", "confidence", "rank", "vote", "vote_weight", "governance", "provider_preference", "model_preference"}
)


@dataclass(frozen=True)
class ReplayMetadata:
    phase_version: str
    architecture_version: str
    replay_corpus_version: str
    validation_framework_version: str
    component_versions: tuple[tuple[str, str], ...]
    timestamp: str
    source_scenario: str
    schema_version: str = "1.0"
    provenance: tuple[tuple[str, Any], ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "phase_version", "architecture_version", "replay_corpus_version",
            "validation_framework_version", "timestamp", "source_scenario", "schema_version",
        ):
            _required(getattr(self, name), name)
        _ordered_pairs(self.component_versions, "component_versions")
        _ordered_pairs(self.provenance, "provenance")


@dataclass(frozen=True)
class ReplayScenario:
    scenario_id: str
    title: str
    purpose: str
    category: str
    source_description: str
    metric_coverage: tuple[str, ...]
    expected_behavior_rationale: str
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    case_ids: tuple[str, ...]
    metadata: ReplayMetadata

    def __post_init__(self) -> None:
        for name in ("scenario_id", "title", "purpose", "category", "source_description", "expected_behavior_rationale"):
            _required(getattr(self, name), name)
        _sorted_unique(self.metric_coverage, "metric_coverage", allow_empty=False)
        _sorted_unique(self.case_ids, "case_ids", allow_empty=False)
        _sorted_unique(self.assumptions, "assumptions")
        _sorted_unique(self.limitations, "limitations")


@dataclass(frozen=True)
class ReplayCase:
    case_id: str
    scenario_id: str
    title: str
    original_intent: Any
    normalized_intent: tuple[tuple[str, Any], ...]
    expected_capability_requirements: tuple[str, ...]
    expected_agent_plan: tuple[tuple[str, tuple[str, ...]], ...]
    expected_execution_plan: tuple[str, ...]
    simulated_outputs: tuple[tuple[str, Any], ...]
    expected_evidence_characteristics: tuple[str, ...]
    expected_consensus_classification: str
    expected_synthesis_characteristics: tuple[str, ...]
    expected_diagnostics: tuple[str, ...]
    comparator_kind: str
    metadata: ReplayMetadata

    def __post_init__(self) -> None:
        for name in ("case_id", "scenario_id", "title"):
            _required(getattr(self, name), name)
        _reject_prohibited(self.original_intent)
        _ordered_pairs(self.normalized_intent, "normalized_intent")
        _ordered_pairs(self.simulated_outputs, "simulated_outputs")
        _sorted_unique(self.expected_capability_requirements, "expected_capability_requirements")
        _sorted_unique(self.expected_execution_plan, "expected_execution_plan")
        _sorted_unique(self.expected_evidence_characteristics, "expected_evidence_characteristics")
        _sorted_unique(self.expected_synthesis_characteristics, "expected_synthesis_characteristics")
        _sorted_unique(self.expected_diagnostics, "expected_diagnostics")
        roles = tuple(role for role, _ in self.expected_agent_plan)
        _sorted_unique(roles, "expected_agent_plan roles")
        for _, capabilities in self.expected_agent_plan:
            _sorted_unique(capabilities, "agent capabilities")
        if self.expected_consensus_classification not in CONSENSUS_CATEGORIES:
            raise ValueError("unsupported expected consensus classification")
        if self.comparator_kind not in {"exact", "compatible"}:
            raise ValueError("case comparator_kind must be exact or compatible")


@dataclass(frozen=True)
class ReplayResult:
    result_id: str
    case_id: str
    dataset_version: str
    artifact_hashes: tuple[tuple[str, str], ...]
    diagnostics: tuple[str, ...]
    state: str
    comparison_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict, compare=False, hash=False, repr=False)

    def __post_init__(self) -> None:
        for name in ("result_id", "case_id", "dataset_version"):
            _required(getattr(self, name), name)
        _ordered_pairs(self.artifact_hashes, "artifact_hashes")
        _sorted_unique(self.diagnostics, "diagnostics")
        if self.state not in {"pass", "fail", "inconclusive"}:
            raise ValueError("result state must be pass, fail, or inconclusive")


def _required(value: Any, name: str) -> None:
    if not str(value or "").strip():
        raise ValueError(f"{name} is required")


def _sorted_unique(values: tuple[Any, ...], name: str, allow_empty: bool = True) -> None:
    if not allow_empty and not values:
        raise ValueError(f"{name} cannot be empty")
    if tuple(sorted(set(values), key=str)) != values:
        raise ValueError(f"{name} must be sorted and unique")


def _ordered_pairs(values: tuple[tuple[Any, Any], ...], name: str) -> None:
    keys = tuple(str(key) for key, _ in values)
    _sorted_unique(keys, f"{name} keys")
    _reject_prohibited(dict(values))


def _reject_prohibited(value: Any) -> None:
    if isinstance(value, Mapping):
        found = sorted({str(key).lower() for key in value} & _PROHIBITED_KEYS)
        if found:
            raise ValueError("prohibited replay semantics: " + ", ".join(found))
        for nested in value.values():
            _reject_prohibited(nested)
    elif isinstance(value, (tuple, list, set, frozenset)):
        for nested in value:
            _reject_prohibited(nested)
