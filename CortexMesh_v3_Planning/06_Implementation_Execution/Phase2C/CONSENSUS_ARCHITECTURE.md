# Phase 2C M6 - Consensus Architecture

## 1. Purpose

This document defines an architecture for deciding whether descriptive evidence from multiple agents is sufficiently aligned to be passed to a later synthesis stage.

In this architecture, consensus means **evidence alignment**, not voting. A consensus assessment describes relationships among evidence. It does not decide truth, create authority, approve action, alter confidence, or make a governance decision.

## 2. Scope

M6 is an architecture milestone only. It defines conceptual contracts, assessment categories, processing rules, boundaries, and risks. It introduces no Python implementation and no runtime integration.

The proposed layer consumes a purpose-built projection of M5 `EvidenceBundle` records. Original evidence remains the system of record. Provider and model identity may remain in original provenance for traceability, but must not enter a consensus input or affect an assessment.

## 3. Architectural Principles

1. Consensus is alignment among evidence claims and supporting context, not a count of agents.
2. Every evidence item retains its independent identity and traceability.
3. Corroboration does not create authority or prove correctness.
4. A minority position is preserved even when most evidence is compatible.
5. Material and unresolved divergence remains visible in the output.
6. Absence of contradiction is not automatically agreement.
7. Insufficient evidence is an explicit outcome, not an error and not implicit agreement.
8. Provider or model identity is prohibited from `ConsensusInput`.
9. No output changes confidence or assigns score, rank, weight, or priority.
10. `ConsensusAssessment` is advisory to synthesis only.
11. GG-02 and the Board process remain the exclusive governance decision mechanism.

## 4. Conceptual Model

### 4.1 ConsensusInput

`ConsensusInput` is a deterministic, identity-neutral projection of evidence relevant to one assessment question.

Required content:

- assessment question or claim scope;
- evidence record identifier;
- source agent role;
- capability fulfilled;
- normalized claims or findings;
- supporting observations or references;
- assumptions;
- limitations;
- diagnostics relevant to interpretation;
- trace and correlation identifiers.

Prohibited content:

- provider or model identity, including aliases and derived identity classes;
- authority designation;
- score, confidence, rank, vote, vote weight, or preference;
- a precomputed consensus label;
- governance approval or decision state.

The projection boundary rejects prohibited fields rather than silently using or transforming them. Source role and fulfilled capability provide traceability and context only; they do not carry weight.

### 4.2 AgreementSignal

`AgreementSignal` describes a non-authoritative alignment found between two or more evidence records. It contains:

- stable signal identifier;
- assessment scope;
- participating evidence record identifiers;
- alignment kind: exact, compatible, or partial;
- aligned claims or compatible propositions;
- supporting context;
- relevant assumptions and limitations;
- trace identifiers;
- a plain-language rationale.

It contains no strength score, confidence, rank, authority, or vote count. The number of participating records is traceability information only and must not determine the assessment by majority.

### 4.3 DivergenceSignal

`DivergenceSignal` describes a visible incompatibility, contradiction, unresolved scope difference, or missing basis between evidence records. It contains:

- stable signal identifier;
- assessment scope;
- affected evidence record identifiers;
- divergence kind: contradiction, incompatible recommendation, scope mismatch, assumption conflict, limitation conflict, or unsupported claim;
- conflicting propositions and their supporting context;
- relevant assumptions and limitations;
- whether the divergence is material to synthesis;
- resolution state: unresolved or explained;
- trace identifiers;
- a plain-language rationale.

Materiality is a categorical relationship to the assessment question, not a score. An explained divergence remains recorded; explanation does not erase the original evidence.

### 4.4 ConsensusAssessment

`ConsensusAssessment` is the deterministic advisory output. It contains:

- assessment identifier and scope;
- one outcome: exact agreement, compatible agreement, partial agreement, material divergence, or insufficient evidence;
- all input evidence record identifiers;
- all agreement signals;
- all divergence signals, including minority evidence;
- unresolved divergences;
- assumptions and limitations affecting interpretation;
- diagnostics;
- trace and correlation identifiers;
- `advisory_to_synthesis_only = true`;
- a plain-language rationale describing why the category applies.

The assessment must never expose authority, score, confidence adjustment, rank, vote weight, winning position, or governance decision fields. It does not modify its source evidence.

### 4.5 ConsensusPolicy

`ConsensusPolicy` defines deterministic comparison and classification rules for a named evidence domain or claim shape. A policy may define:

- how claims are normalized without changing their meaning;
- which claim scopes are comparable;
- what constitutes exact, compatible, partial, or material conflict;
- what evidence context is required before comparison;
- when evidence is insufficient;
- how assumptions and limitations constrain compatibility;
- which divergence kinds block synthesis and which must be carried into synthesis;
- stable ordering and diagnostic rules.

A policy must not define agent majorities, provider preferences, model preferences, scores, confidence thresholds, rankings, vote weights, authority inheritance, or governance outcomes. Policy version is recorded for reproducibility but grants no authority.

### 4.6 ConsensusEvaluator

`ConsensusEvaluator` applies a `ConsensusPolicy` to validated `ConsensusInput` values. It:

1. validates common scope and rejects prohibited identity or authority fields;
2. preserves the original evidence identifiers and trace links;
3. normalizes comparable claims according to policy;
4. derives agreement and divergence signals pairwise or by claim group;
5. preserves unmatched and minority evidence;
6. classifies the complete evidence relationship using the precedence rules below;
7. emits a deterministic `ConsensusAssessment` for advisory synthesis.

It does not select providers, invoke agents, mutate evidence, choose a winner, resolve governance questions, or perform synthesis.

## 5. Assessment Categories

### 5.1 Exact Agreement

All comparable evidence expresses the same material claims under compatible assumptions, scope, and limitations. No material proposition is contradicted or omitted, and no unresolved material divergence exists.

Exact agreement describes equivalence after policy-defined normalization. It is not proof that the shared claim is correct.

### 5.2 Compatible Agreement

Evidence reaches materially compatible conclusions but differs in wording, granularity, supporting observations, or non-conflicting qualifications. Differences can coexist without changing the synthesis outcome. No unresolved material divergence exists.

### 5.3 Partial Agreement

Evidence aligns on at least one material proposition while other material propositions remain unmatched, qualified differently, or non-materially divergent. The aligned and unaligned portions must both be explicit. Partial agreement cannot hide minority evidence.

### 5.4 Material Divergence

At least one unresolved contradiction, incompatible recommendation, assumption conflict, or scope conflict could materially change synthesis. This outcome applies regardless of how many records support either position. Every competing proposition is preserved.

### 5.5 Insufficient Evidence

The available evidence cannot support a meaningful alignment assessment. Examples include a single independent evidence source where corroboration is required, incomparable scopes, missing claims, absent supporting context required by policy, or diagnostics that prevent interpretation.

Insufficient evidence does not imply disagreement, low confidence, or failure by an agent.

## 6. Classification Precedence

The evaluator applies this deterministic precedence:

1. Invalid prohibited input is rejected and produces a diagnostic; it is not classified.
2. If policy-required evidence or comparability is absent, classify `insufficient evidence`.
3. If any unresolved material divergence exists, classify `material divergence`.
4. If material aligned and unaligned portions coexist, classify `partial agreement`.
5. If all material claims are compatible but not equivalent, classify `compatible agreement`.
6. Only if all material claims are equivalent under compatible context, classify `exact agreement`.

No branch uses majority, provider/model identity, source popularity, score, confidence, rank, or vote weight. Deterministic ordering uses stable evidence and signal identifiers only.

## 7. Minority and Divergence Preservation

The assessment includes every valid input record by identifier. A claim is never discarded because fewer agents express it. Minority evidence appears in the applicable agreement or divergence signal, or in an explicit unmatched-evidence section of the assessment rationale.

An unresolved material divergence prevents exact or compatible agreement. A later synthesis component may explain competing evidence, request more evidence, or decline synthesis, but it must not receive a falsely collapsed consensus result.

## 8. Data Flow and Boundaries

1. M5 produces an immutable descriptive `EvidenceBundle`.
2. A future boundary adapter selects evidence relevant to a single assessment scope and creates identity-neutral `ConsensusInput` projections.
3. `ConsensusEvaluator` validates inputs and applies `ConsensusPolicy`.
4. The evaluator emits `ConsensusAssessment` without modifying the evidence bundle.
5. A future synthesis layer may consume the assessment as advice alongside the original evidence.

The synthesis layer must receive or be able to resolve the original evidence records so agreement rationales, minority positions, and divergence remain auditable.

## 9. Governance Boundary

Consensus assessment is not ratification, authorization, certification, approval, escalation resolution, or Board consensus. It cannot replace or influence the formal mechanics of GG-02 by assigning machine-derived voting meaning.

Any governance decision remains governed exclusively by GG-02 and the recorded Board process. If evidence concerns a governance question, the assessment may organize that evidence for human review only.

## 10. Failure and Diagnostic Behavior

The architecture uses explicit rejection or diagnostics for:

- provider/model identity in a consensus input;
- authority, scoring, confidence, ranking, voting, or consensus-result fields in input;
- duplicate evidence identifiers;
- mixed assessment scopes;
- missing traceability required by policy;
- unsupported claim shapes;
- policy version mismatch;
- non-deterministic or ambiguous normalization.

Validation failure must not be converted into apparent disagreement or insufficient evidence. Evaluation errors preserve the input evidence and remain visible to callers.

## 11. Risks and Mitigations

| Risk | Impact | Architectural mitigation |
| --- | --- | --- |
| Consensus is interpreted as majority voting. | Minority evidence may be suppressed and agent counts may become implicit authority. | Pair claims rather than votes; prohibit winning positions and majority rules. |
| Shared error appears as truth. | Exact agreement may be over-trusted. | State that alignment is not correctness; preserve supporting evidence and limitations. |
| Provider/model identity leaks through provenance. | Provider preference may affect assessment. | Use an explicit identity-neutral projection and reject identity fields at the consensus boundary. |
| Normalization erases meaningful differences. | Material divergence may be hidden. | Limit normalization by versioned policy and retain original claims and rationales. |
| Partial agreement hides minority claims. | Synthesis may present false unanimity. | Require all record identifiers, unmatched claims, and unresolved divergence in output. |
| Materiality becomes an implicit score. | Ranking semantics may enter the layer. | Define materiality categorically against the assessment question with a plain-language rationale. |
| Advisory output is treated as governance approval. | GG-02 could be bypassed. | Mark every output advisory-only and explicitly separate Board process. |
| Too little evidence is treated as agreement. | Unsupported synthesis may proceed. | Make insufficient evidence a first-class outcome with policy-defined prerequisites. |

## 12. Implementation Preconditions

A reference implementation may proceed only if it:

- remains isolated under the non-LOCKED Phase2C planning/reference area;
- implements the prohibited-field boundary explicitly;
- has deterministic tests for every assessment category and precedence rule;
- tests minority and unresolved-divergence preservation;
- proves that provider/model identity cannot enter evaluation;
- exposes no scoring, confidence, rank, vote weight, authority, or governance behavior;
- makes no runtime orchestration, Local AI, or LOCKED component change.

## 13. Recommendation

READY FOR REFERENCE IMPLEMENTATION
