# CortexMesh Directory Map

## Purpose

This document is the maintained navigation map for CortexMesh planning, governance, architecture, and evidence directories.

It is not a generated file listing.

It should help reviewers answer:

```text
Where should I look first?
Where does each class of artifact belong?
Which directories are authoritative?
```

## Primary Entry Points

| Path | Purpose |
|------|---------|
| `CortexMesh_v3_Planning/02_Onboarding/REVIEWER_ENTRY_POINT.md` | Stable reviewer entry point. |
| `CortexMesh_v3_Planning/02_Onboarding/Session_09/REVIEW_PACKET.md` | Current Session 09 review packet. |
| `CortexMesh_v3_Planning/00_Governance/GOVERNANCE_CHANGELOG.md` | Governance evolution summary. |
| `CortexMesh_v3_Planning/04_Architecture/ARCHITECTURAL_MISSION.md` | Architectural mission statement. |
| `CortexMesh_v3_Planning/05_Program_Management/V3_PLANNING_INDEX.md` | v3 planning index. |

## Top-Level Planning Structure

```text
CortexMesh_v3_Planning/
├── 00_Governance/
├── 01_Policies/
├── 02_Onboarding/
├── 03_Debt_Management/
├── 04_Architecture/
├── 05_Program_Management/
├── 99_Archive/
├── CORTEXMESH_DIRECTORY_MAP.md
└── Board/
```

## Governance

```text
00_Governance/
├── BOARD_CURRENT_STATE.md
├── BOARD_DECISIONS_REGISTER.md
├── BOARD_HISTORY_SUMMARY.md
├── COMMUNICATION_PROTOCOL_v1.0.md
├── DOCUMENT_AUTHORITY_MATRIX.md
├── GOVERNANCE_ADDENDUM_v1.0.md
├── GOVERNANCE_BASELINE_v1.0.md
├── GOVERNANCE_CHANGELOG.md
├── REVIEW_EVIDENCE_STANDARD_v1.0.md
├── Communications/
└── Repository_Lineage/
```

Use this area for governance baseline documents, board decision records, communications, evidence standards, and repository lineage investigation material.

## Policies

```text
01_Policies/
└── PolicyReview/
    ├── POLICY_INTENT_REPOSITORY_v1.1.md
    ├── POLICY_REVIEW_CHANGELOG_v1.1.md
    ├── POLICY_REVIEW_OPEN_ITEMS_v1.1.md
    └── evidence/
```

Use this area for policy intent, policy review status, and supporting policy evidence.

## Onboarding

```text
02_Onboarding/
├── REVIEWER_ENTRY_POINT.md
├── REVIEWER_PACKET_INDEX.md
├── SESSION_HISTORY.md
├── CURRENT_REVIEW_PACKET.md
├── REPOSITORY_STRUCTURE_STANDARD.md
├── Session_08/
├── Session_09/
├── Templates/
└── Archive/
```

Use this area for reviewer entry points and immutable session review packets.

`CURRENT_REVIEW_PACKET.md` is retained only as a backward-compatibility pointer.

## Debt Management

```text
03_Debt_Management/
├── DEBT_REGISTER_v1.3.md
├── DEBT001/
│   ├── DEBT001_EVIDENCE_PLAN_v1.2.md
│   ├── Execution/
│   └── Task_Corpus/
├── DEBT007/
├── DEBT008/
├── DEBT010/
│   └── StudyD_Benchmark/
└── DEBT011/
    ├── DesignStudy/
    └── ImplementationPlan/
```

Use this area for architecture debt records, evidence plans, task corpora, benchmark evidence, and design studies.

## Architecture

```text
04_Architecture/
├── ARCHITECTURAL_MISSION.md
├── GATE_T0_ARCHITECTURAL_INVENTORY.md
├── LOCK_REGISTRY_v1.0.md
└── Architectural_Identity/
    ├── AI001_ARCHITECTURAL_IDENTITY.md
    ├── AI002_ARCHITECTURAL_BOUNDARY_TEST.md
    ├── AI003_COMPARATIVE_ARCHITECTURE_INDEX.md
    ├── Case_Studies/
    └── Comparative_Matrix/
```

Use this area for architecture mission, inventory, locks, identity, comparative architecture, and boundary analysis.

## Program Management

```text
05_Program_Management/
├── PROGRAM_ROADMAP.md
└── V3_PLANNING_INDEX.md
```

Use this area for roadmap and planning index documents.

## Archive

```text
99_Archive/
├── DEBT011/
└── cortexmesh_governance_update_pack/
```

Use this area for superseded, imported, or historical materials that are no longer the active source of truth.

## Legacy And Compatibility Areas

The following areas exist for compatibility or historical reasons and should not be treated as primary entry points unless a board decision says otherwise:

```text
CortexMesh_v2_Baseline/
CortexMesh_v3_Planning/PolicyReview/
CortexMesh_v3_Planning/Session4_Onboarding/
CortexMesh_v3_Planning/Board/
```

## Maintenance Rule

Update this map when a top-level planning directory, active entry point, or major governance/architecture location changes.

Do not add cache files, generated test artifacts, raw run files, or exhaustive file listings.
