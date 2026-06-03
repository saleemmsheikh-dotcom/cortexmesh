class PerformanceMemory:

    def __init__(self):
        self.agent_scores = {}
        self.agent_usage = {}

    def log_agent(self, name, score):
        if name not in self.agent_scores:
            self.agent_scores[name] = []

        self.agent_scores[name].append(score)

        if name not in self.agent_usage:
            self.agent_usage[name] = 0

        self.agent_usage[name] += 1

    def fitness(self, name):
        scores = self.agent_scores.get(name, [])
        usage = self.agent_usage.get(name, 1)

        if not scores:
            return 0.5

        avg_score = sum(scores) / len(scores)

        # efficiency = quality per usage
        return avg_score / (1 + (usage * 0.1))
