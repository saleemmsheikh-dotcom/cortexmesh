# DEBT-010 Study D Feasibility Assessment

## Classification
OBSERVED feasibility assessment.

## Purpose
Assess whether benchmark execution comparing Docker, Firecracker, and gVisor is currently feasible.

## Requested Study D
Benchmark alternative isolation options such as:
- Docker
- Firecracker
- gVisor

## Local Environment Observations

```text
Docker: available
Firecracker: not found in PATH
gVisor/runsc: not found in PATH
OS: macOS / Darwin x86_64
```

## Feasibility Result
Benchmark execution is currently infeasible in this environment.

## Reason
The environment does not currently provide:
- Firecracker runtime
- gVisor `runsc` runtime
- Comparable Linux test environment for microVM/runtime benchmarking

Docker is available, but a Docker-only benchmark would not answer the Study D comparison question.

## Valid Evidence Produced
This assessment establishes that Study D benchmark numbers should not be invented from the current environment.

## Recommended Next Step
If the board wants Study D executed, provision a comparable Linux benchmark host with:
- Docker Engine
- Firecracker
- gVisor/runsc
- Identical test workload
- Resource measurement tooling
- Repeatable execution harness

## Evidence Boundary
This document is a feasibility assessment only. It contains no performance, security, or isolation benchmark claims.
