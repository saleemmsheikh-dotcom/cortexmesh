# Local AI Provider Interface

## Status

INITIAL INTERFACE CONTRACT

## Purpose

Define the provider-independent contract that all Local AI adapters must satisfy.

## Interface Boundary

The provider interface is the only boundary exposed to Local AI callers.

Provider adapters may implement provider-specific request formatting, response parsing, retries, and health checks internally.

Provider-specific payloads must not cross the interface boundary except inside diagnostic evidence.

## Core Types

### LocalAIRequest

Required fields:

- `prompt`
- `model`
- `request_id`
- `objective_ref`

Optional fields:

- `system_prompt`
- `temperature`
- `max_tokens`
- `timeout_seconds`
- `metadata`

Validation rules:

- `prompt` must be non-empty.
- `model` must be explicit.
- `request_id` must be stable for traceability.
- `objective_ref` must identify the originating work item or verification event.
- provider name must not be accepted as confidence evidence.

### LocalAIResponse

Required fields:

- `request_id`
- `provider`
- `model`
- `content`
- `status`
- `latency_ms`

Optional fields:

- `usage`
- `finish_reason`
- `raw_response_ref`
- `diagnostics`
- `warnings`

Validation rules:

- `provider` identifies provenance only.
- `content` must not be treated as verified evidence until passed through the evidence publication process.
- errors must produce traceable records rather than silent fallback.

### LocalAIProvider

Required operations:

- `name()`
- `validate_config(config)`
- `check_connection(config)`
- `generate(request, config)`
- `normalize_response(raw_response, request)`

Required behavior:

- return provider-independent responses;
- preserve request identifiers;
- preserve model identifiers;
- record error context;
- avoid mutation of governance artifacts;
- avoid direct dependency on LOCKED components.

## Adapter Acceptance Criteria

An adapter is acceptable when:

- it implements the full provider interface;
- provider-specific logic is contained in the adapter;
- connection verification has a recorded evidence artifact;
- invalid configuration fails before generation;
- provider errors are surfaced as traceable errors;
- output provenance includes provider, model, endpoint reference, and request identifier;
- no confidence, rank, vote, or authority is derived from provider identity.
