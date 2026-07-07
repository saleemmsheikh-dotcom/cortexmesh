import sys
import unittest
from pathlib import Path


PHASE1B_PATH = (
    Path(__file__).resolve().parents[1]
    / "CortexMesh_v3_Planning"
    / "06_Implementation_Execution"
    / "Phase1B"
)
if str(PHASE1B_PATH) not in sys.path:
    sys.path.insert(0, str(PHASE1B_PATH))

from local_ai import (  # noqa: E402
    Capability,
    LocalAIManager,
    LocalAIManagerSettings,
    get_capability,
    normalize_capability_name,
    registered_capability_names,
)
from local_ai.provider import ConnectionCheck  # noqa: E402
from local_ai.registry import PROVIDER_REGISTRY, ProviderRegistration  # noqa: E402


class FakeProvider:
    def __init__(self, name, available=True):
        self._name = name
        self.available = available

    def name(self):
        return self._name

    def validate_config(self, config):
        return None

    def check_connection(self, config):
        return ConnectionCheck(
            provider=self._name,
            model=config.model,
            endpoint_ref=f"test://{self._name}",
            ok=self.available,
            status="connected" if self.available else "failed",
            latency_ms=1,
            error=None if self.available else "unavailable",
        )

    def generate(self, request, config):
        raise NotImplementedError("not needed for capability tests")


def registration(name, available=True, capabilities=("text_generation", "health_check")):
    return ProviderRegistration(
        name=name,
        factory=lambda: FakeProvider(name, available=available),
        default_base_url=f"test://{name}",
        default_model=f"{name}-model",
        capabilities=capabilities,
    )


class TestPhase1BCapabilities(unittest.TestCase):
    def test_capability_object_normalizes_name(self):
        capability = Capability("Text Generation", "Generate text")

        self.assertEqual(capability.name, "text_generation")
        self.assertTrue(capability.as_dict()["provenance_only"])

    def test_capability_registry_exposes_known_capabilities(self):
        names = registered_capability_names()

        self.assertIn("text_generation", names)
        self.assertIn("chat_completion", names)
        self.assertEqual(get_capability("text-generation").name, "text_generation")
        self.assertEqual(normalize_capability_name("Health Check"), "health_check")

    def test_provider_registrations_declare_capabilities(self):
        self.assertIn("text_generation", PROVIDER_REGISTRY["ollama"].capabilities)
        self.assertIn("health_check", PROVIDER_REGISTRY["ollama"].capabilities)
        self.assertIn("chat_completion", PROVIDER_REGISTRY["lmstudio"].capabilities)
        self.assertTrue(PROVIDER_REGISTRY["lmstudio"].implemented)

    def test_manager_lists_implemented_capabilities(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="alpha", provider_options=("alpha",)),
            registry={
                "alpha": registration("alpha", capabilities=("text_generation",)),
                "future": ProviderRegistration(
                    name="future",
                    factory=None,
                    default_base_url="test://future",
                    default_model="future-model",
                    status="placeholder",
                    capabilities=("chat_completion",),
                ),
            },
        )

        implemented = [capability.name for capability in manager.list_capabilities()]
        all_declared = [
            capability.name
            for capability in manager.list_capabilities(implemented_only=False)
        ]

        self.assertEqual(implemented, ["text_generation"])
        self.assertEqual(all_declared, ["text_generation", "chat_completion"])

    def test_manager_supports_capability_without_provider_ranking(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="auto", provider_options=("alpha", "beta")),
            registry={
                "alpha": registration("alpha", capabilities=("text_generation",)),
                "beta": registration("beta", capabilities=("chat_completion",)),
            },
        )

        self.assertTrue(manager.supports("text_generation"))
        self.assertTrue(manager.supports("chat-completion"))
        self.assertFalse(manager.supports("image_generation"))

        capabilities = manager.capabilities()
        self.assertFalse(capabilities["ranking_used"])
        self.assertTrue(capabilities["capabilities_are_provenance_only"])
        for forbidden in ("confidence", "score", "authority", "vote_weight", "rank"):
            self.assertNotIn(forbidden, capabilities)

    def test_placeholder_capability_support_is_opt_in(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="alpha", provider_options=("alpha", "future")),
            registry={
                "alpha": registration("alpha", capabilities=("text_generation",)),
                "future": ProviderRegistration(
                    name="future",
                    factory=None,
                    default_base_url="test://future",
                    default_model="future-model",
                    status="placeholder",
                    capabilities=("chat_completion",),
                ),
            },
        )

        self.assertFalse(manager.supports("chat_completion"))
        self.assertTrue(manager.supports("chat_completion", implemented_only=False))

    def test_auto_selection_remains_availability_based(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="auto", provider_options=("first", "second")),
            registry={
                "first": registration(
                    "first",
                    available=True,
                    capabilities=("health_check",),
                ),
                "second": registration(
                    "second",
                    available=True,
                    capabilities=("text_generation", "chat_completion"),
                ),
            },
        )

        selection = manager.select_provider()

        self.assertEqual(selection.provider_name, "first")
        self.assertEqual(selection.diagnostics["selection_basis"], "availability")
        self.assertFalse(selection.diagnostics["ranking_used"])


if __name__ == "__main__":
    unittest.main()
