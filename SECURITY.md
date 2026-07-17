# CortexMesh Security Policy

## Project Status

CortexMesh is an engineering and research platform. It is not production-certified and makes no security-certification or service-level claim.

## Supported Versions

Security review is currently limited to the latest commit on the default branch.

| Version | Supported |
| --- | --- |
| Latest `main` | Yes |
| Historical commits, tags, and archived baselines | No active remediation commitment |

Historical evidence and sealed baselines may remain immutable even when later work identifies a limitation. Any correction must preserve the historical record.

## Reporting a Vulnerability

Do not open a GitHub issue containing exploit details, credentials, personal data, private infrastructure information, or instructions that would enable abuse.

GitHub private vulnerability reporting is not currently enabled for this repository. Contact the repository owner privately through the [GitHub profile](https://github.com/saleemmsheikh-dotcom) to request a secure reporting channel. In the initial contact, provide only:

- a short, non-sensitive description;
- the affected area;
- an assessment of urgency;
- a preferred secure contact method.

Provide technical details, proof of concept, logs, or sensitive artifacts only after a private channel has been established.

## What to Include Privately

- affected commit, component, and configuration;
- prerequisites and reproducible steps;
- expected and observed behaviour;
- realistic impact and affected trust boundary;
- proof of concept with secrets removed;
- known mitigations or workarounds;
- whether the issue is already public or actively exploited.

Do not test against systems or data you do not own or have permission to assess. Do not degrade availability, access private information, invoke providers without authorization, or modify LOCKED components while researching a report.

## Response Process

The maintainer will seek to acknowledge a complete private report, assess scope and severity, preserve evidence, and determine an appropriate disclosure and remediation plan. Response times are best effort; no service-level commitment is made.

A valid report does not itself authorize runtime, governance, provider, research, or LOCKED changes. Remediation follows the applicable CortexMesh engineering and governance process. Where immediate containment is necessary, the project will document the action and preserve the audit trail.

## Public Disclosure

Coordinate disclosure with the maintainer. Allow reasonable time for assessment and remediation, while recognizing that no fixed embargo period is promised. Credit will be offered when requested and appropriate, subject to privacy, safety, and evidence requirements.

Authorized repository users may use the bug-report issue form for non-sensitive defects. This security policy does not invite general contribution or grant repository access, use, modification, or distribution rights.
