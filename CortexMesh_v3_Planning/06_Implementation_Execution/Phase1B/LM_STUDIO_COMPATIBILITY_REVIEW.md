# LM Studio Compatibility Review

## Review ID

PHASE1B-LMSTUDIO-COMPAT-001

## Date

2026-07-06

## Purpose

Assess whether LM Studio can be added as a Phase 1B Local AI provider without changing the existing Local AI provider interface.

This is a design compatibility review only.

No LM Studio adapter is implemented by this document.

## Scope

Reviewed:

- `local_ai/provider.py`
- `local_ai/config.py`
- `local_ai/ollama.py`
- `agents/local_ai_bridge.py`
- `agents/local_solver.py`

Out of scope:

- LM Studio adapter implementation
- Runtime endpoint testing
- LOCKED component modification
- Scoring, authority, contract, snapshot, or ExternalRunner changes

## Existing Provider Interface

The current provider contract defines:

- `LocalAIConfig`
- `LocalAIRequest`
- `LocalAIResponse`
- `ConnectionCheck`
- `LocalAIProvider`

The required provider methods are:

```text
name()
validate_config(config)
check_connection(config)
generate(request, config)
```

The interface separates:

- provider identity;
- endpoint configuration;
- model name;
- request prompt;
- optional system prompt;
- generation parameters;
- response content;
- usage;
- diagnostics;
- connection status.

## LM Studio Compatibility Assessment

LM Studio can be represented through the existing interface.

Expected mapping:

| CortexMesh Field | LM Studio Mapping |
| ---------------- | ----------------- |
| `provider` | `lmstudio` |
| `base_url` | Local LM Studio server base URL |
| `model` | LM Studio loaded model identifier |
| `prompt` | User message content |
| `system_prompt` | System message content |
| `temperature` | Chat completion temperature |
| `max_tokens` | Chat completion max token value |
| `timeout_seconds` | HTTP request timeout |
| `provider_options` | Endpoint path and adapter-specific options |
| `content` | Normalized assistant message content |
| `usage` | Provider usage object when available |
| `finish_reason` | Choice finish reason when available |
| `diagnostics` | Endpoint reference, status, response shape metadata |

Likely endpoint mapping:

```text
provider_options.chat_completions_path = /v1/chat/completions
```

Likely connection check mapping:

```text
GET /v1/models
```

## Interface Change Assessment

Result: NO PROVIDER INTERFACE CHANGE REQUIRED

The existing interface is sufficient for LM Studio because:

- chat-completion style request bodies can be built inside an adapter;
- response normalization can be contained inside an adapter;
- provider-specific endpoint paths can use `provider_options`;
- request and response metadata fields are already generic;
- provenance can continue to record provider/model/request diagnostics without becoming authoritative.

## Adapter Requirements

An eventual LM Studio adapter should:

1. Implement `LocalAIProvider`.
2. Validate `provider == "lmstudio"`.
3. Use `LocalAIConfig.normalized_base_url`.
4. Build a chat-completions request body from `LocalAIRequest`.
5. Normalize response content from `choices[0].message.content`.
6. Preserve usage and finish reason when available.
7. Record endpoint reference in diagnostics.
8. Return `LocalAIResponse`.
9. Never assign confidence, rank, authority, or governance weight based on provider/model identity.

## LOCKED Component Impact

Expected LOCKED component impact: NONE

LM Studio implementation should not require changes to:

- `orchestrator.py`
- `competition/scorer.py`
- `agents/authority.py`
- `core/contracts.py`
- `core/external_runner.py`
- `governance/snapshot.py`

## Risks

LM Studio compatibility risks remain adapter-local:

- OpenAI-compatible response shape may vary by LM Studio version.
- Model listing availability may vary by local configuration.
- Local endpoint availability remains environment-specific.
- Streaming mode should remain disabled or normalized before use.

These risks do not require provider interface changes.

## Recommendation

Implementation may proceed through a new non-LOCKED LM Studio adapter using the existing provider interface.

No architecture, scoring, authority, contract, snapshot, orchestration, or ExternalRunner changes are required for compatibility.

## Result

PASS FOR DESIGN COMPATIBILITY

LM Studio can proceed to implementation planning without changing the Local AI provider interface.
