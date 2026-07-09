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

from local_ai import LocalAIConfig, LocalAIRequest  # noqa: E402
from local_ai.reference_provider import ReferenceProvider  # noqa: E402
from local_ai.registry import ProviderRegistration  # noqa: E402
from tests.provider_contract import ProviderContractCase  # noqa: E402
from tests.provider_contract_mixin import LocalAIProviderContractMixin  # noqa: E402


REFERENCE_CASE = ProviderContractCase(
    provider_name="reference",
    provider_factory=ReferenceProvider,
    config=LocalAIConfig(
        provider="reference",
        base_url="reference://local",
        model="reference-model",
        timeout_seconds=3,
        temperature=0,
        max_tokens=32,
    ),
    health_payload={
        "models": [
            {"name": "reference-model"},
            {"name": "reference-model-secondary"},
        ]
    },
    generation_payload={
        "model": "reference-model",
        "content": "deterministic reference response",
        "finish_reason": "complete",
    },
    invalid_generation_payload={"finish_reason": "complete"},
    health_path="/models",
    generation_path="/generate",
    expected_content="deterministic reference response",
    expected_finish_reason="complete",
)

REFERENCE_REGISTRATION = ProviderRegistration(
    name="reference",
    factory=ReferenceProvider,
    default_base_url="reference://local",
    default_model="reference-model",
    status="example",
    notes="Non-production provider example for PDK certification.",
    capabilities=("text_generation", "health_check"),
)


class TestPhase2AReferenceProvider(
    LocalAIProviderContractMixin,
    unittest.TestCase,
):
    provider_contract_case = REFERENCE_CASE
    provider_registration = REFERENCE_REGISTRATION

    def test_deterministic_behavior_without_external_io(self):
        provider = ReferenceProvider()
        request = LocalAIRequest(
            prompt="example",
            model="reference-model",
            request_id="REFERENCE-001",
            objective_ref="PHASE2A-M5",
        )

        first = provider.generate(request, REFERENCE_CASE.config)
        second = provider.generate(request, REFERENCE_CASE.config)

        self.assertEqual(first.content, "Reference response: example")
        self.assertEqual(first.content, second.content)
        self.assertEqual(first.provider, "reference")
        self.assertTrue(first.diagnostics["reference_only"])
        for forbidden in ("rank", "score", "authority", "confidence", "vote_weight"):
            self.assertNotIn(forbidden, first.diagnostics)

    def test_reference_provider_is_not_in_runtime_registry(self):
        from local_ai.registry import registered_provider_names

        self.assertNotIn("reference", registered_provider_names())


if __name__ == "__main__":
    unittest.main()
