import unittest
from unittest.mock import MagicMock, patch

from cost.budget import Budget
from orchestrator import orchestrate, spend_budget


class TestSpendBudget(unittest.TestCase):
    def test_spend_budget_returns_true_when_available(self):
        budget = Budget(limit=5)

        result = spend_budget(budget)

        self.assertTrue(result)

    def test_spend_budget_returns_false_when_exhausted(self):
        budget = Budget(limit=2)
        spend_budget(budget)
        spend_budget(budget)

        result = spend_budget(budget)

        self.assertFalse(result)

    def test_spend_budget_ticks_counter(self):
        budget = Budget(limit=5)
        initial = budget.count

        spend_budget(budget)

        self.assertEqual(budget.count, initial + 1)

    def test_spend_budget_does_not_tick_after_exhaustion(self):
        budget = Budget(limit=1)
        spend_budget(budget)

        spend_budget(budget)

        self.assertEqual(budget.count, 1)


class TestOrchestratorBudget(unittest.TestCase):
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
            "role_weights": {"Architect": 1.0, "Researcher": 1.0, "Engineer": 1.0},
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

    def _mock_ledger(self):
        ledger = MagicMock()
        ledger.rebalance = {}
        ledger.meta.report.return_value = {}
        return ledger

    @patch("orchestrator.create_governance_snapshot")
    @patch("orchestrator.update_governance_stability")
    @patch("orchestrator.enforce_governance", return_value=[])
    @patch("orchestrator.run_evolution", return_value=[])
    @patch("orchestrator.spawn_successors", return_value=[])
    @patch("orchestrator.entropy_correction")
    @patch("orchestrator.update_role_weights")
    @patch("orchestrator.record_failure")
    @patch("orchestrator.log_confidence")
    @patch("orchestrator.prune_memory")
    @patch("orchestrator.decay_lessons")
    @patch("orchestrator.record_negative_lesson")
    @patch("orchestrator.update_active_conflicts")
    @patch("orchestrator.update_used_negative_lessons")
    @patch("orchestrator.update_used_lessons")
    @patch("orchestrator.record_lesson")
    @patch("orchestrator.AuthorityAgent")
    @patch("orchestrator.score_solution")
    @patch("orchestrator.detect_similarity", return_value=False)
    @patch("orchestrator.detect_conflict", return_value=False)
    @patch("orchestrator.random.random", return_value=0.0)
    @patch("orchestrator.select_unique_agents", return_value=["Architect"])
    @patch("orchestrator.build_selection_weights", return_value={"Architect": 1.0})
    @patch("orchestrator.enforce_rotation", side_effect=lambda solvers, memory: solvers)
    @patch("orchestrator.build_solvers")
    @patch("orchestrator.build_critics")
    @patch("orchestrator.get_mode", return_value="prod")
    @patch("orchestrator.classify_task", return_value="general")
    @patch("orchestrator.cleanup_knowledge_memory")
    @patch("orchestrator.Ledger")
    def test_review_budget_exhaustion_logged(
        self,
        mock_ledger_cls,
        _cleanup,
        _classify,
        _get_mode,
        mock_build_critics,
        mock_build_solvers,
        _rotation,
        _weights,
        _select,
        _random,
        _conflict,
        _similarity,
        mock_score_solution,
        mock_authority_cls,
        *_,
    ):
        ledger = self._mock_ledger()
        mock_ledger_cls.return_value = ledger

        solver = MagicMock()
        solver.name = "Architect"
        solver.role = "architect"
        solver.act.return_value = {
            "agent": "Architect",
            "base_agent": "Architect",
            "solution": "result",
            "confidence": 0.5,
        }
        mock_build_solvers.return_value = [solver]

        critics = []
        for _ in range(20):
            critic = MagicMock()
            critic.review.return_value = {
                "critic": "logic",
                "review": "ok",
                "signal": "refine:logic",
            }
            critics.append(critic)
        mock_build_critics.return_value = critics

        scored = {
            "solution": solver.act.return_value,
            "scores": {"weighted_total": 5.0, "authority_total": 5.0},
        }
        mock_score_solution.return_value = scored
        mock_authority_cls.return_value.decide.return_value = {
            "decision": scored,
            "action": "ACCEPT",
        }

        orchestrate("test task", self.memory)

        self.assertNotIn(
            ("ACTIVATION_FALLBACK", "architect"),
            [call.args for call in ledger.add.call_args_list],
        )
        ledger.add.assert_any_call("budget", "Review budget exhausted")
        self.assertLess(
            sum(1 for critic in critics if critic.review.called),
            len(critics),
        )


if __name__ == "__main__":
    unittest.main()
