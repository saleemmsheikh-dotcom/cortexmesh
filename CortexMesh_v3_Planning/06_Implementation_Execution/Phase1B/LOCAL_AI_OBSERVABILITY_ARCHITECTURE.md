# Local AI Observability Architecture

Status: PROPOSED

---

## Purpose

Define provider-neutral observability and telemetry for the Phase 1B Local AI subsystem.

Observability records operational evidence only. It does not influence provider selection quality, confidence, authority, scoring, ranking, vote weight, or governance decisions.

---

## Scope

The observability framework covers:

- provider lifecycle events;
- capability discovery events;
- health check events;
- request timing events;
- response timing events;
- correlation identifiers;
- trace identifiers;
- diagnostics export.

---

## Event Model

`LocalAIEvent` is the structured telemetry event model.

Each event includes:

- event type;
- trace ID;
- correlation ID;
- UTC timestamp;
- provider, when applicable;
- model, when applicable;
- capability, when applicable;
- request ID, when applicable;
- status, when applicable;
- latency, when applicable;
- diagnostics.

Events are immutable dataclass records.

---

## Event Types

Initial event types:

- `provider_lifecycle`
- `capability_discovery`
- `health_check`
- `request_timing`
- `response_timing`

These are informational categories only.

---

## Trace and Correlation

Trace identifiers link events produced during a single Local AI activity.

Correlation identifiers allow a caller to associate Local AI telemetry with a broader task, review, or evidence package.

No runtime integration is introduced by this document.

---

## Diagnostics Export

`LocalAITelemetryBuffer` provides an in-memory collector and diagnostics export format.

The export includes:

- event list;
- event count;
- informational-only marker;
- ranking-used marker set to `false`.

---

## Safety Rules

Telemetry diagnostics remove decision-affecting keys:

- authority;
- confidence;
- rank;
- score;
- vote weight.

Telemetry must never affect:

- provider ranking;
- authority;
- confidence;
- scoring;
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

## Current Integration Status

M7A introduces observability primitives only.

The telemetry framework is not wired into runtime orchestration.

Future runtime integration requires separate authorization.
