# CortexMesh Onboarding Directory

## Purpose

This directory contains stable reviewer entry points and immutable historical review packets.

## Primary Entry Point

New reviewers should start here:

```text
REVIEWER_ENTRY_POINT.md
```

The entry point identifies the current session and points to the active session packet.

## Current Session

```text
09
```

## Current Review Packet

```text
Session_09/REVIEW_PACKET.md
```

## Directory Structure

```text
02_Onboarding/
├── REVIEWER_ENTRY_POINT.md
├── REVIEWER_PACKET_INDEX.md
├── SESSION_HISTORY.md
├── CURRENT_REVIEW_PACKET.md
├── REPOSITORY_STRUCTURE_STANDARD.md
├── Session_08/
│   ├── REVIEW_PACKET.md
│   └── MANIFEST.md
├── Session_09/
│   ├── REVIEW_PACKET.md
│   └── MANIFEST.md
├── Templates/
│   └── REVIEW_PACKET_MANIFEST_TEMPLATE.md
└── Archive/
    └── REVIEWER_PACKET_KIMI_CURRENT.md
```

## Reading Order

1. `REVIEWER_ENTRY_POINT.md`
2. `Session_09/REVIEW_PACKET.md`
3. `SESSION_HISTORY.md`
4. `REVIEWER_PACKET_INDEX.md`
5. `REPOSITORY_STRUCTURE_STANDARD.md`

## Historical Packet Rule

Session-specific review packets are historical artifacts.

Do not overwrite previous session packets.

When a new session begins:

1. Create `Session_XX/REVIEW_PACKET.md`.
2. Create `Session_XX/MANIFEST.md`.
3. Update `REVIEWER_ENTRY_POINT.md` to point to the new packet.
4. Update `SESSION_HISTORY.md`.

## Compatibility Note

`CURRENT_REVIEW_PACKET.md` is retained as a compatibility pointer only.

It is not the primary onboarding artifact.

## Archive

`Archive/` is reserved for legacy onboarding artifacts that do not fit the immutable `Session_XX/` packet structure.

Do not place new session packets in `Archive/`.
