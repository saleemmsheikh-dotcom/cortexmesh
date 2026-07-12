"""Version, manifest, hashing, and certification for replay releases."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
import hashlib
import json
import re
from typing import Any


_SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


@dataclass(frozen=True)
class ReplayVersion:
    version: str
    schema_version: str
    parent_version: str | None
    change_class: str

    def __post_init__(self) -> None:
        if not _SEMVER.fullmatch(self.version):
            raise ValueError("replay version must use major.minor.patch")
        if self.parent_version is not None and not _SEMVER.fullmatch(self.parent_version):
            raise ValueError("parent replay version must use major.minor.patch")
        if self.change_class not in {"major", "minor", "patch"}:
            raise ValueError("change_class must be major, minor, or patch")
        self.validate_transition()

    def validate_transition(self) -> None:
        if self.parent_version is None:
            return
        current = tuple(map(int, self.version.split(".")))
        parent = tuple(map(int, self.parent_version.split(".")))
        if current <= parent:
            raise ValueError("replay version must advance parent_version")
        expected = "major" if current[0] > parent[0] else "minor" if current[1] > parent[1] else "patch"
        if expected != self.change_class:
            raise ValueError("change_class does not match semantic version transition")


@dataclass(frozen=True)
class ReplayManifest:
    dataset_id: str
    replay_version: ReplayVersion
    scenario_hashes: tuple[tuple[str, str], ...]
    case_hashes: tuple[tuple[str, str], ...]
    comparator_coverage: tuple[str, ...]
    content_hash: str

    def __post_init__(self) -> None:
        if not self.dataset_id.strip():
            raise ValueError("dataset_id is required")
        _validate_pairs(self.scenario_hashes, "scenario_hashes")
        _validate_pairs(self.case_hashes, "case_hashes")
        allowed = {"exact", "compatible", "regression"}
        if not self.comparator_coverage or set(self.comparator_coverage) - allowed:
            raise ValueError("manifest has unsupported comparator coverage")
        if tuple(sorted(set(self.comparator_coverage))) != self.comparator_coverage:
            raise ValueError("comparator coverage must be sorted and unique")
        if self.content_hash != self.calculate_content_hash():
            raise ValueError("manifest content hash mismatch")

    def calculate_content_hash(self) -> str:
        payload = {
            "dataset_id": self.dataset_id,
            "replay_version": asdict(self.replay_version),
            "scenario_hashes": self.scenario_hashes,
            "case_hashes": self.case_hashes,
            "comparator_coverage": self.comparator_coverage,
        }
        return content_hash(payload)

    @classmethod
    def build(
        cls,
        dataset_id: str,
        replay_version: ReplayVersion,
        scenarios: tuple[Any, ...],
        cases: tuple[Any, ...],
        comparator_coverage: tuple[str, ...],
    ) -> "ReplayManifest":
        scenario_hashes = tuple((item.scenario_id, content_hash(item)) for item in scenarios)
        case_hashes = tuple((item.case_id, content_hash(item)) for item in cases)
        provisional = cls.__new__(cls)
        object.__setattr__(provisional, "dataset_id", dataset_id)
        object.__setattr__(provisional, "replay_version", replay_version)
        object.__setattr__(provisional, "scenario_hashes", scenario_hashes)
        object.__setattr__(provisional, "case_hashes", case_hashes)
        object.__setattr__(provisional, "comparator_coverage", comparator_coverage)
        object.__setattr__(provisional, "content_hash", "")
        return cls(dataset_id, replay_version, scenario_hashes, case_hashes, comparator_coverage, provisional.calculate_content_hash())


@dataclass(frozen=True)
class ReplayCertification:
    certification_id: str
    replay_corpus_version: str
    schema_version: str
    content_hash: str
    replay_case_count: int
    replay_scenario_count: int
    comparator_coverage: tuple[str, ...]
    validation_status: str
    approved_at: str | None = None
    approved_by: str | None = None

    def validate(self, manifest: ReplayManifest) -> None:
        expected = (
            manifest.replay_version.version,
            manifest.replay_version.schema_version,
            manifest.content_hash,
            len(manifest.case_hashes),
            len(manifest.scenario_hashes),
            manifest.comparator_coverage,
        )
        actual = (
            self.replay_corpus_version,
            self.schema_version,
            self.content_hash,
            self.replay_case_count,
            self.replay_scenario_count,
            self.comparator_coverage,
        )
        if actual != expected:
            raise ValueError("certification does not match replay manifest")
        if self.validation_status not in {"draft", "failed", "certified"}:
            raise ValueError("unsupported certification status")
        if self.validation_status == "certified" and (not self.approved_at or not self.approved_by):
            raise ValueError("certified replay release requires approval record")


def content_hash(value: Any) -> str:
    payload = json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _canonical(value: Any) -> Any:
    if is_dataclass(value):
        return _canonical(asdict(value))
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    return value


def _validate_pairs(values: tuple[tuple[str, str], ...], name: str) -> None:
    keys = tuple(key for key, _ in values)
    if not values or tuple(sorted(set(keys))) != keys:
        raise ValueError(f"{name} must be non-empty, sorted, and unique")
    if any(not value for _, value in values):
        raise ValueError(f"{name} requires content hashes")
