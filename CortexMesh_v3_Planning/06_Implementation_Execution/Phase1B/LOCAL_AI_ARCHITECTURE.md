# Local AI Architecture

## Status

ACTIVE PHASE 1B ARCHITECTURE

## Purpose

Define the Local AI integration architecture for Phase 1B without binding CortexMesh to any single provider.

## Traceability

| Source | Relevance |
| ------ | --------- |
| `AI005_SYSTEM_MODEL.md` | Provider independence |
| `AI007_AGENT_INTERACTION_MODEL.md` | Agent interaction boundaries |
| `AI011_SECURITY_TRUST_MODEL.md` | Trust does not derive from provider identity |
| `IMP001_IMPLEMENTATION_MAPPING.md` | Agent Adapter Interface and configuration requirements |
| `IMP002_INTERFACE_AND_CONTRACT_SPECIFICATION.md` | Interface validation and provider identity constraints |
| `IMP003_MODULE_DEPENDENCY_ARCHITECTURE.md` | Agent Adapter dependency boundaries |
| `IMP004_VERIFICATION_AND_TEST_ARCHITECTURE.md` | Verification evidence requirements |
| `IMP005_IMPLEMENTATION_ROADMAP_AND_EXECUTION_PLAN.md` | Phase 5 Agent Adapter and independent evidence capture |
| `GG-02_Board_Voting_and_Ratification_Rules_v1.0.md` | Procedural authority for Phase 1B authorization |

## Architecture Principles

- Provider abstraction first.
- Provider-specific behavior belongs only in provider adapters.
- Provider identity must not create authority, confidence, rank, vote weight, or final decision power.
- Configuration must be explicit, traceable, and reproducible.
- Connection verification must produce evidence without mutating ratified governance records.
- Local AI output is an agent output candidate, not a governance decision.

## Component Boundary

```text
LocalAIClient
    |
    v
LocalAIProvider interface
    |
    +-- OllamaProvider adapter
    |
    +-- LMStudio-compatible adapter (future)
    |
    +-- Additional provider adapters (future)
```

## Data Flow

1. A caller submits a provider-independent request to `LocalAIClient`.
2. `LocalAIClient` validates configuration and selects the configured provider adapter.
3. The provider adapter translates the request into provider-specific transport.
4. The provider adapter receives the provider response and normalizes it into a provider-independent response.
5. Verification records capture provider name, model reference, endpoint reference, request metadata, response metadata, errors, and timing.
6. Any downstream evidence publication must preserve provenance and must not infer confidence from provider identity.

## Architecture Decisions

| ID | Decision | Rationale |
| -- | -------- | --------- |
| LAI-AD-001 | Define a `LocalAIProvider` interface before provider implementation. | Prevent provider lock-in and keep Ollama-specific behavior isolated. |
| LAI-AD-002 | Use adapter-owned transport mapping. | Ollama and LM Studio can expose different request and response shapes without leaking into callers. |
| LAI-AD-003 | Normalize responses into a shared response object. | Downstream components should not parse provider-specific payloads. |
| LAI-AD-004 | Treat connection checks as verification evidence. | Supports traceability, repeatability, and audit requirements. |
| LAI-AD-005 | Keep Phase 1B runtime integration out of LOCKED components until separately authorized. | Preserves the LOCKED component governance boundary. |

## Non-Goals

- No modification of `orchestrator.py`.
- No modification of `core/external_runner.py`.
- No modification of `agents/authority.py`.
- No cloud provider implementation.
- No MCP implementation.
- No provider-based confidence, ranking, voting, or authority.
