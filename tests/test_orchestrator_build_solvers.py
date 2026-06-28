import unittest

from agents.local_solver import LocalSolverAgent
from agents.solver import SolverAgent
from orchestrator import build_solvers


class TestBuildSolvers(unittest.TestCase):
    def setUp(self):
        self.mock_memory = {
            "strategy_registry": {
                "Architect": {
                    "active": "Architect_test",
                    "strategies": {
                        "Architect_test": {
                            "version": 1,
                            "status": "active",
                            "traits": ["stronger_reasoning"],
                            "parent": None,
                        }
                    },
                }
            }
        }

    def test_build_solvers_returns_list(self):
        """build_solvers must return a list."""
        solvers = build_solvers("prod", self.mock_memory)
        self.assertIsInstance(solvers, list)

    def test_build_solvers_returns_solver_instances(self):
        """Each item must be a SolverAgent in prod mode."""
        solvers = build_solvers("prod", self.mock_memory)
        self.assertTrue(all(isinstance(s, SolverAgent) for s in solvers))

    def test_build_solvers_returns_local_solver_in_dev_mode(self):
        """Dev mode must use LocalSolverAgent."""
        solvers = build_solvers("dev", self.mock_memory)
        self.assertTrue(all(isinstance(s, LocalSolverAgent) for s in solvers))

    def test_build_solvers_empty_memory_uses_default_registry(self):
        """Empty memory is schema-initialized with default strategies."""
        solvers = build_solvers("prod", {})
        self.assertEqual(len(solvers), 3)
        self.assertTrue(all(isinstance(s, SolverAgent) for s in solvers))

    def test_build_solvers_no_active_strategies(self):
        """No active strategies must return empty list."""
        no_active = {
            "strategy_registry": {
                family: {
                    "active": family,
                    "strategies": {
                        family: {
                            "version": 1,
                            "status": "quarantined",
                            "traits": ["default"],
                            "parent": None,
                        }
                    },
                }
                for family in ("Architect", "Researcher", "Engineer")
            }
        }
        solvers = build_solvers("prod", no_active)
        self.assertEqual(solvers, [])

    def test_build_solvers_sets_attributes(self):
        """Solver must have base_agent, traits, and version set."""
        solvers = build_solvers("prod", self.mock_memory)
        solver = next(s for s in solvers if s.name == "Architect_test")
        self.assertEqual(solver.base_agent, "Architect")
        self.assertEqual(solver.strategy_traits, ["stronger_reasoning"])
        self.assertEqual(solver.strategy_version, 1)

    def test_build_solvers_multiple_strategies(self):
        """Multiple active strategies must return multiple solvers."""
        multi_memory = {
            "strategy_registry": {
                "Architect": {
                    "active": "Architect",
                    "strategies": {
                        "Architect": {
                            "version": 1,
                            "status": "active",
                            "traits": ["default"],
                            "parent": None,
                        },
                        "Architect_v2": {
                            "version": 2,
                            "status": "challenger",
                            "traits": ["risk_expansion"],
                            "parent": "Architect",
                        },
                    },
                },
                "Researcher": {
                    "active": "Researcher",
                    "strategies": {
                        "Researcher": {
                            "version": 1,
                            "status": "active",
                            "traits": ["default"],
                            "parent": None,
                        }
                    },
                },
                "Engineer": {
                    "active": "Engineer",
                    "strategies": {
                        "Engineer": {
                            "version": 1,
                            "status": "active",
                            "traits": ["default"],
                            "parent": None,
                        }
                    },
                },
            }
        }
        solvers = build_solvers("prod", multi_memory)
        self.assertEqual(len(solvers), 4)
        self.assertEqual(
            [solver.name for solver in solvers],
            ["Architect", "Architect_v2", "Researcher", "Engineer"],
        )


if __name__ == "__main__":
    unittest.main()
