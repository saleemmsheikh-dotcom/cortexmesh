import unittest

from core.agent_selector import select_unique_agents


class TestSelectUniqueAgents(unittest.TestCase):
    def test_returns_list(self):
        weights = {"agent_a": 1.0, "agent_b": 1.0, "agent_c": 1.0}

        result = select_unique_agents(weights, k=3)

        self.assertIsInstance(result, list)

    def test_returns_k_agents(self):
        weights = {
            "agent_a": 1.0,
            "agent_b": 1.0,
            "agent_c": 1.0,
            "agent_d": 1.0,
        }

        result = select_unique_agents(weights, k=3)

        self.assertEqual(len(result), 3)

    def test_returns_all_when_less_than_k(self):
        weights = {"agent_a": 1.0, "agent_b": 1.0}

        result = select_unique_agents(weights, k=3)

        self.assertEqual(len(result), 2)

    def test_returns_empty_when_none_available(self):
        result = select_unique_agents({}, k=3)

        self.assertEqual(result, [])

    def test_no_duplicates(self):
        weights = {"agent_a": 100.0, "agent_b": 1.0, "agent_c": 1.0}

        result = select_unique_agents(weights, k=3)

        self.assertEqual(len(result), len(set(result)))

    def test_weighted_selection(self):
        weights = {"agent_a": 100.0, "agent_b": 1.0, "agent_c": 1.0}
        counts = {"agent_a": 0, "agent_b": 0, "agent_c": 0}

        for _ in range(1000):
            result = select_unique_agents(weights, k=1)
            counts[result[0]] += 1

        self.assertGreater(counts["agent_a"], counts["agent_b"])
        self.assertGreater(counts["agent_a"], counts["agent_c"])

    def test_quarantined_excluded(self):
        weights = {"agent_a": 1.0, "agent_b": 1.0, "agent_c": 1.0}
        registry = {
            "family": {
                "strategies": {
                    "agent_b": {"status": "quarantined"},
                },
            },
        }

        result = select_unique_agents(weights, k=3, strategy_registry=registry)

        self.assertNotIn("agent_b", result)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
