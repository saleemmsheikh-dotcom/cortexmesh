# CortexMesh CI Controls

## Purpose

This directory contains repository-local controls used by Foundation 1.1-D
automation. CI automates verification; it does not authorize engineering,
governance, research, provider, runtime, or LOCKED-component changes.

## Protected-path policy

`protected-paths.txt` uses one entry per line:

```text
exact:path/to/file.py
prefix:path/to/directory
glob:path/**/evidence/**
```

- `exact` matches one repository-relative path.
- `prefix` matches the directory itself and every descendant.
- `glob` uses case-sensitive POSIX-style wildcard matching.
- blank lines and lines beginning with `#` are ignored.
- absolute paths, parent traversal, malformed entries, and an empty policy fail
  closed.

The policy is a CI detection aid derived from authoritative CortexMesh records.
It does not replace the Lock Registry, GG-02, Board process, Product Owner
acceptance, research authorization, or certification controls.

## Local equivalence

Compare two Git revisions:

```bash
python3 .github/ci/check_protected_paths.py \
  --base <base-commit> \
  --head <head-commit>
```

Exit codes:

| Code | Meaning |
| ---: | --- |
| 0 | No protected path changed |
| 1 | One or more protected paths changed |
| 2 | Policy, path, or Git comparison could not be validated |

Every matched path and policy pattern is printed deterministically. Detection
blocks for review and never grants a bypass.

## Maintenance

Changes to this policy require:

1. comparison with authoritative governance, LOCKED, validation, and research
   records;
2. focused positive and negative tests;
3. an explicit changed-path review; and
4. Product Owner acceptance under the applicable workstream.

Do not weaken a pattern merely to obtain a passing workflow.
