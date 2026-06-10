# Architectural Decision: Guardrail vs Boundary

## Decision
In-process mechanisms are guardrails, not security boundaries.

## Rationale
Python in-process controls can prevent accidental writes and obvious misuse, but they cannot reliably contain hostile code. Security isolation must happen outside the process.

## Consequence
Third-party and untrusted capabilities must execute through `ExternalRunner`.

## Accepted Boundary
Docker process/container isolation is accepted for v2, with Docker daemon compromise outside the current threat model.

## Known Limitation
VM isolation is stronger than Docker isolation and remains a future roadmap consideration.
