# LM Studio Adapter Design

Status: READY FOR IMPLEMENTATION

---

## 1. Purpose

Define the LM Studio Local AI provider adapter design before implementation.

The design confirms that LM Studio can be added through the existing Phase 1B Local AI architecture without changing public contracts.

---

## 2. Scope

This design covers:

- adapter placement;
- endpoint assumptions;
- request mapping;
- response normalization;
- health checks;
- capability declarations;
- diagnostics;
- telemetry;
- provenance rules;
- verification plan.

Implementation is not included in this document.

---

## 3. Non-Goals

This design does not:

- implement LM Studio;
- modify `LocalAIProvider`;
- modify `LocalAIManager`;
- modify runtime orchestration;
- modify LOCKED components;
- add provider ranking;
- add scoring, confidence, authority, or vote-weight effects;
- add cloud provider support;
- add MCP support.

---

## 4. Architectural Rule

`LocalAIManager` shall be the sole public runtime entry point into the Local AI subsystem.

Runtime callers must not call:

- provider registries directly;
- capability registries directly;
- telemetry buffers directly;
- provider adapters directly.

Provider registries, capability registries, telemetry helpers, and adapters remain internal implementation details of the Local AI subsystem.

This rule prevents runtime callers from becoming provider-aware and keeps provider/model identity as provenance only.

---

## 5. LM Studio Endpoint Assumptions

LM Studio is assumed to expose an OpenAI-compatible local API.

Initial endpoint assumptions:

- `GET /v1/models`
- `POST /v1/chat/completions`

Default local base URL remains:

```text
http://localhost:1234
```

Endpoint paths should be overridable through provider options if needed.

---

## 6. Request Mapping

`LocalAIRequest` maps to LM Studio chat completion input.

Mapping:

| LocalAIRequest | LM Studio Request |
| -------------- | ----------------- |
| `model` | `model` |
| `system_prompt` | `messages[0].content` with role `system` |
| `prompt` | final message content with role `user` |
| `temperature` | `temperature` |
| `max_tokens` | `max_tokens` |
| `timeout_seconds` | transport timeout |
| `metadata` | diagnostics only; not sent unless explicitly safe |

If `system_prompt` is absent, only a user message is sent.

The adapter must not infer confidence, authority, score, rank, or vote weight from the request.

---

## 7. Response Normalization

LM Studio responses normalize into `LocalAIResponse`.

Expected response source:

```text
choices[0].message.content
```

Mapping:

| LM Studio Response | LocalAIResponse |
| ------------------ | --------------- |
| response content | `content` |
| model | `model` |
| completion status | `status` |
| latency measurement | `latency_ms` |
| finish reason | `finish_reason` |
| usage metadata | `usage` |
| endpoint reference | `diagnostics.endpoint_ref` |

Invalid or missing content must fail cleanly with a provider-local error.

---

## 8. Health Check Behavior

The adapter health check should call:

```text
GET /v1/models
```

Health check output must normalize to `ConnectionCheck`.

Expected behavior:

- return `ok=True` when the endpoint responds successfully;
- report model availability when discoverable;
- return `ok=False` with an actionable error when unavailable;
- include endpoint reference and latency;
- never rank providers.

---

## 9. Capability Declarations

LM Studio remains declared through provider registration.

Expected capabilities:

- `chat_completion`
- `text_generation`
- `health_check`

Capability declarations are metadata only.

Capabilities do not imply provider quality, confidence, score, authority, rank, vote weight, or governance status.

---

## 10. Diagnostics and Telemetry

Diagnostics should include:

- provider name;
- model;
- endpoint reference;
- status;
- latency;
- finish reason;
- usage metadata when available;
- safe error details.

Telemetry events may be created through the existing observability framework:

- provider lifecycle;
- health check;
- request timing;
- response timing;
- capability discovery.

Telemetry remains informational only.

---

## 11. Error Handling

The adapter should fail cleanly for:

- connection refusal;
- timeout;
- HTTP error;
- malformed JSON;
- missing `choices`;
- missing message content;
- unavailable model;
- invalid configuration.

Errors should be actionable but must avoid leaking authority, score, confidence, rank, or vote-weight semantics.

---

## 12. Provenance-Only Provider and Model Metadata

Provider and model identity are provenance only.

LM Studio metadata must not affect:

- solver confidence;
- scoring;
- authority;
- ranking;
- vote weight;
- governance decisions.

---

## 13. LOCKED Component Boundary

LM Studio implementation must remain inside the non-LOCKED Phase 1B Local AI subsystem.

No changes are authorized for:

- `orchestrator.py`
- `competition/scorer.py`
- `agents/authority.py`
- `core/contracts.py`
- `core/external_runner.py`
- `governance/snapshot.py`

Runtime orchestration integration remains out of scope.

---

## 14. Verification Plan

Implementation verification should include:

1. `py_compile` for Local AI modules and tests.
2. Unit tests for adapter configuration validation.
3. Unit tests for request mapping.
4. Unit tests for response normalization.
5. Unit tests for malformed response handling.
6. Unit tests for health check success and failure.
7. Registry tests confirming LM Studio is implemented only after adapter addition.
8. Manager tests confirming selection remains configuration and availability driven.
9. Provenance tests confirming no confidence, score, authority, rank, or vote-weight leakage.
10. Full regression suite.

Live endpoint verification should be recorded separately because local LM Studio availability is environment-dependent.

---

## 15. Exit Criteria for Implementation

LM Studio implementation may be considered complete when:

- `LocalAIProvider` remains unchanged;
- `LocalAIManager` remains the public runtime entry point;
- LM Studio adapter implements the existing provider contract;
- provider registration is updated from placeholder to implemented;
- capability declarations remain metadata only;
- health checks return structured diagnostics;
- responses normalize to `LocalAIResponse`;
- telemetry remains informational only;
- no LOCKED components are modified;
- full regression passes;
- implementation evidence is recorded.

---

## Design Conclusion

LM Studio can be implemented through the existing Local AI architecture without changing public contracts.

Design status:

```text
READY FOR IMPLEMENTATION
```
