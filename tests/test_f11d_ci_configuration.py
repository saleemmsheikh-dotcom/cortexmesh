"""Static and functional verification for Foundation 1.1-D CI controls."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / ".github" / "ci" / "check_protected_paths.py"
POLICY_PATH = ROOT / ".github" / "ci" / "protected-paths.txt"


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "f11d_check_protected_paths", CHECKER_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = load_checker()


class ProtectedPathPolicyTests(unittest.TestCase):
    def setUp(self):
        self.patterns = checker.parse_policy(
            [
                "exact:orchestrator.py",
                "prefix:CortexMesh_v3_Planning/00_Governance",
                "glob:CortexMesh_v3_Planning/07_Research/**/raw/**",
            ]
        )

    def test_exact_path_matches(self):
        matches = checker.find_protected_matches(
            ["orchestrator.py"], self.patterns
        )
        self.assertEqual(["orchestrator.py"], [match.path for match in matches])

    def test_prefix_path_matches_descendant(self):
        path = "CortexMesh_v3_Planning/00_Governance/GG-02.md"
        matches = checker.find_protected_matches([path], self.patterns)
        self.assertEqual([path], [match.path for match in matches])

    def test_glob_path_matches(self):
        path = "CortexMesh_v3_Planning/07_Research/RP-001/EXP/raw/result.json"
        matches = checker.find_protected_matches([path], self.patterns)
        self.assertEqual([path], [match.path for match in matches])

    def test_ordinary_documentation_path_passes(self):
        matches = checker.find_protected_matches(
            ["docs/implementation-note.md"], self.patterns
        )
        self.assertEqual((), matches)

    def test_invalid_and_traversal_paths_fail_closed(self):
        invalid = ("../orchestrator.py", "/orchestrator.py", "./README.md")
        for path in invalid:
            with self.subTest(path=path):
                with self.assertRaises(checker.PolicyError):
                    checker.normalize_path(path)

    def test_findings_are_sorted_and_deduplicated(self):
        patterns = checker.parse_policy(
            [
                "prefix:core",
                "exact:core/contracts.py",
                "prefix:core",
            ]
        )
        matches = checker.find_protected_matches(
            ["core/contracts.py", "core/contracts.py"], patterns
        )
        self.assertEqual(
            [
                ("core/contracts.py", "exact", "core/contracts.py"),
                ("core/contracts.py", "prefix", "core"),
            ],
            [
                (match.path, match.pattern.kind, match.pattern.value)
                for match in matches
            ],
        )

    def test_malformed_or_empty_policy_fails_closed(self):
        for lines in ([], ["# comments only"], ["orchestrator.py"]):
            with self.subTest(lines=lines):
                with self.assertRaises(checker.PolicyError):
                    checker.parse_policy(lines)

    def test_real_policy_contains_mandatory_categories(self):
        policy = POLICY_PATH.read_text(encoding="utf-8")
        mandatory = (
            "exact:core/contracts.py",
            "exact:core/external_runner.py",
            "exact:competition/scorer.py",
            "exact:agents/authority.py",
            "exact:orchestrator.py",
            "exact:governance/snapshot.py",
            "prefix:CortexMesh_v3_Planning/00_Governance",
            "prefix:CortexMesh_v3_Planning/06_Implementation_Execution/Phase2C",
            "prefix:CortexMesh_v3_Planning/06_Implementation_Execution/Phase3A/replay/v1.1",
            "exact:CortexMesh_v3_Planning/07_Research/RESEARCH_OBSERVATIONS.md",
            "exact:CortexMesh_v3_Planning/FOUNDATION_BASELINE_v1.0.md",
        )
        for entry in mandatory:
            with self.subTest(entry=entry):
                self.assertIn(entry, policy)


if __name__ == "__main__":
    unittest.main()
