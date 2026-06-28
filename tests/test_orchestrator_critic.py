import unittest
from unittest.mock import patch

from agents.reviewer import ReviewerAgent


class TestCriticReview(unittest.TestCase):
    def test_returns_dict(self):
        critic = ReviewerAgent("logic")
        with patch("agents.reviewer.call_model", return_value="test review"):
            result = critic.review({"solution": "test solution"})
        self.assertIsInstance(result, dict)

    def test_has_required_keys(self):
        critic = ReviewerAgent("logic")
        with patch("agents.reviewer.call_model", return_value="test review"):
            result = critic.review({"solution": "test solution"})
        self.assertIn("critic", result)
        self.assertIn("review", result)
        self.assertIn("signal", result)

    def test_critic_field_matches_role(self):
        critic = ReviewerAgent("logic")
        with patch("agents.reviewer.call_model", return_value="test"):
            result = critic.review({"solution": "test"})
        self.assertEqual(result["critic"], "logic")

    def test_signal_format(self):
        critic = ReviewerAgent("risk")
        with patch("agents.reviewer.call_model", return_value="test"):
            result = critic.review({"solution": "test"})
        self.assertEqual(result["signal"], "refine:risk")

    def test_review_content_from_model(self):
        critic = ReviewerAgent("logic")
        with patch("agents.reviewer.call_model", return_value="model output"):
            result = critic.review({"solution": "test"})
        self.assertEqual(result["review"], "model output")

    def test_different_roles(self):
        logic_critic = ReviewerAgent("logic")
        risk_critic = ReviewerAgent("risk")
        self.assertNotEqual(logic_critic._role_prompt(), risk_critic._role_prompt())

    def test_handles_empty_solution(self):
        critic = ReviewerAgent("logic")
        with patch("agents.reviewer.call_model", return_value=""):
            result = critic.review({"solution": ""})
        self.assertEqual(result["review"], "")


if __name__ == "__main__":
    unittest.main()
