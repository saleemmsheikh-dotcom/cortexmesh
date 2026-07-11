import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = (
    ROOT
    / "CortexMesh_v3_Planning"
    / "06_Implementation_Execution"
    / "Phase2C"
    / "orchestration"
)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


resolver_module = load_module("phase2c_capability_resolver_for_execution", BASE / "capability_resolver.py")
agent_module = load_module("phase2c_agent_planner_for_execution", BASE / "agent_planner.py")
execution_module = load_module("phase2c_execution_plan", BASE / "execution_plan.py")

CapabilityResolver = resolver_module.CapabilityResolver
AgentPlanner = agent_module.AgentPlanner
AgentPlan = agent_module.AgentPlan
AgentRequirement = agent_module.AgentRequirement
ExecutionDependency = execution_module.ExecutionDependency
ExecutionPlan = execution_module.ExecutionPlan
ExecutionPlanner = execution_module.ExecutionPlanner
ExecutionStep = execution_module.ExecutionStep


class TestPhase2CExecutionPlanner(unittest.TestCase):
    def setUp(self):
        self.resolver = CapabilityResolver()
        self.agent_planner = AgentPlanner()
        self.execution_planner = ExecutionPlanner()

    def _agent_plan(self):
        resolution = self.resolver.resolve(
            {
                "objective": "Review security risk and governance evidence",
                "task_type": "review",
                "domain": "governance",
            }
        )
        return self.agent_planner.plan(resolution)

    def test_defines_required_models(self):
        plan = self.execution_planner.plan(self._agent_plan())

        self.assertIsInstance(plan, ExecutionPlan)
        self.assertTrue(all(isinstance(step, ExecutionStep) for step in plan.steps))

    def test_outputs_deterministic_ordered_execution_steps(self):
        agent_plan = self._agent_plan()

        first = self.execution_planner.plan(agent_plan)
        second = self.execution_planner.plan(agent_plan)

        self.assertEqual(first.step_ids(), second.step_ids())
        self.assertEqual(first.role_names(), second.role_names())
        self.assertEqual(first.role_names(), tuple(sorted(first.role_names())))

    def test_preserves_agent_role_and_capability_requirements(self):
        agent_plan = AgentPlan(
            requirements=(
                AgentRequirement(
                    role="risk_reviewer",
                    capabilities=("risk.assessment", "security.review"),
                    reason="test",
                ),
            )
        )

        plan = self.execution_planner.plan(agent_plan)

        self.assertEqual(plan.steps[0].role, "risk_reviewer")
        self.assertEqual(plan.steps[0].capabilities, ("risk.assessment", "security.review"))

    def test_independent_steps_are_parallelizable(self):
        agent_plan = AgentPlan(
            requirements=(
                AgentRequirement(role="architect", capabilities=("orchestration.routing",), reason="test"),
                AgentRequirement(role="risk_reviewer", capabilities=("risk.assessment",), reason="test"),
            )
        )

        plan = self.execution_planner.plan(agent_plan)

        self.assertEqual({step.parallel_group for step in plan.steps}, {0})
        self.assertTrue(all(step.parallelizable for step in plan.steps))
        self.assertTrue(all(step.depends_on == () for step in plan.steps))

    def test_dependent_steps_are_ordered(self):
        agent_plan = AgentPlan(
            requirements=(
                AgentRequirement(role="architect", capabilities=("orchestration.routing",), reason="test"),
                AgentRequirement(role="risk_reviewer", capabilities=("risk.assessment",), reason="test"),
            )
        )

        plan = self.execution_planner.plan(
            agent_plan,
            dependencies=(
                ExecutionDependency(
                    before="architect",
                    after="risk_reviewer",
                    reason="risk review follows architecture",
                ),
            ),
        )

        self.assertEqual(plan.role_names(), ("architect", "risk_reviewer"))
        self.assertEqual(plan.steps[1].depends_on, ("architect",))
        self.assertEqual(plan.steps[0].parallel_group, 0)
        self.assertEqual(plan.steps[1].parallel_group, 1)

    def test_missing_dependency_roles_emit_diagnostics(self):
        agent_plan = AgentPlan(
            requirements=(
                AgentRequirement(role="architect", capabilities=("orchestration.routing",), reason="test"),
            )
        )

        plan = self.execution_planner.plan(
            agent_plan,
            dependencies=(ExecutionDependency(before="architect", after="missing_role"),),
        )

        self.assertIn(
            "missing_dependency_role:architect->missing_role:missing_role",
            plan.diagnostics,
        )
        self.assertEqual(plan.dependencies, ())

    def test_invalid_self_dependency_emits_diagnostics(self):
        agent_plan = AgentPlan(
            requirements=(
                AgentRequirement(role="architect", capabilities=("orchestration.routing",), reason="test"),
            )
        )

        plan = self.execution_planner.plan(
            agent_plan,
            dependencies=(ExecutionDependency(before="architect", after="architect"),),
        )

        self.assertIn("invalid_dependency_self:architect", plan.diagnostics)

    def test_cyclic_dependencies_emit_diagnostics(self):
        agent_plan = AgentPlan(
            requirements=(
                AgentRequirement(role="architect", capabilities=("orchestration.routing",), reason="test"),
                AgentRequirement(role="risk_reviewer", capabilities=("risk.assessment",), reason="test"),
            )
        )

        plan = self.execution_planner.plan(
            agent_plan,
            dependencies=(
                ExecutionDependency(before="architect", after="risk_reviewer"),
                ExecutionDependency(before="risk_reviewer", after="architect"),
            ),
        )

        self.assertIn("cyclic_dependencies:architect,risk_reviewer", plan.diagnostics)
        self.assertEqual(set(plan.role_names()), {"architect", "risk_reviewer"})

    def test_no_agent_provider_scoring_authority_consensus_fields(self):
        plan = self.execution_planner.plan(self._agent_plan())

        self.assertFalse(hasattr(plan, "selected_provider"))
        self.assertFalse(hasattr(plan, "invoked_agent"))
        self.assertFalse(hasattr(plan, "score"))
        self.assertFalse(hasattr(plan, "authority"))
        self.assertFalse(hasattr(plan, "confidence"))
        self.assertFalse(hasattr(plan, "vote_weight"))
        self.assertFalse(hasattr(plan, "consensus"))

    def test_rejects_provider_model_identity_in_provenance(self):
        polluted = AgentPlan(
            requirements=(
                AgentRequirement(role="architect", capabilities=("orchestration.routing",), reason="test"),
            ),
            provenance={"model": "llama"},
        )

        with self.assertRaises(ValueError):
            self.execution_planner.plan(polluted)

    def test_empty_agent_plan_is_explicit(self):
        plan = self.execution_planner.plan(AgentPlan(requirements=()))

        self.assertEqual(plan.steps, ())
        self.assertIn("no_execution_steps_planned", plan.diagnostics)

    def test_provenance_is_informational_only(self):
        plan = self.execution_planner.plan(self._agent_plan())

        self.assertTrue(plan.provenance["provenance_only"])
        self.assertEqual(plan.provenance["planner"], "phase2c.reference.execution_planner")
        self.assertNotIn("provider", plan.provenance)
        self.assertNotIn("model", plan.provenance)


if __name__ == "__main__":
    unittest.main()
