#!/usr/bin/env python3
"""Fail closed when a Git comparison changes CortexMesh protected paths."""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence


POLICY_KINDS = frozenset({"exact", "prefix", "glob"})


class PolicyError(ValueError):
    """Raised when policy or path input cannot be interpreted safely."""


@dataclass(frozen=True, order=True)
class PolicyPattern:
    kind: str
    value: str

    def __post_init__(self) -> None:
        if self.kind not in POLICY_KINDS:
            raise PolicyError(f"unsupported policy kind: {self.kind!r}")
        normalized = normalize_path(self.value, allow_glob=self.kind == "glob")
        object.__setattr__(self, "value", normalized.rstrip("/"))


@dataclass(frozen=True, order=True)
class ProtectedMatch:
    path: str
    pattern: PolicyPattern


def normalize_path(value: str, *, allow_glob: bool = False) -> str:
    """Return a safe repository-relative POSIX path."""
    candidate = value.strip().replace("\\", "/")
    if not candidate:
        raise PolicyError("path must not be empty")
    if candidate.startswith("/") or PurePosixPath(candidate).is_absolute():
        raise PolicyError(f"absolute path is prohibited: {value!r}")

    raw_parts = candidate.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        raise PolicyError(f"non-normal path is prohibited: {value!r}")
    parts = PurePosixPath(candidate).parts
    if not allow_glob and any(token in candidate for token in ("*", "?", "[")):
        raise PolicyError(f"glob token is prohibited for this pattern: {value!r}")
    return "/".join(parts)


def parse_policy(lines: Iterable[str]) -> tuple[PolicyPattern, ...]:
    """Parse, validate, sort, and deduplicate policy lines."""
    patterns: set[PolicyPattern] = set()
    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        kind, separator, value = line.partition(":")
        if not separator:
            raise PolicyError(
                f"line {line_number}: expected '<kind>:<repository-path>'"
            )
        try:
            patterns.add(PolicyPattern(kind.strip(), value.strip()))
        except PolicyError as exc:
            raise PolicyError(f"line {line_number}: {exc}") from exc
    if not patterns:
        raise PolicyError("policy contains no patterns")
    return tuple(sorted(patterns))


def load_policy(path: Path) -> tuple[PolicyPattern, ...]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PolicyError(f"cannot read policy {path}: {exc}") from exc
    return parse_policy(content.splitlines())


def pattern_matches(path: str, pattern: PolicyPattern) -> bool:
    normalized = normalize_path(path)
    if pattern.kind == "exact":
        return normalized == pattern.value
    if pattern.kind == "prefix":
        return normalized == pattern.value or normalized.startswith(
            f"{pattern.value}/"
        )
    return fnmatch.fnmatchcase(normalized, pattern.value)


def find_protected_matches(
    paths: Iterable[str], patterns: Sequence[PolicyPattern]
) -> tuple[ProtectedMatch, ...]:
    matches = {
        ProtectedMatch(normalize_path(path), pattern)
        for path in paths
        for pattern in patterns
        if pattern_matches(path, pattern)
    }
    return tuple(sorted(matches))


def changed_paths(base: str, head: str) -> tuple[str, ...]:
    """Return deterministic changed paths for the explicit Git range."""
    if not base.strip() or not head.strip():
        raise PolicyError("base and head revisions are required")
    command = [
        "git",
        "diff",
        "--name-only",
        "-z",
        "--diff-filter=ACDMRTUXB",
        base,
        head,
        "--",
    ]
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=False,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PolicyError(f"git comparison failed for {base}..{head}: {exc}") from exc

    decoded = result.stdout.decode("utf-8")
    paths = {
        normalize_path(item)
        for item in decoded.split("\0")
        if item
    }
    return tuple(sorted(paths))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Git base revision")
    parser.add_argument("--head", required=True, help="Git head revision")
    parser.add_argument(
        "--policy",
        type=Path,
        default=Path(".github/ci/protected-paths.txt"),
        help="protected-path policy file",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        patterns = load_policy(args.policy)
        paths = changed_paths(args.base, args.head)
        matches = find_protected_matches(paths, patterns)
    except (PolicyError, UnicodeError) as exc:
        print(f"protected-path policy error: {exc}", file=sys.stderr)
        return 2

    if matches:
        print("Protected path changes detected:")
        for match in matches:
            print(
                f"- {match.path} "
                f"(matched {match.pattern.kind}:{match.pattern.value})"
            )
        print("CI detection does not authorize this change.")
        return 1

    print(f"No protected paths changed across {len(paths)} changed path(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
