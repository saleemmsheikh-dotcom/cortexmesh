# IMP003 - Module Dependency Architecture

Status: PROPOSED

---

# Purpose

Define the implementation dependency architecture for CortexMesh.

Dependency architecture is required so that implementation can proceed without weakening the approved architectural boundaries.

This document describes module ownership, dependency direction, execution ordering, state boundaries, error propagation, and extension constraints.

It does not select technologies, programming languages, databases, frameworks, infrastructure, or deployment environments.

It does not introduce new architecture.

---

# Architectural Principles

Implementation dependencies shall preserve the approved CortexMesh architecture.

Dependencies shall follow these principles:

- loose coupling
- high cohesion
- deterministic execution where inputs, policies, configuration, and orchestration state are identical
- reproducibility through stable artifact identity and provenance
- evidence traceability
- governance compliance
- separation of responsibilities
- explicit ownership boundaries
- immutable evidence references after publication
- human governance authority over final governed decisions

Implementation dependencies shall not:

- rank agents
- elect winners
- suppress minority findings
- discard evidence to resolve conflicts
- assign confidence from voting alone
- convert consensus into final authority
- approve final decisions without human governance action

---

# Module Inventory

The following modules are derived from IMP001 and constrained by IMP002.

## Governance Review Module

Purpose:
Support human governance review of objectives, governance decision packages, escalations, and governed outcomes.

Responsibilities:

- receive Governance Decision Packages
- support approval, rejection, revision, deferral, or escalation
- provide governed outcomes to the Decision Record Module
- preserve human governance authority

Inputs:

- Governance Decision Package
- escalation records
- governance context
- supporting artifact references

Outputs:

- governance action
- governed outcome
- decision record input
- escalation disposition where applicable

Dependencies:

- Authority Decision Module
- Decision Record Module
- Audit Log Module
- Governance Policy Adapter

Governance Constraints:

- shall not be bypassed for final governed decisions
- shall not be replaced by automated authority
- shall retain final authority for approval, rejection, deferral, revision, and escalation

---

## Governance Policy Adapter

Purpose:
Expose governance constraints to implementation modules without transferring governance authority to them.

Responsibilities:

- provide policy references and constraints to execution modules
- provide authority constraints to the Authority Decision Module
- support reproducible policy context
- avoid embedding unapproved governance logic

Inputs:

- approved governance policy references
- Board decision references where applicable
- lifecycle context

Outputs:

- governance constraint references
- authority constraint context
- policy provenance references

Dependencies:

- Governance Review Module
- Audit Log Module

Governance Constraints:

- shall represent recorded governance policy only
- shall not create new governance rules
- shall not approve decisions

---

## Intent Intake Module

Purpose:
Capture the governed objective that starts the reasoning lifecycle.

Responsibilities:

- record objective identity
- record governing intent
- record constraints and review context
- initiate orchestration through the Orchestration Command Interface

Inputs:

- governed objective
- governance constraints
- reproducibility context
- review requirements

Outputs:

- objective artifact
- lifecycle start request
- orchestration command
- audit event

Dependencies:

- Governance Review Module
- Governance Policy Adapter
- Orchestration Runtime
- Audit Log Module

Governance Constraints:

- shall not transform objective intake into decision approval
- shall preserve governing intent as an auditable artifact

---

## Orchestration Runtime

Purpose:
Coordinate lifecycle execution, routing, ordering, and module invocation.

Responsibilities:

- create lifecycle state
- dispatch independent reasoning tasks
- enforce lifecycle ordering
- route artifacts to the next eligible module
- trigger escalation when authority or validation constraints fail

Inputs:

- orchestration command
- objective artifact
- governance constraints
- lifecycle configuration

Outputs:

- lifecycle state
- agent task requests
- lifecycle transition records
- escalation records
- audit events

Dependencies:

- Intent Intake Module
- Governance Policy Adapter
- Agent Adapter Interface
- Evidence Publication Module
- Audit Log Module

Governance Constraints:

- shall coordinate workflow only
- shall not determine outcomes
- shall not bypass required evidence or governance checkpoints

---

## Agent Adapter Interface

Purpose:
Provide the boundary through which independent reasoning agents receive tasks and return reasoning outputs.

Responsibilities:

- receive agent task requests
- preserve independent reasoning before comparative review
- collect agent outputs
- transfer outputs to Evidence Publication

Inputs:

- agent task request
- objective reference
- task context
- evidence publication requirements

Outputs:

- agent output artifact
- reasoning summary
- assumptions
- uncertainty
- supporting references

Dependencies:

- Orchestration Runtime
- Evidence Publication Module
- Audit Log Module

Governance Constraints:

- shall not assign agent rank
- shall not assign vote weight
- shall not approve findings
- shall not mutate published evidence

---

## Evidence Publication Module

Purpose:
Validate and publish reasoning outputs as immutable evidence artifacts for the current lifecycle.

Responsibilities:

- validate evidence object structure
- assign or confirm stable artifact identity
- record provenance references
- publish evidence to the Evidence Repository
- reject or escalate invalid evidence submissions

Inputs:

- agent outputs
- challenge-derived evidence
- evidence validation context

Outputs:

- published Evidence Objects
- validation results
- escalation records where applicable
- audit events

Dependencies:

- Agent Adapter Interface
- Challenge Coordination Module
- Evidence Repository
- Audit Log Module

Governance Constraints:

- shall not discard invalid evidence silently
- shall not convert evidence publication into endorsement
- shall preserve rejected or escalated evidence attempts through audit events

---

## Evidence Repository

Purpose:
Serve as the authoritative repository for evidence artifacts, provenance, uncertainty, challenges, minority findings, and supporting references.

Responsibilities:

- store published Evidence Objects
- preserve artifact immutability within the lifecycle
- support evidence queries by stable reference
- preserve source-to-derived traceability
- maintain persistence boundaries for evidence artifacts

Inputs:

- published Evidence Objects
- evidence package references
- consensus package references
- decision provenance references

Outputs:

- evidence query results
- evidence references
- provenance chains
- recovery records where applicable

Dependencies:

- Evidence Publication Module
- Evidence Synthesis Module
- Consensus Convergence Module
- Authority Decision Module
- Decision Record Module
- Audit Log Module

Governance Constraints:

- shall not delete or suppress evidence to resolve conflicts
- shall not replace governance review
- shall preserve minority and unresolved conflict references

---

## Comparative Review Module

Purpose:
Compare published evidence to identify convergence candidates, divergence, complementary findings, and unanswered questions.

Responsibilities:

- query evidence artifacts
- compare findings against objective scope
- identify compatible finding candidates
- identify divergence and uncertainty
- produce review records

Inputs:

- objective reference
- published evidence references
- evidence query results

Outputs:

- convergence candidates
- divergence records
- complementary finding records
- unanswered question records
- audit events

Dependencies:

- Evidence Repository
- Challenge Coordination Module
- Audit Log Module

Governance Constraints:

- shall not produce recommendations
- shall not discard incompatible findings
- shall preserve uncertainty and divergence

---

## Challenge Coordination Module

Purpose:
Coordinate structured challenge activity that clarifies disagreement, uncertainty, and evidentiary gaps.

Responsibilities:

- receive comparative review records
- create challenge records
- route challenge activity
- publish challenge-derived evidence through Evidence Publication
- preserve unresolved disagreement

Inputs:

- convergence candidates
- divergence records
- unanswered questions
- challenge responses

Outputs:

- challenge records
- challenge evidence
- unresolved disagreement records
- audit events

Dependencies:

- Comparative Review Module
- Evidence Publication Module
- Evidence Repository
- Audit Log Module

Governance Constraints:

- shall treat challenges as evidence activity, not voting
- shall not suppress minority findings
- shall escalate unresolved conflicts when required

---

## Evidence Synthesis Module

Purpose:
Transform collected and challenged evidence into a MAC003 Evidence Package.

Responsibilities:

- collect evidence references
- validate Evidence Package structure
- synthesize supported observations
- preserve assumptions, uncertainty, challenges, and minority findings
- prepare recommendation candidates where supported by evidence

Inputs:

- objective reference
- published evidence references
- challenge records
- divergence records
- uncertainty records

Outputs:

- Evidence Package
- synthesized observations
- recommendation candidates
- audit events

Dependencies:

- Evidence Repository
- Challenge Coordination Module
- Consensus Convergence Module
- Audit Log Module

Governance Constraints:

- shall not determine objective truth
- shall not suppress divergence
- shall not assign confidence to agents
- shall preserve evidence references for every synthesized observation

---

## Consensus Convergence Module

Purpose:
Transform the Evidence Package into a MAC004 Consensus Package while preserving evidence integrity and minority positions.

Responsibilities:

- identify compatible finding groups
- produce converged conclusions
- preserve minority positions
- preserve unresolved conflicts
- aggregate confidence context from evidence quality
- identify escalation requirements

Inputs:

- Evidence Package
- evidence quality context
- governance constraints

Outputs:

- Consensus Package
- converged conclusions
- confidence context
- preserved minority positions
- unresolved conflict records
- escalation requirements

Dependencies:

- Evidence Synthesis Module
- Evidence Repository
- Recommendation Assembly Module
- Authority Decision Module
- Audit Log Module

Governance Constraints:

- shall not discard evidence
- shall not convert majority support into truth
- shall not assign confidence from voting alone
- shall not approve final decisions

---

## Recommendation Assembly Module

Purpose:
Prepare evidence-backed recommendation candidates for authority decision preparation.

Responsibilities:

- assemble recommendation candidates from evidence-backed conclusions
- preserve supporting evidence references
- preserve confidence and uncertainty context
- preserve minority and unresolved conflict references

Inputs:

- converged conclusions
- recommendation candidates from Evidence Package
- confidence context
- unresolved conflict records

Outputs:

- recommendation candidate package
- supporting evidence map
- uncertainty summary
- audit events

Dependencies:

- Consensus Convergence Module
- Evidence Repository
- Authority Decision Module
- Audit Log Module

Governance Constraints:

- shall not select a final decision
- shall not remove minority findings
- shall not present unsupported recommendations

---

## Authority Decision Module

Purpose:
Prepare Governance Decision Packages from converged consensus while enforcing authority constraints.

Responsibilities:

- validate governance readiness
- validate authority constraints
- assemble Decision Candidates
- preserve provenance chains
- prepare escalation routing where required
- present packages to Governance Review

Inputs:

- Consensus Package
- recommendation candidate package
- governance constraints
- evidence references
- escalation requirements

Outputs:

- Governance Decision Package
- Decision Candidate
- confidence and uncertainty report
- escalation record where applicable
- audit events

Dependencies:

- Consensus Convergence Module
- Recommendation Assembly Module
- Evidence Repository
- Governance Policy Adapter
- Governance Review Module
- Audit Log Module

Governance Constraints:

- shall not approve final decisions
- shall not bypass human governance
- shall not record governed outcomes
- shall escalate authority failures

---

## Decision Record Module

Purpose:
Record governed outcomes and preserve the complete decision provenance chain.

Responsibilities:

- receive governance action
- record governed outcome
- preserve decision provenance
- preserve confidence and uncertainty reporting
- preserve escalation outcomes
- link Decision Records to supporting artifacts

Inputs:

- governance action
- governed outcome
- Governance Decision Package reference
- Decision Candidate reference
- audit references

Outputs:

- Decision Record
- decision provenance chain
- audit events

Dependencies:

- Governance Review Module
- Authority Decision Module
- Evidence Repository
- Audit Log Module

Governance Constraints:

- shall not create a Decision Record without human governance action
- shall not alter supporting evidence
- shall preserve approval, rejection, deferral, revision, and escalation outcomes

---

## Audit Log Module

Purpose:
Record lifecycle events, artifact references, validation outcomes, failures, escalations, and governance actions.

Responsibilities:

- receive audit events from all modules
- preserve ordering metadata
- reference artifacts without replacing them
- support reproducibility and review
- support failure and recovery traceability

Inputs:

- audit events
- artifact references
- lifecycle references
- governance context
- error and escalation context

Outputs:

- audit records
- lifecycle event history
- traceability support records

Dependencies:

- all modules as event producers

Governance Constraints:

- shall not replace Evidence Objects, Consensus Packages, Governance Decision Packages, or Decision Records
- shall not approve decisions
- shall preserve traceability independently of operational success

---

# Dependency Rules

## Allowed Dependencies

Allowed dependencies are those required to preserve the approved lifecycle and interface contracts:

- downstream lifecycle dependencies through IMP002 interfaces
- read-only evidence queries through the Evidence Query Interface
- audit event submission from any module to the Audit Log Module
- governance constraint access through the Governance Policy Adapter
- escalation routing to Governance Review through approved escalation contracts
- Decision Record creation only after Governance Review provides a governance action

## Forbidden Dependencies

Implementation modules shall not depend on:

- agent identity to determine confidence
- vote counts to determine confidence
- provider identity to establish authority
- direct mutation of Evidence Repository artifacts after publication
- direct creation of Decision Records by non-governance modules
- direct final approval by orchestration, consensus, recommendation, authority, or agent modules
- bypass paths from agent outputs to recommendations without evidence publication
- bypass paths from consensus to Decision Records without Governance Review
- hidden dependencies that alter governance constraints outside recorded policy

## Dependency Direction

Primary dependency direction follows lifecycle order:

```text
Governance Review
        |
        v
Intent Intake
        |
        v
Orchestration Runtime
        |
        v
Agent Adapter Interface
        |
        v
Evidence Publication
        |
        v
Evidence Repository
        |
        v
Comparative Review
        |
        v
Challenge Coordination
        |
        v
Evidence Synthesis
        |
        v
Consensus Convergence
        |
        v
Recommendation Assembly
        |
        v
Authority Decision
        |
        v
Governance Review
        |
        v
Decision Record
```

The Audit Log Module receives events from all modules.

The Governance Policy Adapter provides constraints to modules but does not receive operational authority from them.

The Evidence Repository may be queried by review, synthesis, convergence, recommendation, authority, and decision modules, but published evidence remains immutable within the lifecycle.

## Ownership Boundaries

Each module owns its own produced artifacts.

Derived artifacts shall reference source artifacts rather than replacing them.

No module shall assume ownership of evidence produced by another module.

No module shall assume governance authority because it consumes governance constraints.

## Interface Requirements

Dependencies shall cross module boundaries through the interfaces defined in IMP002.

Implementation-specific schemas are deferred to later implementation design.

Interface contracts shall preserve:

- stable artifact identity
- lifecycle references
- objective references
- source references
- provenance references
- validation status
- audit references

## Evidence Boundaries

Evidence crosses module boundaries by reference after publication.

Evidence publication is the boundary between mutable submission and immutable lifecycle evidence.

Synthesis, convergence, recommendation, authority, and decision modules shall reference evidence rather than copying or rewriting evidence as authoritative source material.

## Governance Boundaries

Governance authority remains outside automated execution.

Implementation modules may prepare, validate, route, and record artifacts.

Implementation modules shall not approve, ratify, or authorize final governed decisions.

---

# Execution Order

Logical execution sequence:

1. Governance Review provides objective, constraints, and review context.
2. Intent Intake records the objective and initiates lifecycle state.
3. Orchestration Runtime creates lifecycle state and dispatches independent tasks.
4. Agent Adapter Interface routes tasks to independent agents.
5. Evidence Publication validates and publishes agent outputs.
6. Evidence Repository preserves published evidence and provenance.
7. Comparative Review identifies convergence candidates, divergence, complementary findings, and unanswered questions.
8. Challenge Coordination records structured challenges and challenge evidence.
9. Evidence Synthesis produces the MAC003 Evidence Package.
10. Consensus Convergence produces the MAC004 Consensus Package.
11. Recommendation Assembly prepares evidence-backed recommendation candidates.
12. Authority Decision prepares the MAC005 Governance Decision Package.
13. Governance Review determines the governed outcome.
14. Decision Record records the governed outcome and provenance chain.
15. Audit Log records lifecycle events across all stages.

Prerequisite relationships:

- Intent Intake requires a governed objective.
- Agent tasks require lifecycle state.
- Comparative Review requires published evidence.
- Challenge Coordination requires comparative review records or explicit challenge triggers.
- Evidence Synthesis requires evidence package inputs and validation context.
- Consensus Convergence requires a valid Evidence Package.
- Recommendation Assembly requires evidence-backed conclusions or recommendation candidates.
- Authority Decision requires a valid Consensus Package and governance constraints.
- Decision Record requires a governance action.

Lifecycle ordering shall be deterministic when the same inputs, governance policy, configuration, and orchestration state are used.

---

# State Management

## State Ownership

State ownership shall follow module responsibility:

| State Type | Owner |
| ---------- | ----- |
| Governance objective state | Intent Intake Module |
| Lifecycle state | Orchestration Runtime |
| Agent task state | Orchestration Runtime |
| Agent output submission state | Agent Adapter Interface |
| Evidence publication state | Evidence Publication Module |
| Evidence artifact state | Evidence Repository |
| Comparative review state | Comparative Review Module |
| Challenge state | Challenge Coordination Module |
| Evidence Package state | Evidence Synthesis Module |
| Consensus Package state | Consensus Convergence Module |
| Recommendation candidate state | Recommendation Assembly Module |
| Governance Decision Package state | Authority Decision Module |
| Decision Record state | Decision Record Module |
| Audit event state | Audit Log Module |

## State Transitions

State transitions shall be explicit, ordered, auditable, and reproducible.

A module may advance an artifact only when:

- required inputs are present
- validation succeeds
- source references are preserved
- governance constraints are satisfied
- audit events are recorded

Failed transitions shall produce error or escalation records.

## Persistence Boundaries

Persistence boundaries shall preserve the distinction between:

- lifecycle state
- evidence artifacts
- derived packages
- decision records
- audit records
- governance policy references

Implementation may choose later how to persist these categories.

This document does not define storage technology.

## Recovery Expectations

Recovery shall preserve:

- lifecycle identity
- objective reference
- evidence immutability
- provenance chains
- audit ordering
- governance constraints
- unresolved errors or escalations

Recovery shall not:

- regenerate evidence without preserving the original record
- delete failed evidence submissions
- reassign confidence from vote counts
- create final decisions without governance action

## Deterministic Behaviour Requirements

Deterministic behaviour requires:

- stable input artifact references
- stable governance policy references
- stable lifecycle ordering
- explicit configuration references
- audit ordering metadata
- documented variability where external reasoning outputs are nondeterministic

---

# Error Propagation

Errors shall propagate as traceable error records or escalation records.

## Failure Containment

Failure containment shall prevent one module failure from corrupting evidence, governance state, or decision records.

Modules shall fail closed when:

- required evidence is missing
- provenance is incomplete
- authority constraints fail
- confidence rationale is unsupported
- final decision recording is attempted without governance action

## Evidence Preservation

Errors shall not be resolved by deleting, overwriting, or suppressing evidence.

Invalid evidence submissions shall be recorded through validation outcomes and audit events.

Conflicting evidence shall be preserved and routed to challenge, convergence, escalation, or governance review as appropriate.

## Recovery Principles

Recovery shall resume from the last valid lifecycle state or require governance review when state validity cannot be established.

Recovery shall preserve all artifacts created before failure.

Recovery shall not create new governance authority.

## Escalation Boundaries

Escalation is required when:

- a module cannot validate required inputs
- evidence quality is insufficient for confidence assignment
- incompatible findings cannot be converged without governance judgment
- authority constraints fail
- governance action is required to proceed
- recovery cannot establish a reproducible state

Escalation shall route to human governance, request additional evidence, request objective revision, or record deferral as defined by IMP002.

---

# Extension Architecture

Extension architecture shall preserve approved boundaries.

## Extension Points

Permitted extension points include:

- additional agent adapters
- additional evidence object types consistent with MAC003
- additional challenge workflows consistent with MAC002 and IMP002
- additional confidence rationale fields tied to evidence quality
- additional audit event types
- additional reporting views over existing artifacts
- future governance-approved modules

## Future Modules

Future modules may be proposed for:

- intent resolution
- evidence quality review
- policy compliance review support
- audit reporting
- governance workflow support

Future modules remain candidates until approved through governance.

## Version Compatibility

Module changes shall preserve compatibility with:

- stable artifact identity
- source references
- evidence provenance
- audit references
- governance policy references
- Decision Record provenance

Breaking changes to artifact contracts require governance review before implementation.

## Governance Approval Requirements

Extensions require governance approval when they:

- alter governance authority
- alter evidence preservation rules
- alter confidence assignment rules
- alter decision recording behavior
- alter escalation routing
- change approved architecture boundaries
- affect LOCKED components or governed policy constraints

---

# Architectural Constraints

This document explicitly makes no:

- implementation technology decisions
- programming language assumptions
- database assumptions
- framework assumptions
- infrastructure assumptions
- deployment assumptions
- provider assumptions
- user interface assumptions

All implementation dependencies remain planning-level architectural dependencies.

Technology selection, schema implementation, deployment topology, and production code are deferred to later approved implementation work.

---

# Relationship to Previous Work

Derived from:

- IMP001 Implementation Mapping
- IMP002 Interface and Contract Specification
- AI004 Core Architectural Principles
- AI005 System Model
- AI006 Decision Model
- AI007 Agent Interaction Model
- AI008 Architectural Review
- AI009 Reference Architecture
- AI010 Authority Architecture
- AI011 Security and Trust Model
- MAC001 Consensus Principles
- MAC002 Reasoning Lifecycle
- MAC003 Evidence Synthesis
- MAC004 Consensus Convergence
- MAC005 Final Decision Architecture

Provides input to:

- IMP004 Verification & Test Architecture
- IMP005 Implementation Execution Plan

---

# Traceability Matrix

| Dependency Area | Source Documents |
| --------------- | ---------------- |
| Module inventory | IMP001 |
| Interface boundaries | IMP002 |
| Governance authority boundary | AI004, AI006, AI010, MAC005, IMP002 |
| Orchestration dependency direction | AI005, AI007, AI009, MAC002, IMP001 |
| Evidence publication and preservation | AI005, AI007, AI011, MAC002, MAC003, IMP002 |
| Comparative review and challenge | AI006, AI007, MAC002, IMP001, IMP002 |
| Evidence synthesis | MAC003, IMP001, IMP002 |
| Consensus convergence | MAC001, MAC004, IMP001, IMP002 |
| Recommendation assembly | AI006, AI007, MAC003, MAC004, IMP001 |
| Authority decision preparation | AI010, MAC005, IMP001, IMP002 |
| Decision records | AI006, AI010, MAC005, IMP001, IMP002 |
| Audit and recovery | AI005, AI011, MAC004, MAC005, IMP001, IMP002 |
| Extension constraints | AI004, AI005, AI011, MAC005, IMP002 |

---

# Completion Criteria

IMP003 is complete when:

- implementation dependencies are completely described
- module ownership is defined
- dependency direction is defined
- allowed and forbidden dependencies are defined
- execution ordering is defined
- state ownership is defined
- error propagation is defined
- extension boundaries are defined
- no technology assumptions exist
- architecture remains consistent with approved governance

---

# Risks & Assumptions

## Risks

- Hidden dependencies may bypass evidence publication if module boundaries are not enforced.
- Operational state may be mistaken for evidence provenance if persistence boundaries are not preserved.
- Convenience dependencies may allow recommendations or decisions to form without complete evidence references.
- Extension points may introduce new architecture if not governed.
- Recovery behavior may accidentally regenerate or overwrite evidence if immutability is not enforced.
- Governance support modules may be mistaken for governance authority.

## Assumptions

- IMP001 and IMP002 are approved implementation planning inputs.
- The governance checkpoint has authorized continuation of implementation planning.
- AI004-AI011 and MAC001-MAC005 remain the approved architecture baseline for this work package.
- Production implementation has not begun under this document.
- Detailed verification architecture is deferred to IMP004.
- Detailed execution planning is deferred to IMP005.
- Human governance remains the final authority.
