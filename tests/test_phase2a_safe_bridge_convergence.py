import inspect
import os
import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

from agents import local_ai_bridge


PHASE1B_PATH = (
    Path(__file__).resolve().parents[1]
    / "CortexMesh_v3_Planning"
    / "06_Implementation_Execution"
    / "Phase1B"
)
if str(PHASE1B_PATH) not in sys.path:
    sys.path.insert(0, str(PHASE1B_PATH))

from local_ai import (  # noqa: E402
    LocalAIManager,
    LocalAIManagerResult,
    LocalAIManagerSettings,
    LocalAIRequest,
)
from local_ai.provider import ConnectionCheck, LocalAIResponse  # noqa: E402
from local_ai.registry import ProviderRegistration  # noqa: E402


class FakeProvider:
    def __init__(self, name):
        self._name = name
        self.seen_model = None

    def name(self):
        return self._name

    def validate_config(self, config):
        return None

    def check_connection(self, config):
        return ConnectionCheck(
            provider=self._name,
            model=config.model,
            endpoint_ref=f"test://{self._name}",
            ok=True,
            status="connected",
            latency_ms=1,
        )

    def generate(self, request, config):
        request.validate()
        self.seen_model = request.model
        return LocalAIResponse(
            request_id=request.request_id,
            provider=self._name,
            model=request.model,
            content="manager generated response",
            status="complete",
            latency_ms=2,
            finish_reason="stop",
            diagnostics={"endpoint_ref": f"test://{self._name}/generate"},
        )


def registration(name, provider):
    return ProviderRegistration(
        name=name,
        factory=lambda: provider,
        default_base_url=f"test://{name}",
        default_model=f"{name}-default-model",
        notes="test provider",
    )


@dataclass
class CapturingManager:
    settings: LocalAIManagerSettings

    last_request = None
    last_settings = None

    def __post_init__(self):
        CapturingManager.last_settings = self.settings

    def generate(self, request):
        CapturingManager.last_request = request
        selected_provider = (
            self.settings.provider_options[0]
            if self.settings.provider == "auto"
            else self.settings.provider
        )
        response = LocalAIResponse(
            request_id=request.request_id,
            provider=selected_provider,
            model=request.model or "manager-default-model",
            content="bridge response",
            status="complete",
            latency_ms=3,
            finish_reason="stop",
            diagnostics={"endpoint_ref": "test://manager/generate"},
        )
        return LocalAIManagerResult(
            response=response,
            provenance={
                "provider": response.provider,
                "model": response.model,
                "selected_provider": selected_provider,
                "provider_selection": self.settings.provider,
                "provider_options": list(self.settings.provider_options),
                "request_id": response.request_id,
                "endpoint_ref": response.diagnostics["endpoint_ref"],
                "status": response.status,
                "latency_ms": response.latency_ms,
                "finish_reason": response.finish_reason,
                "authoritative": False,
            },
            diagnostics={
                "manager": "LocalAIManager",
                "ranking_used": False,
                "provider_identity_is_provenance_only": True,
            },
        )


class TestPhase2ASafeBridgeConvergence(unittest.TestCase):
    def setUp(self):
        self._env = os.environ.copy()
        CapturingManager.last_request = None
        CapturingManager.last_settings = None

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._env)

    def test_bridge_uses_manager_not_registry_or_provider_adapters(self):
        source = inspect.getsource(local_ai_bridge)
        forbidden = [
            "auto_select_available_provider",
            "get_registration",
            "select_provider",
            "PROVIDER_REGISTRY",
            "CAPABILITY_REGISTRY",
            "OllamaProvider",
            "LMStudioProvider",
            "LocalAITelemetryBuffer",
        ]

        for token in forbidden:
            self.assertNotIn(token, source)
        self.assertIn("LocalAIManager", source)

    def test_disabled_bridge_returns_none(self):
        os.environ.pop("CORTEX_LOCAL_AI_ENABLED", None)

        self.assertIsNone(
            local_ai_bridge.generate_local_solution(
                "Architect_test",
                "architect",
                "Architect",
                "Test task",
            )
        )

    def test_bridge_routes_generation_through_manager(self):
        os.environ["CORTEX_LOCAL_AI_ENABLED"] = "1"
        os.environ["CORTEX_LOCAL_AI_PROVIDER"] = "auto"
        os.environ["CORTEX_LOCAL_AI_PROVIDER_OPTIONS"] = "ollama,lmstudio"
        os.environ["CORTEX_LOCAL_AI_MODEL"] = "configured-model"

        with patch("local_ai.LocalAIManager", CapturingManager):
            result = local_ai_bridge.generate_local_solution(
                "Architect_test",
                "architect",
                "Architect",
                "Test task",
            )

        settings = CapturingManager.last_settings
        request = CapturingManager.last_request
        provenance = result["provenance"]

        self.assertEqual(settings.provider, "auto")
        self.assertEqual(settings.provider_options, ("ollama", "lmstudio"))
        self.assertIsInstance(request, LocalAIRequest)
        self.assertEqual(request.model, "configured-model")
        self.assertEqual(result["solution"], "bridge response")
        self.assertEqual(provenance["provider"], "ollama")
        self.assertEqual(provenance["selected_provider"], "ollama")
        self.assertEqual(provenance["provider_selection"], "auto")
        self.assertEqual(provenance["provider_options"], ["ollama", "lmstudio"])
        self.assertFalse(provenance["authoritative"])
        self.assertEqual(
            provenance["confidence_source"],
            "static_local_solver_default",
        )
        self.assertEqual(provenance["integration_path"], "agents.local_solver")
        self.assertNotIn("confidence", provenance)
        self.assertNotIn("score", provenance)
        self.assertNotIn("authority", provenance)
        self.assertNotIn("vote_weight", provenance)

    def test_manager_fills_default_model_when_bridge_leaves_model_empty(self):
        provider = FakeProvider("alpha")
        manager = LocalAIManager(
            LocalAIManagerSettings(provider="alpha", provider_options=("alpha",)),
            registry={"alpha": registration("alpha", provider)},
        )
        request = LocalAIRequest(
            prompt="test",
            model="",
            request_id="REQ-1",
            objective_ref="TEST",
        )

        result = manager.generate(request)

        self.assertEqual(provider.seen_model, "alpha-default-model")
        self.assertEqual(result.response.model, "alpha-default-model")
        self.assertEqual(result.provenance["model"], "alpha-default-model")


if __name__ == "__main__":
    unittest.main()
