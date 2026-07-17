"""Static and functional verification for Foundation 1.1-D CI controls."""

from __future__ import annotations

import importlib.util
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / ".github" / "ci" / "check_protected_paths.py"
POLICY_PATH = ROOT / ".github" / "ci" / "protected-paths.txt"
GATES_PATH = ROOT / ".github" / "workflows" / "quality-gates.yml"
OBSERVATIONS_PATH = (
    ROOT / ".github" / "workflows" / "quality-observations.yml"
)


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


class RequiredWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = GATES_PATH.read_text(encoding="utf-8")

    def test_workflow_has_expected_top_level_structure(self):
        required = (
            "name: Quality Gates",
            "\non:\n",
            "\npermissions:\n",
            "\nconcurrency:\n",
            "\njobs:\n",
        )
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, self.workflow)
        self.assertNotIn("\t", self.workflow)

    def test_required_triggers_are_present(self):
        self.assertRegex(self.workflow, r"(?m)^  pull_request:$")
        self.assertRegex(self.workflow, r"(?m)^  push:$")
        self.assertRegex(self.workflow, r"(?m)^  workflow_dispatch:$")
        self.assertGreaterEqual(
            len(re.findall(r"(?m)^      - main$", self.workflow)), 2
        )

    def test_permissions_are_read_only_and_no_secrets_are_used(self):
        self.assertRegex(
            self.workflow, r"(?ms)^permissions:\n  contents: read\n"
        )
        prohibited = ("contents: write", "id-token: write", "secrets.", "password:")
        for text in prohibited:
            with self.subTest(text=text):
                self.assertNotIn(text, self.workflow)

    def test_action_references_are_approved_full_shas(self):
        uses = re.findall(r"(?m)^\s*uses:\s*(\S+)", self.workflow)
        self.assertTrue(uses)
        approved = {
            "actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5",
            "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1",
        }
        for reference in uses:
            with self.subTest(reference=reference):
                self.assertIn(reference, approved)
                self.assertRegex(reference, r"@[0-9a-f]{40}$")

    def test_required_jobs_and_python_version_are_stable(self):
        for job in ("scope", "whitespace", "compile", "regression"):
            with self.subTest(job=job):
                self.assertRegex(self.workflow, rf"(?m)^  {job}:$")
                self.assertRegex(self.workflow, rf"(?m)^    name: {job}$")
        self.assertIn('python-version: "3.14"', self.workflow)

    def test_canonical_regression_command_is_present(self):
        self.assertIn(
            "PYTHONDONTWRITEBYTECODE=1 python -m unittest discover tests",
            self.workflow,
        )

    def test_required_failures_are_not_masked(self):
        prohibited = (
            "continue-on-error",
            "retry",
            "nick-fields/retry",
            "|| true",
        )
        for text in prohibited:
            with self.subTest(text=text):
                self.assertNotIn(text, self.workflow)

    def test_prohibited_execution_commands_are_absent(self):
        prohibited = (
            "python main.py",
            "LocalAI",
            "ollama",
            "lmstudio",
            "exp001_runner.py",
            "exp001_analyze.py",
            "docker ",
            "deploy",
            "release",
            "publish",
        )
        lowered = self.workflow.lower()
        for text in prohibited:
            with self.subTest(text=text):
                self.assertNotIn(text.lower(), lowered)


class ObservationalWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = OBSERVATIONS_PATH.read_text(encoding="utf-8")

    def test_workflow_has_expected_top_level_structure_and_triggers(self):
        required = (
            "name: Quality Observations",
            "\non:\n",
            "\npermissions:\n",
            "\nconcurrency:\n",
            "\njobs:\n",
            "  pull_request:\n",
            "  push:\n",
            "  workflow_dispatch:\n",
        )
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, self.workflow)
        self.assertNotIn("\t", self.workflow)

    def test_permissions_are_read_only_and_no_secrets_are_used(self):
        self.assertRegex(
            self.workflow, r"(?ms)^permissions:\n  contents: read\n"
        )
        for text in ("contents: write", "id-token: write", "secrets."):
            with self.subTest(text=text):
                self.assertNotIn(text, self.workflow)

    def test_action_references_are_approved_full_shas(self):
        uses = re.findall(r"(?m)^\s*uses:\s*(\S+)", self.workflow)
        approved = {
            "actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5",
            "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1",
            "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02",
        }
        self.assertTrue(uses)
        for reference in uses:
            with self.subTest(reference=reference):
                self.assertIn(reference, approved)
                self.assertRegex(reference, r"@[0-9a-f]{40}$")

    def test_jobs_python_and_artifact_retention_are_stable(self):
        for job in ("coverage", "dependency-audit"):
            with self.subTest(job=job):
                self.assertRegex(self.workflow, rf"(?m)^  {job}:$")
                self.assertRegex(self.workflow, rf"(?m)^    name: {job}$")
        self.assertIn('python-version: "3.14"', self.workflow)
        self.assertEqual(2, self.workflow.count("retention-days: 14"))

    def test_coverage_is_existing_scoped_command_and_descriptive(self):
        self.assertIn(
            "python tools/audit/audit_coverage.py", self.workflow
        )
        self.assertIn("descriptive-coverage", self.workflow)
        prohibited = ("--fail-under", "coverage threshold", "coveralls")
        for text in prohibited:
            with self.subTest(text=text):
                self.assertNotIn(text, self.workflow.lower())

    def test_dependency_audit_is_pinned_observational_and_non_mutating(self):
        required = (
            "pip-audit==2.10.1",
            "pip-audit exit code",
            "descriptive-dependency-audit",
            "no security certification or automatic mutation",
        )
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, self.workflow)
        prohibited = (
            "pip install --upgrade -r requirements.txt",
            "dependabot",
            "git commit",
            "git push",
            "gh issue",
        )
        for text in prohibited:
            with self.subTest(text=text):
                self.assertNotIn(text, self.workflow)

    def test_artifact_paths_are_allowlisted(self):
        paths = re.findall(r"(?m)^\s+path:\s*(\S+)\s*$", self.workflow)
        self.assertEqual(
            [
                "ci-artifacts/coverage",
                "ci-artifacts/dependency-audit",
            ],
            paths,
        )
        prohibited = (
            "EXP-001/raw",
            "EXP-001/analysis",
            "memory/memory.json",
            ".env",
            "*.bundle",
        )
        for text in prohibited:
            with self.subTest(text=text):
                self.assertNotIn(text, self.workflow)

    def test_observational_workflow_has_no_write_or_release_behavior(self):
        prohibited = (
            "continue-on-error",
            "python main.py",
            "docker ",
            "deploy",
            "release",
            "publish",
            "create-pull-request",
        )
        lowered = self.workflow.lower()
        for text in prohibited:
            with self.subTest(text=text):
                self.assertNotIn(text.lower(), lowered)


if __name__ == "__main__":
    unittest.main()
