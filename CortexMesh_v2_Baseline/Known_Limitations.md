# CortexMesh v2 Known Limitations

Certified limitations accepted by the board:

1. Docker isolation rather than VM isolation.
2. Docker daemon compromise outside current threat model.
3. ExternalRunner boundary required for timeout guarantees.
4. Raw Docker execution is unsupported.
5. Technical Specification remains partially complete (§2 approved).
6. Board composition currently project-specific.
7. Entropy monitoring exists but is not part of authority scoring.

These limitations are recorded for transparency and future roadmap planning.
Their existence does not invalidate current certification status.
