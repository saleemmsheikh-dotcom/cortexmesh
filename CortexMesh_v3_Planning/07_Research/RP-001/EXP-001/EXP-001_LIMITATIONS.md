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
