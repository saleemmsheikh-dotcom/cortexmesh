# Repository Structure Standard

## Purpose

Defines folder and naming standards for CortexMesh planning/governance artifacts.

## Folder Structure

| Folder | Purpose |
|---|---|
| 00_Governance | Board rules, authority, state, decisions |
| 01_Policies | Policy drafts, changelogs, open findings |
| 02_Onboarding | Reviewer packets and fresh-session materials |
| 03_Debt_Management | Debt evidence, design studies, implementation plans |
| 04_Architecture | Lock registry, architecture inventory, ADRs |
| 05_Program_Management | Roadmap and planning index |
| 99_Archive | Superseded or historical materials |

## Onboarding Structure

The onboarding directory separates stable entry points from historical review packets.

```text
02_Onboarding/
├── REVIEWER_ENTRY_POINT.md
├── REVIEWER_PACKET_INDEX.md
├── SESSION_HISTORY.md
├── CURRENT_REVIEW_PACKET.md
├── Session_XX/
│   ├── REVIEW_PACKET.md
│   └── MANIFEST.md
├── Archive/
└── Templates/
    └── REVIEW_PACKET_MANIFEST_TEMPLATE.md
```

Rules:

1. `REVIEWER_ENTRY_POINT.md` is the permanent reviewer handoff file.
2. `Session_XX/REVIEW_PACKET.md` is immutable after the session closes.
3. `Session_XX/MANIFEST.md` records packet status and scope.
4. `CURRENT_REVIEW_PACKET.md` may exist only as a compatibility pointer.
5. New sessions create a new `Session_XX/` folder rather than overwriting older packets.
6. `Archive/` is reserved for legacy onboarding artifacts that do not fit the session-folder model.

## Naming Convention

Use:

CATEGORY_SUBJECT_vX.Y.md

Examples:
- GOVERNANCE_BASELINE_v1.0.md
- GOVERNANCE_ADDENDUM_v1.0.md
- BOARD_CURRENT_STATE.md
- POLICY_INTENT_REPOSITORY_v1.1.md
- DEBT011_DESIGN_STUDY_v1.1.md
- DEBT011_IMPLEMENTATION_PLAN_v1.0.md

## Rules

1. Governance-critical files use uppercase names.
2. DEBT IDs always use DEBT###.
3. Versioned files use _vX.Y.
4. No spaces in filenames.
5. Raw evidence may retain lowercase descriptive names.
6. Superseded files move to 99_Archive unless needed beside current evidence.
7. Source code folders are not reorganized under this standard.
