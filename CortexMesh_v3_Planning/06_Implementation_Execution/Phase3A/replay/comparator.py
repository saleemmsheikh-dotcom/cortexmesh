"""Deterministic replay comparator selection and comparison."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Mapping

from .manifest import content_hash


class ReplayComparator:
    SUPPORTED = ("compatible", "exact", "regression")

    @classmethod
    def select(cls, kind: str) -> "ReplayComparator":
        normalized = str(kind).strip().lower()
        if normalized == "future runtime":
            raise ValueError("future runtime replay is reserved and not implemented")
        if normalized not in cls.SUPPORTED:
            raise ValueError("unsupported replay comparator")
        return cls(normalized)

    def __init__(self, kind: str):
        if kind not in self.SUPPORTED:
            raise ValueError("unsupported replay comparator")
        self.kind = kind

    def compare(self, expected: Any, actual: Any, compatibility: Mapping[str, tuple[Any, ...]] | None = None) -> dict[str, Any]:
        left = _plain(expected)
        right = _plain(actual)
        if self.kind == "exact":
            matched = left == right
        elif self.kind == "compatible":
            matched = _compatible(left, right, compatibility or {})
        else:
            matched = left == right
        return {
            "kind": self.kind,
            "matched": matched,
            "expected_hash": content_hash(left),
            "actual_hash": content_hash(right),
            "outcome": "match" if matched else "regression" if self.kind == "regression" else "failure",
        }


def _plain(value: Any) -> Any:
    return asdict(value) if is_dataclass(value) else value


def _compatible(expected: Any, actual: Any, rules: Mapping[str, tuple[Any, ...]], path: str = "") -> bool:
    if expected == actual:
        return True
    if path in rules and actual in rules[path] and expected in rules[path]:
        return True
    if isinstance(expected, dict) and isinstance(actual, dict) and expected.keys() == actual.keys():
        return all(_compatible(expected[key], actual[key], rules, f"{path}.{key}".strip(".")) for key in expected)
    if isinstance(expected, (tuple, list)) and isinstance(actual, (tuple, list)) and len(expected) == len(actual):
        return all(_compatible(left, right, rules, f"{path}[{index}]") for index, (left, right) in enumerate(zip(expected, actual)))
    return False
