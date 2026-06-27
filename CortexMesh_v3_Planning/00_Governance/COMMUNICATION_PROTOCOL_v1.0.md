# COMMUNICATION_PROTOCOL_v1.0

Status: PROPOSED

## Purpose

Define the standard communication protocol for CortexMesh governance activities.

Objectives:

- reduce conversational overhead
- improve traceability
- maintain an auditable decision trail
- distinguish governance discussion from execution work

## CP-01 — Board-to-Board Communication

All communications between board members shall be produced as standalone Markdown files.

## CP-02 — Sender Identification

Every board communication must identify sender and role.

Required header:

```text
Communication ID:
Author:
Role:
Recipient:
Session:
Classification:
```

## CP-03 — Product Owner Mediation

Saleem acts as Product Owner and communication coordinator.

Board members provide instructions to Saleem.

Saleem executes work and reports results.

## CP-04 — Direct Instructions to Saleem

Instructions intended for Saleem may remain conversational.

They should be explicit, sequential, and actionable.

## CP-05 — Saleem Progress Reports

Saleem reports should include:

* OBSERVED actions completed
* commit IDs
* remaining work
* known limitations

Execution reports do not create governance decisions.

## CP-06 — Governance Decisions

Governance decisions are created only by board vote.

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

Use:

* OBSERVED
* INFERRED
* PROPOSED
* DECISION

Mixed classifications must be explicitly separated.

## CP-10 — Exception

Direct discussion between Saleem and board members may remain conversational unless it enters the board record.
