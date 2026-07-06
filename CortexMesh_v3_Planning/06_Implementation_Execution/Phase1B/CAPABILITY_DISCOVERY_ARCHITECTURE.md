# Capability Discovery Architecture

Status: PROPOSED

---

## Purpose

Define a provider-neutral capability discovery model for Phase 1B Local AI integration.

The objective is to let CortexMesh reason about available Local AI capabilities without treating provider identity as authority, quality, confidence, score, rank, or vote weight.

---

## Responsibilities

The capability discovery framework is responsible for:

- defining provider-neutral capability objects;
- maintaining a capability registry;
- allowing provider registrations to advertise declared capabilities;
- exposing manager-level `supports(capability)` checks;
- exposing manager-level `list_capabilities()` discovery;
- preserving provider/model identity as provenance only;
- returning diagnostics without provider ranking.

---

## Non-Goals

The framework does not:

- select winners;
- rank providers;
- score providers;
- alter confidence;
- alter authority;
- alter vote weight;
- alter governance decisions;
- implement LM Studio;
- modify orchestration, scoring, authority, contracts, snapshots, or ExternalRunner.

---

## Capability Object

A capability is neutral metadata with:

- name;
- description;
- category;
- optional metadata;
- explicit provenance-only semantics.

Capability names are normalized for lookup.

---

## Capability Registry

The registry lists known capability definitions independently of providers.

Initial registered capabilities:

- `text_generation`
- `chat_completion`
- `health_check`

The registry does not imply runtime availability. Availability remains determined by provider implementation status and health checks.

---

## Provider Advertisement

Provider registrations may declare capabilities.

This is declaration only.

Declaration does not:

- make an unimplemented provider executable;
- imply provider quality;
- influence provider ranking;
- affect scoring or authority.

Ollama remains an implemented provider.

LM Studio remains a placeholder provider with declared future capabilities only.

---

## Manager Discovery

`LocalAIManager` exposes:

- `list_capabilities(implemented_only=True)`
- `supports(capability, implemented_only=True)`
- `capabilities()`

The default behavior considers implemented providers only.

Placeholder capability discovery is opt-in through `implemented_only=False`.

---

## Provenance Rules

Capability and provider metadata are operational evidence only.

They must never influence:

- confidence;
- score;
- authority;
- rank;
- vote weight;
- governance decisions.

---

## LOCKED Boundaries

This framework is limited to the non-LOCKED Phase 1B Local AI subsystem.

No changes are authorized for:

- `orchestrator.py`
- `competition/scorer.py`
- `agents/authority.py`
- `core/contracts.py`
- `core/external_runner.py`
- `governance/snapshot.py`

---

## Future Provider Support

Future providers may advertise capabilities through provider registration metadata.

Provider-specific transport, parsing, and model behavior must remain inside provider adapters.

Capability declarations must remain separate from quality, scoring, authority, and governance semantics.
