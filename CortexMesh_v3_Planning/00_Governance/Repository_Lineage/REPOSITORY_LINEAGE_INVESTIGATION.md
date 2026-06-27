# Repository Lineage Investigation

Status: PROPOSED

## Purpose

Investigate repository lineage for similarly named planning folders before any migration, archive, or removal decision is made.

## 1. Are the folders duplicates?

Pending investigation.

Required evidence:

- directory comparison
- file-count comparison
- path-level differences
- content-level differences for matching filenames

## 2. Do they contain unique files?

Pending investigation.

Required evidence:

- files present only in `CortexMesh_v3_Planning`
- files present only in `CortexMesh_v3_Planning 2`
- files present only in `CortexMesh_v3_Planning 3`
- files with same names but different contents

## 3. If unique, should those files be migrated, archived, or retained separately?

Pending board classification.

Possible dispositions:

| Disposition | Meaning |
|---|---|
| MIGRATE | Move unique material into the canonical planning tree. |
| ARCHIVE | Preserve unique material in `99_Archive` without making it authoritative. |
| RETAIN SEPARATELY | Keep the folder separate because it represents a distinct lineage or evidence set. |

## 4. What board decision is required?

Pending investigation result.

Required board decision should specify:

- whether each folder is duplicate, partial duplicate, or distinct lineage
- which unique files, if any, become authoritative
- which unique files, if any, are archived as legacy evidence
- whether any folder may be removed after preservation
