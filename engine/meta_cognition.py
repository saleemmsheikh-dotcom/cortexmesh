class MetaCognition:

    def __init__(self):
        self.agent_wins = {}
        self.selection_history = []

    def log_win(self, agent):
        self.agent_wins[agent] = self.agent_wins.get(agent, 0) + 1

    def dominant_agent(self):
        if not self.agent_wins:
            return None

        return max(self.agent_wins, key=self.agent_wins.get)

    def imbalance(self):
        if not self.agent_wins:
            return {}

        total = sum(self.agent_wins.values())

        return {
            k: v / total for k, v in self.agent_wins.items()
        }

    def report(self):
        dominant = self.dominant_agent()

        if not dominant:
            return "No dominant reasoning pattern yet."

        return (
            f"Meta Insight:\n"
            f"- Dominant reasoning style: {dominant}\n"
            f"- System bias: leaning toward {dominant} outputs\n"
            f"- Interpretation risk: alternative styles may be underweighted"
        )
