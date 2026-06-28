# Repository Lineage Investigation - Executive Summary

## Scope

This investigation reviews duplicate and parallel CortexMesh planning trees to determine which artifacts belong in the canonical planning structure.

This is an investigation artifact only.

It does not authorize file migration, archival, deletion, or repository cleanup.

## Evidence Reviewed

- `Evidence/planning_current_inventory.txt`
- `Evidence/planning2_inventory.txt`
- `Evidence/planning3_inventory.txt`
- `Evidence/current_hashes.txt`
- `Evidence/planning2_hashes.txt`
- `Evidence/planning3_hashes.txt`
- `Evidence/diff_current_vs_2.txt`
- `Evidence/diff_current_vs_3.txt`
- `Evidence/diff_2_vs_3.txt`

## Key Findings

- Repository lineage evidence has been collected for the current planning tree and duplicate planning trees.
- Three diff reports exist and should be used as the factual basis for the comparison matrix.
- The detailed reports currently define the correct investigation sequence: comparison matrix, migration plan, archive plan, final recommendation.
- No cleanup action should occur until the board reviews the populated reports.

## Risks

- Premature restructuring could destroy useful lineage evidence.
- Duplicate planning trees may contain unique artifacts not yet categorized.
- Permission-bit noise from SMB-mounted files can obscure the actual investigation status if Git file-mode tracking is enabled.
- Final recommendations made before the comparison matrix is populated would be premature.

## Recommendations

1. Populate `FILE_COMPARISON_MATRIX.md` from the three diff reports.
2. Populate `MIGRATION_PLAN.md` only with files that have evidence-supported migration need.
3. Populate `ARCHIVE_PLAN.md` only after migration dependencies are identified.
4. Keep `FINAL_RECOMMENDATION.md` evidence-driven and complete it last.
5. Do not migrate, archive, or delete files during the investigation phase.

## Board Decisions Requested

- Confirm that repository lineage work remains investigation-only.
- Confirm the report sequence: evidence, comparison matrix, migration plan, archive plan, executive summary, final recommendation.
- Confirm that cleanup requires a later board decision after reports are populated.
