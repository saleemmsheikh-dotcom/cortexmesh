# Ollama Adapter

## Status

INITIAL ADAPTER DESIGN

## Purpose

Define the first Local AI provider adapter for Ollama while preserving provider-independent caller behavior.

## Provider Boundary

All Ollama-specific behavior is contained in `OllamaProvider`.

No Ollama-specific request fields, response fields, endpoint paths, model naming assumptions, or connection behavior may leak into `LocalAIClient` or future provider callers.

## Adapter Responsibilities

- validate Ollama configuration;
- check local provider availability;
- translate `LocalAIRequest` into an Ollama-compatible request;
- submit generation requests to the configured Ollama endpoint;
- normalize Ollama responses into `LocalAIResponse`;
- record provider diagnostics for verification evidence;
- surface connection, timeout, model, and response errors as traceable errors.

## Configuration Inputs

Required:

- provider: `ollama`
- base URL
- model
- timeout seconds

Optional:

- temperature
- max tokens
- system prompt
- request metadata

## Connection Verification

The adapter must support a non-destructive connection check.

The connection check records:

- provider name;
- configured base URL;
- configured model;
- check timestamp;
- transport status;
- response status;
- failure reason where applicable.

## LM Studio Compatibility Constraint

`OllamaProvider` shall not define the shared Local AI contract.

The shared contract belongs to `LOCAL_AI_PROVIDER_INTERFACE.md`, so an LM Studio adapter can reuse the same request, response, configuration, and verification model without copying Ollama-specific logic.

## Error Handling

Adapter errors must include:

- request identifier where available;
- provider;
- model;
- endpoint reference;
- error category;
- retryability where known;
- evidence record reference when recorded.

Error categories:

- configuration invalid;
- provider unavailable;
- model unavailable;
- timeout;
- invalid provider response;
- generation failed;
- verification failed.

## Initial Acceptance Criteria

- Provider-specific logic remains isolated.
- Configuration validation fails fast.
- Connection verification produces a record.
- Generation output is normalized.
- Errors are traceable.
- No LOCKED component is modified.
