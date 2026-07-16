# CortexMesh Research

## Purpose

`07_Research/` is the home for versioned, evidence-based CortexMesh research programs. It exists to test questions that are not yet implementation claims and to preserve negative, null, and inconclusive findings alongside successful results.

Research does not authorize product implementation, runtime integration, governance change, provider use, or modification of LOCKED components. Those actions require their own approved engineering or governance process.

## Operating Principles

- research questions precede experiments;
- hypotheses are falsifiable and registered before observation;
- controls and exclusions are explicit;
- metrics remain independent and non-compensating;
- reproducibility precedes performance claims;
- evidence is preserved even when it contradicts the preferred hypothesis;
- provider and model identity remain descriptive provenance;
- minority, divergent, null, and adverse results remain visible;
- ethics, governance, security, privacy, and LOCKED boundaries apply throughout;
- publication distinguishes observation, inference, limitation, and recommendation.

## Structure

Each research program uses a stable identifier such as `RP-001` and contains, at minimum:

- a program README;
- a charter;
- a research method;
- success criteria;
- versioned inputs, protocols, analysis, results, and publication records when execution is authorized.

Experiments within a program use stable `EXP-NNN` identifiers. Their full identity is the pair `RP-NNN/EXP-NNN`. Experiment numbering is local to its research program and identifiers are never reused, even when an experiment is withdrawn or invalidated.

The research hierarchy is:

```text
Foundation Baseline
  -> Research Program (RP-NNN)
    -> Experiment (EXP-NNN)
      -> Replay Results
        -> Publication
```

Every experiment must have an immutable preregistration before data collection. A changed design requires a new preregistration version or experiment identifier; the original record remains preserved.

Independent reproductions use the parent experiment identifier plus `-RNN`, for example `EXP-001-R1`. A reproduction is an appendix to the registered experiment, not a new experiment number, and must preserve both original and reproduction evidence.

Permanent cross-program observations use `OBS-NNN` identifiers and are recorded in `RESEARCH_OBSERVATIONS.md`. Observations describe evidence; they do not create implementation or governance authority.

`RESEARCH_LOGBOOK.md` records the chronological development of research knowledge. It is append-only institutional memory, not an implementation tracker or decision authority.

## Program Register

| Program | Title | Status | Scope |
| --- | --- | --- | --- |
| RP-001 | Evidence-Based Orchestration Effectiveness | ACTIVE - EXP-001 CHARACTERIZED AND REPRODUCED | Controlled offline study of measurable orchestration value |

## Foundation Relationship

Research builds on `FOUNDATION_BASELINE_v1.0.md`. It may test extensions or alternatives, but it may not silently redefine Foundation 1.0 principles, sealed baselines, governance authority, or certification history.
