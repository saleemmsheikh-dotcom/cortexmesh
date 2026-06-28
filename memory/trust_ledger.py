class TrustLedger:

    def __init__(self, agent_trust=None):
        self.agent_trust = agent_trust or {
            "Architect": 1.0,
            "Researcher": 1.0,
            "Engineer": 1.0
        }

    def reward(self, winner):
        self.agent_trust[winner] = min(
            2.0,
            self.agent_trust[winner] + 0.05
        )

    def penalize(self, agents, winner):
        for agent in agents:
            if agent == winner:
                continue

            self.agent_trust[agent] = max(
                0.5,
                self.agent_trust[agent] - 0.01
            )

    def get(self, agent):
        return self.agent_trust.get(agent, 1.0)
