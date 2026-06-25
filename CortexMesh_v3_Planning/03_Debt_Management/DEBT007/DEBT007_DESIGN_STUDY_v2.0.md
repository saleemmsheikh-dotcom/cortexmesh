# DEBT-007 Remediation Design Study v2.0

## Classification
Planning artifact only.

No implementation authorized.

## Scope
Startup resilience only.

In scope:
- Missing memory file
- Corrupt JSON at load
- Invalid schema types at load
- Recovery from startup failure

Out of scope:
- Runtime write corruption
- Semantic validity
- Migration infrastructure

## Adopted Model
Model E: Auto-Default with Recovery Notification

## Model E Summary
On startup memory failure:
1. Preserve corrupt/original file for forensics.
2. Log error or warning.
3. Create default memory.
4. Add recovery information to memory.
5. Continue startup.

## Recovery Info Example
```python
memory["_recovery_info"] = {
    "reason": "corrupt_json" | "invalid_schema",
    "preserved_file": "...",
    "instructions": "Review preserved file and restore if needed"
}
```
