import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "CortexMesh_v3_Planning/06_Implementation_Execution/Phase2C/orchestration"


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, BASE / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


resolver_module = load_module("phase2c_resolver_for_engine", "capability_resolver.py")
agent_module = load_module("phase2c_agent_for_engine", "agent_planner.py")
execution_module = load_module("phase2c_execution_for_engine", "execution_plan.py")
evidence_module = load_module("phase2c_evidence_for_engine", "evidence.py")
consensus_module = load_module("phase2c_consensus_for_engine", "consensus.py")
synthesis_module = load_module("phase2c_synthesis_for_engine", "synthesis.py")
engine_module = load_module("phase2c_engine", "engine.py")

CapabilityResolver = resolver_module.CapabilityResolver
AgentPlanner = agent_module.AgentPlanner
ExecutionPlanner = execution_module.ExecutionPlanner
EvidenceCollector = evidence_module.EvidenceCollector
ConsensusEvaluator = consensus_module.ConsensusEvaluator
EvidenceSynthesizer = synthesis_module.EvidenceSynthesizer
OrchestrationContext = engine_module.OrchestrationContext
OrchestrationEngine = engine_module.OrchestrationEngine
OrchestrationRequest = engine_module.OrchestrationRequest
OrchestrationResult = engine_module.OrchestrationResult


class TestPhase2COrchestrationEngine(unittest.TestCase):
    def setUp(self):
        self.components = {
            "capability_resolver": CapabilityResolver(),
            "agent_planner": AgentPlanner(),
            "execution_planner": ExecutionPlanner(),
            "evidence_collector": EvidenceCollector(),
            "consensus_evaluator": ConsensusEvaluator(),
            "evidence_synthesizer": EvidenceSynthesizer(),
        }
        self.engine = OrchestrationEngine(**self.components)
        self.intent = {
            "objective": "Review governance evidence",
            "task_type": "review",
            "domain": "governance",
        }

    def planned_outputs(self, claim="bounded"):
        resolution = self.components["capability_resolver"].resolve(self.intent)
        plan = self.components["agent_planner"].plan(resolution)
        execution = self.components["execution_planner"].plan(plan)
        return {
            step.step_id: {
                "output": {"claims": [claim]},
                "assumptions": ["simulated input"],
                "limitations": ["no runtime invocation"],
            }
            for step in execution.steps
        }

    def request(self, outputs=None):
        return OrchestrationRequest(
            request_id="request-1",
            intent=self.intent,
            simulated_outputs=self.planned_outputs() if outputs is None else outputs,
            scope="governance evidence review",
        )

    def test_defines_required_models_and_full_pipeline_context(self):
        result = self.engine.run(self.request())
        self.assertIsInstance(result, OrchestrationResult)
        self.assertIsInstance(result.context, OrchestrationContext)
        self.assertTrue(OrchestrationRequest.__dataclass_fields__)
        self.assertTrue(result.context.capability_resolution.requirements)
        self.assertTrue(result.context.agent_plan.requirements)
        self.assertTrue(result.context.execution_plan.steps)
        self.assertTrue(result.context.evidence_bundle.records)
        self.assertEqual(result.context.consensus_assessment.outcome, "exact agreement")
        self.assertIs(result.response, result.context.synthesis_result)

    def test_pipeline_uses_only_simulated_outputs(self):
        result = self.engine.run(self.request())
        self.assertTrue(result.simulated_only)
        self.assertTrue(result.context.simulated_only)
        self.assertTrue(result.advisory_only)
        self.assertTrue(all(record.source.provenance["simulated"] for record in result.context.evidence_bundle.records))
        self.assertTrue(all("no runtime invocation" in record.limitations for record in result.context.evidence_bundle.records))

    def test_deterministic_execution(self):
        request = self.request()
        self.assertEqual(self.engine.run(request), self.engine.run(request))

    def test_all_components_are_dependency_injected(self):
        with self.assertRaisesRegex(ValueError, "all pipeline components"):
            OrchestrationEngine(**{**self.components, "consensus_evaluator": None})

    def test_missing_simulated_outputs_are_diagnostic_not_invoked(self):
        result = self.engine.run(self.request(outputs={}))
        self.assertEqual(result.context.evidence_bundle.records, ())
        self.assertEqual(result.context.consensus_assessment.outcome, "insufficient evidence")
        self.assertTrue(any(item.startswith("missing_simulated_output:") for item in result.diagnostics))

    def test_unplanned_simulated_output_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unplanned steps"):
            self.engine.run(self.request(outputs={"step-unplanned": {"output": {"claims": ["x"]}}}))

    def test_provider_model_selection_and_governance_semantics_are_rejected(self):
        for key in (
            "provider", "model", "authority", "score", "confidence", "rank",
            "vote", "vote_weight", "governance",
        ):
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "prohibited orchestration input"):
                outputs = self.planned_outputs()
                first = sorted(outputs)[0]
                outputs[first] = {**outputs[first], key: "forbidden"}
                self.engine.run(self.request(outputs=outputs))

    def test_result_has_no_authoritative_runtime_or_provider_fields(self):
        result = self.engine.run(self.request())
        for name in (
            "provider", "model", "invoked_agent", "authority", "score", "confidence",
            "rank", "vote", "vote_weight", "governance",
        ):
            self.assertFalse(hasattr(result, name))

    def test_execution_roles_and_capabilities_flow_to_evidence(self):
        result = self.engine.run(self.request())
        steps = {step.step_id: step for step in result.context.execution_plan.steps}
        for record in result.context.evidence_bundle.records:
            step = steps[record.step_id]
            self.assertEqual(record.source.agent_role, step.role)
            self.assertIn(record.source.capability_fulfilled, step.capabilities)


if __name__ == "__main__":
    unittest.main()
