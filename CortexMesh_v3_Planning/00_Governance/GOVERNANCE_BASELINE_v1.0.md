# CortexMesh Governance Baseline v1.0

## Voting
All board members have equal voting rights.

Board:
- Kimi
- DeepSeek
- ChatGPT

Product Owner:
- Saleem

No decision is final until unanimously approved.

## Adopted Safeguards

### Plausibility Bias Statement
Plausible explanations are not evidence.

### Required Classification
All governance records must distinguish:
- OBSERVED
- INFERRED
- PROPOSED

### Evidence / Interpretation / Decision / Policy
Governance records must distinguish:
- Evidence
- Interpretation
- Decision
- Policy

A board vote may create policy.
A board vote does not create evidence.

### Severity-Action Consistency Rule
HIGH severity debt requires:
- Investigation, or
- Remediation, or
- Explicit board rationale for continued monitoring.

### HIGH-Severity Evidence Collection Trigger
Any HIGH-severity debt item remaining in monitoring beyond one planning phase must either:
1. Receive an approved evidence-collection plan, or
2. Receive explicit board rationale for continued monitoring, or
3. Be reclassified.

## Current Board State (2026-06-20)

| Debt     | Severity | Status                   | Notes                                                     |
| -------- | -------- | ------------------------ | --------------------------------------------------------- |
| DEBT-001 | MEDIUM   | MONITOR                  | Reclassified after pilot evidence review                  |
| DEBT-010 | HIGH     | MONITOR                  | Path F selected; implementation not authorized            |
| DEBT-011 | MEDIUM   | INVESTIGATE              | Design study approved; implementation planning authorized |
| DEBT-008 | MEDIUM   | INVESTIGATE              | Design study deferred                                     |
| DEBT-007 | HIGH     | INVESTIGATE              | Model E adopted; implementation not authorized            |
| DEBT-016 | CLOSED   | Closed by board decision |                                                           |

## Session 6 Outcome

### DEBT-010

Selected Path: F (Defense-in-Depth Docker)

Board Decision:

* Unanimous approval
* Study F accepted
* Study D partially completed
* Path D remains reopenable if complete workload evidence becomes available

Implementation Status:

* Planning only
* No implementation authorized
* No LOCKED component changes authorized

## Session 7 Outcome

### DEBT-011

Design Study:

* DEBT011_DESIGN_STUDY_v1.1 approved

Implementation Planning:

* Authorized

Implementation:

* Not authorized

Required Future Deliverable:

* DEBT011_IMPLEMENTATION_PLAN_v1.0.md

Implementation Plan must include:

1. Verified termination design
2. Audit trail enhancements
3. Container-state verification
4. Impact analysis on current timeout behavior

## Active Re-entry Triggers

Session 8 may be convened when:

1. DEBT-011 implementation plan submitted
2. DEBT-008 design study authorization requested
3. DEBT-010 reopening condition satisfied
4. DEBT-001 monitoring condition triggered
5. DEBT-007 implementation authorization requested
6. New debt identified
7. v3 planning authorization requested
8. Board-requested planning activity
