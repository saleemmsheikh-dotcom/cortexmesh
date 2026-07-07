import sys
import unittest
from pathlib import Path
from unittest.mock import patch


PHASE1B_PATH = (
    Path(__file__).resolve().parents[1]
    / "CortexMesh_v3_Planning"
    / "06_Implementation_Execution"
    / "Phase1B"
)
if str(PHASE1B_PATH) not in sys.path:
    sys.path.insert(0, str(PHASE1B_PATH))

from local_ai import LocalAIConfig, LocalAIManager, LocalAIManagerSettings, LocalAIRequest  # noqa: E402
from local_ai.lmstudio import LMStudioProvider  # noqa: E402
from local_ai.registry import PROVIDER_REGISTRY  # noqa: E402


class TestLMStudioProvider(unittest.TestCase):
    def test_registry_marks_lmstudio_as_implemented(self):
        registration = PROVIDER_REGISTRY["lmstudio"]

        self.assertTrue(registration.implemented)
        self.assertEqual(registration.status, "available")
        self.assertIn("chat_completion", registration.capabilities)
        self.assertIn("text_generation", registration.capabilities)
        self.assertIn("health_check", registration.capabilities)

    def test_validate_config_uses_existing_provider_contract(self):
        provider = LMStudioProvider()
        config = LocalAIConfig(
            provider="lmstudio",
            base_url="http://localhost:1234",
            model="local-model",
        )

        provider.validate_config(config)

        with self.assertRaisesRegex(ValueError, "provider is not registered"):
            provider.validate_config(
                LocalAIConfig(
                    provider="ollama",
                    base_url="http://localhost:11434",
                    model="model",
                )
            )

    def test_health_check_discovers_models(self):
        provider = LMStudioProvider()
        config = LocalAIConfig(
            provider="lmstudio",
            base_url="http://localhost:1234/",
            model="local-model",
        )

        with patch.object(
            provider,
            "_request_json",
            return_value={"data": [{"id": "local-model"}, {"id": "other-model"}]},
        ) as request_json:
            check = provider.check_connection(config)

        request_json.assert_called_once_with(
            method="GET",
            url="http://localhost:1234/v1/models",
            timeout=config.timeout_seconds,
        )
        self.assertTrue(check.ok)
        self.assertEqual(check.provider, "lmstudio")
        self.assertEqual(check.model, "local-model")
        self.assertEqual(check.status, "connected")
        self.assertEqual(check.endpoint_ref, "http://localhost:1234/v1/models")
        self.assertTrue(check.diagnostics["model_available"])
        self.assertEqual(check.diagnostics["model_count"], 2)

    def test_health_check_fails_cleanly(self):
        provider = LMStudioProvider()
        config = LocalAIConfig(
            provider="lmstudio",
            base_url="http://localhost:1234",
            model="local-model",
        )

        with patch.object(provider, "_request_json", side_effect=RuntimeError("offline")):
            check = provider.check_connection(config)

        self.assertFalse(check.ok)
        self.assertEqual(check.status, "failed")
        self.assertEqual(check.error, "offline")

    def test_request_mapping_uses_chat_completions(self):
        provider = LMStudioProvider()
        config = LocalAIConfig(
            provider="lmstudio",
            base_url="http://localhost:1234",
            model="local-model",
            temperature=0.2,
            max_tokens=128,
        )
        request = LocalAIRequest(
            prompt="Explain the design",
            model="local-model",
            request_id="REQ-1",
            objective_ref="OBJ-1",
            system_prompt="Stay concise",
        )

        with patch.object(
            provider,
            "_request_json",
            return_value={
                "model": "local-model",
                "choices": [
                    {
                        "message": {"content": "Design response"},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 3, "completion_tokens": 2},
            },
        ) as request_json:
            response = provider.generate(request, config)

        call = request_json.call_args.kwargs
        self.assertEqual(call["method"], "POST")
        self.assertEqual(call["url"], "http://localhost:1234/v1/chat/completions")
        self.assertEqual(call["body"]["model"], "local-model")
        self.assertEqual(
            call["body"]["messages"],
            [
                {"role": "system", "content": "Stay concise"},
                {"role": "user", "content": "Explain the design"},
            ],
        )
        self.assertEqual(call["body"]["temperature"], 0.2)
        self.assertEqual(call["body"]["max_tokens"], 128)
        self.assertEqual(response.content, "Design response")
        self.assertEqual(response.status, "complete")
        self.assertEqual(response.finish_reason, "stop")
        self.assertEqual(response.usage["prompt_tokens"], 3)
        self.assertNotIn("confidence", response.diagnostics)
        self.assertNotIn("score", response.diagnostics)
        self.assertNotIn("authority", response.diagnostics)
        self.assertNotIn("vote_weight", response.diagnostics)

    def test_response_normalization_rejects_invalid_payloads(self):
        provider = LMStudioProvider()
        request = LocalAIRequest("prompt", "model", "REQ-1", "OBJ-1")
        config = LocalAIConfig(
            provider="lmstudio",
            base_url="http://localhost:1234",
            model="model",
        )

        invalid_payloads = [
            ({}, "missing choices"),
            ({"choices": [{}]}, "missing message"),
            ({"choices": [{"message": {}}]}, "missing string content"),
        ]

        for payload, message in invalid_payloads:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    provider.normalize_response(payload, request, config, "endpoint", 1)

    def test_manager_selects_lmstudio_by_configuration(self):
        manager = LocalAIManager(
            LocalAIManagerSettings(
                provider="lmstudio",
                provider_options=("lmstudio",),
                base_url="http://localhost:1234",
                model="local-model",
            )
        )

        with patch.object(
            LMStudioProvider,
            "check_connection",
            return_value=type(
                "Check",
                (),
                {
                    "provider": "lmstudio",
                    "model": "local-model",
                    "endpoint_ref": "http://localhost:1234/v1/models",
                    "ok": True,
                    "status": "connected",
                    "latency_ms": 1,
                    "diagnostics": {},
                    "error": None,
                },
            )(),
        ):
            selection = manager.select_provider()

        self.assertEqual(selection.provider_name, "lmstudio")
        self.assertEqual(selection.selection_mode, "explicit")
        self.assertFalse(selection.diagnostics["ranking_used"])
        self.assertEqual(selection.config.provider, "lmstudio")


if __name__ == "__main__":
    unittest.main()
