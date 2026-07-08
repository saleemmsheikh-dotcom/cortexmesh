# Provider Template

## Purpose

Provide a standard template for implementing and testing a new Local AI provider.

This is a reference template only. It does not modify the Local AI architecture.

---

## Adapter Skeleton

```python
class ExampleProvider:
    provider_name = "example"

    def name(self) -> str:
        return self.provider_name

    def validate_config(self, config: LocalAIConfig) -> None:
        config.validate({self.provider_name})

    def check_connection(self, config: LocalAIConfig) -> ConnectionCheck:
        self.validate_config(config)
        # Provider-specific non-destructive health check.
        # Return ConnectionCheck.

    def generate(self, request: LocalAIRequest, config: LocalAIConfig) -> LocalAIResponse:
        self.validate_config(config)
        request.validate()
        # Provider-specific request mapping and transport.
        # Return normalized LocalAIResponse.
```

---

## Registry Skeleton

```python
ProviderRegistration(
    name="example",
    factory=_example_factory,
    default_base_url="http://localhost:0000",
    default_model="example-model",
    notes="Implemented provider adapter.",
    capabilities=("text_generation", "health_check"),
)
```

---

## Contract Test Skeleton

```python
class TestExampleProviderContract(unittest.TestCase, LocalAIProviderContractMixin):
    provider_contract_case = EXAMPLE_PROVIDER_CASE
    provider_registration = get_registration("example")
```

---

## Required Fixture Data

Each provider contract case must define:

- provider name;
- provider factory;
- valid config;
- health payload;
- generation payload;
- invalid generation payload;
- health endpoint path;
- generation endpoint path;
- expected content;
- expected finish reason.

---

## Prohibited Additions

Provider implementations must not introduce:

- provider ranking;
- score effects;
- authority effects;
- confidence effects;
- vote-weight effects;
- governance effects;
- runtime orchestration changes;
- LOCKED component changes.

---

## Optional Code Template

An optional Python skeleton is available at:

`templates/provider_template.py`
