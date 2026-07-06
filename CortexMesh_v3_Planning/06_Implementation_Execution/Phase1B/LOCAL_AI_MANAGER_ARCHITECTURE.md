# Local AI Manager Architecture

## Document ID

PHASE1B-M4.1-LOCAL-AI-MANAGER-ARCHITECTURE

## Status

PROPOSED

## Date

2026-07-07

## Purpose

Define the architecture for a provider-neutral `LocalAIManager` before implementation.

The manager is intended to coordinate Local AI provider configuration, selection, health checks, diagnostics, and provenance while preserving the existing `LocalAIProvider` interface.

This document is design-only.

No manager code is implemented by this document.

## Responsibilities

The `LocalAIManager` is responsible for:

- loading Local AI configuration;
- reading the provider registry;
- selecting an explicit provider when configured;
- auto-selecting from configured provider options when requested;
- creating provider-specific configuration objects;
- running non-destructive health checks;
- exposing provider capability metadata;
- invoking provider generation through the existing `LocalAIProvider` interface;
- normalizing diagnostics around provider selection and execution;
- preserving provider/model identity as provenance only.

## Non-Goals

The `LocalAIManager` shall not:

- modify or replace the `LocalAIProvider` interface;
- implement a specific provider adapter;
- implement LM Studio;
- change orchestration behavior;
- change scoring behavior;
- change authority behavior;
- assign confidence;
- assign rank;
- assign vote weight;
- make governance decisions;
- select providers based on perceived reasoning quality;
- write to LOCKED components.

## Relationship to LocalAIProvider

`LocalAIManager` sits above provider adapters.

It uses the existing provider interface:

```text
name()
validate_config(config)
check_connection(config)
generate(request, config)
```

Provider adapters remain responsible for provider-specific transport, payload formatting, response normalization, and endpoint behavior.

The manager remains provider-neutral and must not contain provider-specific request or response parsing logic.

## Provider Registry Usage

The manager shall use the Phase 1B provider registry as the source of provider availability metadata.

The registry may contain:

- implemented providers;
- placeholder providers;
- default base URLs;
- default model names;
- provider status;
- adapter notes.

Current expected registry state:

```text
ollama    implemented
lmstudio  placeholder
```

The manager may instantiate implemented providers only.

Placeholder providers must fail cleanly until an adapter exists.

## Configuration Loading

Configuration may be loaded from environment variables, a future local config file, or an injected configuration object.

Current environment-driven configuration should remain supported:

```text
CORTEX_LOCAL_AI_ENABLED
CORTEX_LOCAL_AI_PROVIDER
CORTEX_LOCAL_AI_PROVIDER_OPTIONS
CORTEX_LOCAL_AI_BASE_URL
CORTEX_LOCAL_AI_MODEL
CORTEX_LOCAL_AI_TIMEOUT
CORTEX_LOCAL_AI_TEMPERATURE
CORTEX_LOCAL_AI_MAX_TOKENS
```

Provider-specific settings should remain inside `provider_options` rather than changing the provider interface.

## Provider Selection

The manager shall support two selection modes.

### Explicit Selection

When a provider is explicitly configured, the manager shall select that provider if implemented.

Unknown providers must fail cleanly.

Registered but unimplemented providers must fail cleanly.

### Auto Selection

When configured with:

```text
CORTEX_LOCAL_AI_PROVIDER=auto
```

the manager shall inspect configured provider options and select the first implemented provider that passes a health check.

Auto-selection is an availability mechanism only.

It must not imply quality, reliability, confidence, priority, rank, or governance authority.

## Health Checks

The manager shall support non-destructive health checks through provider adapters.

Health checks may report:

- provider;
- model;
- endpoint reference;
- availability;
- latency;
- error;
- diagnostics.

Health checks shall not invoke scoring, authority, governance, or orchestration logic.

## Capability Discovery

The manager may expose provider capability metadata for diagnostics and planning.

Capability discovery may include:

- implemented provider names;
- placeholder provider names;
- configured provider options;
- selected provider;
- default endpoint;
- default model;
- known adapter status.

Capability discovery must not be treated as evidence of output quality or governance readiness.

## Diagnostics

The manager shall produce diagnostics for:

- selected provider;
- selection mode;
- provider options;
- configuration source;
- endpoint reference;
- health check outcome;
- generation status;
- adapter errors.

Diagnostics are operational evidence.

They are not scoring input unless a future Board-approved architecture explicitly says otherwise.

## Telemetry

The manager may record local telemetry such as:

- request ID;
- selected provider;
- model;
- latency;
- status;
- finish reason;
- endpoint reference.

Telemetry must not include hidden ranking, confidence, or vote-weight calculations.

Telemetry must preserve privacy and avoid leaking sensitive prompts or outputs unless explicitly recorded as an approved evidence artifact.

## Error Handling

The manager shall fail cleanly for:

- unknown provider;
- registered but unimplemented provider;
- invalid configuration;
- unavailable endpoint;
- failed health check;
- invalid provider response;
- provider timeout.

Errors should include enough diagnostics for evidence review while avoiding sensitive host-path or credential leakage.

## Provenance Rules

Provider/model identity is provenance only.

The manager may record:

```text
provider
model
selected_provider
provider_selection
provider_options
request_id
endpoint_ref
status
latency_ms
finish_reason
```

The manager shall not map provider/model identity into:

- confidence;
- score;
- rank;
- vote weight;
- authority;
- trust;
- governance approval.

## LOCKED Component Boundaries

The manager shall remain outside LOCKED components.

It must not require changes to:

- `orchestrator.py`
- `competition/scorer.py`
- `agents/authority.py`
- `core/contracts.py`
- `core/external_runner.py`
- `governance/snapshot.py`

Any future integration touching those files requires explicit Board authorization.

## Future Provider Support

Future providers should be added by:

1. implementing a new adapter that satisfies `LocalAIProvider`;
2. registering the adapter in the provider registry;
3. adding provider-specific tests;
4. adding verification evidence;
5. preserving provenance-only provider identity.

The provider interface should remain stable unless evidence shows it cannot represent a required provider class.

## Future Runtime Integration Constraints

Future runtime integration shall remain constrained by:

- non-LOCKED implementation paths unless Board approval says otherwise;
- existing solver schema compatibility;
- explicit environment or config selection;
- provider-neutral manager behavior;
- provenance-only provider identity;
- no scoring/authority/confidence changes based on provider/model identity.

## Key Architecture Decisions

1. The manager coordinates providers but does not become a provider.
2. The provider registry remains the source of provider availability metadata.
3. Auto-selection is based on availability, not quality.
4. Provider identity remains provenance only.
5. The existing `LocalAIProvider` interface remains unchanged.
6. LM Studio remains unimplemented until separately authorized.
7. LOCKED components remain untouched.

## Result

READY FOR DESIGN REVIEW

The `LocalAIManager` architecture can proceed to implementation planning without changing LOCKED components or the existing provider interface.
