import importlib.util
from pathlib import Path
import sys
import unittest


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "CortexMesh_v3_Planning"
    / "06_Implementation_Execution"
    / "Phase2C"
    / "orchestration"
    / "capability_resolver.py"
)


def load_resolver_module():
    spec = importlib.util.spec_from_file_location("phase2c_capability_resolver", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


resolver_module = load_resolver_module()
CapabilityResolver = resolver_module.CapabilityResolver
IntentDescriptor = resolver_module.IntentDescriptor
CapabilityRequirement = resolver_module.CapabilityRequirement
CapabilityResolution = resolver_module.CapabilityResolution


class TestPhase2CCapabilityResolver(unittest.TestCase):
    def setUp(self):
        self.resolver = CapabilityResolver()

    def test_defines_required_models(self):
        intent = IntentDescriptor(objective="Review API risk", task_type="review", domain="security")
        resolution = self.resolver.resolve(intent)

        self.assertIsInstance(resolution, CapabilityResolution)
        self.assertTrue(all(isinstance(req, CapabilityRequirement) for req in resolution.requirements))

    def test_normalizes_input_before_resolution(self):
        resolution = self.resolver.resolve(
            {
                "objective": "  Review   API   Risk  ",
                "task_type": " Review ",
                "domain": " Security ",
                "constraints": [" Evidence ", "RISK"],
            }
        )

        self.assertEqual(resolution.intent.objective, "review api risk")
        self.assertEqual(resolution.intent.task_type, "review")
        self.assertEqual(resolution.intent.domain, "security")
        self.assertEqual(resolution.intent.constraints, ("evidence", "risk"))

    def test_resolves_capability_requirements_deterministically(self):
        intent = {
            "objective": "Review API security risk evidence",
            "task_type": "review",
            "domain": "security",
        }

        first = self.resolver.resolve(intent)
        second = self.resolver.resolve(intent)

        self.assertEqual(first.capability_names(), second.capability_names())
        self.assertIn("risk.assessment", first.capability_names())
        self.assertIn("security.review", first.capability_names())
        self.assertIn("architecture.api_design", first.capability_names())
        self.assertEqual(first.capability_names(), tuple(sorted(first.capability_names())))

    def test_unknown_elements_emit_diagnostics(self):
        resolution = self.resolver.resolve(
            {
                "objective": "Investigate zephyr quasar",
                "task_type": "mystery",
                "domain": "unknown-domain",
            }
        )

        diagnostics = " ".join(resolution.diagnostics)
        self.assertIn("unknown_task_type:mystery", diagnostics)
        self.assertIn("unknown_domain:unknown-domain", diagnostics)
        self.assertIn("unresolved_terms:investigate,quasar,zephyr", diagnostics)

    def test_no_agent_or_provider_selection_fields(self):
        resolution = self.resolver.resolve(
            {
                "objective": "Plan governance evidence review",
                "task_type": "planning",
                "domain": "governance",
            }
        )

        self.assertFalse(hasattr(resolution, "selected_agent"))
        self.assertFalse(hasattr(resolution, "selected_provider"))
        self.assertFalse(hasattr(resolution, "score"))
        self.assertFalse(hasattr(resolution, "authority"))
        self.assertFalse(hasattr(resolution, "confidence"))
        self.assertFalse(hasattr(resolution, "vote_weight"))

    def test_rejects_provider_identity_input(self):
        with self.assertRaises(ValueError):
            self.resolver.resolve(
                {
                    "objective": "Review evidence",
                    "task_type": "review",
                    "domain": "governance",
                    "provider": "ollama",
                }
            )

        with self.assertRaises(ValueError):
            IntentDescriptor(
                objective="Review evidence",
                provenance={"model": "llama"},
            ).normalized()

    def test_provenance_is_informational_only(self):
        resolution = self.resolver.resolve(
            {
                "objective": "Design orchestration routing",
                "task_type": "design",
                "domain": "systems",
                "provenance": {"source": "unit-test"},
            }
        )

        self.assertTrue(resolution.provenance["provenance_only"])
        self.assertEqual(resolution.intent.provenance["source"], "unit-test")
        self.assertNotIn("provider", resolution.provenance)
        self.assertNotIn("model", resolution.provenance)

    def test_fallback_is_explicit_when_nothing_resolves(self):
        resolution = self.resolver.resolve(
            {
                "objective": "",
                "task_type": "unmapped",
                "domain": "unmapped",
            }
        )

        self.assertIn("reasoning.general", resolution.capability_names())
        self.assertIn("no_capabilities_resolved", resolution.diagnostics)


if __name__ == "__main__":
    unittest.main()
