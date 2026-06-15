# DEBT-001 Evidence Collection Plan v1.2

## Purpose
Define how claims about orchestrator randomness can be tested.

The objective is not to prove randomness harmful or beneficial.

## Research Questions
- Does randomness cause materially different winners?
- Does randomness reduce score quality?
- Does randomness break audit reproducibility?
- Does randomness improve final decision quality?
- Does randomness affect governance consistency?

## Methodology
Fixed seeds:
- 10
- 42
- 123
- 999

Random condition:
- random.seed(None)

Controls:
- Same memory snapshot
- Same configuration
- External capabilities mocked
- Frozen model version where feasible
- Fixed prompts
- Network disabled

## Pilot
20 runs per fixed seed plus 20 random runs.

Purpose:
- Estimate variance
- Compute effect size
- Determine final sample size

## Metrics
- Winner reproducibility
- Agent-selection reproducibility
- Winner score distribution
- Score variance
- Normalized ledger consistency
- Seed sensitivity index

## Statistical Tests
- Winner difference: chi-square or Fisher exact
- Score difference: t-test or Mann-Whitney
- Seed sensitivity: ANOVA
- Reproducibility: descriptive agreement percentage

## Materiality Thresholds
These are board-defined materiality thresholds, not proof thresholds.

- Winner difference >5% triggers board review
- Score difference >2% triggers board review
- Winner difference <=5% and score difference <=2% supports neutrality review

## Task Corpus
Delegated to Product Owner Saleem.

Requirements:
- Minimum 10 tasks
- Covers engineering, research, systems
- Reproducible inputs
- No external dependencies
- Representative of CortexMesh use cases

Deadline:
7 days from delegation.
