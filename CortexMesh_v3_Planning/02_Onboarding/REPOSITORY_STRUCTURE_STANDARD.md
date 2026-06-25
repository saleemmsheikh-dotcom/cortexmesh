# REPOSITORY_STRUCTURE_STANDARD

## Status

DRAFT

## Purpose

Define the reorganized CortexMesh planning-folder standard.

## Folder Standard

| Folder | Purpose |
|--------|---------|
| `00_Governance/` | Board state, history, baseline governance, decision records |
| `01_Policies/` | Policy documents and policy-review packets |
| `02_Onboarding/` | Fresh-session onboarding and reviewer packets |
| `03_Debt_Management/` | Debt register, evidence, design studies, implementation plans |
| `04_Architecture/` | Lock registry and architecture inventory |
| `05_Program_Management/` | Roadmap and planning indexes |
| `99_Archive/` | Retired or superseded planning material |

## Naming Standard

Use `CATEGORY_SUBJECT_VERSION.md` for governance-critical documents where practical.

Rules:

- Uppercase document category
- DEBT IDs always `DEBT###`
- Version always `_vX.Y`
- No spaces in folder or file names
- No mixed case for governance-critical documents
- Evidence/raw files may keep descriptive lowercase names

## Source Code Boundary

This structure applies to planning and governance documents only. Source folders such as `core/`, `engine/`, `agents/`, `tests/`, and `governance/` remain outside this reorganization pass.
