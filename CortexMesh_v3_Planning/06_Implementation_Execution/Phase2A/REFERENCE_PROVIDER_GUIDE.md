# Reference Provider Guide

## Status

CERTIFIED EXAMPLE

## Purpose

`ReferenceProvider` is a deterministic, non-production example showing how to
implement and certify a `LocalAIProvider` using the Phase 2A Provider
Development Kit.

It is not a runtime backend and is intentionally absent from the production
provider registry.

## Implementation Pattern

The provider demonstrates:

- the unchanged `LocalAIProvider` contract;
- configuration validation;
- deterministic health and model discovery;
- request validation;
- normalized `LocalAIResponse` output;
- explicit capability declaration;
- actionable, informational diagnostics;
- provenance-only provider and model metadata; and
- clean error behavior.

## Certification

The test class uses `LocalAIProviderContractMixin` and supplies only:

- a provider-neutral `ProviderContractCase`; and
- a standalone `ProviderRegistration`.

No provider-specific contract exception is used. The same shared checks used
for Ollama and LM Studio certify the reference implementation.

## Copying the Example

1. Copy `local_ai/reference_provider.py` into a provider-specific adapter.
2. Replace deterministic request behavior with adapter-local transport.
3. Keep provider-specific behavior inside the adapter.
4. Declare capabilities as metadata.
5. Add a contract case using `LocalAIProviderContractMixin`.
6. Complete `PROVIDER_CERTIFICATION_CHECKLIST.md`.
7. Register the provider only after production authorization and verification.

## Architectural Boundaries

The reference provider:

- does not modify `LocalAIProvider` or `LocalAIManager`;
- does not participate in runtime selection;
- does not modify the SAFE bridge or orchestration;
- does not affect confidence, rank, score, authority, or vote weight; and
- does not modify any LOCKED component.
