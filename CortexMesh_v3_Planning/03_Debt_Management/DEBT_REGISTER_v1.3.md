# Architecture Debt Register v1.3

## Open Items

### DEBT-001: Orchestrator Randomness
Severity: MEDIUM
Status: MONITOR
Evidence of harm: Not established
Evidence of benefit: Not established
Evidence Plan: v1.2 approved
Next Action: Product Owner delivers task corpus

### DEBT-007: Memory Integrity Startup Resilience
Severity: HIGH
Status: INVESTIGATE
Observed failures:
- Corrupt JSON causes load failure
- Invalid schema types cause load failure
- No fallback
- No recovery logging

Design: Model E adopted as planning artifact
Implementation: Not authorized

### DEBT-008: Merkle Anchoring
Status: OPEN
Topic: Hash-chain to Merkle tree and external anchoring

### DEBT-010: Docker Daemon Risk
Status: MONITOR
Topic: Docker daemon compromise and isolation hardening

### DEBT-011: Timeout / Zombie Process Risk
Status: OPEN
Topic: kill failures, daemon hangs, zombie process handling

## Closed Items

### DEBT-016: Orchestrator Coverage
Status: CLOSED
Result: 99% coverage achieved
Note: Closure does not prove every branch is defect-free.
