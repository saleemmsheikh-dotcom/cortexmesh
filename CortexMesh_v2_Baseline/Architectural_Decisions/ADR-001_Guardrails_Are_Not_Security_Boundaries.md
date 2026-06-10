# ADR-001 Guardrails Are Not Security Boundaries

## Status
Accepted (v2 certification)

## Context
During Gate 5 certification, the board discovered that in-process Python guardrails (AST checks, import blocking, memory mutation detection) were being treated as sufficient protection for untrusted code. This was a fundamental architectural error.

## Decision
Guardrails reduce accidental misuse. Security boundaries enforce trust separation. These are distinct concepts and must not be conflated.

Untrusted capabilities must execute through ExternalRunner (Docker isolation). In-process guardrails are defense-in-depth only.

## Consequences
- ExternalRunner became mandatory for external capabilities
- SecurityBoundaryViolation added to enforce at API level
- AST-based Check 10 added to verify isolation flags pre-execution
- All previous "sandbox" approaches deprecated

## Alternatives Considered
- Strengthen in-process sandboxing: REJECTED — Python sandboxing is fundamentally unreliable
- Use seccomp-bpf: REJECTED — adds complexity without addressing Python-specific escape vectors
- Accept VM overhead: DEFERRED — Docker isolation is baseline, VM is v3 roadmap

## References
- Charter v1.1 §5 (Architectural Invariants)
- Gate 5b (Isolation Verification)
- P0 Trust Level Enforcement
