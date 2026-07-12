"""Immutable published replay dataset aggregate."""

from __future__ import annotations

from dataclasses import dataclass

from .manifest import ReplayCertification, ReplayManifest, content_hash
from .schema import ReplayCase, ReplayScenario


@dataclass(frozen=True)
class ReplayDataset:
    dataset_id: str
    scenarios: tuple[ReplayScenario, ...]
    cases: tuple[ReplayCase, ...]
    manifest: ReplayManifest
    certification: ReplayCertification | None = None
    published: bool = False

    def __post_init__(self) -> None:
        scenario_ids = tuple(item.scenario_id for item in self.scenarios)
        case_ids = tuple(item.case_id for item in self.cases)
        if tuple(sorted(set(scenario_ids))) != scenario_ids:
            raise ValueError("scenarios must be sorted and unique")
        if tuple(sorted(set(case_ids))) != case_ids:
            raise ValueError("cases must be sorted and unique")
        if self.dataset_id != self.manifest.dataset_id:
            raise ValueError("dataset identifier does not match manifest")
        expected_scenarios = tuple((item.scenario_id, content_hash(item)) for item in self.scenarios)
        expected_cases = tuple((item.case_id, content_hash(item)) for item in self.cases)
        if expected_scenarios != self.manifest.scenario_hashes or expected_cases != self.manifest.case_hashes:
            raise ValueError("dataset content does not match manifest")
        known_cases = set(case_ids)
        known_scenarios = set(scenario_ids)
        for scenario in self.scenarios:
            if not set(scenario.case_ids) <= known_cases:
                raise ValueError("scenario references unknown replay case")
        if any(case.scenario_id not in known_scenarios for case in self.cases):
            raise ValueError("replay case references unknown scenario")
        if self.certification is not None:
            self.certification.validate(self.manifest)
        if self.published and (self.certification is None or self.certification.validation_status != "certified"):
            raise ValueError("published replay dataset requires certification")

    def publish(self, certification: ReplayCertification) -> "ReplayDataset":
        if self.published:
            raise ValueError("published replay dataset is immutable")
        certification.validate(self.manifest)
        if certification.validation_status != "certified":
            raise ValueError("only a certified replay release can be published")
        return ReplayDataset(self.dataset_id, self.scenarios, self.cases, self.manifest, certification, True)
