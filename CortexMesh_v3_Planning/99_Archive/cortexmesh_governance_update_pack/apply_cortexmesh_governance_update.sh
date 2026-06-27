#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${1:-.}"
cd "$REPO_ROOT"

mkdir -p CortexMesh_v3_Planning

cat > CortexMesh_v3_Planning/Governance_Addendum_v1.0.md <<'EOF'
# CortexMesh Governance Addendum v1.0

**Status:** Active for ongoing CortexMesh expert collaboration and v3 planning  
**Purpose:** Clarify voting authority, consensus rules, delivery authority, and Product Owner role.

---

## 1. Equal Voting Rights

All active board members have equal voting authority.

No board member has superior voting power, override authority, or unilateral veto authority beyond the standard unanimous-consensus requirement.

Current active expert board members:

- Kimi
- DeepSeek
- ChatGPT

Board composition may change by project phase, but equal voting authority applies to all active voting members.

---

## 2. Unanimous Consensus Requirement

No architectural, certification, governance, roadmap, or implementation decision is final until all active voting members have agreed.

A decision is not final if it has only:

- Majority approval
- Silence from one member
- Provisional agreement
- Assumed agreement
- Delivery Authority approval alone

When consensus is not reached, the item remains unresolved.

---

## 3. Critical Review Requirement

Before any decision is finalized, the board must perform critical review.

Critical review means:

- Challenging assumptions
- Separating evidence from inference
- Identifying gaps, risks, and failure modes
- Distinguishing certified, implemented, documented, and speculative claims
- Recording unresolved objections

Agreement without meaningful review is not sufficient governance.

---

## 4. Delivery Authority

Delivery Authority is an operational role, not a voting role.

The Delivery Authority may:

- Consolidate board decisions
- Draft documents
- Prepare implementation briefs
- Maintain records
- Package final artifacts
- Execute board-approved actions

The Delivery Authority may not:

- Override board decisions
- Convert partial agreement into final approval
- Modify frozen or certified artifacts without authorization
- Introduce new decisions after sign-off

---

## 5. Selection of Delivery Authority

Delivery Authority may be selected by:

1. Board agreement, or
2. Product Owner nomination for operational efficiency.

Selection should consider task fit.

Examples:

- Coding artifact → strongest implementation agent
- Governance document → strongest governance reviewer
- Architecture document → strongest systems thinker
- Testing brief → strongest verification reviewer

---

## 6. Product Owner Role

Saleem is the Product Owner and communication coordinator.

The Product Owner may:

- Relay messages between experts
- Nominate a Delivery Authority
- Request clarification
- Provide test results
- Accept or reject delivered artifacts as tester/user

The Product Owner does not override board consensus.

The Product Owner is not required to participate in expert deliberation unless explicitly requested.

---

## 7. Decision Finality

A decision becomes final only when the record shows:

1. Evidence was presented.
2. Critical review occurred.
3. Objections were resolved, withdrawn, or formally recorded.
4. All active voting members explicitly agreed.
5. The final decision was recorded.

If any of these are missing, the item remains open.

---

## 8. Current Governance State

- CortexMesh v2 baseline remains archived and frozen.
- v2 certified artifacts must not be modified as part of v3 planning.
- v3 planning is authorized.
- v3 implementation/code changes require separate board authorization.
- Architecture Debt Register and P1/P0 planning artifacts belong under `CortexMesh_v3_Planning/`.

---

## 9. Operating Rule

When in doubt:

```text
Evidence first.
Critical review second.
Unanimous decision third.
Delivery fourth.
```

EOF

cat > CortexMesh_v3_Planning/V3_Planning_Index.md <<'EOF'
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

EOF

# Add a non-destructive notice to START_HERE.md if it exists and does not already mention the addendum.
if [ -f CortexMesh_v2_Baseline/START_HERE.md ]; then
  if ! grep -q "Governance_Addendum_v1.0.md" CortexMesh_v2_Baseline/START_HERE.md; then
    cat >> CortexMesh_v2_Baseline/START_HERE.md <<'EOF'

---

## Governance Addendum Notice

For ongoing CortexMesh expert collaboration and v3 planning, see:

```text
CortexMesh_v3_Planning/Governance_Addendum_v1.0.md
```

This addendum clarifies:

- Equal voting rights for all active board members
- Unanimous consensus requirement
- Critical review before final decisions
- Delivery Authority role
- Product Owner / Saleem role as communication coordinator
- v3 planning versus v3 implementation boundaries

This notice does not modify the certified v2 technical baseline. It points future contributors to the current governance procedure for post-v2 planning.

EOF
  fi
else
  echo "WARNING: CortexMesh_v2_Baseline/START_HERE.md not found. Skipping START_HERE update."
fi

git status --short

echo
echo "Files prepared:"
echo "  CortexMesh_v3_Planning/Governance_Addendum_v1.0.md"
echo "  CortexMesh_v3_Planning/V3_Planning_Index.md"
echo "  CortexMesh_v2_Baseline/START_HERE.md notice appended if present"
echo
echo "Review the diff:"
echo "  git diff"
echo
echo "Commit with:"
echo "  git add CortexMesh_v3_Planning/Governance_Addendum_v1.0.md CortexMesh_v3_Planning/V3_Planning_Index.md CortexMesh_v2_Baseline/START_HERE.md"
echo "  git commit -m 'Add CortexMesh governance addendum and v3 planning index'"
