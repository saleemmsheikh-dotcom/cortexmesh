# COMMUNICATION_PROTOCOL_v1.1

**Status:** PROPOSED

---

# Purpose

Define the mandatory communication protocol for CortexMesh governance activities.

Objectives:

* reduce conversational overhead
* improve traceability
* maintain an auditable decision trail
* distinguish governance discussion from execution work
* ensure deterministic governance communications

---

## CP-01 — Board-to-Board Communication

All governance communications between Board members SHALL be produced as standalone Markdown files.

Communications not intended for the governance record MAY remain conversational.

---

## CP-02 — Standard Communication Header

Every governance communication MUST begin with the following header in the exact order shown.

```text
Communication ID:
Subject:
Author:
Role:
Recipient:
Session:
Classification:
Status:
```

This is the single authoritative communication header.

No additional header fields SHALL be added.

No mandatory header fields SHALL be omitted.

Header field order SHALL NOT be modified.

---

## CP-03 — Product Owner Mediation

Saleem acts as Product Owner and communication coordinator.

Board members provide governance instructions to Saleem.

Saleem executes approved work and reports implementation progress.

Execution activities do not create governance authority.

---

## CP-03a — Board Deliberation

Board members MAY communicate directly for governance deliberation.

Saleem's coordination role applies to execution activities and communication management.

Governance authority remains with the Board.

---

## CP-04 — Direct Instructions

Instructions intended for Saleem MAY remain conversational.

Instructions intended for execution SHALL be:

* explicit
* sequential
* actionable

---

## CP-05 — Progress Reports

Execution reports SHALL include applicable information from:

* observed work completed
* commit identifiers
* remaining work
* known limitations

Execution reports SHALL NOT create governance decisions.

---

## CP-06 — Governance Decisions

Governance decisions are created only by recorded Board vote.

No Board member, Product Owner, Delivery Authority, Implementation Agent, facilitator, assistant, or automation may unilaterally declare a governance decision.

Communications MAY:

* propose motions
* record votes
* report outcomes

A communication SHALL use the classification **DECISION** only after the required Board approval has been completed and recorded.

---

## CP-07 — Repository Location

Board communications SHALL be stored under:

```text
00_Governance/Communications/
```

---

## CP-08 — Naming Convention

Communication IDs SHALL use hyphens.

```text
COMM-S##-AUTHOR-###
```

Communication filenames SHALL use underscores.

```text
COMM-S##_AUTHOR_###.md
```

Example:

```text
Communication ID:
COMM-S11-CHATGPT-001

Filename:
COMM-S11_CHATGPT_001.md
```

Communication identifiers SHALL be unique.

Sequence numbers SHALL be sequential for each author within a session.

---

## CP-09 — Communication Classification

Each communication SHALL contain exactly one header Classification.

Permitted values are:

* OBSERVED
* INFERRED
* PROPOSED
* DECISION

Where multiple content types exist within the communication body, they SHALL be separated using section headings.

The header Classification SHALL identify the primary purpose of the communication.

---

## CP-10 — Conversational Exception

Direct discussion between Saleem and Board members MAY remain conversational unless intended for the governance record.

Communications entering the governance record SHALL comply with this protocol.

---

## CP-11 — Communication Lifecycle

Governance communications SHALL follow the lifecycle below.

| State        | Description                              |
| ------------ | ---------------------------------------- |
| DRAFT        | Prepared but not shared                  |
| SUBMITTED    | Delivered for review                     |
| ACKNOWLEDGED | Receipt confirmed                        |
| SUPERSEDED   | Replaced by a later communication        |
| CLOSED       | Archived with no further action required |

Communications SHALL NOT be deleted.

Superseded communications remain part of the governance record.

---

## CP-12 — Subject Identifier

Every governance communication MUST include a Subject Identifier.

The Subject identifies the governance topic independently of session number.

---

## CP-13 — Protocol Compliance

Compliance with this protocol is mandatory.

Governance communications MUST:

* comply with CP-02 header requirements
* comply with CP-08 naming convention
* comply with CP-09 classification rules
* comply with CP-11 lifecycle states
* comply with CP-12 subject requirements

Board members SHALL NOT:

* invent additional header fields
* omit mandatory fields
* change header ordering
* create alternative communication formats
* declare governance decisions outside CP-06
* modify this protocol without Board approval

A communication that violates any mandatory requirement is **INVALID**.

INVALID is a compliance condition, not a lifecycle state.

INVALID communications SHALL NOT enter the governance record.

INVALID communications SHALL be corrected and resubmitted beginning at the DRAFT lifecycle state.

Protocol compliance SHALL be verified before a communication is accepted into the governance record.

---

# Changelog

## v1.1

* Consolidated duplicate communication header definitions.
* Established a single authoritative communication header.
* Strengthened governance decision authority.
* Clarified communication classification.
* Introduced mandatory protocol compliance requirements.
* Defined INVALID as a compliance condition.
* Standardized normative language.
* Removed redundant communication header duplication.
* Removed redundant communication layout guidance.
* No governance workflow changes.
* No repository structure changes.
* No lifecycle changes.
