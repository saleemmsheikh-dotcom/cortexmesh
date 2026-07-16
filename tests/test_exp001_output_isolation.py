from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock


REPOSITORY = Path(__file__).resolve().parents[1]
HARNESS = REPOSITORY / "CortexMesh_v3_Planning/07_Research/RP-001/EXP-001/harness"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HARNESS / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RUNNER = load_module("test_exp001_runner", "exp001_runner.py")
ANALYZER = load_module("test_exp001_analyzer", "exp001_analyze.py")


class OutputIsolationTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.exp = Path(self.temporary.name) / "EXP-001"
        self.reproduction = self.exp / "reproduction"
        self.patches = [
            mock.patch.object(RUNNER, "EXP", self.exp),
            mock.patch.object(RUNNER, "OUTPUT", self.exp / "raw"),
            mock.patch.object(RUNNER, "REPRODUCTION", self.reproduction),
            mock.patch.object(ANALYZER, "EXP", self.exp),
            mock.patch.object(ANALYZER, "RAW", self.exp / "raw"),
            mock.patch.object(ANALYZER, "ANALYSIS", self.exp / "analysis"),
            mock.patch.object(ANALYZER, "REPRODUCTION", self.reproduction),
        ]
        for patcher in self.patches:
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_default_paths_are_unchanged(self):
        self.assertEqual(RUNNER.selected_output(None), (self.exp / "raw", None))
        self.assertEqual(
            ANALYZER.selected_paths(None, None),
            (self.exp / "raw", self.exp / "analysis"),
        )

    def test_published_outputs_remain_protected_by_default(self):
        (self.exp / "raw").mkdir(parents=True)
        (self.exp / "raw" / "immutable.jsonl").write_text("published\n")
        output, _ = RUNNER.selected_output(None)
        self.assertTrue(RUNNER.directory_has_files(output))
        (self.exp / "analysis").mkdir()
        (self.exp / "analysis" / "metrics.json").write_text("{}\n")
        raw, analysis = ANALYZER.selected_paths(None, None)
        self.assertTrue(RUNNER.directory_has_files(raw))
        self.assertTrue(ANALYZER.directory_has_files(analysis))
        with self.assertRaisesRegex(RuntimeError, "raw output directory is not empty"):
            RUNNER.main([])
        with self.assertRaisesRegex(RuntimeError, "analysis output directory is not empty"):
            ANALYZER.main([])

    def test_clean_isolated_package_is_accepted(self):
        raw, package = RUNNER.selected_output("reproduction/EXP-001-R2")
        self.assertEqual(package, (self.reproduction / "EXP-001-R2").resolve())
        self.assertEqual(raw, package / "raw")
        self.assertEqual(
            ANALYZER.selected_paths(
                "reproduction/EXP-001-R2/raw",
                "reproduction/EXP-001-R2/analysis",
            ),
            (package / "raw", package / "analysis"),
        )

    def test_nonempty_isolated_raw_or_analysis_is_rejected(self):
        package = self.reproduction / "EXP-001-R2"
        (package / "analysis").mkdir(parents=True)
        (package / "analysis" / "existing.json").write_text("{}\n")
        with self.assertRaisesRegex(RuntimeError, "not empty"):
            RUNNER.selected_output("reproduction/EXP-001-R2")
        with self.assertRaisesRegex(RuntimeError, "analysis output directory is not empty"):
            ANALYZER.main([
                "--input-root", "reproduction/EXP-001-R2/raw",
                "--output-root", "reproduction/EXP-001-R2/analysis",
            ])

    def test_paths_outside_reproduction_space_are_rejected(self):
        invalid = ("../outside", "raw", "analysis", "reproduction/../raw")
        for value in invalid:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    RUNNER.reproduction_package(value)
        with self.assertRaises(ValueError):
            ANALYZER.selected_paths(
                "reproduction/EXP-001-R2/../../raw",
                "reproduction/EXP-001-R2/analysis",
            )

    def test_analyzer_requires_one_matching_reproduction_package(self):
        with self.assertRaisesRegex(ValueError, "requires both"):
            ANALYZER.selected_paths("reproduction/EXP-001-R2/raw", None)
        with self.assertRaisesRegex(ValueError, "same package"):
            ANALYZER.selected_paths(
                "reproduction/EXP-001-R2/raw",
                "reproduction/EXP-001-R3/analysis",
            )

    def test_scientific_constants_and_expected_values_are_unchanged(self):
        self.assertEqual(RUNNER.REPETITIONS, 10)
        self.assertEqual(RUNNER.EXPECTED_ENGINE, "a72d11fe57f9026ab307efeaf962b97095527039")
        self.assertEqual(RUNNER.EXPECTED_VALIDATION, "6c41364c56883043c20d237d37b8fcd83ec02547")
        self.assertEqual(
            RUNNER.EXPECTED_CORPUS_HASH,
            "20e4b446097db5b3dcaa6fbf214218038c9c297d2e60bbbc57b9d24bc1e59788",
        )
        self.assertEqual(
            RUNNER.outputs_for(
                {"payload": {"mode": "same", "claims": ["claim"]}},
                [type("Step", (), {"step_id": "step-001"})()],
            )["step-001"]["output"],
            {"claims": ["claim"]},
        )


if __name__ == "__main__":
    unittest.main()
