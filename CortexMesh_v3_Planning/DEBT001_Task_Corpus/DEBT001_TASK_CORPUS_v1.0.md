# DEBT-001 Task Corpus v1.0

## Classification
PROPOSED evidence input corpus.

## Purpose
Provide reproducible task inputs for evaluating whether orchestrator randomness affects:
- Winner reproducibility
- Agent-selection reproducibility
- Winner score distribution
- Normalized ledger consistency
- Governance consistency

## Scope
The corpus covers engineering, research, and systems/governance tasks.

## Corpus

| ID | Domain | File |
|---|---|---|
| E1 | Engineering | tasks/E1_refactoring_input.md |
| E2 | Engineering | tasks/E2_unit_test_spec.md |
| E3 | Engineering | tasks/E3_failure_analysis.md |
| E4 | Engineering | tasks/E4_api_review.md |
| R1 | Research | tasks/R1_persistence_comparison.md |
| R2 | Research | tasks/R2_dependency_risk.md |
| R3 | Research | tasks/R3_evidence_classification.md |
| S1 | Systems/Governance | tasks/S1_debt_prioritization.md |
| S2 | Systems/Security | tasks/S2_trust_boundary.md |
| S3 | Systems/Governance | tasks/S3_governance_review.md |

## Execution Constraints
- Use identical memory snapshot across runs.
- Use fixed seeds from DEBT001_EVIDENCE_PLAN_v1.2.md.
- Disable external network dependencies.
- Do not modify CORE_v2 or certified v2 artifacts.
- Record OBSERVED, INFERRED, and PROPOSED claims separately.

## Status
Ready for board review before evidence execution.
