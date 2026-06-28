import unittest
from contextlib import ExitStack
from unittest.mock import MagicMock, patch

import orchestrator


class TestOrchestratorHelperBranches(unittest.TestCase):
    def test_add_noise_applies_uniform_noise(self):
        with patch("orchestrator.random.uniform", return_value=0.05):
            self.assertEqual(orchestrator.add_noise([1.0, 2.0]), [1.05, 2.05])

    def test_weighted_agents_orders_by_weighted_random_key(self):
        low = MagicMock()
        low.name = "low"
        high = MagicMock()
        high.name = "high"

        with patch("orchestrator.random.random", return_value=1.0):
            result = orchestrator.weighted_agents(
                [low, high],
                {"low": 1.0, "high": 3.0},
            )

        self.assertEqual([agent.name for agent in result], ["high", "low"])

    def test_update_role_weights_rewards_winner_and_normalizes(self):
        memory = {
            "role_weights": {
                "Architect": 1.0,
                "Researcher": 1.0,
                "Engineer": 1.0,
            },
        }

        orchestrator.update_role_weights(memory, "Architect_v2")

        self.assertGreater(memory["role_weights"]["Architect"], 1 / 3)
        self.assertAlmostEqual(sum(memory["role_weights"].values()), 1.0)

    def test_entropy_correction_increases_low_entropy_weights(self):
        memory = {
            "role_weights": {
                "Architect": 1.0,
                "Researcher": 0.0,
                "Engineer": 0.0,
            },
            "entropy_target": 1.0,
            "entropy_drift": 0.05,
        }

        orchestrator.entropy_correction(memory)

        self.assertGreater(memory["role_weights"]["Researcher"], 0.0)
        self.assertAlmostEqual(sum(memory["role_weights"].values()), 1.0)

    def test_entropy_correction_reduces_high_entropy_weights(self):
        memory = {
            "role_weights": {
                "Architect": 1.0,
                "Researcher": 1.0,
                "Engineer": 1.0,
            },
            "entropy_target": 0.1,
            "entropy_drift": 0.01,
        }

        orchestrator.entropy_correction(memory)

        self.assertAlmostEqual(sum(memory["role_weights"].values()), 1.0)

    def test_build_selection_weights_applies_floor(self):
        agent = MagicMock()
        agent.name = "Architect"
        agent.base_agent = "Architect"
        memory = {
            "agent_wins": {},
            "role_weights": {"Architect": 0.01},
        }

        with patch("orchestrator.random.uniform", return_value=0.0):
            result = orchestrator.build_selection_weights([agent], memory)

        self.assertEqual(result["Architect"], orchestrator.MIN_PROB)

    def test_enforce_rotation_soft_cooldown(self):
        agent = MagicMock()
        agent.name = "Architect"
        memory = {"agent_usage": {"Architect": 6}}

        result = orchestrator.enforce_rotation([agent], memory)

        self.assertEqual(result, [agent])
        self.assertAlmostEqual(memory["agent_usage"]["Architect"], 4.2)

    def test_reviews_for_out_of_range_returns_empty_list(self):
        self.assertEqual(orchestrator.reviews_for([], 3), [])


class TestOrchestratorIntegrationBranches(unittest.TestCase):
    def setUp(self):
        self.memory = {
            "strategy_registry": {},
            "governance_frozen": False,
            "governance_violations": [],
            "governance_actions": [],
            "governance_snapshots": [],
            "governance_tamper_log": [],
            "governance_tamper_anchor": None,
            "governance_incidents": 0,
            "governance_clean_runs": 0,
            "governance_risk_score": 0.0,
            "governance_risk_history": [],
            "task_trust": {},
            "agent_trust": {},
            "confidence_history": {},
            "role_weights": {
                "Architect": 1.0,
                "Researcher": 1.0,
                "Engineer": 1.0,
            },
            "agent_wins": {},
            "agent_usage": {},
            "knowledge_memory": {},
            "negative_knowledge": {},
            "knowledge_conflicts": [],
            "failure_memory": {},
            "evolution_events": [],
            "entropy_target": 0.5,
            "entropy_drift": 0.1,
            "runs": 0,
            "strategy_scores": {},
        }

    def _solver(self, name, solution_text):
        solver = MagicMock()
        solver.name = name
        solver.role = name.lower()
        solver.base_agent = name
        solver.act.return_value = {
            "agent": name,
            "base_agent": name,
            "solution": solution_text,
            "confidence": 0.5,
        }
        return solver

    def _run_with_patches(
        self,
        solvers,
        critics=None,
        random_values=None,
        authority_action="ACCEPT",
        detect_conflict=False,
        detect_similarity=False,
        evolution_events=None,
        task_type="general",
        mode="prod",
    ):
        ledger = MagicMock()
        ledger.rebalance = {}
        ledger.meta.report.return_value = {}
        mocks = {}

        names = [solver.name for solver in solvers]
        weights = {name: 1.0 for name in names}
        critics = critics if critics is not None else []
        evolution_events = evolution_events if evolution_events is not None else []

        def score_solution(solution, _reviews, _ledger):
            return {
                "solution": solution,
                "scores": {
                    "weighted_total": 5.0,
                    "authority_total": 5.0,
                    "total": 5.0,
                },
            }

        def decide(scored, _ledger, task_type="general"):
            if authority_action == "CONFLICT_RESOLUTION":
                return {
                    "decision": scored[0],
                    "alternatives": scored,
                    "action": "CONFLICT_RESOLUTION",
                }
            return {
                "decision": scored[0],
                "action": "ACCEPT",
            }

        with ExitStack() as stack:
            stack.enter_context(patch("orchestrator.Ledger", return_value=ledger))
            stack.enter_context(patch("orchestrator.cleanup_knowledge_memory"))
            stack.enter_context(patch("orchestrator.classify_task", return_value=task_type))
            stack.enter_context(patch("orchestrator.get_mode", return_value=mode))
            stack.enter_context(patch("orchestrator.enforce_governance", return_value=[]))
            stack.enter_context(patch("orchestrator.spawn_successors", return_value=[]))
            stack.enter_context(patch("orchestrator.run_evolution", return_value=evolution_events))
            stack.enter_context(patch("orchestrator.update_governance_stability"))
            stack.enter_context(patch("orchestrator.create_governance_snapshot"))
            stack.enter_context(patch("orchestrator.build_solvers", return_value=solvers))
            stack.enter_context(patch("orchestrator.enforce_rotation", side_effect=lambda s, _m: s))
            stack.enter_context(patch("orchestrator.build_selection_weights", return_value=weights))
            stack.enter_context(patch("orchestrator.select_unique_agents", return_value=names))
            stack.enter_context(patch("orchestrator.build_critics", return_value=critics))
            stack.enter_context(patch("orchestrator.detect_conflict", return_value=detect_conflict))
            stack.enter_context(patch("orchestrator.detect_similarity", return_value=detect_similarity))
            stack.enter_context(patch("orchestrator.score_solution", side_effect=score_solution))
            stack.enter_context(patch("orchestrator.AuthorityAgent"))
            mocks["record_lesson"] = stack.enter_context(patch("orchestrator.record_lesson"))
            mocks["update_used_lessons"] = stack.enter_context(patch("orchestrator.update_used_lessons"))
            mocks["update_used_negative_lessons"] = stack.enter_context(patch("orchestrator.update_used_negative_lessons"))
            mocks["update_active_conflicts"] = stack.enter_context(patch("orchestrator.update_active_conflicts"))
            mocks["record_negative_lesson"] = stack.enter_context(patch("orchestrator.record_negative_lesson"))
            mocks["decay_lessons"] = stack.enter_context(patch("orchestrator.decay_lessons"))
            mocks["prune_memory"] = stack.enter_context(patch("orchestrator.prune_memory"))
            mocks["log_confidence"] = stack.enter_context(patch("orchestrator.log_confidence"))
            mocks["record_failure"] = stack.enter_context(patch("orchestrator.record_failure"))
            mocks["determine_failure_reason"] = stack.enter_context(
                patch("orchestrator.determine_failure_reason", return_value="test_failure")
            )
            mocks["update_role_weights"] = stack.enter_context(patch("orchestrator.update_role_weights"))
            mocks["entropy_correction"] = stack.enter_context(patch("orchestrator.entropy_correction"))
            mocks["print_audit_report"] = stack.enter_context(patch("orchestrator.print_audit_report"))
            stack.enter_context(patch("orchestrator.compute_rebalance", return_value={}))

            if random_values is not None:
                stack.enter_context(patch("orchestrator.random.random", side_effect=random_values))

            authority_cls = orchestrator.AuthorityAgent
            authority_cls.return_value.decide.side_effect = decide

            result = orchestrator.orchestrate("test task", self.memory)

        return result, ledger, mocks

    def test_random_activation_skip_then_execute_next_solver(self):
        skipped = self._solver("Architect", "skipped")
        executed = self._solver("Researcher", "executed")

        result, ledger, _mocks = self._run_with_patches(
            [skipped, executed],
            random_values=[0.99, 0.0],
        )

        skipped.act.assert_not_called()
        executed.act.assert_called_once()
        self.assertEqual(result["final"]["agent"], "Researcher")
        self.assertNotIn(
            ("ACTIVATION_FALLBACK", "architect"),
            [call.args for call in ledger.add.call_args_list],
        )

    def test_refinement_loop_replaces_original_solutions(self):
        solver = self._solver("Architect", "original")
        solver.act.side_effect = [
            {
                "agent": "Architect",
                "base_agent": "Architect",
                "solution": "original",
                "confidence": 0.5,
            },
            {
                "agent": "Architect",
                "base_agent": "Architect",
                "solution": "refined",
                "confidence": 0.6,
            },
        ]
        critic = MagicMock()
        critic.review.return_value = {
            "critic": "logic",
            "review": "missing operational detail",
            "signal": "refine:logic",
        }

        result, ledger, _mocks = self._run_with_patches(
            [solver],
            critics=[critic],
            random_values=[0.0],
        )

        self.assertEqual(solver.act.call_count, 2)
        ledger.add.assert_any_call("REFINEMENT_TRIGGERED", True)
        ledger.add.assert_any_call("refined_solution", result["final"])
        self.assertEqual(result["final"]["solution"], "refined")

    def test_conflict_resolution_returns_primary_and_alternatives(self):
        solver = self._solver("Architect", "primary")

        result, ledger, _mocks = self._run_with_patches(
            [solver],
            random_values=[0.0],
            authority_action="CONFLICT_RESOLUTION",
            detect_conflict=True,
        )

        ledger.add.assert_any_call("CONFLICT_DETAILS", result["authority"]["alternatives"])
        self.assertTrue(result["conflict_resolved"])
        self.assertIn("primary", result["final"])
        self.assertIn("alternatives", result["final"])

    def test_similarity_warning_logged(self):
        solver = self._solver("Architect", "same")

        _result, ledger, _mocks = self._run_with_patches(
            [solver],
            random_values=[0.0],
            detect_similarity=True,
        )

        ledger.add.assert_any_call(
            "DIVERSITY_WARNING",
            "All solutions identical - forcing variation",
        )

    def test_non_specialist_result_records_negative_lesson(self):
        solver = self._solver("Researcher", "non specialist")

        _result, _ledger, mocks = self._run_with_patches(
            [solver],
            random_values=[0.0],
            task_type="systems",
        )

        mocks["record_negative_lesson"].assert_called_once()

    def test_losing_solution_records_failure(self):
        winner = self._solver("Architect", "winner")
        loser = self._solver("Researcher", "loser")

        _result, _ledger, mocks = self._run_with_patches(
            [winner, loser],
            random_values=[0.0, 0.0],
        )

        mocks["record_failure"].assert_called_once()

    def test_evolution_events_logged(self):
        solver = self._solver("Architect", "winner")

        _result, ledger, _mocks = self._run_with_patches(
            [solver],
            random_values=[0.0],
            evolution_events=[{"event": "spawned"}],
        )

        ledger.add.assert_any_call("EVOLUTION", [{"event": "spawned"}])

    def test_audit_mode_prints_audit_report(self):
        solver = self._solver("Architect", "winner")

        _result, _ledger, mocks = self._run_with_patches(
            [solver],
            random_values=[0.0],
            mode="audit",
        )

        mocks["print_audit_report"].assert_called_once()


if __name__ == "__main__":
    unittest.main()
