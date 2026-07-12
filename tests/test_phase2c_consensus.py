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


evidence_module = load_module("phase2c_evidence_for_consensus", BASE / "evidence.py")
consensus_module = load_module("phase2c_consensus", BASE / "consensus.py")

EvidenceBundle = evidence_module.EvidenceBundle
EvidenceRecord = evidence_module.EvidenceRecord
EvidenceSource = evidence_module.EvidenceSource
AgreementSignal = consensus_module.AgreementSignal
ConsensusAssessment = consensus_module.ConsensusAssessment
ConsensusEvaluator = consensus_module.ConsensusEvaluator
ConsensusInput = consensus_module.ConsensusInput
ConsensusPolicy = consensus_module.ConsensusPolicy
DivergenceSignal = consensus_module.DivergenceSignal


class TestPhase2CConsensus(unittest.TestCase):
    def setUp(self):
        self.evaluator = ConsensusEvaluator()

    def record(self, record_id, claims, role="reviewer", provenance=None):
        return EvidenceRecord(
            record_id=record_id,
            step_id=f"step-{record_id}",
            source=EvidenceSource(
                agent_role=role,
                capability_fulfilled="risk.review",
                provenance=provenance or {"run": record_id},
            ),
            output={"claims": claims, "supporting_context": [f"context-{record_id}"]},
            assumptions=("scope is stable",),
            limitations=("reference assessment",),
            diagnostics=(),
            trace_id=f"trace-{record_id}",
            correlation_id="correlation-1",
        )

    def bundle(self, *records):
        return EvidenceBundle(records=records, diagnostics=("descriptive evidence",))

    def test_defines_required_models(self):
        assessment = self.evaluator.evaluate(
            self.bundle(self.record("1", ["safe"]), self.record("2", ["safe"]))
        )
        self.assertIsInstance(assessment, ConsensusAssessment)
        self.assertTrue(all(isinstance(signal, AgreementSignal) for signal in assessment.agreement_signals))
        self.assertTrue(ConsensusInput.__dataclass_fields__)
        self.assertTrue(DivergenceSignal.__dataclass_fields__)

    def test_exact_agreement(self):
        result = self.evaluator.evaluate(
            self.bundle(self.record("2", ["bounded", "safe"]), self.record("1", ["safe", "bounded"]))
        )
        self.assertEqual(result.outcome, "exact agreement")
        self.assertEqual(result.evidence_record_ids, ("1", "2"))
        self.assertEqual(result.agreement_signals[0].alignment_kind, "exact")

    def test_compatible_agreement_uses_declared_aliases(self):
        policy = ConsensusPolicy(compatible_claims={"acceptable": "safe", "safe": "safe"})
        result = self.evaluator.evaluate(
            self.bundle(self.record("1", ["safe"]), self.record("2", ["acceptable"])), policy
        )
        self.assertEqual(result.outcome, "compatible agreement")

    def test_partial_agreement_preserves_unmatched_minority_evidence(self):
        result = self.evaluator.evaluate(
            self.bundle(
                self.record("1", ["shared", "common"]),
                self.record("2", ["shared", "common"]),
                self.record("3", ["shared", "minority finding"], role="risk_reviewer"),
            )
        )
        self.assertEqual(result.outcome, "partial agreement")
        self.assertIn("3", result.minority_evidence_record_ids)
        self.assertEqual(set(result.evidence_record_ids), {"1", "2", "3"})

    def test_material_divergence_has_precedence_and_remains_unresolved(self):
        policy = ConsensusPolicy(material_conflicts=(("deploy", "do not deploy"),))
        result = self.evaluator.evaluate(
            self.bundle(
                self.record("1", ["shared", "deploy"]),
                self.record("2", ["shared", "deploy"]),
                self.record("3", ["shared", "do not deploy"]),
            ),
            policy,
        )
        self.assertEqual(result.outcome, "material divergence")
        self.assertTrue(result.unresolved_divergences)
        self.assertTrue(result.unresolved_divergences[0].material)
        self.assertEqual(result.unresolved_divergences[0].resolution_state, "unresolved")
        self.assertIn("3", result.evidence_record_ids)

    def test_insufficient_evidence(self):
        result = self.evaluator.evaluate(self.bundle(self.record("1", ["safe"])))
        self.assertEqual(result.outcome, "insufficient evidence")
        self.assertIn("insufficient_comparable_evidence", result.diagnostics)

    def test_classification_is_deterministic_across_input_order(self):
        records = (self.record("2", ["shared", "two"]), self.record("1", ["shared", "one"]))
        self.assertEqual(
            self.evaluator.evaluate(self.bundle(*records)),
            self.evaluator.evaluate(self.bundle(*reversed(records))),
        )

    def test_provider_and_model_identity_are_rejected(self):
        for key in ("provider", "provider_id", "model", "model_id", "model_name"):
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "provider/model identity"):
                self.evaluator.evaluate(
                    self.bundle(
                        self.record("1", ["safe"], provenance={key: "identity"}),
                        self.record("2", ["safe"]),
                    )
                )

    def test_authoritative_and_voting_inputs_are_rejected_recursively(self):
        for key in ("authority", "score", "confidence", "rank", "vote", "vote_weight", "governance"):
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "prohibited consensus input"):
                polluted = self.record("1", ["safe"])
                polluted = EvidenceRecord(
                    **{**polluted.__dict__, "output": {"claims": ["safe"], "nested": {key: 1}}}
                )
                self.evaluator.evaluate(self.bundle(polluted, self.record("2", ["safe"])))

    def test_output_is_advisory_and_has_no_prohibited_semantics(self):
        result = self.evaluator.evaluate(
            self.bundle(self.record("1", ["safe"]), self.record("2", ["safe"]))
        )
        self.assertTrue(result.advisory_to_synthesis_only)
        for name in ("authority", "score", "confidence", "rank", "vote", "vote_weight", "governance"):
            self.assertFalse(hasattr(result, name))

    def test_requires_evidence_bundle_like_records(self):
        with self.assertRaises(TypeError):
            self.evaluator.evaluate([self.record("1", ["safe"]), self.record("2", ["safe"])])

    def test_duplicate_record_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "unique"):
            self.evaluator.evaluate(self.bundle(self.record("1", ["safe"]), self.record("1", ["safe"])))


if __name__ == "__main__":
    unittest.main()
