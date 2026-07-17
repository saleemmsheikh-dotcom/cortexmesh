# Contributing to CortexMesh

Thank you for helping improve CortexMesh. Contributions are welcome when they preserve the project's evidence, governance, validation, and historical-integrity boundaries.

## Before You Begin

Read:

- the [project README](README.md);
- the [Foundation 1.0 baseline](CortexMesh_v3_Planning/FOUNDATION_BASELINE_v1.0.md);
- the [directory map](CortexMesh_v3_Planning/CORTEXMESH_DIRECTORY_MAP.md);
- the [Code of Conduct](CODE_OF_CONDUCT.md);
- the [Security Policy](SECURITY.md) before reporting a vulnerability.

Open an issue before substantial work. A discussion, issue response, or pull-request review is not governance approval, implementation authorization, certification, or permission to modify a LOCKED component.

## Suitable Contributions

Examples include:

- correcting documentation or traceability;
- adding focused tests for existing behaviour;
- improving diagnostics without changing authority semantics;
- proposing provider-neutral extensions;
- strengthening replay, reproducibility, or validation assets;
- reporting reproducible defects and preserving negative results.

Do not silently:

- modify LOCKED components or governance authority;
- integrate the isolated reference engine into the live runtime;
- introduce scoring, ranking, confidence adjustment, voting, or provider authority;
- rewrite sealed evidence, certified corpora, research records, or historical decisions;
- present research evidence as implementation or governance authorization.

Proposals affecting those boundaries require the applicable evidence and approved CortexMesh process before implementation.

## Development Workflow

1. Fork the repository and create a focused branch.
2. Reproduce the current behaviour before changing it.
3. Keep the change limited to one reviewable purpose.
4. Add or update tests and documentation in proportion to risk.
5. Preserve existing evidence and unrelated worktree changes.
6. Run the relevant focused tests and the full regression suite.
7. Run `git diff --check`.
8. Submit a pull request using the repository template.

Use clear commits that separate design, implementation, authorization, execution evidence, and closeout when those are distinct lifecycle events.

## Validation

The standard full regression command is:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover tests
```

Also run focused tests for the affected subsystem. Report exact commands and results in the pull request. Do not use an aggregate score to hide an independently failing validation gate.

Documentation-only changes normally require link, scope, and whitespace checks. A reviewer may request broader validation when documentation changes operational instructions, certification records, or security guidance.

## Pull-Request Expectations

A pull request should state:

- the problem and bounded scope;
- files and architectural boundaries affected;
- tests and verification performed;
- runtime, provider, Local AI, governance, research, and LOCKED impact;
- risks, limitations, and rollback where relevant;
- whether generated or historical evidence is included.

Keep minority evidence, unresolved divergence, failed checks, and limitations visible. Do not alter expected results after observing an outcome without an explicit new version or deviation record.

## Reviews and Acceptance

Maintainer review can request changes or accept a contribution into the repository. It does not supersede GG-02 or other ratified CortexMesh governance where those rules apply. Contributions that affect protected architecture, certification, roadmap, implementation authority, or LOCKED components may require a separate governance decision.

## Licensing Contributions

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in CortexMesh is provided under the [Apache License 2.0](LICENSE), consistent with Section 5 of that license. By submitting a contribution, you represent that you have the right to do so.

No Contributor License Agreement is currently required.
