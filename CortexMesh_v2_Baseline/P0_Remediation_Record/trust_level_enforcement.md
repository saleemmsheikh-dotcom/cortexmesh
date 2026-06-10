# P0 Remediation Record: Trust-Level Enforcement

## Status
COMPLETE

## Remediation
External capabilities are routed through `ExternalRunner` and cannot be treated as in-process trusted code.

## Key Decisions
- `external` is the default trust level.
- `core` and `certified` are project-maintained trust levels.
- In-process guardrails are accident-prevention only.
- Security isolation is provided by Docker process/container boundaries.

## Regression Coverage
`tests/test_external_capability_boundary.py` verifies that an external capability cannot request in-process execution using a bypass path.

## Verification
Local unit tests passed:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover tests

Ran 11 tests
OK
```
