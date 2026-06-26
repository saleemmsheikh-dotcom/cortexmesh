# DEBT-011 Design Study v1.0

## Status

Planning artifact only. No implementation authorized.

## 1. Purpose

Assess timeout enforcement, kill signal reliability, zombie-process risk, and silent failure detection in the Docker-based `ExternalRunner` execution path.

## 2. Current Mechanism Analysis

### OBSERVED

- `core/external_runner.py` exists and is a LOCKED component.
- `TIMEOUT_SECONDS = 30`.
- Runtime timeout enforcement uses `threading.Timer`.
- Timeout handler calls `docker kill <container_name>`.
- Timeout handler also calls `proc.kill()`.
- `docker kill` is itself bounded with `timeout=10`.
- Timeout paths return `status: timeout`.
- Timeout audit trail records `killed: True`.

### INFERRED

- Timeout enforcement is implemented.
- Docker container termination is attempted.
- Local subprocess termination is attempted.
- The current audit trail records attempted termination, not verified termination.

## 3. Evidence Summary

| Evidence File | Finding |
|---|---|
| `external_runner_timeout_grep.txt` | Timeout, kill, and Docker references identified |
| `external_runner_timeout_block.txt` | Timer, docker kill, proc.kill, timeout response observed |
| `external_runner_timeout_callsite.txt` | Docker build timeout observed |
| `external_runner_audit_trail_grep.txt` | Audit trail paths identified |
| `external_runner_docker_state_verification_grep.txt` | No docker inspect / docker ps verification found |

## 4. Failure Modes

| ID | Failure Mode | Classification | Description |
|---|---|---|---|
| F1 | Docker kill failure | INFERRED | `docker kill` may fail but return code is not recorded in the observed timeout block |
| F2 | Container continues after timeout | INFERRED | No post-kill verification confirms container stopped |
| F3 | Misleading audit trail | INFERRED | `killed: True` may mean kill attempted, not kill verified |
| F4 | Docker daemon hang | INFERRED | `docker kill` has timeout=10, but failure outcome is not surfaced clearly |
| F5 | Build timeout visibility gap | INFERRED | Docker build has timeout protection, but timeout audit behavior is not documented in reviewed excerpt |

## 5. Silent Failure Detection Architecture

### PROPOSED

Timeout handling should distinguish:

| State | Meaning |
|---|---|
| `kill_requested` | Timer fired and kill was attempted |
| `kill_command_succeeded` | Docker kill command returned success |
| `container_absent_or_stopped` | Post-kill verification confirmed container stopped |
| `local_process_killed` | Local subprocess handle was killed |
| `termination_verified` | System confirmed no execution remains |

## 6. Candidate Mitigations

| Mitigation | Description | Benefit | Cost |
|---|---|---|---|
| M1 | Record docker kill return code/stdout/stderr | Makes failure visible | Low |
| M2 | Add post-kill `docker inspect` verification | Confirms stopped state | Medium |
| M3 | Add final `docker rm -f` cleanup attempt | Reduces residue | Low/Medium |
| M4 | Record timeout lifecycle in audit trail | Improves governance evidence | Low |
| M5 | Add host-level anomaly check | Detects surviving processes | Medium/High |

## 7. Path F Compatibility

### OBSERVED

DEBT-010 selected Path F: Defense-in-Depth Docker.

### INFERRED

DEBT-011 mitigations are compatible with Path F because they improve Docker runtime observability without changing the isolation architecture.

## 8. Recommendation

### PROPOSED

Adopt a verified-termination design for future implementation planning:

1. Treat `killed: True` as insufficient.
2. Replace or supplement it with structured timeout lifecycle fields.
3. Verify container state after kill.
4. Record kill command result.
5. Record cleanup result.
6. Surface timeout anomalies to the ledger/audit trail.

## 9. Open Questions

| Question | Status |
|---|---|
| Should failed kill verification escalate severity? | REQUIRES BOARD |
| Should timeout anomalies be written to ledger? | REQUIRES BOARD |
| Should host-level process checks be included? | REQUIRES BOARD |
| Should `killed: True` be deprecated in favor of structured fields? | REQUIRES BOARD |
