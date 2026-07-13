# EXP-001 Limitations

## Registered Scope Limitations

- The study characterizes one sealed engine version.
- The study uses one certified, compact, synthetic replay corpus.
- The 24 cases are a fixed study set, not a random sample of all CortexMesh tasks.
- Ten repetitions characterize within-environment stability, not population variability.
- No Local AI, external provider, live agent, production input, or runtime path is exercised.
- No adaptive orchestration, alternative planner, or single-path comparator is evaluated.
- Latency is environment-specific and observational.
- Exact replay does not establish semantic correctness outside registered expectations.
- Stable outputs do not prove future runtime safety or integration benefit.
- The study cannot establish superiority, optimization value, or causal effectiveness.

## Validity Threats to Record After Execution

- environment and dependency specificity;
- measurement overhead and clock behavior;
- canonicalization exclusions;
- corpus expectation defects;
- harness defects;
- case coverage gaps;
- reviewer or anomaly-classification bias;
- incomplete cross-environment reproduction.

## Non-Claims

EXP-001 does not authorize or establish:

- runtime integration;
- provider or model selection;
- agent invocation;
- confidence, score, rank, voting, or authority change;
- governance decisions;
- LOCKED modification;
- production readiness;
- comparative improvement.

This document will be extended after execution only to record observed limitations, not to conceal or weaken preregistered constraints.

## Observed Limitations

- Collection used one declared macOS/x86_64 environment with CPython 3.14.5; independent reproduction has not yet occurred.
- The first repetition contained the maximum latency observation, and repetition 8 contained another high observation; no causal attribution is available.
- Expected rejection paths and completed paths have different latency distributions, so the aggregate coefficient of variation is not a homogeneous workload measure.
- Corpus `statements` semantics are ambiguous for compatible alias canonicalization and insufficient-evidence presentation. Four cases therefore differ under literal synthesis-string comparison while preserving raw evidence.
- Diagnostic matching for the prohibited-input case used the registered semantic expectation and the resolver's concrete provider/model rejection language; it was not an exact-string comparison.
- Evidence completeness measures registered fields and identifiers, not external truth or real-world evidentiary sufficiency.
- The harness is research infrastructure introduced after authorization and frozen through pre-collection Deviation 001; it is not part of the sealed engine or permanent validation framework.

These limitations do not invalidate the completed characterization, but they constrain generalization and future comparisons.
