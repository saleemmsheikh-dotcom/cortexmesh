# COMMUNICATION_PROTOCOL_v1.0

Status: PROPOSED

## Purpose

Define the standard communication protocol for CortexMesh governance activities.

Objectives:

- reduce conversational overhead
- improve traceability
- maintain an auditable decision trail
- distinguish governance discussion from execution work

## CP-01 - Board-to-Board Communication

All communications between board members shall be produced as standalone Markdown files.

## CP-02 - Sender Identification

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

## CP-03 - Product Owner Mediation

Saleem acts as Product Owner and communication coordinator.

Board members provide instructions to Saleem.

Saleem executes work and reports results.

## CP-03a - Board-to-Board Deliberation

Board members may communicate directly with each other for governance deliberation.

Saleem's coordination role applies to execution workstreams, implementation activities, and message consolidation, not to board deliberation.

## CP-04 - Direct Instructions to Saleem

Instructions intended for Saleem may remain conversational.

They should be explicit, sequential, and actionable.

## CP-05 - Saleem Progress Reports

Saleem reports should include:

- OBSERVED actions completed
- commit IDs
- remaining work
- known limitations

Execution reports do not create governance decisions.

## CP-06 - Governance Decisions

Governance decisions are created only by board vote.

## CP-07 - Repository Location

Board communications are stored under:

```text
00_Governance/Communications/
```

## CP-08 - Naming Convention

Format:

```text
COMM-S##-SENDER-###.md
```

Examples:

```text
COMM-S11-SALEEM-001.md
COMM-S11-KIMI-001.md
COMM-S11-CHATGPT-001.md
COMM-S11-DEEPSEEK-001.md
```

## CP-09 - Communication Classification

Use:

- OBSERVED
- INFERRED
- PROPOSED
- DECISION

Mixed classifications must be explicitly separated.

## CP-10 - Exception

Direct discussion between Saleem and board members may remain conversational unless it enters the board record.

## CP-11 - Communication Lifecycle

Board communications follow the lifecycle below.

| State | Description |
| ----- | ----------- |
| DRAFT | Communication prepared but not yet shared. |
| SUBMITTED | Delivered to the board. |
| ACKNOWLEDGED | Receipt confirmed by at least one board member. |
| SUPERSEDED | Replaced by a later communication on the same subject. |
| CLOSED | No further action required. Archived as part of the permanent governance record. |

Communications are never deleted.

Superseded communications remain part of the governance history.

## CP-12 - Subject Identifier

Every communication shall include a Subject Identifier.

Example:

```text
Subject:
COMMUNICATION_PROTOCOL
```

or

```text
Subject:
POLICY_REVIEW
```

or

```text
Subject:
DEBT011
```

The Subject Identifier allows related communications to be grouped independently of session number.

## CP-13 - Standard Communication Header

Every board communication shall begin with:

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

## CP-14 - Standard Board Communication Format

All new Session 11 board communications shall use the following standard format:

```text
Communication ID: COMM-S11-<AUTHOR>-###
Subject: <Subject>
Author: <Author>
Role: <Role>
Recipient: <Recipients>
Session: 11
Classification: <OBSERVED | INFERRED | PROPOSED | DECISION>
Status: <DRAFT | SUBMITTED | ACKNOWLEDGED | SUPERSEDED | CLOSED>
```

The communication body shall preserve the following sections where applicable:

- OBSERVED
- INFERRED
- PROPOSED
- DECISION
- COMMANDS
- REMAINING WORK
- KNOWN LIMITATIONS
- REFERENCES

Sections that do not apply may be omitted.

Mixed classifications shall remain explicitly separated into their applicable sections.

## CP-15 - Commands Section

When a board communication includes execution instructions, repository commands, file paths, or procedural steps, it shall include a COMMANDS section.

The COMMANDS section shall:

- preserve command ordering;
- identify commands intended for execution;
- distinguish commands from governance decisions;
- avoid implying authorization beyond the communication's classification and status.

Commands included in a communication are instructions or evidence unless separately approved as governance decisions.

