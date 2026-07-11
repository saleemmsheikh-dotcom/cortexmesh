import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESOLVER_PATH = (
    ROOT
    / "CortexMesh_v3_Planning"
    / "06_Implementation_Execution"
    / "Phase2C"
    / "orchestration"
    / "capability_resolver.py"
)
PLANNER_PATH = (
    ROOT
    / "CortexMesh_v3_Planning"
    / "06_Implementation_Execution"
    / "Phase2C"
    / "orchestration"
    / "agent_planner.py"
)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


resolver_module = load_module("phase2c_capability_resolver_for_planner", RESOLVER_PATH)
planner_module = load_module("phase2c_agent_planner", PLANNER_PATH)

CapabilityResolver = resolver_module.CapabilityResolver
AgentDescriptor = planner_module.AgentDescriptor
AgentRequirement = planner_module.AgentRequirement
AgentPlan = planner_module.AgentPlan
AgentPlanner = planner_module.AgentPlanner


class TestPhase2CAgentPlanner(unittest.TestCase):
    def setUp(self):
        self.resolver = CapabilityResolver()
        self.planner = AgentPlanner()

    def test_defines_required_models(self):
        resolution = self.resolver.resolve(
            {"objective": "Review security risk", "task_type": "review", "domain": "security"}
        )
        plan = self.planner.plan(resolution)

        self.assertIsInstance(plan, AgentPlan)
        self.assertTrue(all(isinstance(req, AgentRequirement) for req in plan.requirements))

    def test_maps_capabilities_to_deterministic_agent_roles(self):
        resolution = self.resolver.resolve(
            {
                "objective": "Design orchestration routing with governance evidence",
                "task_type": "design",
                "domain": "governance",
            }
        )

        first = self.planner.plan(resolution)
        second = self.planner.plan(resolution)

        self.assertEqual(first.role_names(), second.role_names())
        self.assertEqual(first.role_names(), tuple(sorted(first.role_names())))
        self.assertIn("architect", first.role_names())
        self.assertIn("governance_reviewer", first.role_names())

    def test_capabilities_determine_agent_eligibility(self):
        resolution = self.resolver.resolve(
            {
                "objective": "Refactor code and design tests",
                "task_type": "implementation",
                "domain": "code",
            }
        )
        plan = self.planner.plan(resolution)

        engineer = next(req for req in plan.requirements if req.role == "implementation_engineer")
        self.assertIn("code.generation", engineer.capabilities)
        self.assertIn("code.review", engineer.capabilities)
        self.assertIn("code.reasoning", engineer.capabilities)

    def test_multiple_agents_only_for_distinct_capability_coverage(self):
        resolution = self.resolver.resolve(
            {
                "objective": "Review security risk and governance evidence",
                "task_type": "review",
                "domain": "governance",
            }
        )
        plan = self.planner.plan(resolution)

        roles = set(plan.role_names())
        self.assertIn("governance_reviewer", roles)
        self.assertIn("risk_reviewer", roles)
        self.assertTrue(
            all(req.capabilities for req in plan.requirements),
            "every planned role must cover at least one distinct capability",
        )

    def test_missing_capability_coverage_emits_diagnostics(self):
        custom_agent = AgentDescriptor(role="limited", capabilities=("known.capability",))
        planner = AgentPlanner(agents=(custom_agent,))
        resolution = self.resolver.resolve(
            {
                "objective": "Review security risk",
                "task_type": "review",
                "domain": "security",
            }
        )

        plan = planner.plan(resolution)
        diagnostics = " ".join(plan.diagnostics)

        self.assertIn("missing_capability_coverage:risk.assessment", diagnostics)
        self.assertIn("missing_capability_coverage:security.review", diagnostics)

    def test_no_provider_or_model_identity_is_accepted(self):
        resolution = self.resolver.resolve(
            {"objective": "Review risk", "task_type": "review", "domain": "security"}
        )

        polluted = resolver_module.CapabilityResolution(
            intent=resolution.intent,
            requirements=resolution.requirements,
            diagnostics=resolution.diagnostics,
            provenance={"provider": "ollama"},
        )

        with self.assertRaises(ValueError):
            self.planner.plan(polluted)

    def test_no_ranking_scoring_confidence_authority_or_vote_weight_fields(self):
        resolution = self.resolver.resolve(
            {"objective": "Plan evidence review", "task_type": "planning", "domain": "governance"}
        )
        plan = self.planner.plan(resolution)

        self.assertFalse(hasattr(plan, "selected_provider"))
        self.assertFalse(hasattr(plan, "agent_rank"))
        self.assertFalse(hasattr(plan, "score"))
        self.assertFalse(hasattr(plan, "authority"))
        self.assertFalse(hasattr(plan, "confidence"))
        self.assertFalse(hasattr(plan, "vote_weight"))

    def test_provenance_is_informational_only(self):
        resolution = self.resolver.resolve(
            {"objective": "Compare evidence", "task_type": "comparison", "domain": "systems"}
        )
        plan = self.planner.plan(resolution)

        self.assertTrue(plan.provenance["provenance_only"])
        self.assertEqual(plan.provenance["planner"], "phase2c.reference.agent_planner")
        self.assertNotIn("provider", plan.provenance)
        self.assertNotIn("model", plan.provenance)

    def test_no_requirements_planned_is_explicit(self):
        custom_agent = AgentDescriptor(role="limited", capabilities=("known.capability",))
        planner = AgentPlanner(agents=(custom_agent,))
        resolution = self.resolver.resolve(
            {"objective": "", "task_type": "unmapped", "domain": "unmapped"}
        )

        plan = planner.plan(resolution)

        self.assertEqual(plan.requirements, ())
        self.assertIn("no_agent_requirements_planned", plan.diagnostics)


if __name__ == "__main__":
    unittest.main()
