# Provider Implementation Guide

## Purpose

Guide implementation of new Local AI providers while preserving provider neutrality, `LocalAIManager` ownership, and SAFE bridge compatibility.

---

## Step 1 - Confirm Architecture Fit

Before writing code, confirm the provider can be represented through the existing `LocalAIProvider` interface:

- `name()`
- `validate_config(config)`
- `check_connection(config)`
- `generate(request, config)`

Do not add provider-specific public APIs.

---

## Step 2 - Create Provider Adapter

Create a provider adapter module inside the Local AI subsystem.

The adapter owns only provider-specific transport and response mapping.

It must not:

- rank providers;
- alter confidence;
- alter scores;
- alter authority;
- alter vote weight;
- modify governance state;
- call LOCKED components.

---

## Step 3 - Implement Health Check

Health checks must return `ConnectionCheck`.

Health diagnostics should include model availability and model count when the provider exposes model discovery.

Health status is operational metadata only.

---

## Step 4 - Implement Request Mapping

Map `LocalAIRequest` into the provider-specific request body.

The adapter must call `request.validate()` before transport.

Provider defaults should come from `LocalAIConfig` and registry metadata, not from runtime callers.

---

## Step 5 - Normalize Response

Normalize provider payloads into `LocalAIResponse`.

Required normalized fields:

- `request_id`
- `provider`
- `model`
- `content`
- `status`
- `latency_ms`
- `usage`
- `finish_reason`
- `diagnostics`

---

## Step 6 - Register Provider

Add a `ProviderRegistration` entry with:

- provider name;
- factory;
- default base URL;
- default model;
- implementation status;
- notes;
- capabilities.

Capabilities must be operational metadata only.

---

## Step 7 - Add Contract Test

Create a `ProviderContractCase` for the provider and run the shared contract.

Preferred pattern:

```python
class TestNewProviderContract(unittest.TestCase, LocalAIProviderContractMixin):
    provider_contract_case = NEW_PROVIDER_CASE
    provider_registration = get_registration("new_provider")
```

Do not add provider-specific exceptions to the contract.

---

## Step 8 - Run Verification

Required command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover tests
```

Provider certification requires a green full regression suite.

---

## Step 9 - Complete Certification Checklist

Complete `PROVIDER_CERTIFICATION_CHECKLIST.md` for the provider before requesting acceptance.

---

## Completion Standard

The provider is ready for review when it can be selected by configuration through `LocalAIManager` and passes the shared provider contract suite without Local AI architecture changes.
