# Evidence Collection Design

## Purpose

Define a non-LOCKED, deterministic layer that captures execution outputs and their descriptive context for later synthesis. Evidence collection records what occurred; it does not decide what is correct or authoritative.

## Model

- `EvidenceSource`: agent role, fulfilled capability, and provenance.
- `EvidenceRecord`: step output plus assumptions, limitations, diagnostics, and trace/correlation identifiers.
- `EvidenceBundle`: deterministically ordered records and bundle diagnostics, explicitly marked `descriptive_only`.
- `EvidenceCollector`: validates and normalizes step output mappings or existing records.

Provider and model identity may be retained inside provenance to describe origin. They are rejected when supplied as authority input. Authority, score, confidence, rank, vote weight, and consensus fields are rejected rather than interpreted.

## Determinism

Records sort by step identifier, record identifier, and stable output representation. String collections are normalized, deduplicated, and sorted; mappings are key-sorted recursively. Duplicate record identifiers are invalid.

## Boundaries

The implementation is isolated in `Phase2C/orchestration/evidence.py`. It performs no provider selection, agent invocation, runtime orchestration, scoring, confidence adjustment, ranking, voting, or consensus. It changes no LOCKED component and has no dependency on `LocalAIManager` or `LocalAIProvider`.

## Follow-on Use

A future consensus design may consume bundles as descriptive inputs, but must establish its own governance boundary and must not reinterpret provenance identity as authority.

## Recommendation

READY FOR CONSENSUS DESIGN
