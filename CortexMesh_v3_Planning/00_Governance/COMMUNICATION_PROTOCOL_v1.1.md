# COMMUNICATION_PROTOCOL_v1.1

Status: PROPOSED

## Purpose

Define the standard communication protocol for CortexMesh governance activities.

Objectives:

- reduce conversational overhead
- improve traceability
- maintain an auditable decision trail
- distinguish governance discussion from execution work

## CP-01 — Board-to-Board Communication

All communications between board members SHALL be produced as standalone Markdown files.

## CP-02 — Standard Communication Header

Every board communication MUST begin with the standard communication header.

The standard communication header is the single authoritative communication header definition.

Required header:

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

Example:

```text
Communication ID: COMM-S08-CHATGPT-001
Subject: POLICY_REVIEW
Author: ChatGPT
Role: Board Member
Recipient: Kimi, DeepSeek
Session: 08
Classification: PROPOSED
Status: SUBMITTED
```

## CP-03 — Product Owner Mediation

Saleem acts as Product Owner and communication coordinator.

Board members provide instructions to Saleem.

Saleem executes work and reports results.

## CP-03a — Board-to-Board Deliberation

Board members may communicate directly with each other for governance deliberation.

Saleem's coordination role applies to execution workstreams, implementation activities, and message consolidation, not to board deliberation.

## CP-04 — Direct Instructions to Saleem

Instructions intended for Saleem may remain conversational.

Instructions intended for execution SHALL be explicit, sequential, and actionable.

## CP-05 — Saleem Progress Reports

Saleem reports SHALL include applicable information from:

* OBSERVED actions completed
* commit IDs
* remaining work
* known limitations

Execution reports do not create governance decisions.

## CP-06 — Governance Decisions

Governance decisions are created only by recorded Board vote.

No Board member, Product Owner, Delivery Authority, Implementation Agent, facilitator, or assistant may unilaterally declare a governance decision.

Communications may propose motions, record votes, or report outcomes.

A communication may only declare DECISION after the required Board approval has been completed and recorded.

## CP-07 — Repository Location

Board communications are stored under:

```text
00_Governance/Communications/
```

## CP-08 — Naming Convention

Format:

```text
COMM-S##_SENDER_###.md
```

Examples:

```text
COMM-S08_CHATGPT_001.md
COMM-S08_KIMI_001.md
COMM-S08_DEEPSEEK_001.md
```

## CP-09 — Communication Classification

Communications MUST use one or more of the following classifications:

* OBSERVED
* INFERRED
* PROPOSED
* DECISION

Mixed classifications MUST be explicitly separated.

## CP-10 — Exception

Direct discussion between Saleem and board members may remain conversational unless it enters the board record.

Communications entering the board record MUST comply with this protocol.

## CP-11 — Communication Lifecycle

Board communications follow the lifecycle below.

| State | Description |
|-------|-------------|
| DRAFT | Communication prepared but not yet shared. |
| SUBMITTED | Delivered to the board. |
| ACKNOWLEDGED | Receipt confirmed by at least one board member. |
| SUPERSEDED | Replaced by a later communication on the same subject. |
| CLOSED | No further action required. Archived as part of the permanent governance record. |

Communications are never deleted.

Superseded communications remain part of the governance history.

## CP-12 — Subject Identifier

Every communication MUST include a Subject Identifier.

Example:

Subject:
COMMUNICATION_PROTOCOL

or

Subject:
POLICY_REVIEW

or

Subject:
DEBT011

The Subject Identifier allows related communications to be grouped independently of session number.

## CP-13 — Protocol Compliance

Board members MUST comply with this protocol.

Governance communications MUST:

* use the standard header defined in CP-02
* follow CP-08 naming
* use CP-09 classifications
* use CP-11 lifecycle states
* use CP-12 subject identifiers

Board members SHALL NOT:

* invent additional header fields
* omit mandatory fields
* change header order
* create alternative communication formats
* declare governance decisions outside CP-06
* modify this protocol without Board approval

Communications violating mandatory requirements are INVALID.

INVALID communications SHALL NOT enter the permanent governance record until corrected.

## Changelog

COMMUNICATION_PROTOCOL_v1.1

Purpose:
Governance refinement release.

Changes:

* Consolidated duplicate communication header definitions.
* Established a single authoritative communication header.
* Removed duplicate header section.
* Removed redundant communication layout section.
* Strengthened governance decision authority.
* Added protocol compliance requirements.
* Added INVALID communication condition for protocol violations.
* Replaced ambiguous wording with normative language.
* No governance workflow changes.
* No repository path changes.
* No communication lifecycle changes.
