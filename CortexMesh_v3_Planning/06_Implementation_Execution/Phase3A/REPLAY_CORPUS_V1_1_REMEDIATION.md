# Replay Corpus v1.1 Remediation

## Objective

Correct corpus fidelity defects found by M6 without changing `phase2c-complete`.

## Remediation Contract

v1.1 adds executable role-keyed payload profiles resolved to actual planned step IDs, negative-input modes, consensus aliases/conflicts, exact observed planning expectations, minority/divergence claims, and statement-level synthesis/diagnostic expectations.

v1.0 remains immutable and reproducible. v1.1 is a new minor release with independent manifest, hashes, tests, results, and certification.

## Rules

- Planning expectations are captured from the sealed public reference contracts and reviewed before v1.1 measurement.
- Payload resolution may map planned roles to step IDs; it may not change plans.
- Negative cases encode the actual prohibited, missing, malformed, or extra input.
- Consensus policies are case data, not engine defaults.
- Expected statements identify required claims, evidence IDs, sections, and diagnostics.
- No engine, runtime, Local AI, provider, or LOCKED change is permitted.

## Acceptance

All v1.1 files must validate, hashes must recompute, all 24 cases must be executable or explicitly expected to reject, and identical baseline metrics must be repeated independently.
