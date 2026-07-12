from dataclasses import FrozenInstanceError
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE3A = ROOT / "CortexMesh_v3_Planning/06_Implementation_Execution/Phase3A"
sys.path.insert(0, str(PHASE3A))

from replay import (  # noqa: E402
    ReplayCase,
    ReplayCertification,
    ReplayComparator,
    ReplayDataset,
    ReplayManifest,
    ReplayMetadata,
    ReplayResult,
    ReplayScenario,
    ReplayVersion,
)
from replay.manifest import content_hash  # noqa: E402


class TestPhase3AReplaySchema(unittest.TestCase):
    def metadata(self, version="1.0.0"):
        return ReplayMetadata(
            phase_version="3A",
            architecture_version="1.0",
            replay_corpus_version=version,
            validation_framework_version="1.0",
            component_versions=(("phase2c", "phase2c-complete"),),
            timestamp="2026-07-12T00:00:00Z",
            source_scenario="scenario-001",
        )

    def scenario(self):
        return ReplayScenario(
            scenario_id="scenario-001",
            title="Exact evidence alignment",
            purpose="Validate exact replay",
            category="exact-agreement",
            source_description="Synthetic validation scenario",
            metric_coverage=("consensus-correctness", "determinism"),
            expected_behavior_rationale="Equivalent claims must align exactly.",
            assumptions=(),
            limitations=("synthetic",),
            case_ids=("case-001",),
            metadata=self.metadata(),
        )

    def case(self):
        return ReplayCase(
            case_id="case-001",
            scenario_id="scenario-001",
            title="Two identical simulated findings",
            original_intent="Review evidence",
            normalized_intent=(("domain", "general"), ("objective", "review evidence"), ("task_type", "review")),
            expected_capability_requirements=("reasoning.review", "risk.assessment"),
            expected_agent_plan=(("research_analyst", ("reasoning.review",)), ("risk_reviewer", ("risk.assessment",))),
            expected_execution_plan=("step-001-research_analyst", "step-002-risk_reviewer"),
            simulated_outputs=(("step-001-research_analyst", "bounded"), ("step-002-risk_reviewer", "bounded")),
            expected_evidence_characteristics=("complete", "traceable"),
            expected_consensus_classification="exact agreement",
            expected_synthesis_characteristics=("all-sections", "descriptive-only"),
            expected_diagnostics=(),
            comparator_kind="exact",
            metadata=self.metadata(),
        )

    def manifest(self):
        return ReplayManifest.build(
            "phase3a-canonical",
            ReplayVersion("1.0.0", "1.0", None, "major"),
            (self.scenario(),),
            (self.case(),),
            ("compatible", "exact", "regression"),
        )

    def certification(self, manifest=None):
        manifest = manifest or self.manifest()
        return ReplayCertification(
            certification_id="phase3a-replay-1.0.0",
            replay_corpus_version="1.0.0",
            schema_version="1.0",
            content_hash=manifest.content_hash,
            replay_case_count=1,
            replay_scenario_count=1,
            comparator_coverage=("compatible", "exact", "regression"),
            validation_status="certified",
            approved_at="2026-07-12T00:00:00Z",
            approved_by="Product Owner",
        )

    def test_required_models_are_defined(self):
        models = (ReplayCase, ReplayScenario, ReplayDataset, ReplayManifest, ReplayResult)
        self.assertTrue(all(model.__dataclass_fields__ for model in models))

    def test_schema_validation_accepts_complete_case(self):
        case = self.case()
        self.assertEqual(case.expected_consensus_classification, "exact agreement")
        self.assertEqual(case.metadata.replay_corpus_version, "1.0.0")

    def test_schema_requires_deterministic_ordering(self):
        with self.assertRaisesRegex(ValueError, "sorted and unique"):
            ReplayScenario(
                **{**self.scenario().__dict__, "metric_coverage": ("z", "a")}
            )

    def test_prohibited_semantics_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "prohibited replay semantics"):
            ReplayCase(**{**self.case().__dict__, "original_intent": {"authority": "system"}})

    def test_manifest_hash_is_deterministic_and_validated(self):
        first = self.manifest()
        second = self.manifest()
        self.assertEqual(first, second)
        self.assertEqual(first.content_hash, first.calculate_content_hash())
        with self.assertRaisesRegex(ValueError, "content hash mismatch"):
            ReplayManifest(**{**first.__dict__, "content_hash": "incorrect"})

    def test_dataset_validates_manifest_and_references(self):
        dataset = ReplayDataset("phase3a-canonical", (self.scenario(),), (self.case(),), self.manifest())
        self.assertFalse(dataset.published)
        with self.assertRaisesRegex(ValueError, "does not match manifest"):
            ReplayDataset("different", dataset.scenarios, dataset.cases, dataset.manifest)

    def test_published_dataset_is_certified_and_immutable(self):
        dataset = ReplayDataset("phase3a-canonical", (self.scenario(),), (self.case(),), self.manifest())
        published = dataset.publish(self.certification(dataset.manifest))
        self.assertTrue(published.published)
        self.assertEqual(published.certification.validation_status, "certified")
        with self.assertRaises(FrozenInstanceError):
            published.dataset_id = "changed"
        with self.assertRaisesRegex(ValueError, "immutable"):
            published.publish(self.certification(dataset.manifest))

    def test_certification_must_match_release(self):
        manifest = self.manifest()
        invalid = ReplayCertification(**{**self.certification(manifest).__dict__, "replay_case_count": 2})
        with self.assertRaisesRegex(ValueError, "does not match"):
            invalid.validate(manifest)

    def test_version_compatibility_checks(self):
        ReplayVersion("1.1.0", "1.0", "1.0.0", "minor")
        with self.assertRaisesRegex(ValueError, "change_class"):
            ReplayVersion("1.1.0", "1.0", "1.0.0", "patch")
        with self.assertRaisesRegex(ValueError, "advance"):
            ReplayVersion("1.0.0", "1.0", "1.0.0", "patch")

    def test_comparator_selection(self):
        self.assertEqual(ReplayComparator.select("exact").kind, "exact")
        self.assertEqual(ReplayComparator.select("compatible").kind, "compatible")
        self.assertEqual(ReplayComparator.select("regression").kind, "regression")
        with self.assertRaisesRegex(ValueError, "reserved"):
            ReplayComparator.select("future runtime")

    def test_exact_compatible_and_regression_comparison(self):
        self.assertTrue(ReplayComparator.select("exact").compare({"a": 1}, {"a": 1})["matched"])
        compatible = ReplayComparator.select("compatible").compare(
            {"outcome": "safe"}, {"outcome": "acceptable"}, {"outcome": ("acceptable", "safe")}
        )
        self.assertTrue(compatible["matched"])
        regression = ReplayComparator.select("regression").compare({"a": 1}, {"a": 2})
        self.assertEqual(regression["outcome"], "regression")

    def test_content_hash_is_mapping_order_independent(self):
        self.assertEqual(content_hash({"a": 1, "b": 2}), content_hash({"b": 2, "a": 1}))


if __name__ == "__main__":
    unittest.main()
