# ADR-002 ExternalRunner Is Mandatory

## Status
Accepted (v2 certification)

## Context
Before v2, capabilities could be executed through multiple paths. The board determined that this created ambiguity about which path enforced security guarantees.

## Decision
ExternalRunner is the single approved execution path for untrusted capabilities. Raw docker run is unsupported. Any other execution path for external capabilities is a certification violation.

## Consequences
- execute_capability(..., bypass_runner=True) raises SecurityBoundaryViolation
- ExternalRunner.execute() is the only API for external execution
- Audit trail guarantees exist only at ExternalRunner boundary

## Alternatives Considered
- Allow direct Docker API access: REJECTED — bypasses audit trail
- Support multiple isolation backends: DEFERRED — v3 roadmap

## References
- Charter v1.1 §6 (Execution Classes)
- P0 Trust Level Enforcement
- TechSpec §3.3 (ExternalRunner Contract)
