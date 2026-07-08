"""Unittest mixin for certifying LocalAIProvider implementations."""

from __future__ import annotations

from tests.provider_contract import (
    ProviderContractCase,
    assert_provider_contract,
    assert_provider_registration_contract,
)


class LocalAIProviderContractMixin:
    """Mixin for provider adapter certification tests.

    Subclasses must define:

    - ``provider_contract_case`` as a ``ProviderContractCase``.
    - ``provider_registration`` as the provider's registry entry.

    The mixin intentionally performs the same provider-neutral checks for every
    adapter and does not allow provider-specific exceptions.
    """

    provider_contract_case: ProviderContractCase | None = None
    provider_registration = None

    def test_provider_satisfies_local_ai_contract(self):
        self.assertIsNotNone(self.provider_contract_case)
        assert_provider_contract(self, self.provider_contract_case)

    def test_provider_registration_declares_capabilities_only(self):
        self.assertIsNotNone(self.provider_registration)
        assert_provider_registration_contract(self, self.provider_registration)
