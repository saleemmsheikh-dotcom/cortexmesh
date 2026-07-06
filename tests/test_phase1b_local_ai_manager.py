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
    LocalAIHealthResult,
    LocalAIManager,
    LocalAIManagerSettings,
    LocalAIRequest,
)
from local_ai.provider import ConnectionCheck, LocalAIResponse  # noqa: E402
from local_ai.registry import ProviderRegistration  # noqa: E402


class FakeProvider:
    def __init__(self, name, available=True):
        self._name = name
        self.available = available

    def name(self):
        return self._name

    def validate_config(self, config):
        if config.provider != self._name:
            raise ValueError("provider mismatch")

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
        return LocalAIResponse(
            request_id=request.request_id,
            provider=self._name,
            model=config.model,
            content=f"{self._name} response",
            status="complete",
            latency_ms=2,
            finish_reason="stop",
            diagnostics={"endpoint_ref": f"test://{self._name}/generate"},
        )


def registration(name, available=True):
    return ProviderRegistration(
        name=name,
        factory=lambda: FakeProvider(name, available=available),
        default_base_url=f"test://{name}",
        default_model=f"{name}-model",
        notes="test provider",
    )


class TestLocalAIManager(unittest.TestCase):
    def test_explicit_selection_uses_configured_provider(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="alpha", provider_options=("alpha",)),
            registry={"alpha": registration("alpha")},
        )

        selection = manager.select_provider()

        self.assertEqual(selection.provider_name, "alpha")
        self.assertEqual(selection.selection_mode, "explicit")
        self.assertFalse(selection.diagnostics["ranking_used"])
        self.assertTrue(selection.diagnostics["availability_checked"])
        self.assertTrue(selection.diagnostics["health"]["ok"])

    def test_auto_selection_uses_availability_not_ranking(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(
                provider="auto",
                provider_options=("down", "up"),
            ),
            registry={
                "down": registration("down", available=False),
                "up": registration("up", available=True),
            },
        )

        selection = manager.select_provider()

        self.assertEqual(selection.provider_name, "up")
        self.assertEqual(selection.selection_mode, "auto")
        self.assertTrue(selection.diagnostics["availability_checked"])
        self.assertFalse(selection.diagnostics["ranking_used"])
        self.assertEqual(
            [item["provider"] for item in selection.diagnostics["health_checks"]],
            ["down", "up"],
        )
        self.assertEqual(selection.diagnostics["selection_basis"], "availability")

    def test_unavailable_selected_provider_fails_cleanly(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="down", provider_options=("down",)),
            registry={"down": registration("down", available=False)},
        )

        with self.assertRaisesRegex(RuntimeError, "selected Local AI provider is unavailable"):
            manager.select_provider()

    def test_auto_selection_falls_back_from_unavailable_provider(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="auto", provider_options=("down", "up")),
            registry={
                "down": registration("down", available=False),
                "up": registration("up", available=True),
            },
        )

        selection = manager.select_provider()
        health_checks = selection.diagnostics["health_checks"]

        self.assertEqual(selection.provider_name, "up")
        self.assertFalse(health_checks[0]["ok"])
        self.assertTrue(health_checks[1]["ok"])
        self.assertFalse(selection.diagnostics["ranking_used"])

    def test_all_providers_unavailable_fails_with_diagnostics(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="auto", provider_options=("down", "also_down")),
            registry={
                "down": registration("down", available=False),
                "also_down": registration("also_down", available=False),
            },
        )

        with self.assertRaisesRegex(RuntimeError, "no available Local AI provider"):
            manager.select_provider()

    def test_health_result_has_structured_diagnostics(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="down", provider_options=("down",)),
            registry={"down": registration("down", available=False)},
        )

        health = manager.health_result("down")
        diagnostics = health.as_diagnostics()

        self.assertIsInstance(health, LocalAIHealthResult)
        self.assertEqual(diagnostics["provider"], "down")
        self.assertFalse(diagnostics["ok"])
        self.assertEqual(diagnostics["status"], "failed")
        self.assertEqual(diagnostics["endpoint_ref"], "test://down")
        self.assertEqual(diagnostics["error"], "unavailable")

    def test_unknown_provider_fails_cleanly(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="missing"),
            registry={"alpha": registration("alpha")},
        )

        with self.assertRaisesRegex(ValueError, "unknown Local AI provider"):
            manager.select_provider()

    def test_placeholder_provider_fails_cleanly(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="placeholder"),
            registry={
                "placeholder": ProviderRegistration(
                    name="placeholder",
                    factory=None,
                    default_base_url="test://placeholder",
                    default_model="placeholder-model",
                    status="placeholder",
                )
            },
        )

        with self.assertRaisesRegex(ValueError, "registered but not implemented"):
            manager.select_provider()

    def test_generate_returns_provenance_without_authority(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="alpha", provider_options=("alpha",)),
            registry={"alpha": registration("alpha")},
        )
        request = LocalAIRequest(
            prompt="test",
            model="alpha-model",
            request_id="REQ-1",
            objective_ref="TEST",
        )

        result = manager.generate(request)

        self.assertEqual(result.response.content, "alpha response")
        self.assertEqual(result.provenance["provider"], "alpha")
        self.assertEqual(result.provenance["selected_provider"], "alpha")
        self.assertFalse(result.provenance["authoritative"])
        self.assertTrue(result.diagnostics["provider_identity_is_provenance_only"])
        self.assertFalse(result.diagnostics["ranking_used"])
        self.assertNotIn("confidence", result.diagnostics)
        self.assertNotIn("score", result.diagnostics)
        self.assertNotIn("authority", result.diagnostics)
        self.assertNotIn("vote_weight", result.diagnostics)

    def test_capabilities_expose_status_without_ranking(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="alpha", provider_options=("alpha", "future")),
            registry={
                "alpha": registration("alpha"),
                "future": ProviderRegistration(
                    name="future",
                    factory=None,
                    default_base_url="test://future",
                    default_model="future-model",
                    status="placeholder",
                ),
            },
        )

        capabilities = manager.capabilities()

        self.assertTrue(capabilities["providers"]["alpha"]["implemented"])
        self.assertFalse(capabilities["providers"]["future"]["implemented"])
        self.assertNotIn("rank", capabilities["providers"]["alpha"])
        self.assertEqual(capabilities["configured_options"], ["alpha", "future"])


if __name__ == "__main__":
    unittest.main()
