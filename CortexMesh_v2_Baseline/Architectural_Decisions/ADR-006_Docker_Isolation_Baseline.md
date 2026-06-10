# ADR-006 Docker Isolation Baseline

## Status
Accepted (v2 certification)

## Context
The board needed to select an isolation baseline for untrusted capability execution. Options included in-process sandboxing, seccomp, Docker, and VM-level isolation.

## Decision
Docker process isolation is the v2 baseline. VM-level isolation is roadmap. Host Docker daemon compromise is accepted risk with mitigation plan (rootless Docker).

## Consequences
- ExternalRunner uses Docker with --network=none --read-only --memory=256m --cpus=0.5
- Gate 5b verifies 11 isolation checkpoints
- Documented limitation: Docker daemon compromise accepted risk

## Alternatives Considered
- In-process sandboxing: REJECTED — unreliable for hostile code
- seccomp-bpf: REJECTED — insufficient for Python escape vectors
- VM isolation: DEFERRED — v3 roadmap (high value, medium risk)

## References
- TechSpec §6 (Isolation & Security)
- Gate 5b Evidence
- Known Limitations §1-4
