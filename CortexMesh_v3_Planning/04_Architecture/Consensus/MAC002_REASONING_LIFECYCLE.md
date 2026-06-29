# MAC002 - Reasoning Lifecycle

Status: PROPOSED

---

## Purpose

Define the lifecycle by which independent reasoning progresses into evidence synthesis and governance review.

This document establishes the architectural sequence for collaborative reasoning.

It does not define implementation.

---

# Lifecycle

## RL-01 Intent

Human governance defines the objective.

---

## RL-02 Independent Analysis

Agents reason independently.

No inter-agent communication occurs.

---

## RL-03 Evidence Publication

Agents publish immutable reasoning packages.

Evidence includes:

- observations
- assumptions
- rationale
- uncertainty
- supporting references

---

## RL-04 Comparative Review

Evidence packages are compared.

Agreement and disagreement are identified.

No synthesis occurs.

---

## RL-05 Structured Challenge

Agents may examine conflicting evidence.

The purpose is clarification rather than persuasion.

Additional evidence may be produced.

---

## RL-06 Evidence Synthesis

The orchestration layer constructs a structured evidence package.

Minority findings remain visible.

No aggregate scoring occurs.

---

## RL-07 Recommendation

Recommendations are derived from the synthesized evidence.

Every recommendation remains traceable to its supporting evidence.

---

## RL-08 Governance Review

Human governance evaluates the recommendation.

Final authority remains external to the reasoning lifecycle.

---

# Characteristics

The lifecycle is:

- evidence-first
- asynchronous
- reproducible
- auditable
- provider independent

---

# Relationship

Derived from:

- AI006 Decision Model
- AI007 Agent Interaction Model
- MAC001 Consensus Principles

Provides input to:

- MAC003 Evidence Synthesis
- MAC004 Disagreement Protocol
- MAC005 Reference Architecture
