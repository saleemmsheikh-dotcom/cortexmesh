# Architectural Refinement Tracker

Status: PROPOSED

---

## Purpose

Track the architectural refinements required by BD-09-002 prior to completion of MAC003 through MAC005.

---

| ID | Requirement                              | Target Document          | Status | Commit |
| -- | ---------------------------------------- | ------------------------ | ------ | ------ |
| C1 | Structured Challenge alignment           | AI006                    | COMPLETE | 1984792 |
| C2 | Evidence Synthesis terminology           | AI007 / MAC002           | COMPLETE | 26f43b5, 65ef28c |
| C3 | Evidence format definition               | MAC003                   | OPEN   |        |
| C4 | Deterministic / Reproducible definitions | AI004 or AI005           | OPEN   |        |
| C5 | Evidence quality / confidence scoring    | MAC003                   | OPEN   |        |
| C6 | Authority selection architecture         | New AI document          | OPEN   |        |
| C7 | Security / Trust model                   | AI005 or new AI document | OPEN   |        |

---

No item shall be marked COMPLETE until committed and referenced in a Session 09 communication artifact.

---

## Work Order

Rather than starting MAC003 immediately, proceed in the following order:

```text
C1
|
v
C2
|
v
AI010 Authority Architecture (C6)
|
v
AI011 Security & Trust Model (C7)
|
v
MAC003 Evidence Synthesis
|
v
MAC004 Disagreement Protocol
|
v
MAC005 Reference Consensus Architecture
```
