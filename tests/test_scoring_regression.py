import unittest

from agents.authority import AuthorityAgent, compute_specialist_boost
from competition.scorer import (
    apply_review_adjustments,
    compute_total_score,
    get_weights,
    score,
    score_solution,
    select_best,
)
from evolution.strategy_registry import default_registry
from memory.task_trust import DEFAULT_TASK_TRUST


class MockLedger:
    def __init__(self, memory=None):
        self.memory = {}
        self.persistent_memory = memory or {}


class TestScoringDeterminism(unittest.TestCase):
    def test_same_evidence_same_score(self):
        solution = {"evidence": {"has_systematic_structure": True}}
        self.assertEqual(score(solution, "logic"), score(solution, "logic"))

    def test_keyword_immune(self):
        a = {
            "solution": "systematic approach",
            "evidence": {"has_systematic_structure": True},
        }
        b = {
            "solution": "structured methodology",
            "evidence": {"has_systematic_structure": True},
        }
        self.assertEqual(score(a, "logic"), score(b, "logic"))

    def test_all_evidence_flags_adjust_scores(self):
        self.assertEqual(
            score({"evidence": {"has_logical_gaps": True}}, "logic"),
            4,
        )
        self.assertEqual(
            score({"evidence": {"has_failure_modes": True}}, "risk"),
            7,
        )
        self.assertEqual(
            score({"evidence": {"is_over_abstract": True}}, "risk"),
            4,
        )
        self.assertEqual(
            score({"evidence": {"has_alternatives": True}}, "completeness"),
            7,
        )
        self.assertEqual(
            score({"evidence": {"is_single_path": True}}, "completeness"),
            4,
        )

    def test_keyword_fallback_all_critics(self):
        self.assertEqual(score({"solution": "system structure"}, "logic"), 7)
        self.assertEqual(score({"solution": "step only"}, "logic"), 4)
        self.assertEqual(score({"solution": "fail validate"}, "risk"), 7)
        self.assertEqual(score({"solution": "abstract"}, "risk"), 4)
        self.assertEqual(
            score({"solution": "compare alternatives"}, "completeness"),
            7,
        )
        self.assertEqual(score({"solution": "single"}, "completeness"), 4)

    def test_scores_are_clamped(self):
        self.assertEqual(
            apply_review_adjustments(
                {"logic": 1, "risk": 5, "completeness": 5},
                [{"critic": "logic", "verdict": "negative", "confidence": 2}],
            )["logic"],
            0,
        )
        self.assertEqual(
            apply_review_adjustments(
                {"logic": 9, "risk": 5, "completeness": 5},
                [{"critic": "logic", "verdict": "positive", "confidence": 2}],
            )["logic"],
            10,
        )


class TestScorerWeightsAndReviews(unittest.TestCase):
    def test_weights_fallback_to_ledger_memory(self):
        ledger = type("Ledger", (), {"memory": {"critic_agreement": [0.1] * 4}})()
        self.assertEqual(
            tuple(round(weight, 2) for weight in get_weights(ledger)),
            (0.5, 0.3, 0.2),
        )

    def test_weights_handle_invalid_memory(self):
        ledger = type("Ledger", (), {"persistent_memory": "bad"})()
        self.assertEqual(get_weights(ledger), (0.4, 0.3, 0.3))

    def test_high_agreement_increases_risk_weight(self):
        ledger = MockLedger({"critic_agreement": [0.9, 0.9, 0.9, 0.9]})
        self.assertEqual(
            tuple(round(weight, 2) for weight in get_weights(ledger)),
            (0.3, 0.4, 0.3),
        )

    def test_review_adjustments_ignore_unknown_inputs(self):
        scores = {"logic": 5, "risk": 5, "completeness": 5}
        adjusted = apply_review_adjustments(
            scores,
            [
                {"critic": "novelty", "verdict": "positive"},
                {"critic": "risk", "verdict": "neutral"},
            ],
        )
        self.assertEqual(adjusted, scores)

    def test_positive_and_negative_reviews_affect_total(self):
        solution = {"solution": "system fail compare"}
        ledger = MockLedger()
        negative = compute_total_score(
            solution,
            [{"critic": "logic", "verdict": "negative", "confidence": 1.0}],
            ledger,
        )
        positive = compute_total_score(
            solution,
            [{"critic": "logic", "verdict": "positive", "confidence": 1.0}],
            ledger,
        )
        self.assertGreater(positive["total"], negative["total"])

    def test_score_solution_wraps_solution_and_scores(self):
        solution = {"solution": "system"}
        result = score_solution(solution, [], MockLedger())
        self.assertIs(result["solution"], solution)
        self.assertIn("weighted_total", result["scores"])

    def test_select_best_returns_highest_total(self):
        scored = [
            {"solution": {"agent": "low"}, "scores": {"total": 1}},
            {"solution": {"agent": "high"}, "scores": {"total": 9}},
        ]
        self.assertEqual(select_best(scored)["solution"]["agent"], "high")

    def test_select_best_rejects_empty_input(self):
        with self.assertRaises(ValueError):
            select_best([])


class TestSpecialistBoost(unittest.TestCase):
    def test_no_boost_when_winning(self):
        for overall in [1.0, 5.0, 9.0]:
            for specialist in [overall + 0.1, overall + 1.0, overall + 5.0]:
                boost = compute_specialist_boost(specialist, overall)
                self.assertEqual(
                    boost,
                    0.0,
                    f"specialist={specialist}, overall={overall}",
                )

    def test_boost_when_close_behind(self):
        boost = compute_specialist_boost(4.5, 5.0)
        self.assertEqual(boost, 0.15)

    def test_no_boost_when_too_far_behind(self):
        boost = compute_specialist_boost(2.0, 5.0)
        self.assertEqual(boost, 0.0)


class TestSinglePath(unittest.TestCase):
    def test_compute_total_score_has_no_repetition_penalty(self):
        solution = {
            "agent": "Architect",
            "evidence": {"has_systematic_structure": True},
        }
        memory = {
            "recent_structures": [{"agent": "Architect"} for _ in range(4)]
        }
        result = compute_total_score(solution, [], MockLedger(memory))

        self.assertNotIn("repetition_penalty", result)
        self.assertAlmostEqual(result["weighted_total"], 5.8)

    def test_authority_applies_repetition_once(self):
        memory = {
            "strategy_registry": default_registry(),
            "task_trust": DEFAULT_TASK_TRUST.copy(),
            "confidence_history": {},
            "recent_structures": [{"agent": "Architect"} for _ in range(2)],
        }
        scored = [{
            "solution": {
                "agent": "Architect",
                "base_agent": "Architect",
                "solution": "candidate",
            },
            "scores": {
                "logic": 7.0,
                "risk": 5.0,
                "completeness": 5.0,
                "weighted_total": 5.8,
                "total": 5.8,
            },
        }]

        result = AuthorityAgent().decide(
            scored,
            MockLedger(memory),
            task_type="systems",
        )
        scores = result["decision"]["scores"]

        self.assertEqual(scores["repetition_penalty"], 0.4)
        self.assertGreater(scores["authority_total"], 0)


if __name__ == "__main__":
    unittest.main()
