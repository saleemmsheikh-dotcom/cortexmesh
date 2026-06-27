# DEBT-011 Implementation Plan v1.0

## Status
Planning artifact only. Implementation not authorized.

## 1. Purpose

Define an implementation-ready plan for strengthening timeout enforcement observability in the Docker-based `ExternalRunner` path.

This plan focuses on four board-required areas:

1. Verified termination design
2. Audit trail enhancements
3. Container-state verification
4. Existing timeout behavior impact analysis

No source-code implementation is authorized by this document.

## 2. Governance Constraints

- `core/external_runner.py` is a LOCKED component.
- This document is planning only.
- No implementation is authorized until board approval is recorded.
- Proposed changes must preserve the existing timeout contract unless the board explicitly authorizes behavior changes.
- Timeout audit fields must distinguish attempted actions from verified outcomes.

## 3. Current Timeout Flow

### OBSERVED

The current timeout path uses a timer-based enforcement model.

Current flow:

1. Runtime execution starts a subprocess.
2. A `threading.Timer` is created using `TIMEOUT_SECONDS`.
3. If the timer fires, the timeout handler attempts `docker kill <container_name>`.
4. The timeout handler also calls `proc.kill()` on the local subprocess handle.
5. The result path returns `status: timeout`.
6. The audit trail records `killed: True`.

### INFERRED

The current flow records that kill actions were attempted, but does not independently verify that the Docker container stopped.

## 4. Proposed Verified Termination Flow

### 1. Verified Termination Design

### PROPOSED

Replace the current single `killed: True` timeout signal with a verified termination lifecycle.

Proposed lifecycle:

1. Timeout fires.
2. Record `timeout_triggered: true`.
3. Attempt Docker container termination.
4. Record Docker kill command result.
5. Attempt local subprocess termination.
6. Record local process kill result.
7. Verify container state after kill.
8. Attempt cleanup if required.
9. Record final termination verification outcome.
10. Return `status: timeout` while preserving existing external behavior.

### Proposed Lifecycle Fields

| Field | Meaning |
|---|---|
| `timeout_triggered` | Timer fired for the execution. |
| `kill_requested` | Termination was attempted. |
| `docker_kill_attempted` | Docker kill command was issued. |
| `docker_kill_returncode` | Docker kill command return code. |
| `docker_kill_stdout` | Captured Docker kill stdout, bounded for audit size. |
| `docker_kill_stderr` | Captured Docker kill stderr, bounded for audit size. |
| `local_process_kill_attempted` | Local subprocess kill was attempted. |
| `container_state_checked` | Post-kill Docker state verification was attempted. |
| `container_absent_or_stopped` | Container was verified absent or not running. |
| `cleanup_attempted` | Cleanup command such as `docker rm -f` was attempted. |
| `termination_verified` | No remaining container execution was detected. |
| `termination_anomaly` | Timeout handling encountered an unverified or failed termination condition. |

### Compatibility Rule

The existing `status: timeout` result should remain unchanged for callers unless the board explicitly authorizes a contract change.

## 5. Audit Trail Enhancements

### 2. Audit Trail Enhancements

### PROPOSED

Expand timeout audit records so they capture both attempted enforcement and verified enforcement.

Current audit behavior records `killed: True` after timeout handling.

Proposed audit behavior should record:

- timeout trigger
- kill request
- Docker kill command result
- local process kill attempt
- container-state verification result
- cleanup attempt result
- final verified termination status
- anomaly details when verification fails

### Proposed Audit Semantics

| Audit Concept | Required Meaning |
|---|---|
| Attempted termination | The system tried to stop execution. |
| Successful kill command | Docker command returned success. |
| Verified termination | Follow-up state check confirms no active container remains. |
| Cleanup success | Residual container state was removed or confirmed absent. |
| Timeout anomaly | Timeout occurred but termination could not be verified. |

### Compatibility Note

If `killed: True` is retained for backward compatibility, it should be treated as a legacy field meaning "kill attempted" only.

A new field such as `termination_verified` should carry the stronger verified outcome.

## 6. Container-State Verification

### 3. Container-State Verification

### PROPOSED

After timeout-triggered kill attempts, verify Docker container state before recording verified termination.

Candidate verification commands:

```text
docker inspect <container_name>
```

or

```text
docker ps -a --filter name=<container_name>
```

### Verification Outcomes

| Outcome | Interpretation |
|---|---|
| Container absent | Termination/cleanup verified. |
| Container exists and not running | Runtime termination verified; cleanup may still be needed. |
| Container exists and running | Termination failed or is incomplete. |
| Docker verification command failed | Termination cannot be verified. |
| Docker verification command timed out | Termination cannot be verified; anomaly should be recorded. |

### Cleanup Strategy

If the container remains present after `docker kill`, the implementation plan should evaluate a bounded cleanup attempt:

```text
docker rm -f <container_name>
```

Cleanup results should be recorded separately from kill results.

## 7. Impact on Existing Timeout Behavior

### 4. Existing Timeout Behaviour Impact Analysis

### OBSERVED

Existing timeout behavior returns `status: timeout` and attempts both Docker and local subprocess termination.

### PROPOSED

The implementation should preserve existing caller-visible timeout behavior while strengthening internal audit evidence.

### Expected Impacts

| Area | Expected Impact |
|---|---|
| Caller status | Should remain `timeout`. |
| Timeout duration | May increase slightly due to bounded verification commands. |
| Audit trail | More detailed and more accurate. |
| Operational visibility | Improved detection of failed or partial termination. |
| Backward compatibility | Preserved if legacy fields remain available. |
| Governance evidence | Stronger distinction between attempted kill and verified termination. |

### Risk Controls

- All Docker verification and cleanup commands must use bounded timeouts.
- Audit fields should be additive where possible.
- Existing timeout status should not change without board approval.
- Verification failure should surface as an audit anomaly, not silently disappear.

## 8. Implementation Risks

| Risk | Description | Mitigation |
|---|---|---|
| R1 | Verification adds latency to timeout path. | Use short bounded command timeouts. |
| R2 | Docker daemon failure prevents verification. | Record anomaly and preserve `status: timeout`. |
| R3 | Legacy consumers depend on `killed`. | Retain field as legacy attempted-kill signal. |
| R4 | Cleanup command removes useful forensic residue. | Record cleanup details and consider board-approved retention rules. |
| R5 | Audit payload becomes too large. | Bound stdout/stderr capture lengths. |

## 9. Test Plan

Future implementation planning should include tests for:

1. Normal execution without timeout.
2. Timeout with successful Docker kill.
3. Timeout where Docker kill fails.
4. Timeout where container remains running after kill.
5. Timeout where Docker inspect fails.
6. Timeout where Docker inspect times out.
7. Timeout where cleanup succeeds.
8. Timeout where cleanup fails.
9. Preservation of existing `status: timeout` behavior.
10. Audit trail records attempted versus verified termination distinctly.

## 10. Board Approval Requirements

Before implementation, the board must approve:

1. Whether `killed: True` is retained as a legacy attempted-kill field.
2. The final audit field names.
3. Whether timeout anomalies are written to the ledger or audit trail only.
4. Whether cleanup via `docker rm -f` is authorized.
5. Acceptable additional latency in timeout handling.
6. Test coverage required before modifying the LOCKED runner component.
