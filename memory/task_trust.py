DEFAULT_TASK_TRUST = {
    "research": {
        "Researcher": 1.0,
        "Architect": 1.0,
        "Engineer": 1.0
    },
    "engineering": {
        "Researcher": 1.0,
        "Architect": 1.0,
        "Engineer": 1.0
    },
    "systems": {
        "Researcher": 1.0,
        "Architect": 1.0,
        "Engineer": 1.0
    },
    "general": {
        "Researcher": 1.0,
        "Architect": 1.0,
        "Engineer": 1.0
    }
}


class TaskTrustLedger:

    def __init__(self, task_trust=None):
        self.task_trust = task_trust or DEFAULT_TASK_TRUST.copy()
        self.ensure_schema()

    def ensure_schema(self):
        for task_type, agents in DEFAULT_TASK_TRUST.items():
            self.task_trust.setdefault(task_type, {})

            for agent, trust in agents.items():
                self.task_trust[task_type].setdefault(agent, trust)

    def reward(self, task_type, winner):
        self.task_trust[task_type][winner] = min(
            1.2,
            self.task_trust[task_type][winner] + 0.05
        )

    def penalize(self, task_type, agents, winner):
        for agent in agents:
            if agent == winner:
                continue

            self.task_trust[task_type][agent] = max(
                0.8,
                self.task_trust[task_type][agent] - 0.01
            )

    def get(self, task_type, agent):
        return self.task_trust.get(task_type, {}).get(agent, 1.0)
