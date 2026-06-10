# CortexMesh Technical Specification v1.0

## Certification Status
Board approved for the CortexMesh v2 certified baseline.

Certification date: 2026-06-11

Board:
- Kimi
- DeepSeek
- ChatGPT

## Scope
This specification records the v2 certified architecture and implementation status for CortexMesh core execution, scoring, memory integrity, governance, and external capability isolation.

## Certification Scope Matrix
| Area | Status | Evidence |
|------|--------|----------|
| CONTRACTS_v2 | CERTIFIED | `core/contracts.py`, capability-boundary tests |
| GOVERNANCE_v2 | CERTIFIED | tamper log enforcement, recovery, Gate 4/B+ evidence |
| CORE_v2 | CERTIFIED | scoring regression tests, authority routing, orchestration path |
| ExternalRunner | IMPLEMENTED | `core/external_runner.py`, Gate 5b evidence |
| Docker Isolation | IMPLEMENTED | no network, read-only filesystem, memory/CPU caps, no socket mount |
| Entropy Monitoring | IMPLEMENTED | orchestration-only, not authority scoring |
| Full TechSpec Beyond v2 Scope | PARTIAL | carried forward to v3 planning |

## 1. Execution Model
CortexMesh executes a task through the main orchestration path in `orchestrator.py`.

Primary flow:
1. Classify task type.
2. Load and normalize persistent memory.
3. Enforce governance before execution.
4. Build active solver strategies.
5. Select unique agents with quarantine filtering.
6. Generate candidate solutions.
7. Run critic review.
8. Score candidates through the canonical scoring path.
9. Resolve final decision through Authority.
10. Update memory, trust, failure records, governance stability, and evolution state.

## 2. Scoring Specification
Scoring consumes structured evidence flags. Keyword matching is not a certified scoring mechanism.

Canonical scoring function:

`competition.scorer.compute_total_score(solution, reviews, ledger)`

Certified scoring properties:
- Scoring is deterministic for identical validated evidence.
- Review verdicts may adjust sub-scores.
- Weighted total is calculated once in `competition.scorer`.
- Repetition penalty is not applied in base scoring.
- Authority applies repetition penalty exactly once.

Rubric dimensions:
- Logic: systematic structure, stepwise process.
- Risk: failure modes, abstraction level.
- Completeness: alternatives, single-approach limitation.

## 3. Trust And Execution
Trust and execution boundaries are handled by `core/contracts.py`, `core/capability_guardrails.py`, and `core/external_runner.py`.

Trust levels:
- `external`: default for untrusted/third-party capability code.
- `core`: project-maintained in-process code.
- `certified`: project-maintained code accepted by the board.

External capabilities must execute through `ExternalRunner`. In-process guardrails are accident-prevention mechanisms and are not certified as a hostile-code security boundary.

## 4. Memory Integrity
Persistent memory is defined in `memory/memory_store.py` and includes:
- run counters
- agent wins and usage
- role weights
- task trust
- confidence history
- failure memory
- knowledge memory
- negative knowledge
- knowledge conflicts
- governance violations/actions
- tamper log and anchor
- governance snapshots
- strategy registry
- entropy target/drift

The ledger in `ledger/ledger.py` records tagged execution events during a run and exposes recent entries by tag. Persistent memory is schema-normalized on load.

## 5. Governance Interfaces
Governance verifies strategy constraints, tamper-log integrity, recovery behavior, freeze/unfreeze state, and snapshot rollback.

Certified governance properties:
- Illegal strategy versions are quarantined.
- Strategy overflow is enforced.
- Tamper-log mismatch is detected.
- Critical tamper events trigger policy response.
- Valid snapshots can be restored.
- Governance actions are recorded.

## 6. Isolation And Security
External capability isolation is implemented in `core/external_runner.py`.

Container launch controls:
- `--network=none`
- `--read-only`
- `--memory=256m`
- `--cpus=0.5`
- no `--privileged`
- no Docker socket mount
- no host root mount

Timeout controls:
- `ExternalRunner` assigns a unique container name.
- A `threading.Timer` independently calls `docker kill`.
- Timeout results return `status: timeout` and `audit_trail.killed: true`.

Error handling:
- Host paths are sanitized from error strings.
- Container stderr is included only after sanitization.

## 7. Known Limitations
Certified limitations:
1. Docker isolation is used rather than VM isolation.
2. Docker daemon compromise is outside the v2 threat model.
3. Timeout guarantees apply only through `ExternalRunner`.
4. Raw Docker execution is unsupported.
5. Full technical specification work beyond this baseline continues in v3 planning.
6. Board composition is project-specific.
7. Entropy monitoring is orchestration-only and not part of authority scoring.

## 8. Test Evidence
Unit test command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover tests
```

Recorded result:

```text
Ran 11 tests
OK
```

Gate 5b result:

```json
{
  "gate5b_status": "PASS",
  "passed": 11,
  "total": 11
}
```

## 9. Baseline Status
CortexMesh v2 baseline status: ACTIVE.

This document is part of the `CortexMesh_v2_Baseline` archive and is included in the `v2-certified` tag.
