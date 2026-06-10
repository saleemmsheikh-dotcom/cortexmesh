# CortexMesh v2 Baseline — START HERE

**Status:** CortexMesh v2 certified, archived, and frozen  
**Certification Date:** 2026-06-11  
**Certified Tag:** `v2-certified`  
**Certified Commit:** `45d29edd618a54cd397378f6fd2bec5a020ab8a1`  
**Board:** Kimi / DeepSeek / ChatGPT  
**Current Phase:** Preservation → v3 Planning  

---

## 1. Purpose of This Folder

This folder is the authoritative onboarding and preservation archive for **CortexMesh v2**.

A new chat, agent, reviewer, developer, or auditor should read this file first before making claims, proposing changes, or reopening prior board decisions.

The purpose of this archive is to preserve the certified v2 baseline so that future v3 work does not contaminate or rewrite the certified state.

---

## 2. Current Governance State

```text
CortexMesh v2 Certification  = ACTIVE
CortexMesh v2 Baseline       = ARCHIVED
CortexMesh v2                = FROZEN
CortexMesh v3 Development    = NOT AUTHORIZED
CortexMesh v3 Planning       = AUTHORIZED
```

No further v2 development is authorized unless the governance board formally reopens certification.

---

## 3. Locked Systems

```text
CONTRACTS_v2    LOCKED
GOVERNANCE_v2   LOCKED
CORE_v2         LOCKED
```

These systems were locked after unanimous board approval and closure of all P0 blockers.

---

## 4. Required Reading Order

New agents and contributors should read the archive in this order:

1. `Certification_Record_v2.1.md`
2. `Executive_Record_v1.1.md`
3. `Charter_v1.1.md`
4. `TechSpec_v1.0.md`
5. `Known_Limitations.md`
6. `Architectural_Decisions/guardrail_vs_boundary.md`
7. `Architectural_Decisions/entropy_orchestration_only.md`
8. `P0_Remediation_Record/trust_level_enforcement.md`
9. `P0_Remediation_Record/scoring_specification.md`
10. `Gate5b_Evidence/verification_record.md`

Do not rely on chat memory alone. The archive documents are authoritative.

---

## 5. Document Authority Hierarchy

If documents or implementation appear to conflict, use this authority order:

```text
1. CortexMesh Charter v1.1
2. Certification Record v2.1
3. Technical Specification v1.0
4. Implementation and tests
5. Chat transcripts or informal notes
```

Implementation does not override governance.

---

## 6. Certification Scope

The following components are certified:

| Component | Status |
|---|---|
| Trust-level enforcement | CERTIFIED |
| Scoring specification | CERTIFIED |
| ExternalRunner isolation | CERTIFIED |
| Governance model | CERTIFIED |
| Isolation and security model | CERTIFIED |

The following components are implemented but not fully certified:

| Component | Status |
|---|---|
| Architecture overview | IMPLEMENTED |
| Memory integrity | IMPLEMENTED |
| Entropy subsystem | IMPLEMENTED |
| Evolution system | IMPLEMENTED |
| Strategy registry | IMPLEMENTED |

Important rule:

```text
CERTIFIED != IMPLEMENTED != SPECIFIED
```

Do not treat every documented component as equally certified.

---

## 7. Core Architectural Invariants

The following invariants govern CortexMesh v2:

1. Untrusted capabilities shall never execute in-process.
2. All external execution must pass through an approved isolation boundary.
3. Certification status does not alter trust classification without governance approval.
4. Components shall attempt audit recording before state-changing operations.
5. The board's unanimous decisions are binding and cannot be overridden by implementation without reconvening.

Changes to these invariants require board recertification.

---

## 8. Security Principle

The central security principle of CortexMesh v2 is:

```text
Guardrails do not constitute security boundaries.
```

In-process guardrails reduce accidental misuse. They do not protect against hostile Python code.

Untrusted or uncertified capability execution must go through the approved external isolation path.

---

## 9. Execution Classes

| Class | Execution | Trust Basis |
|---|---|---|
| `core` | In-process Python | Framework-owned trusted logic |
| `certified` | In-process Python | Reviewed, tested, approved capability |
| `external` | Docker via ExternalRunner | Untrusted or unvetted capability |

External capabilities must not bypass ExternalRunner.

---

## 10. Key Certified Decisions

### ADR-001 — Guardrails Are Not Security Boundaries

In-process Python sandboxing is not a reliable hostile-code security boundary. Guardrails remain useful for accidental misuse prevention only.

### ADR-002 — ExternalRunner Is Mandatory for Untrusted Code

Untrusted capabilities must execute through ExternalRunner using Docker isolation.

### ADR-003 — Entropy Is Orchestration Only

Entropy is retained as an orchestration and role-weight monitoring metric. It is not part of authority scoring.

### ADR-004 — Single Authority Score

CortexMesh v2 uses one canonical scoring path. Authority scoring must not be duplicated across modules.

---

## 11. Known Limitations

Certified limitations accepted by the board:

1. Docker isolation is used, not VM isolation.
2. Docker daemon compromise is an accepted risk with mitigation roadmap.
3. Timeout guarantees exist at the ExternalRunner boundary.
4. Raw Docker execution is not a supported secured execution path.
5. Some Technical Specification sections document implemented but uncertified components.
6. Board composition is currently project-specific.
7. Entropy monitoring exists but does not influence authority scoring.
8. Hash-chain tamper detection is implemented; Merkle verification and external anchoring are not complete.
9. Host-level watchdog for Docker daemon unresponsiveness is not implemented.
10. Capability demotion states such as deprecated, revoked, and quarantined are v3 roadmap items.

These limitations do not invalidate v2 certification.

---

## 12. Board Decisions That Must Not Be Re-Litigated Without New Evidence

The following decisions are closed unless new evidence is presented:

- CortexMesh v2 certification is active.
- CONTRACTS_v2, GOVERNANCE_v2, and CORE_v2 are locked.
- Guardrails are not security boundaries.
- ExternalRunner is the approved isolation boundary for untrusted execution.
- Trust-level enforcement P0 item is closed.
- Scoring specification P0 item is closed.
- Entropy is orchestration-only and excluded from authority scoring.
- `competition/selector.py` is non-authoritative for certified production selection.
- No v3 development is authorized until the v2 baseline is archived and preserved.

---

## 13. New Agent Operating Instructions

A new agent joining the project should:

1. Read this file first.
2. Read the required documents in the order listed above.
3. Treat the certified v2 baseline as frozen.
4. Avoid reopening closed decisions unless new evidence exists.
5. Clearly distinguish certified, implemented, and proposed behavior.
6. Route v3 ideas into planning, not v2 modification.
7. Preserve governance hierarchy over implementation preference.

---

## 14. Current Next Phase

The next authorized phase is **v3 planning**, not v3 development.

Recommended order:

1. Confirm v2 archive completeness.
2. Complete any remaining documentation under archive governance.
3. Conduct architecture debt review.
4. Draft v3 roadmap.
5. Seek board authorization before opening v3 implementation.

---

## 15. Quick Context for New Chats

If this file is being pasted into a new chat, the essential context is:

```text
CortexMesh v2 is certified, locked, archived, and frozen.
The authoritative project state is in CortexMesh_v2_Baseline/.
The board is Kimi / DeepSeek / ChatGPT.
The current phase is preservation to v3 planning.
No v2 changes and no v3 implementation are authorized without board process.
```
