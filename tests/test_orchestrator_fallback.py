import unittest
from unittest.mock import MagicMock, patch

from orchestrator import orchestrate


class TestOrchestratorFallback(unittest.TestCase):
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
    @patch("orchestrator.build_critics", return_value=[])
    @patch("orchestrator.detect_similarity", return_value=False)
    @patch("orchestrator.detect_conflict", return_value=False)
    @patch("orchestrator.random.random", return_value=0.99)
    @patch("orchestrator.select_unique_agents", return_value=["Architect"])
    @patch("orchestrator.build_selection_weights", return_value={"Architect": 1.0})
    @patch("orchestrator.enforce_rotation", side_effect=lambda solvers, memory: solvers)
    @patch("orchestrator.build_solvers")
    @patch("orchestrator.get_mode", return_value="prod")
    @patch("orchestrator.classify_task", return_value="general")
    @patch("orchestrator.cleanup_knowledge_memory")
    @patch("orchestrator.Ledger")
    def test_fallback_when_no_primary_solutions(
        self,
        mock_ledger_cls,
        _cleanup,
        _classify,
        _get_mode,
        mock_build_solvers,
        _rotation,
        _weights,
        _select,
        _random,
        _conflict,
        _similarity,
        _critics,
        mock_score_solution,
        mock_authority_cls,
        *_,
    ):
        ledger = self._mock_ledger()
        mock_ledger_cls.return_value = ledger

        solver = MagicMock()
        solver.name = "Architect"
        solver.role = "generalist"
        solver.act.return_value = {
            "agent": "Architect",
            "base_agent": "Architect",
            "solution": "fallback result",
            "confidence": 0.5,
        }
        mock_build_solvers.return_value = [solver]

        scored = {
            "solution": solver.act.return_value,
            "scores": {"weighted_total": 5.0, "authority_total": 5.0},
        }
        mock_score_solution.return_value = scored
        mock_authority_cls.return_value.decide.return_value = {
            "decision": scored,
            "action": "ACCEPT",
        }

        result = orchestrate("test task", self.memory)

        solver.act.assert_called_once()
        ledger.add.assert_any_call("ACTIVATION_FALLBACK", "generalist")
        self.assertEqual(result["final"]["agent"], "Architect")

    @patch("orchestrator.enforce_governance", return_value=[])
    @patch("orchestrator.spawn_successors", return_value=[])
    @patch("orchestrator.build_solvers", return_value=[])
    @patch("orchestrator.build_selection_weights", return_value={})
    @patch("orchestrator.select_unique_agents", return_value=[])
    @patch("orchestrator.build_critics", return_value=[])
    @patch("orchestrator.detect_conflict", return_value=False)
    @patch("orchestrator.detect_similarity", return_value=False)
    @patch("orchestrator.classify_task", return_value="general")
    @patch("orchestrator.cleanup_knowledge_memory")
    def test_empty_solvers_raises(
        self,
        _cleanup,
        _classify,
        _similarity,
        _conflict,
        _critics,
        _select,
        _weights,
        _build,
        _spawn,
        _governance,
    ):
        with self.assertRaises(RuntimeError):
            orchestrate("test task", self.memory)


if __name__ == "__main__":
    unittest.main()
