import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "CortexMesh_v3_Planning/06_Implementation_Execution/Phase3A/replay/v1.0"


class TestCertifiedReplayCorpusV1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((CORPUS / "MANIFEST.json").read_text())
        cls.cases = json.loads((CORPUS / "cases/cases.json").read_text())
        cls.scenarios = json.loads((CORPUS / "scenarios/scenarios.json").read_text())
        cls.comparators = json.loads((CORPUS / "comparators/definitions.json").read_text())

    def test_release_identity_and_certification(self):
        self.assertEqual(self.manifest["corpus_version"], "1.0.0")
        self.assertEqual(self.manifest["schema_version"], "1.0")
        self.assertEqual(self.manifest["status"], "CERTIFIED")
        self.assertEqual(self.manifest["runtime_replay"], "NOT CERTIFIED")

    def test_counts_and_deterministic_ordering(self):
        case_ids = [item["id"] for item in self.cases["cases"]]
        scenario_ids = [item["id"] for item in self.scenarios["scenarios"]]
        self.assertEqual(len(case_ids), self.manifest["case_count"])
        self.assertEqual(len(scenario_ids), self.manifest["scenario_count"])
        self.assertEqual(case_ids, sorted(set(case_ids)))
        self.assertEqual(scenario_ids, sorted(set(scenario_ids)))

    def test_all_scenario_references_resolve(self):
        cases = {item["id"]: item for item in self.cases["cases"]}
        scenarios = {item["id"]: item for item in self.scenarios["scenarios"]}
        for scenario in scenarios.values():
            self.assertLessEqual(set(scenario["cases"]), set(cases))
        for case in cases.values():
            self.assertIn(case["scenario"], scenarios)

    def test_case_schema_completeness(self):
        required = {
            "id", "scenario", "intent", "normalized", "capabilities", "agents", "steps",
            "evidence", "consensus", "synthesis", "comparator", "validation",
        }
        for case in self.cases["cases"]:
            with self.subTest(case=case["id"]):
                self.assertLessEqual(required, case.keys())
                self.assertTrue(all(case[field] for field in required))

    def test_consensus_and_content_coverage(self):
        categories = {item["consensus"] for item in self.cases["cases"]}
        self.assertEqual(categories, {"exact agreement", "compatible agreement", "partial agreement", "material divergence", "insufficient evidence"})
        scenario_categories = {item["category"] for item in self.scenarios["scenarios"]}
        for required in ("architecture design", "implementation planning", "refactoring", "governance", "provider integration", "evidence collection", "consensus", "synthesis", "risk assessment", "insufficient evidence", "conflicting evidence", "edge cases"):
            self.assertIn(required, scenario_categories)

    def test_comparator_coverage(self):
        certified = tuple(sorted(item["kind"] for item in self.comparators["comparators"] if item["certified"]))
        self.assertEqual(certified, tuple(self.manifest["comparator_coverage"]))
        runtime = next(item for item in self.comparators["comparators"] if item["kind"] == "future runtime")
        self.assertFalse(runtime["certified"])

    def test_file_and_manifest_hash_integrity(self):
        entries = []
        for item in self.manifest["files"]:
            digest = hashlib.sha256((CORPUS / item["path"]).read_bytes()).hexdigest()
            self.assertEqual(digest, item["sha256"])
            entries.append((item["path"], digest))
        payload = "\n".join(f"{path}:{digest}" for path, digest in entries)
        self.assertEqual(hashlib.sha256(payload.encode()).hexdigest(), self.manifest["content_hash"])


if __name__ == "__main__":
    unittest.main()
