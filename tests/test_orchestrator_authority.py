import unittest

from agents.authority import AuthorityAgent, compute_specialist_boost


class MockLedger:
    def __init__(self, memory=None, conflict=False):
        self.persistent_memory = memory or {}
        self._conflict = conflict

    def get(self, key, default=None):
        if key == "CONFLICT_MODE":
            return self._conflict
        return default


class TestAuthorityDecide(unittest.TestCase):
    def setUp(self):
        self.authority = AuthorityAgent()

    def _make_scored(self, agent, base_agent, weighted_total):
        return {
            "solution": {
                "agent": agent,
                "base_agent": base_agent,
            },
            "scores": {
                "weighted_total": weighted_total,
            },
        }

    def _ledger_for(self, scored_solutions, conflict=False):
        registry = {}
        for scored in scored_solutions:
            solution = scored["solution"]
            base_agent = solution["base_agent"]
            agent = solution["agent"]
            registry.setdefault(
                base_agent,
                {
                    "active": agent,
                    "strategies": {},
                },
            )
            registry[base_agent]["strategies"][agent] = {
                "version": 1,
                "status": "active",
                "traits": ["test"],
                "parent": None,
            }
        return MockLedger({"strategy_registry": registry}, conflict=conflict)

    def test_returns_dict(self):
        scored = [self._make_scored("a", "generalist", 5.0)]
        result = self.authority.decide(
            scored,
            self._ledger_for(scored),
            "general",
        )
        self.assertIsInstance(result, dict)

    def test_has_required_keys(self):
        scored = [self._make_scored("a", "generalist", 5.0)]
        result = self.authority.decide(
            scored,
            self._ledger_for(scored),
            "general",
        )
        self.assertIn("decision", result)
        self.assertIn("action", result)
        self.assertIn("task_type", result)

    def test_selects_highest_score(self):
        scored = [
            self._make_scored("low", "generalist", 3.0),
            self._make_scored("high", "generalist", 7.0),
            self._make_scored("mid", "generalist", 5.0),
        ]
        result = self.authority.decide(
            scored,
            self._ledger_for(scored),
            "general",
        )
        self.assertEqual(result["decision"]["solution"]["agent"], "high")

    def test_rejects_disallowed_strategies(self):
        scored = [
            self._make_scored("allowed", "generalist", 5.0),
            self._make_scored("blocked", "generalist", 10.0),
        ]
        ledger = self._ledger_for(scored)
        ledger.persistent_memory["strategy_registry"]["generalist"]["strategies"][
            "blocked"
        ]["status"] = "quarantined"

        result = self.authority.decide(scored, ledger, "general")

        self.assertEqual(result["decision"]["solution"]["agent"], "allowed")
        self.assertEqual(
            ledger.persistent_memory["governance_actions"][0]["action"],
            "authority_reject",
        )

    def test_raises_when_all_blocked(self):
        scored = [self._make_scored("blocked", "generalist", 5.0)]
        ledger = self._ledger_for(scored)
        ledger.persistent_memory["strategy_registry"]["generalist"]["strategies"][
            "blocked"
        ]["status"] = "quarantined"

        with self.assertRaises(RuntimeError):
            self.authority.decide(scored, ledger, "general")

    def test_applies_score_components(self):
        scored = [self._make_scored("a", "generalist", 5.0)]
        result = self.authority.decide(
            scored,
            self._ledger_for(scored),
            "general",
        )
        scores = result["decision"]["scores"]

        self.assertIn("authority_total", scores)
        self.assertIn("diversity_bonus", scores)
        self.assertIn("repetition_penalty", scores)
        self.assertIn("trust", scores)
        self.assertIn("calibration", scores)

    def test_specialist_boost_when_close(self):
        scored = [
            self._make_scored("general", "Engineer", 6.0),
            self._make_scored("special", "Architect", 5.95),
        ]
        result = self.authority.decide(
            scored,
            self._ledger_for(scored),
            "systems",
        )

        self.assertEqual(result["decision"]["solution"]["agent"], "special")
        self.assertGreater(result["decision"]["scores"]["specialist_boost"], 0.0)

    def test_no_specialist_boost_when_winning(self):
        scored = [
            self._make_scored("general", "Engineer", 5.0),
            self._make_scored("special", "Architect", 8.0),
        ]
        result = self.authority.decide(
            scored,
            self._ledger_for(scored),
            "systems",
        )

        self.assertEqual(result["decision"]["solution"]["agent"], "special")
        self.assertEqual(result["decision"]["scores"]["specialist_boost"], 0)

    def test_conflict_mode(self):
        scored = [self._make_scored("a", "generalist", 5.0)]
        result = self.authority.decide(
            scored,
            self._ledger_for(scored, conflict=True),
            "general",
        )
        self.assertEqual(result["action"], "CONFLICT_RESOLUTION")
        self.assertIn("alternatives", result)

    def test_no_conflict_mode(self):
        scored = [self._make_scored("a", "generalist", 5.0)]
        result = self.authority.decide(
            scored,
            self._ledger_for(scored),
            "general",
        )
        self.assertEqual(result["action"], "ACCEPT")
        self.assertNotIn("alternatives", result)


class TestSpecialistBoost(unittest.TestCase):
    def test_no_boost_when_winning(self):
        boost = compute_specialist_boost(8.0, 5.0)
        self.assertEqual(boost, 0.0)

    def test_boost_when_close_behind(self):
        boost = compute_specialist_boost(5.0, 6.0)
        self.assertGreater(boost, 0.0)

    def test_no_boost_when_too_far_behind(self):
        boost = compute_specialist_boost(2.0, 6.0)
        self.assertEqual(boost, 0.0)


if __name__ == "__main__":
    unittest.main()
