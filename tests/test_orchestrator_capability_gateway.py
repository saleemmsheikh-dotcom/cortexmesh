import unittest
from unittest.mock import patch

from orchestrator import orchestrate
from evolution.strategy_registry import default_registry


def memory_with_gateway():
    return {
        "runs": 0,
        "agent_wins": {},
        "authority_actions": {},
        "conflicts_detected": 0,
        "conflicts_resolved": 0,
        "recent_structures": [],
        "role_weights": {
            "Architect": 1.0,
            "Researcher": 1.0,
            "Engineer": 1.0,
        },
        "strategy_registry": default_registry(),
        "governance_actions": [],
        "capability_gateway_enabled": True,
        "capability_module": "capabilities.external_echo",
        "capability_input": {"mode": "audit"},
    }


class TestOrchestratorCapabilityGateway(unittest.TestCase):
    @patch("orchestrator.execute_capability")
    @patch("orchestrator.random.random", return_value=0.0)
    def test_orchestrator_invokes_external_runner_gateway(
        self,
        _random,
        execute_capability,
    ):
        execute_capability.return_value = {
            "status": "executed",
            "output": {"ok": True},
            "audit_trail": {"isolated": True},
        }

        result = orchestrate("Design a resilient gateway", memory_with_gateway())

        execute_capability.assert_called_once()
        self.assertIn("final", result)
        self.assertEqual(
            execute_capability.call_args.kwargs["capability_request"]["input"],
            {"mode": "audit"},
        )


if __name__ == "__main__":
    unittest.main()
