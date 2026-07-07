import os
import unittest
from unittest.mock import patch

from agents import local_ai_bridge


class FakeProvider:
    def name(self):
        return "fake"

    def validate_config(self, config):
        return None

    def check_connection(self, config):
        return type(
            "Connection",
            (),
            {
                "ok": True,
                "status": "connected",
                "error": None,
                "diagnostics": {},
            },
        )()

    def generate(self, request, config):
        return type(
            "Response",
            (),
            {
                "content": "fake response",
                "provider": config.provider,
                "model": config.model,
                "request_id": request.request_id,
                "status": "complete",
                "latency_ms": 0,
                "finish_reason": "test",
                "diagnostics": {"endpoint_ref": "test://provider"},
            },
        )()


class TestPhase1BProviderSelection(unittest.TestCase):
    def setUp(self):
        self._env = os.environ.copy()
        local_ai_bridge._ensure_phase1b_import_path()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._env)

    def test_registry_exposes_implemented_ollama_and_lmstudio(self):
        from local_ai import (
            get_registration,
            implemented_provider_names,
            registered_provider_names,
        )

        self.assertIn("ollama", implemented_provider_names())
        self.assertIn("lmstudio", implemented_provider_names())
        self.assertIn("ollama", registered_provider_names())
        self.assertIn("lmstudio", registered_provider_names())
        self.assertTrue(get_registration("lmstudio").implemented)

    def test_explicit_provider_selection_is_configuration_driven(self):
        os.environ["CORTEX_LOCAL_AI_ENABLED"] = "1"
        os.environ["CORTEX_LOCAL_AI_PROVIDER"] = "ollama"
        os.environ["CORTEX_LOCAL_AI_MODEL"] = "unit-test-model"

        with patch("local_ai.registry.create_provider", return_value=FakeProvider()):
            result = local_ai_bridge.generate_local_solution(
                "Architect_test",
                "architect",
                "Architect",
                "Test task",
            )

        provenance = result["provenance"]
        self.assertEqual(result["solution"], "fake response")
        self.assertEqual(provenance["provider"], "ollama")
        self.assertEqual(provenance["selected_provider"], "ollama")
        self.assertEqual(provenance["provider_selection"], "ollama")
        self.assertFalse(provenance["authoritative"])
        self.assertEqual(provenance["confidence_source"], "static_local_solver_default")

    def test_auto_selection_uses_available_provider_options(self):
        os.environ["CORTEX_LOCAL_AI_ENABLED"] = "1"
        os.environ["CORTEX_LOCAL_AI_PROVIDER"] = "auto"
        os.environ["CORTEX_LOCAL_AI_PROVIDER_OPTIONS"] = "ollama"
        os.environ["CORTEX_LOCAL_AI_MODEL"] = "unit-test-model"

        with patch(
            "local_ai.auto_select_available_provider",
            return_value=(
                "ollama",
                FakeProvider(),
                local_ai_bridge._local_config(
                    local_ai_bridge.load_local_ai_solver_config(),
                    "ollama",
                ),
            ),
        ):
            result = local_ai_bridge.generate_local_solution(
                "Architect_test",
                "architect",
                "Architect",
                "Test task",
            )

        provenance = result["provenance"]
        self.assertEqual(provenance["selected_provider"], "ollama")
        self.assertEqual(provenance["provider_selection"], "auto")
        self.assertEqual(provenance["provider_options"], ["ollama"])

    def test_unknown_provider_fails_cleanly(self):
        os.environ["CORTEX_LOCAL_AI_ENABLED"] = "1"
        os.environ["CORTEX_LOCAL_AI_PROVIDER"] = "unknown-provider"

        with self.assertRaisesRegex(ValueError, "unknown Local AI provider"):
            local_ai_bridge.generate_local_solution(
                "Architect_test",
                "architect",
                "Architect",
                "Test task",
            )


if __name__ == "__main__":
    unittest.main()
