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

from local_ai import LocalAIConfig, get_registration  # noqa: E402
from local_ai.lmstudio import LMStudioProvider  # noqa: E402
from local_ai.ollama import OllamaProvider  # noqa: E402
from tests.provider_contract import (  # noqa: E402
    ProviderContractCase,
    assert_provider_contract,
    assert_provider_registration_contract,
)


OLLAMA_CASE = ProviderContractCase(
    provider_name="ollama",
    provider_factory=OllamaProvider,
    config=LocalAIConfig(
        provider="ollama",
        base_url="http://localhost:11434",
        model="contract-model",
        timeout_seconds=3,
        temperature=0,
        max_tokens=32,
    ),
    health_payload={
        "models": [
            {"name": "contract-model"},
            {"name": "other-model"},
        ],
    },
    generation_payload={
        "model": "contract-model",
        "response": "ollama contract response",
        "done": True,
    },
    invalid_generation_payload={"done": True},
    health_path="/api/tags",
    generation_path="/api/generate",
    expected_content="ollama contract response",
    expected_finish_reason="done",
)


LMSTUDIO_CASE = ProviderContractCase(
    provider_name="lmstudio",
    provider_factory=LMStudioProvider,
    config=LocalAIConfig(
        provider="lmstudio",
        base_url="http://localhost:1234",
        model="contract-model",
        timeout_seconds=3,
        temperature=0,
        max_tokens=32,
    ),
    health_payload={
        "data": [
            {"id": "contract-model"},
            {"id": "other-model"},
        ],
    },
    generation_payload={
        "model": "contract-model",
        "choices": [
            {
                "message": {"content": "lmstudio contract response"},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 1, "completion_tokens": 2},
    },
    invalid_generation_payload={"choices": []},
    health_path="/v1/models",
    generation_path="/v1/chat/completions",
    expected_content="lmstudio contract response",
    expected_finish_reason="stop",
)


class TestPhase2AProviderContract(unittest.TestCase):
    def test_ollama_satisfies_provider_contract(self):
        assert_provider_contract(self, OLLAMA_CASE)

    def test_lmstudio_satisfies_provider_contract(self):
        assert_provider_contract(self, LMSTUDIO_CASE)

    def test_registered_providers_declare_capabilities_without_authority_semantics(self):
        for provider_name in ("ollama", "lmstudio"):
            with self.subTest(provider=provider_name):
                assert_provider_registration_contract(
                    self,
                    get_registration(provider_name),
                )


if __name__ == "__main__":
    unittest.main()
