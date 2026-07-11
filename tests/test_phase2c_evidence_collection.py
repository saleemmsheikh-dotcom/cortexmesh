import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "CortexMesh_v3_Planning/06_Implementation_Execution/Phase2C/orchestration/evidence.py"
spec = importlib.util.spec_from_file_location("phase2c_evidence", PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

EvidenceBundle = module.EvidenceBundle
EvidenceCollector = module.EvidenceCollector
EvidenceRecord = module.EvidenceRecord
EvidenceSource = module.EvidenceSource


class TestEvidenceCollection(unittest.TestCase):
    def setUp(self):
        self.collector = EvidenceCollector()
        self.item = {
            "record_id": "record-2",
            "step_id": "step-2",
            "agent_role": "reviewer",
            "capability_fulfilled": "risk.review",
            "output": {"finding": "bounded"},
            "provenance": {"model": "local-model", "provider": "local", "run": "7"},
            "assumptions": ["inputs complete"],
            "limitations": ["static review"],
            "diagnostics": ["no runtime invocation"],
        }

    def test_defines_models_and_collects_all_descriptive_context(self):
        bundle = self.collector.collect([self.item], trace_id="trace-1", correlation_id="corr-1")
        record = bundle.records[0]
        self.assertIsInstance(bundle, EvidenceBundle)
        self.assertIsInstance(record, EvidenceRecord)
        self.assertIsInstance(record.source, EvidenceSource)
        self.assertEqual(record.source.agent_role, "reviewer")
        self.assertEqual(record.source.capability_fulfilled, "risk.review")
        self.assertEqual(record.source.provenance["provider"], "local")
        self.assertEqual(record.assumptions, ("inputs complete",))
        self.assertEqual(record.limitations, ("static review",))
        self.assertEqual(record.diagnostics, ("no runtime invocation",))
        self.assertEqual((record.trace_id, record.correlation_id), ("trace-1", "corr-1"))

    def test_bundle_is_deterministic(self):
        first = self.collector.collect([self.item, {**self.item, "record_id": "record-1", "step_id": "step-1"}])
        second = self.collector.collect(list(reversed([self.item, {**self.item, "record_id": "record-1", "step_id": "step-1"}])))
        self.assertEqual(first, second)

    def test_provider_model_identity_is_provenance_only(self):
        bundle = self.collector.collect([self.item])
        self.assertTrue(bundle.descriptive_only)
        with self.assertRaisesRegex(ValueError, "provider/model identity"):
            self.collector.collect([self.item], authority_input={"model": "local-model"})

    def test_rejects_authority_scoring_and_consensus_fields(self):
        for field in ("authority", "score", "confidence", "rank", "vote_weight", "consensus"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.collector.collect([{**self.item, field: 1}])

    def test_models_have_no_authoritative_attributes(self):
        bundle = self.collector.collect([self.item])
        for name in ("authority", "score", "confidence", "rank", "vote_weight", "consensus"):
            self.assertFalse(hasattr(bundle.records[0], name))

    def test_record_identifiers_are_required_and_unique(self):
        with self.assertRaisesRegex(ValueError, "record_id"):
            self.collector.collect([{**self.item, "record_id": ""}])
        with self.assertRaisesRegex(ValueError, "unique"):
            self.collector.collect([self.item, self.item])


if __name__ == "__main__":
    unittest.main()
