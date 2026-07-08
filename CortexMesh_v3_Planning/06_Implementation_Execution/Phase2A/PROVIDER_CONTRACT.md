# Provider Contract

## Milestone

Phase 2A M3 - Shared Provider Contract Test Suite

## Status

IMPLEMENTED

---

## Purpose

Define the provider-independent behavioral contract that every `LocalAIProvider` implementation must satisfy.

The contract exists to ensure local AI providers remain interchangeable through the existing provider-neutral architecture.

---

## Contract Scope

Each provider must satisfy identical requirements for:

1. initialization;
2. configuration validation;
3. health checks;
4. model discovery diagnostics;
5. request validation;
6. response normalization;
7. diagnostics;
8. error handling;
9. capability declaration;
10. provenance fields.

---

## Required Provider Behavior

### Initialization

Providers expose a stable provider name through `name()`.

### Configuration Validation

Providers validate `LocalAIConfig` using the provider-neutral configuration model.

Invalid provider names, missing base URLs, missing models, and invalid limits must fail cleanly.

### Health

Providers return `ConnectionCheck` for health checks.

Health checks must include:

- provider;
- model;
- endpoint reference;
- ok status;
- status string;
- latency;
- diagnostics;
- optional error.

### Model Discovery

Model discovery must be reported as diagnostics only.

Model availability and model counts must not affect authority, score, confidence, rank, or vote weight.

### Request Validation

Providers must validate `LocalAIRequest` before generation.

Invalid requests must fail before transport behavior is required.

### Response Normalization

Provider-specific payloads must normalize into `LocalAIResponse`.

The normalized response must include:

- request ID;
- provider;
- model;
- content;
- status;
- latency;
- usage mapping;
- finish reason;
- diagnostics.

### Diagnostics

Diagnostics must be actionable and provider-neutral.

Diagnostics must not include decision-affecting fields such as:

- confidence;
- score;
- authority;
- rank;
- vote weight.

### Error Handling

Health-check transport failures must return failed health results.

Invalid generation payloads must fail cleanly.

### Capability Declaration

Provider capabilities are metadata only.

Capabilities must not imply authority, ranking, scoring, confidence, or governance status.

### Provenance Fields

Providers must return the fields required for provenance construction:

- provider;
- model;
- request ID;
- endpoint reference.

---

## Current Providers

The shared contract suite applies to:

- Ollama;
- LM Studio.

Both providers are tested through the same contract harness without provider-specific test exceptions.

---

## Constraints

- No `LocalAIProvider` interface changes.
- No `LocalAIManager` API changes.
- No LOCKED component modifications.
- No provider ranking.
- No runtime orchestration changes.

---

## Verification Artifact

Implementation evidence is recorded in:

`VERIFICATION_EVIDENCE_004_PROVIDER_CONTRACT.md`
