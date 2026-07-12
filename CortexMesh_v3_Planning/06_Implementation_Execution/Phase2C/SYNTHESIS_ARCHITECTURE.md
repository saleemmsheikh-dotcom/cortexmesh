# Phase 2C M8 - Evidence Synthesis Architecture

## 1. Purpose

This document defines a non-authoritative synthesis layer that converts an M5 `EvidenceBundle` and an M7 `ConsensusAssessment` into a final structured response. Synthesis organizes and presents evidence; it does not decide truth, create authority, approve action, change confidence, or make a governance decision.

## 2. Scope

M8 is an architecture milestone only. It defines conceptual contracts, required output sections, category-specific behavior, validation boundaries, and risks. It introduces no Python or runtime implementation.

The synthesis layer receives both original descriptive evidence and its advisory alignment assessment. The `EvidenceBundle` remains the source of record. `ConsensusAssessment` is an organizational aid and must never replace, suppress, or mutate the underlying evidence.

## 3. Architectural Principles

1. Synthesis presents evidence and relationships; it creates no authority.
2. `ConsensusAssessment` is advisory input only.
3. Original evidence takes precedence if an assessment and its referenced evidence differ.
4. Material and unresolved divergence must remain prominent and explicit.
5. Minority evidence must never be erased, merged into apparent unanimity, or dismissed by source count.
6. Assumptions and limitations remain explicit and attributable.
7. Provenance, evidence record identifiers, trace identifiers, and correlation identifiers remain available in the result.
8. Provider/model identity remains descriptive provenance only and cannot affect inclusion, ordering, wording, or prominence.
9. Synthesis does not change confidence or assign score, rank, authority, vote, vote weight, winner, or approval state.
10. Missing or insufficient evidence produces a bounded response, not invented completion.
11. Governance decisions remain outside synthesis and exclusively under GG-02 and the Board process.

## 4. Conceptual Model

### 4.1 SynthesisInput

`SynthesisInput` is the validated synthesis request. It contains:

- synthesis scope and requested response objective;
- one immutable `EvidenceBundle`;
- one advisory `ConsensusAssessment` for the same scope;
- an explicit `SynthesisPolicy` identifier and version;
- optional presentation context that does not affect evidence interpretation.

Validation requires:

- every assessment evidence identifier resolves to an evidence record;
- every agreement, divergence, unresolved-divergence, and minority identifier resolves to an evidence record;
- trace and correlation identifiers remain consistent or discrepancies are diagnosed;
- the assessment is marked advisory-only;
- source evidence is descriptive-only where that marker is available;
- the assessment outcome is a supported categorical value;
- no authority, scoring, confidence-adjustment, ranking, voting, or governance instruction is supplied.

Evidence provenance may include provider/model identity for origin traceability. Identity fields are copied only into the provenance section and are prohibited from synthesis policy conditions, selection rules, grouping rules, summaries, or claims of reliability.

### 4.2 SynthesisSection

`SynthesisSection` is one deterministic, typed part of the response. It contains:

- section identifier and section type;
- ordered content items or statements;
- contributing evidence record identifiers;
- relevant provenance references;
- trace and correlation identifiers;
- section assumptions and limitations;
- diagnostics;
- an explicit empty-state reason when no supported content exists.

Section ordering follows the output contract, not evidence source prestige or agent count. Each material statement must resolve to at least one evidence record. A section cannot silently omit referenced minority or divergent evidence.

### 4.3 SynthesisResult

`SynthesisResult` is the final deterministic structured response. It contains:

- synthesis identifier, scope, and policy version;
- the required ordered sections;
- the advisory consensus category used for presentation;
- all source evidence record identifiers;
- unresolved question identifiers;
- result-level diagnostics;
- trace and correlation identifiers;
- `descriptive_only = true`;
- `advisory_output = true`;
- a statement that governance decisions remain outside synthesis.

It contains no authority, score, confidence adjustment, rank, preference, vote, vote weight, winning claim, approval, ratification, or governance-decision field.

### 4.4 SynthesisPolicy

`SynthesisPolicy` defines deterministic presentation rules. It may specify:

- claim normalization that preserves original wording and references;
- stable record and statement ordering;
- grouping rules for aligned, divergent, and minority evidence;
- required provenance and traceability detail;
- how empty sections are represented;
- when a limitation or diagnostic creates an unresolved question;
- category-specific summary templates;
- maximum presentation length only if truncation preserves references and exposes omissions.

A policy must not:

- choose evidence by provider, model, agent popularity, majority, or reputation;
- infer truth from consensus category;
- suppress minority or unresolved divergent evidence;
- generate scores, confidence changes, ranks, weights, or authority;
- decide governance outcomes;
- resolve a contradiction without new evidence.

Policy identity supports reproducibility only and grants no authority.

### 4.5 EvidenceSynthesizer

`EvidenceSynthesizer` validates `SynthesisInput`, applies a `SynthesisPolicy`, and creates a `SynthesisResult`. It:

1. validates evidence/assessment referential integrity and advisory boundaries;
2. indexes original evidence by stable record identifier;
3. maps agreement signals to aligned findings;
4. maps all divergence signals to divergent findings;
5. maps all minority identifiers and unmatched evidence to minority evidence;
6. aggregates assumptions, limitations, diagnostics, provenance, and traceability without losing attribution;
7. creates unresolved questions from insufficient evidence, unresolved divergence, missing references, or policy-defined gaps;
8. produces a bounded summary appropriate to the assessment category;
9. emits the complete ordered result without modifying its inputs.

It does not recollect evidence, reevaluate consensus, invoke agents, select providers, perform runtime orchestration, or make governance decisions.

## 5. Required Output Structure

Every `SynthesisResult` contains these sections in this order, including explicit empty states:

### 5.1 Summary

A concise description of what the evidence supports, the advisory alignment category, and any material qualification. It must distinguish alignment from correctness. If divergence or insufficiency exists, that condition appears in the summary rather than only in later sections.

### 5.2 Aligned Findings

Claims represented by `AgreementSignal` values or otherwise supported as aligned under the supplied assessment. Each finding cites contributing evidence identifiers. Exact and compatible agreement remain distinguishable.

### 5.3 Divergent Findings

Every `DivergenceSignal`, its conflicting claims, materiality, resolution state, rationale, and evidence identifiers. Unresolved material divergence cannot be collapsed, softened into agreement, or relegated only to diagnostics.

### 5.4 Minority Evidence

Every assessment-designated minority record and any evidence left unmatched by agreement/divergence mappings. The section presents the claim and context without calling it weaker, lower-ranked, or less credible because fewer sources express it.

### 5.5 Assumptions

All material evidence and assessment assumptions, deduplicated for presentation but retaining record-level attribution. Conflicting assumptions are also represented in divergent findings.

### 5.6 Limitations

All material limitations from evidence and assessment, with attribution. Limitations are never converted into confidence adjustments.

### 5.7 Diagnostics

Evidence, assessment, validation, and synthesis diagnostics. Diagnostics describe processing or interpretive conditions and carry no authority or quality score.

### 5.8 Provenance

Source agent role, fulfilled capability, evidence record identifier, and original provenance for every included record. Provider/model identity may appear here only as descriptive origin metadata. No identity is summarized as competence, reliability, preference, or authority.

### 5.9 Traceability

Evidence record, step, trace, and correlation identifiers plus mappings from synthesized statements to source records. The mapping must permit reconstruction of every section from original evidence and assessment signals.

### 5.10 Unresolved Questions

Questions or evidence gaps arising from unresolved material divergence, partial alignment, insufficient evidence, missing references, assumptions requiring validation, or limiting diagnostics. This section requests or describes needed evidence; it does not invent a resolution.

## 6. Category-Specific Synthesis Behavior

### 6.1 Exact Agreement Synthesis

- State that all comparable material claims are aligned under the policy.
- Present the common claims in aligned findings with every contributing record.
- Preserve all qualifications, provenance, assumptions, limitations, and diagnostics.
- Do not describe exact agreement as verified truth or increased confidence.
- Keep divergent and minority sections with explicit empty states if none exist.

### 6.2 Compatible Agreement Synthesis

- Present the materially compatible conclusion and retain meaningful wording or granularity differences.
- Identify the policy-defined compatibility relationship.
- Preserve every contributing record and qualification.
- Do not rewrite distinct claims as textually identical or imply greater reliability.

### 6.3 Partial Agreement Synthesis

- State the aligned portion and the unaligned portion separately in the summary.
- Put shared claims in aligned findings.
- Put unmatched or differing claims in divergent findings or minority evidence as classified.
- Create unresolved questions for material gaps that synthesis cannot answer.
- Never use the aligned portion to conceal or dismiss the remainder.

### 6.4 Material Divergence Synthesis

- Lead the summary with the presence of unresolved material divergence.
- Present each competing proposition symmetrically with supporting evidence identifiers.
- Preserve every unresolved divergence and associated minority evidence.
- Avoid a single recommended conclusion unless separately and explicitly supplied as non-governance evidence; even then, competing evidence remains visible.
- Create unresolved questions describing the evidence needed to distinguish the positions.

### 6.5 Insufficient Evidence Response

- State that the available evidence does not support meaningful alignment or a complete synthesis.
- Present the evidence that does exist without extrapolation.
- Use explicit empty states for unsupported findings.
- Surface missing claims, incomparable scopes, absent support, or blocking diagnostics as unresolved questions.
- Do not characterize insufficiency as low confidence, agent failure, disagreement, or governance rejection.

## 7. Preservation and Referential Integrity

The synthesizer must account for every input evidence record. Each record appears in at least one content, provenance, or traceability section. Records referenced by minority or divergence fields must appear in the corresponding visible section.

If assessment references are missing, mixed-scope, or inconsistent, synthesis must not silently continue as if alignment were complete. The result either fails validation or produces a clearly diagnosed bounded response according to policy. The original evidence and assessment remain unchanged.

Deduplication is presentational only. It may combine identical statements while retaining all contributing record identifiers; it may not delete distinct assumptions, limitations, qualifications, or provenance.

## 8. Determinism

For the same validated input and policy version, the result must be identical. Determinism requires:

- stable section order defined in Section 5;
- stable ordering by normalized statement then evidence identifier;
- stable identifier generation from scope, policy, and input identifiers;
- deterministic aggregation and deduplication;
- no dependence on arrival order, provider/model identity, runtime state, or agent count;
- explicit empty-section representation.

Determinism does not grant authority or correctness.

## 9. Governance Boundary

Synthesis is not ratification, approval, certification, authorization, Board consensus, or a substitute for human decision records. It cannot create policy, resolve escalation, or apply GG-02 voting mechanics.

When evidence concerns governance, the result may organize material for Board review only. All governance decisions remain exclusively governed by GG-02 and the recorded Board process.

## 10. Failure and Diagnostic Behavior

The architecture requires explicit validation failure or visible diagnostics for:

- missing or duplicate evidence record identifiers;
- assessment references that do not resolve to evidence;
- a non-advisory consensus assessment;
- unsupported consensus categories;
- mixed synthesis scopes;
- missing traceability required by policy;
- authoritative, scoring, confidence-adjustment, ranking, voting, or governance instructions;
- a policy rule based on provider/model identity;
- an attempted omission of minority or unresolved divergent evidence;
- ambiguous normalization or non-deterministic ordering.

Validation failure must not be rewritten as exact, compatible, or partial agreement.

## 11. Risks and Mitigations

| Risk | Impact | Architectural mitigation |
| --- | --- | --- |
| A fluent summary overstates correctness. | Readers may treat aligned evidence as verified truth. | Require categorical qualification and distinguish alignment from correctness. |
| Divergence is buried below the summary. | Material conflict may be missed. | Require divergence in the summary and a dedicated visible section. |
| Minority evidence is compressed away. | Apparent unanimity may be fabricated. | Account for every record and require a minority section with explicit mappings. |
| Deduplication loses attribution or qualifications. | Traceability and nuance may be lost. | Deduplicate presentation only while retaining all sources, assumptions, and limitations. |
| Provider/model provenance becomes implicit authority. | Identity bias may shape inclusion or prominence. | Confine identity to provenance and prohibit identity-dependent policy rules. |
| Consensus category becomes a confidence proxy. | Synthesis may alter governed confidence semantics. | Prohibit confidence fields and describe categories only as evidence relationships. |
| Missing assessment references are ignored. | Output may misrepresent the evidence set. | Enforce referential integrity and bounded failure behavior. |
| Unresolved questions are presented as recommendations. | Synthesis may appear to decide action. | Phrase gaps as evidence needs and keep action/governance decisions outside scope. |
| Structured output is mistaken for governance approval. | GG-02 could be bypassed. | Mark result descriptive/advisory and preserve an explicit governance boundary statement. |

## 12. Reference Implementation Preconditions

A reference implementation may proceed only if it:

- remains isolated under the non-LOCKED Phase2C reference area;
- accepts EvidenceBundle-like and advisory ConsensusAssessment-like inputs only;
- implements every required section and explicit empty states;
- validates assessment-to-evidence referential integrity;
- tests all five category-specific behaviors;
- proves preservation of minority evidence and unresolved divergence;
- proves provider/model identity affects provenance output only;
- preserves assumptions, limitations, diagnostics, provenance, and trace identifiers;
- exposes no authority, scoring, confidence, ranking, voting, or governance semantics;
- makes no runtime orchestration, Local AI, or LOCKED component change.

## 13. Recommendation

READY FOR REFERENCE IMPLEMENTATION
