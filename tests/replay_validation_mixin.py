"""Reusable unittest mixin for certifying Phase 3A replay datasets.

Subclasses provide a fully built ``replay_dataset`` and declared expected
release values.  The mixin validates static corpus structure only; it never
executes orchestration, agents, providers, Local AI, or runtime behavior.
"""

from __future__ import annotations


class ReplayDatasetCertificationMixin:
    """Provider-neutral, non-runtime replay release certification checks."""

    replay_dataset = None
    expected_dataset_id: str | None = None
    expected_corpus_version: str | None = None
    expected_schema_version: str | None = None
    expected_scenario_count: int | None = None
    expected_case_count: int | None = None
    required_comparator_coverage: tuple[str, ...] = ("compatible", "exact", "regression")

    def test_replay_dataset_identity_and_version(self):
        dataset = self._required_dataset()
        self.assertEqual(dataset.dataset_id, self.expected_dataset_id)
        self.assertEqual(dataset.manifest.dataset_id, self.expected_dataset_id)
        self.assertEqual(dataset.manifest.replay_version.version, self.expected_corpus_version)
        self.assertEqual(dataset.manifest.replay_version.schema_version, self.expected_schema_version)

    def test_replay_dataset_has_expected_counts(self):
        dataset = self._required_dataset()
        self.assertEqual(len(dataset.scenarios), self.expected_scenario_count)
        self.assertEqual(len(dataset.cases), self.expected_case_count)
        self.assertEqual(len(dataset.manifest.scenario_hashes), self.expected_scenario_count)
        self.assertEqual(len(dataset.manifest.case_hashes), self.expected_case_count)

    def test_replay_dataset_ordering_and_references(self):
        dataset = self._required_dataset()
        scenario_ids = tuple(item.scenario_id for item in dataset.scenarios)
        case_ids = tuple(item.case_id for item in dataset.cases)
        self.assertEqual(scenario_ids, tuple(sorted(set(scenario_ids))))
        self.assertEqual(case_ids, tuple(sorted(set(case_ids))))
        known_cases = set(case_ids)
        known_scenarios = set(scenario_ids)
        for scenario in dataset.scenarios:
            self.assertLessEqual(set(scenario.case_ids), known_cases)
        for case in dataset.cases:
            self.assertIn(case.scenario_id, known_scenarios)

    def test_replay_manifest_hash_and_content_bindings(self):
        dataset = self._required_dataset()
        self.assertEqual(dataset.manifest.content_hash, dataset.manifest.calculate_content_hash())
        self.assertEqual(
            tuple(item.scenario_id for item in dataset.scenarios),
            tuple(identifier for identifier, _ in dataset.manifest.scenario_hashes),
        )
        self.assertEqual(
            tuple(item.case_id for item in dataset.cases),
            tuple(identifier for identifier, _ in dataset.manifest.case_hashes),
        )

    def test_replay_comparator_coverage(self):
        dataset = self._required_dataset()
        self.assertEqual(dataset.manifest.comparator_coverage, self.required_comparator_coverage)
        self.assertNotIn("future runtime", dataset.manifest.comparator_coverage)

    def test_replay_cases_have_minimum_metadata_and_expectations(self):
        dataset = self._required_dataset()
        for case in dataset.cases:
            with self.subTest(case_id=case.case_id):
                metadata = case.metadata
                self.assertTrue(metadata.phase_version)
                self.assertTrue(metadata.architecture_version)
                self.assertEqual(metadata.replay_corpus_version, self.expected_corpus_version)
                self.assertTrue(metadata.validation_framework_version)
                self.assertTrue(metadata.component_versions)
                self.assertTrue(metadata.timestamp)
                self.assertEqual(metadata.source_scenario, case.scenario_id)
                self.assertEqual(metadata.schema_version, self.expected_schema_version)
                self.assertTrue(case.expected_capability_requirements)
                self.assertTrue(case.expected_agent_plan)
                self.assertTrue(case.expected_execution_plan)
                self.assertTrue(case.expected_evidence_characteristics)
                self.assertTrue(case.expected_synthesis_characteristics)

    def test_replay_release_is_certified_and_manifest_bound(self):
        dataset = self._required_dataset()
        self.assertTrue(dataset.published)
        self.assertIsNotNone(dataset.certification)
        self.assertEqual(dataset.certification.validation_status, "certified")
        dataset.certification.validate(dataset.manifest)
        self.assertTrue(dataset.certification.approved_at)
        self.assertTrue(dataset.certification.approved_by)

    def _required_dataset(self):
        self.assertIsNotNone(self.replay_dataset)
        self.assertIsNotNone(self.expected_dataset_id)
        self.assertIsNotNone(self.expected_corpus_version)
        self.assertIsNotNone(self.expected_schema_version)
        self.assertIsNotNone(self.expected_scenario_count)
        self.assertIsNotNone(self.expected_case_count)
        return self.replay_dataset
