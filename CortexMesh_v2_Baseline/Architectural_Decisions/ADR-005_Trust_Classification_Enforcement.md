# ADR-005 Trust Classification Enforcement

## Status
Accepted (v2 certification)

## Context
Before v2, trust classification (core/certified/external) was declared but not enforced at runtime. A capability could claim to be certified and run in-process, bypassing isolation.

## Decision
Trust classification must be enforced, not merely declared. External capabilities attempting in-process execution raise SecurityBoundaryViolation. Test must fail if enforcement is removed.

## Consequences
- SecurityBoundaryViolation added to contracts
- execute_capability() API includes enforcement check
- test_external_capability_boundary.py verifies bypass rejection

## Alternatives Considered
- Convention-based enforcement: REJECTED — not auditable
- Runtime capability scanning: DEFERRED — v3 roadmap

## References
- Charter v1.1 §5 (Invariant 2)
- P0 Trust Level Enforcement
- TechSpec §3.2 (Enforcement Mechanisms)
