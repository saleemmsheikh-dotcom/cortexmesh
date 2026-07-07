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

from local_ai import LocalAIConfig, LocalAIConfigError, LocalAIRequest  # noqa: E402
from local_ai.ollama import OllamaProvider  # noqa: E402


class TestPhase1BSubsystemStabilisation(unittest.TestCase):
    def test_config_validation_rejects_invalid_core_fields(self):
        cases = [
            (
                LocalAIConfig(provider="", base_url="http://local", model="m"),
                "provider must be explicit",
            ),
            (
                LocalAIConfig(provider="ollama", base_url="", model="m"),
                "base_url must be explicit",
            ),
            (
                LocalAIConfig(provider="ollama", base_url="http://local", model=""),
                "model must be explicit",
            ),
            (
                LocalAIConfig(
                    provider="ollama",
                    base_url="http://local",
                    model="m",
                    timeout_seconds=0,
                ),
                "timeout_seconds must be positive",
            ),
            (
                LocalAIConfig(
                    provider="ollama",
                    base_url="http://local",
                    model="m",
                    temperature=-0.1,
                ),
                "temperature must not be negative",
            ),
            (
                LocalAIConfig(
                    provider="ollama",
                    base_url="http://local",
                    model="m",
                    max_tokens=0,
                ),
                "max_tokens must be positive",
            ),
        ]

        for config, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(LocalAIConfigError, message):
                    config.validate({"ollama"})

    def test_config_validation_rejects_unregistered_provider(self):
        config = LocalAIConfig(
            provider="unknown",
            base_url="http://local",
            model="m",
        )

        with self.assertRaisesRegex(LocalAIConfigError, "provider is not registered"):
            config.validate({"ollama"})

    def test_request_validation_rejects_invalid_core_fields(self):
        cases = [
            (
                LocalAIRequest("", "m", "REQ-1", "OBJ-1"),
                "prompt must be non-empty",
            ),
            (
                LocalAIRequest("prompt", "", "REQ-1", "OBJ-1"),
                "model must be explicit",
            ),
            (
                LocalAIRequest("prompt", "m", "", "OBJ-1"),
                "request_id must be explicit",
            ),
            (
                LocalAIRequest("prompt", "m", "REQ-1", ""),
                "objective_ref must be explicit",
            ),
            (
                LocalAIRequest("prompt", "m", "REQ-1", "OBJ-1", max_tokens=0),
                "max_tokens must be positive",
            ),
            (
                LocalAIRequest("prompt", "m", "REQ-1", "OBJ-1", timeout_seconds=0),
                "timeout_seconds must be positive",
            ),
        ]

        for request, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    request.validate()

    def test_ollama_response_normalization_is_provider_neutral(self):
        provider = OllamaProvider()
        request = LocalAIRequest(
            prompt="hello",
            model="configured-model",
            request_id="REQ-1",
            objective_ref="OBJ-1",
        )
        config = LocalAIConfig(
            provider="ollama",
            base_url="http://localhost:11434/",
            model="configured-model",
        )

        response = provider.normalize_response(
            {"response": "hello back", "done": True, "model": "runtime-model"},
            request,
            config,
            "http://localhost:11434/api/generate",
            12,
        )

        self.assertEqual(response.request_id, "REQ-1")
        self.assertEqual(response.provider, "ollama")
        self.assertEqual(response.model, "runtime-model")
        self.assertEqual(response.content, "hello back")
        self.assertEqual(response.status, "complete")
        self.assertEqual(response.finish_reason, "done")
        self.assertEqual(
            response.diagnostics["endpoint_ref"],
            "http://localhost:11434/api/generate",
        )
        self.assertNotIn("confidence", response.diagnostics)
        self.assertNotIn("score", response.diagnostics)
        self.assertNotIn("authority", response.diagnostics)
        self.assertNotIn("vote_weight", response.diagnostics)

    def test_ollama_response_normalization_rejects_invalid_payload(self):
        provider = OllamaProvider()
        request = LocalAIRequest("prompt", "model", "REQ-1", "OBJ-1")
        config = LocalAIConfig(
            provider="ollama",
            base_url="http://localhost:11434",
            model="model",
        )

        with self.assertRaisesRegex(ValueError, "missing string response"):
            provider.normalize_response({}, request, config, "endpoint", 1)


if __name__ == "__main__":
    unittest.main()
