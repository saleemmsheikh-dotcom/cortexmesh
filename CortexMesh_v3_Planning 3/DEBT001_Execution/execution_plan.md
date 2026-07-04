# DEBT-001 Execution Plan

## Objective
Determine whether orchestrator randomness materially affects outcomes.

## Inputs
- DEBT001 Task Corpus v1.0
- Evidence Plan v1.2

## Pilot
- 20 runs per fixed seed
- 20 random runs

## Metrics
- Winner
- Winner score
- Output hash (optional)
- Agent selection reproducibility
- Score variance
- Ledger consistency
- Seed sensitivity index

## Outputs
- `pilot_results.csv`
- `pilot_analysis.md`
- `severity_review.md`

## Suggested Future Structure
```text
DEBT001_Execution/
├── environment.md
├── execution_plan.md
├── seed_matrix.csv
├── pilot/
│   ├── raw_runs/
│   ├── pilot_results.csv
│   └── pilot_analysis.md
├── results/
│   ├── full_experiment.csv
│   └── statistical_analysis.md
└── reports/
    ├── neutrality_assessment.md
    ├── severity_review.md
    └── board_submission.md
```

## Tagging Note
After the board formally closes Session 4 and before execution artifacts are added, create the accepted-corpus tag:

```bash
git tag debt001-corpus-v1.0
git push origin debt001-corpus-v1.0
```
