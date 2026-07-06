# Local AI Configuration Model

## Status

INITIAL CONFIGURATION MODEL

## Purpose

Define the provider-independent configuration model for Local AI integration.

## Configuration Object

Required fields:

- `provider`
- `base_url`
- `model`
- `timeout_seconds`

Optional fields:

- `temperature`
- `max_tokens`
- `system_prompt`
- `metadata`

## Provider Values

Initial authorized provider:

- `ollama`

Designed compatibility provider:

- `lm_studio`

Future providers may be added only by adapter extension and configuration registration.

## Validation Rules

- `provider` must match a registered provider adapter.
- `base_url` must be explicit.
- `model` must be explicit.
- `timeout_seconds` must be positive.
- provider-specific options must be namespaced under adapter-owned configuration.
- configuration must not encode governance authority.
- configuration must not assign confidence, ranking, voting, or decision authority.

## Traceability Requirements

Every execution using Local AI configuration must preserve:

- configuration reference;
- provider;
- model;
- endpoint reference;
- request identifier;
- verification evidence reference where applicable.

## Example

```text
provider: ollama
base_url: http://localhost:11434
model: local-model-name
timeout_seconds: 30
temperature: 0.2
max_tokens: 1024
```

The example is illustrative only. Actual values must be verified in the local environment before use.
