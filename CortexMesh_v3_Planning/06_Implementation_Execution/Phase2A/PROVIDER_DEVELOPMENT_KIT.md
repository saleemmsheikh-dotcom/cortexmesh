# Provider Development Kit

## Milestone

Phase 2A M4 - Provider Development Kit

## Status

IMPLEMENTED

---

## Purpose

The Provider Development Kit standardizes how new Local AI providers are designed, implemented, tested, and certified.

The PDK reduces provider implementation effort while preserving the provider-neutral Local AI architecture established in Phase 1B and consolidated in Phase 2A.

---

## Architecture Rule

`LocalAIManager` remains the sole public runtime entry point into the Local AI subsystem.

Provider adapters implement `LocalAIProvider`.

Runtime callers must not call provider adapters, provider registries, capability registries, or telemetry buffers directly.

---

## Implementation Lifecycle

```text
Architecture
        ↓
Provider Implementation
        ↓
Contract Tests
        ↓
Capability Verification
        ↓
Health Verification
        ↓
Diagnostics Verification
        ↓
Provider Certification
```

---

## PDK Contents

| Artifact | Purpose |
| -------- | ------- |
| `PROVIDER_DEVELOPMENT_KIT.md` | PDK overview and lifecycle |
| `PROVIDER_IMPLEMENTATION_GUIDE.md` | Step-by-step provider implementation guide |
| `PROVIDER_CERTIFICATION_CHECKLIST.md` | Certification gate checklist |
| `PROVIDER_TEMPLATE.md` | Adapter and test skeleton reference |
| `tests/provider_contract.py` | Shared provider contract assertions |
| `tests/provider_contract_mixin.py` | Reusable unittest mixin for future provider tests |

---

## Minimum Provider Requirements

Every provider must provide:

- `LocalAIProvider` implementation;
- health check;
- model discovery;
- request validation;
- response normalization;
- diagnostics;
- capability declaration;
- provenance handling;
- contract test compliance.

---

## Certification Standard

A provider is certifiable when:

- it builds successfully;
- health behavior is verified;
- shared contract tests pass;
- capabilities are declared;
- provenance remains non-authoritative;
- provider identity remains provenance only;
- no provider ranking is introduced;
- no authority, confidence, score, rank, or vote-weight effects are introduced;
- no governance impact is introduced;
- `LocalAIManager` compatibility is preserved;
- SAFE bridge compatibility is preserved.

---

## Constraints

- No LOCKED component modifications.
- No `LocalAIProvider` interface changes.
- No `LocalAIManager` API changes.
- No runtime orchestration changes.
- No provider ranking.
- Documentation-first provider onboarding.

---

## Success Condition

A competent developer can implement a new provider using only this PDK and pass the shared provider contract suite without modifying the Local AI architecture.
