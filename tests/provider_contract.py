"""Reusable LocalAIProvider contract checks for Phase 2A."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Callable, Mapping
from unittest.mock import patch

from local_ai import LocalAIConfig, LocalAIProvider, LocalAIRequest
from local_ai.registry import ProviderRegistration


ProviderFactory = Callable[[], LocalAIProvider]


@dataclass(frozen=True)
class ProviderContractCase:
    """Provider fixture data for one shared contract run."""

    provider_name: str
    provider_factory: ProviderFactory
    config: LocalAIConfig
    health_payload: Mapping[str, Any]
    generation_payload: Mapping[str, Any]
    invalid_generation_payload: Mapping[str, Any]
    health_path: str
    generation_path: str
    expected_content: str
    expected_finish_reason: str


def assert_provider_contract(testcase, case: ProviderContractCase) -> None:
    """Assert one LocalAIProvider satisfies the provider-neutral contract."""

    provider = case.provider_factory()

    assert_initialization_contract(testcase, provider, case)
    assert_health_contract(testcase, provider, case)
    assert_request_validation_contract(testcase, provider, case)
    assert_response_normalization_contract(testcase, provider, case)
    assert_diagnostics_contract(testcase, provider, case)
    assert_error_handling_contract(testcase, provider, case)
    assert_provenance_fields_contract(testcase, provider, case)


def assert_initialization_contract(testcase, provider, case: ProviderContractCase) -> None:
    testcase.assertEqual(provider.name(), case.provider_name)
    provider.validate_config(case.config)

    wrong_provider_config = replace(case.config, provider=f"{case.provider_name}-wrong")
    with testcase.assertRaises(ValueError):
        provider.validate_config(wrong_provider_config)


def assert_health_contract(testcase, provider, case: ProviderContractCase) -> None:
    with patch.object(provider, "_request_json", return_value=case.health_payload):
        health = provider.check_connection(case.config)

    testcase.assertEqual(health.provider, case.provider_name)
    testcase.assertEqual(health.model, case.config.model)
    testcase.assertTrue(health.ok)
    testcase.assertEqual(health.status, "connected")
    testcase.assertGreaterEqual(health.latency_ms, 0)
    testcase.assertTrue(health.endpoint_ref.endswith(case.health_path))
    testcase.assertIn("model_available", health.diagnostics)
    testcase.assertIn("model_count", health.diagnostics)
    testcase.assertTrue(health.diagnostics["model_available"])
    testcase.assertEqual(health.diagnostics["model_count"], 2)


def assert_request_validation_contract(testcase, provider, case: ProviderContractCase) -> None:
    invalid_request = LocalAIRequest(
        prompt="",
        model=case.config.model,
        request_id=f"{case.provider_name}-REQ",
        objective_ref="PHASE2A-CONTRACT",
    )

    with patch.object(provider, "_request_json", return_value=case.generation_payload):
        with testcase.assertRaises(ValueError):
            provider.generate(invalid_request, case.config)


def assert_response_normalization_contract(testcase, provider, case: ProviderContractCase) -> None:
    request = _request(case)
    with patch.object(provider, "_request_json", return_value=case.generation_payload):
        response = provider.generate(request, case.config)

    testcase.assertEqual(response.request_id, request.request_id)
    testcase.assertEqual(response.provider, case.provider_name)
    testcase.assertEqual(response.model, case.config.model)
    testcase.assertEqual(response.content, case.expected_content)
    testcase.assertEqual(response.status, "complete")
    testcase.assertGreaterEqual(response.latency_ms, 0)
    testcase.assertEqual(response.finish_reason, case.expected_finish_reason)
    testcase.assertIsInstance(response.usage, Mapping)


def assert_diagnostics_contract(testcase, provider, case: ProviderContractCase) -> None:
    request = _request(case)
    with patch.object(provider, "_request_json", return_value=case.generation_payload):
        response = provider.generate(request, case.config)

    testcase.assertIn("endpoint_ref", response.diagnostics)
    testcase.assertTrue(response.diagnostics["endpoint_ref"].endswith(case.generation_path))
    testcase.assertNotIn("rank", response.diagnostics)
    testcase.assertNotIn("score", response.diagnostics)
    testcase.assertNotIn("authority", response.diagnostics)
    testcase.assertNotIn("confidence", response.diagnostics)
    testcase.assertNotIn("vote_weight", response.diagnostics)


def assert_error_handling_contract(testcase, provider, case: ProviderContractCase) -> None:
    with patch.object(provider, "_request_json", side_effect=RuntimeError("boom")):
        health = provider.check_connection(case.config)

    testcase.assertFalse(health.ok)
    testcase.assertEqual(health.status, "failed")
    testcase.assertIn("boom", health.error)

    request = _request(case)
    with patch.object(provider, "_request_json", return_value=case.invalid_generation_payload):
        with testcase.assertRaises(ValueError):
            provider.generate(request, case.config)


def assert_provenance_fields_contract(testcase, provider, case: ProviderContractCase) -> None:
    request = _request(case)
    with patch.object(provider, "_request_json", return_value=case.generation_payload):
        response = provider.generate(request, case.config)

    testcase.assertEqual(response.request_id, request.request_id)
    testcase.assertEqual(response.provider, case.provider_name)
    testcase.assertEqual(response.model, case.config.model)
    testcase.assertIn("endpoint_ref", response.diagnostics)


def assert_provider_registration_contract(
    testcase,
    registration: ProviderRegistration,
) -> None:
    """Assert registry declarations remain capability metadata only."""

    testcase.assertTrue(registration.implemented)
    testcase.assertTrue(registration.default_base_url)
    testcase.assertTrue(registration.default_model)
    testcase.assertIn("health_check", registration.capabilities)
    testcase.assertIn("text_generation", registration.capabilities)

    capability_text = " ".join(registration.capabilities).lower()
    testcase.assertNotIn("rank", capability_text)
    testcase.assertNotIn("score", capability_text)
    testcase.assertNotIn("authority", capability_text)
    testcase.assertNotIn("confidence", capability_text)
    testcase.assertNotIn("vote", capability_text)


def _request(case: ProviderContractCase) -> LocalAIRequest:
    return LocalAIRequest(
        prompt="Produce a provider contract response.",
        model=case.config.model,
        request_id=f"PHASE2A-{case.provider_name.upper()}-REQ",
        objective_ref="PHASE2A-PROVIDER-CONTRACT",
        system_prompt="Provider contract test.",
        temperature=0,
        max_tokens=32,
        timeout_seconds=case.config.timeout_seconds,
    )
