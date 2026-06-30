# MAC004 - Consensus Convergence

Status: PROPOSED

---

## Purpose

Define how multiple independent agent outputs are transformed into a single governed consensus while preserving evidence integrity, minority opinions, and complete auditability.

Consensus convergence organizes synthesized evidence into a consensus package suitable for final decision preparation.

It does not determine truth, replace governance, rank agents, or discard evidence.

---

# Design Goals

Consensus convergence shall:

- preserve all evidence produced during the reasoning cycle
- maintain traceability from each conclusion to supporting evidence
- preserve minority positions as first-class architectural artifacts
- derive confidence from evidence quality rather than voting alone
- remain deterministic and reproducible where inputs, policies, and orchestration state are identical
- support human governance review without transferring authority to the system

---

# Consensus Principles

Consensus is evidence convergence.

Consensus is not unanimity.

Consensus is not voting.

Consensus is not authority.

Consensus exists to prepare evidence-backed conclusions for governed decision review.

Disagreement remains evidence throughout the convergence process.

---

# Convergence Workflow

## 1. Receive Evidence Package

The convergence workflow begins with the Evidence Package defined by MAC003.

The package includes:

- objective
- independent findings
- assumptions
- supporting evidence
- challenges
- minority findings
- synthesized observations
- recommendation candidates

---

## 2. Validate Evidence Integrity

The orchestration layer verifies that required evidence package elements are present.

Validation confirms structure, traceability, and provenance.

Validation does not evaluate agent capability.

---

## 3. Group Compatible Findings

Findings are grouped by objective, claim, supporting evidence, assumptions, and uncertainty.

Compatible findings may support a shared conclusion.

Incompatible findings remain preserved for minority or conflict handling.

---

## 4. Identify Converged Conclusions

A converged conclusion is a conclusion supported by one or more evidence-backed findings.

Convergence depends on:

- traceable supporting evidence
- corroboration across independent findings
- consistency with governing intent
- documented assumptions
- explicit uncertainty

Convergence does not require unanimity.

---

## 5. Preserve Minority Positions

Minority positions are retained with their supporting evidence, rationale, assumptions, and uncertainty.

Minority positions may become governance conditions, review flags, or future evidence requirements.

They are never removed because they lack majority support.

---

## 6. Assign Consensus Confidence

Consensus confidence is assigned to each converged conclusion.

Confidence reflects evidence quality and unresolved uncertainty.

Confidence does not describe agent capability.

---

## 7. Produce Consensus Package

The output of convergence is a Consensus Package.

Each Consensus Package shall contain:

- objective
- converged conclusions
- supporting evidence references
- recommendation candidates
- confidence context
- preserved minority positions
- unresolved conflicts
- escalation requirements
- audit trail

---

# Majority vs Minority Handling

Majority support may indicate corroboration.

Majority support does not establish truth.

Minority support may indicate uncertainty, omitted evidence, alternative assumptions, or risk.

The architecture shall preserve:

- majority-aligned conclusions
- minority findings
- dissenting rationale
- supporting evidence for each position
- unresolved assumptions
- governance implications

No finding is discarded solely because it is held by fewer agents.

---

# Confidence Aggregation

Confidence aggregation describes the confidence of a conclusion or recommendation candidate.

It never describes the quality of an agent.

Confidence aggregation considers:

- evidence traceability
- evidence corroboration
- evidence completeness
- consistency across independent findings
- unresolved uncertainty
- unresolved conflicts
- quality of supporting references and artifacts

The number of aligned findings may be recorded as corroboration context.

Numerical support alone shall not determine confidence.

Confidence may be represented using categories such as:

- High
- Moderate
- Low
- Insufficient Evidence

The assignment methodology is implementation-specific.

---

# Evidence Preservation

Consensus convergence must never discard evidence.

The Evidence Repository remains the authoritative source for reasoning artifacts.

The Consensus Package references evidence rather than replacing it.

Preserved evidence includes:

- original independent findings
- assumptions
- reasoning
- supporting references
- challenge records
- revised evidence
- minority findings
- unresolved conflicts
- confidence rationale

Evidence preservation supports reproducibility, auditability, and governance review.

---

# Conflict Resolution

Conflict resolution organizes disagreement into governed outcomes.

It does not suppress disagreement.

Conflicts may be resolved by:

- identifying compatible assumptions
- separating conclusions by scope
- recording uncertainty
- requesting additional evidence
- preserving unresolved disagreement
- escalating to human governance

If conflict cannot be resolved through evidence, it remains recorded as an unresolved conflict.

Unresolved conflict may reduce confidence or prevent a final recommendation from being formed.

---

# Deadlock / Escalation Rules

A deadlock exists when convergence cannot produce a governed consensus package without exceeding architectural authority.

Deadlock conditions include:

- missing required evidence
- contradictory evidence with no resolution path
- incompatible assumptions that materially affect conclusions
- insufficient confidence for recommendation preparation
- governance constraints that cannot be satisfied
- authority questions outside orchestration responsibility

When deadlock occurs:

1. Preserve all evidence.
2. Record the deadlock condition.
3. Identify the affected conclusions or recommendation candidates.
4. Document evidence required to continue.
5. Escalate to human governance.

No automated mechanism may override deadlock by electing a winner.

---

# Human Governance Integration

Human governance remains authoritative.

Consensus convergence prepares evidence-backed conclusions for review.

Governance may:

- accept the consensus package
- request additional evidence
- accept a minority position
- reject a recommendation candidate
- revise the objective or constraints
- defer the decision

The system may support governance review.

It shall not approve, reject, or implement governance decisions autonomously.

---

# Audit & Traceability

Every converged conclusion shall reference supporting evidence.

Every confidence assignment shall include confidence context.

Every minority position shall remain traceable to its source evidence.

Every escalation shall include the triggering condition and affected evidence.

The audit trail shall preserve:

- objective
- input evidence package
- convergence rules applied
- grouped findings
- conclusion mappings
- confidence context
- minority findings
- unresolved conflicts
- governance handoff

---

# Architectural Characteristics

Consensus convergence is:

- evidence-first
- deterministic where inputs, policies, and orchestration state are identical
- reproducible
- auditable
- non-competitive
- provider independent
- implementation independent
- governance constrained

---

# Example Execution Flow

1. Human governance defines an objective.
2. Agents perform independent reasoning.
3. Agents publish immutable evidence.
4. Comparative review identifies convergence and divergence.
5. Structured challenge produces additional evidence.
6. MAC003 synthesizes the evidence into an Evidence Package.
7. MAC004 validates the package and groups compatible findings.
8. Converged conclusions are formed with supporting evidence references.
9. Minority positions and unresolved conflicts are preserved.
10. Consensus confidence is assigned from evidence quality.
11. A Consensus Package is produced for final decision preparation.
12. Human governance remains the final authority.

---

# Relationship

Derived from:

- AI004 Core Architectural Principles
- AI005 System Model
- AI006 Decision Model
- AI007 Agent Interaction Model
- AI010 Authority Architecture
- AI011 Security and Trust Model
- MAC001 Consensus Principles
- MAC002 Reasoning Lifecycle
- MAC003 Evidence Synthesis

Provides input to:

- MAC005 Final Decision Architecture
