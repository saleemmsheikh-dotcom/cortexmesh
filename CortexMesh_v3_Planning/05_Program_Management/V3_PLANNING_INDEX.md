# CortexMesh v3 Planning Index

**Status:** Active planning index  
**Purpose:** Direct new agents and contributors to the correct v3 planning materials without modifying the frozen v2 baseline.

---

## 1. Current Phase

```text
CortexMesh v2 Certification = ACTIVE
CortexMesh v2 Baseline = ARCHIVED + FROZEN
v3 Planning = AUTHORIZED
v3 Development = NOT AUTHORIZED
```

---

## 2. Authoritative v2 Baseline

Do not modify certified v2 documents.

Read first:

1. `CortexMesh_v2_Baseline/START_HERE.md`
2. `CortexMesh_v2_Baseline/Baseline_Manifest.md`
3. `CortexMesh_v2_Baseline/Charter_v1.1.md`
4. `CortexMesh_v2_Baseline/TechSpec_v1.0.md`
5. `CortexMesh_v2_Baseline/Architectural_Decisions/ADR_INDEX.md`

---

## 3. v3 Planning Documents

Recommended active planning set:

| Document | Purpose |
|----------|---------|
| `Architecture_Debt_Register_v1.2.md` | Known architecture debt and planning risks |
| `P0_Audit_Charter_v1.1.md` | Scope, evidence, pass/fail criteria for P0 audits |
| `P0_Audit_Findings.md` | Evidence collected from audit execution |
| `P1_Design_Study_Orchestrator_Determinism_v1.2.md` | Planning study for reproducibility and determinism |
| `Governance_Addendum_v1.0.md` | Voting, consensus, Delivery Authority, Product Owner role |

---

## 4. Current Board Decisions

| Item | Status |
|------|--------|
| CortexMesh strategic orientation | Decision-support oriented |
| L1 scoring determinism | Required |
| L2 orchestrator determinism | Optional, subject to future evidence |
| L3 outcome determinism | Not evaluated |
| DEBT-001 orchestrator randomness | High severity, monitor/investigate |
| v3 code changes | Not authorized |

---

## 5. Current Open Items

| Item | Status |
|------|--------|
| DEBT-005 execution path audit | Partial / requires further evidence |
| DEBT-007 memory integrity | Certification gap |
| DEBT-016 orchestrator coverage | Failed at 74%, target ≥80% for defined scope |
| DEBT-006 scoring pipeline | Passed |
| DEBT-020 TechSpec amendment | Deferred until post-audit review |

---

## 6. Rule for New Agents

New agents must not assume prior chat context.

They should treat the archive and planning documents as the source of truth.

If a claim is not in a document or supported by evidence, classify it as:

```text
UNVERIFIED
```

