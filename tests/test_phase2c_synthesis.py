import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "CortexMesh_v3_Planning/06_Implementation_Execution/Phase2C/orchestration"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


evidence = load_module("phase2c_evidence_for_synthesis", BASE / "evidence.py")
consensus = load_module("phase2c_consensus_for_synthesis", BASE / "consensus.py")
synthesis = load_module("phase2c_synthesis", BASE / "synthesis.py")

EvidenceBundle = evidence.EvidenceBundle
EvidenceRecord = evidence.EvidenceRecord
EvidenceSource = evidence.EvidenceSource
ConsensusEvaluator = consensus.ConsensusEvaluator
ConsensusPolicy = consensus.ConsensusPolicy
EvidenceSynthesizer = synthesis.EvidenceSynthesizer
SynthesisInput = synthesis.SynthesisInput
SynthesisPolicy = synthesis.SynthesisPolicy
SynthesisResult = synthesis.SynthesisResult
SynthesisSection = synthesis.SynthesisSection


class TestPhase2CSynthesis(unittest.TestCase):
    def setUp(self):
        self.consensus = ConsensusEvaluator()
        self.synthesizer = EvidenceSynthesizer()

    def record(self, record_id, claims, provenance=None):
        return EvidenceRecord(
            record_id=record_id,
            step_id=f"step-{record_id}",
            source=EvidenceSource(
                agent_role="reviewer",
                capability_fulfilled="evidence.review",
                provenance=provenance or {"run": record_id},
            ),
            output={"claims": claims},
            assumptions=(f"assumption-{record_id}",),
            limitations=(f"limitation-{record_id}",),
            diagnostics=(f"diagnostic-{record_id}",),
            trace_id=f"trace-{record_id}",
            correlation_id="correlation-1",
        )

    def bundle(self, *records):
        return EvidenceBundle(records=records, diagnostics=("bundle diagnostic",))

    def result(self, records, policy=None):
        bundle = self.bundle(*records)
        assessment = self.consensus.evaluate(bundle, policy)
        return self.synthesizer.synthesize(bundle, assessment)

    def test_defines_required_models_and_sections(self):
        result = self.result((self.record("1", ["safe"]), self.record("2", ["safe"])))
        self.assertIsInstance(result, SynthesisResult)
        self.assertTrue(all(isinstance(section, SynthesisSection) for section in result.sections))
        self.assertTrue(SynthesisInput.__dataclass_fields__)
        self.assertTrue(SynthesisPolicy.__dataclass_fields__)
        self.assertEqual(
            tuple(section.name for section in result.sections),
            synthesis.SECTION_ORDER,
        )

    def test_exact_agreement_synthesis(self):
        result = self.result((self.record("1", ["safe"]), self.record("2", ["safe"])))
        self.assertEqual(result.consensus_category, "exact agreement")
        self.assertIn("exact categorical alignment", result.section("summary").items[0])
        self.assertTrue(result.section("aligned findings").items)
        self.assertIsNotNone(result.section("divergent findings").empty_reason)

    def test_compatible_agreement_synthesis(self):
        result = self.result(
            (self.record("1", ["safe"]), self.record("2", ["acceptable"])),
            ConsensusPolicy(compatible_claims={"acceptable": "safe", "safe": "safe"}),
        )
        self.assertEqual(result.consensus_category, "compatible agreement")
        self.assertIn("materially compatible", result.section("summary").items[0])
        self.assertIn("compatible:", result.section("aligned findings").items[0])

    def test_partial_synthesis_preserves_minority(self):
        records = (
            self.record("1", ["shared", "common"]),
            self.record("2", ["shared", "common"]),
            self.record("3", ["shared", "minority"]),
        )
        result = self.result(records)
        self.assertEqual(result.consensus_category, "partial agreement")
        self.assertIn("3", result.section("minority evidence").evidence_record_ids)
        self.assertTrue(any(item.startswith("3:") for item in result.section("minority evidence").items))
        self.assertTrue(result.section("unresolved questions").items)

    def test_material_divergence_is_visible_and_unresolved(self):
        records = (self.record("1", ["deploy"]), self.record("2", ["do not deploy"]))
        result = self.result(records, ConsensusPolicy(material_conflicts=(("deploy", "do not deploy"),)))
        self.assertEqual(result.consensus_category, "material divergence")
        self.assertIn("Unresolved material divergence", result.section("summary").items[0])
        self.assertTrue(result.section("divergent findings").items)
        self.assertTrue(result.section("unresolved questions").items)
        self.assertEqual(set(result.section("divergent findings").evidence_record_ids), {"1", "2"})

    def test_insufficient_evidence_is_bounded(self):
        result = self.result((self.record("1", ["safe"]),))
        self.assertEqual(result.consensus_category, "insufficient evidence")
        self.assertIn("insufficient", result.section("summary").items[0])
        self.assertTrue(result.section("unresolved questions").items)

    def test_preserves_assumptions_limitations_diagnostics_provenance_and_traces(self):
        result = self.result((self.record("1", ["safe"]), self.record("2", ["safe"])))
        self.assertEqual(len(result.section("assumptions").items), 2)
        self.assertEqual(len(result.section("limitations").items), 2)
        self.assertIn("diagnostic-1", " ".join(result.section("diagnostics").items))
        self.assertEqual(len(result.section("provenance").items), 2)
        self.assertEqual(result.trace_ids, ("trace-1", "trace-2"))
        self.assertEqual(result.correlation_ids, ("correlation-1",))
        self.assertEqual(result.evidence_record_ids, ("1", "2"))

    def test_provider_model_identity_is_descriptive_provenance_only(self):
        # Consensus inputs prohibit identity, so use an advisory assessment made from
        # identity-neutral copies and synthesize against the source-of-record bundle.
        neutral = self.bundle(self.record("1", ["safe"]), self.record("2", ["safe"]))
        assessment = self.consensus.evaluate(neutral)
        source = self.bundle(
            self.record("1", ["safe"], {"provider": "local", "model": "model-a"}),
            self.record("2", ["safe"], {"provider": "remote", "model": "model-b"}),
        )
        result = self.synthesizer.synthesize(source, assessment)
        provenance_text = " ".join(result.section("provenance").items)
        self.assertIn('"provider":"local"', provenance_text)
        self.assertIn('"model":"model-b"', provenance_text)
        self.assertNotIn("provider", result.section("summary").items[0].lower())

    def test_rejects_authority_scoring_confidence_ranking_voting_and_governance(self):
        neutral = self.record("2", ["safe"])
        for key in ("authority", "score", "confidence", "rank", "vote", "vote_weight", "governance"):
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "prohibited synthesis semantics"):
                polluted = self.record("1", ["safe"])
                polluted = EvidenceRecord(
                    **{**polluted.__dict__, "output": {"claims": ["safe"], "nested": {key: 1}}}
                )
                clean_bundle = self.bundle(self.record("1", ["safe"]), neutral)
                assessment = self.consensus.evaluate(clean_bundle)
                self.synthesizer.synthesize(self.bundle(polluted, neutral), assessment)

    def test_consensus_assessment_must_remain_advisory(self):
        bundle = self.bundle(self.record("1", ["safe"]), self.record("2", ["safe"]))
        assessment = self.consensus.evaluate(bundle)
        polluted = consensus.ConsensusAssessment(
            **{**assessment.__dict__, "advisory_to_synthesis_only": False}
        )
        with self.assertRaisesRegex(ValueError, "advisory"):
            self.synthesizer.synthesize(bundle, polluted)

    def test_missing_assessment_reference_is_rejected(self):
        bundle = self.bundle(self.record("1", ["safe"]), self.record("2", ["safe"]))
        assessment = self.consensus.evaluate(bundle)
        incomplete = self.bundle(self.record("1", ["safe"]))
        with self.assertRaisesRegex(ValueError, "missing evidence"):
            self.synthesizer.synthesize(incomplete, assessment)

    def test_output_is_deterministic_across_evidence_order(self):
        records = (self.record("2", ["shared", "two"]), self.record("1", ["shared", "one"]))
        first_bundle = self.bundle(*records)
        second_bundle = self.bundle(*reversed(records))
        assessment = self.consensus.evaluate(first_bundle)
        self.assertEqual(
            self.synthesizer.synthesize(first_bundle, assessment),
            self.synthesizer.synthesize(second_bundle, assessment),
        )

    def test_result_has_no_authoritative_semantics(self):
        result = self.result((self.record("1", ["safe"]), self.record("2", ["safe"])))
        self.assertTrue(result.descriptive_only)
        self.assertTrue(result.advisory_output)
        for name in ("authority", "score", "confidence", "rank", "vote", "vote_weight", "approval"):
            self.assertFalse(hasattr(result, name))


if __name__ == "__main__":
    unittest.main()
