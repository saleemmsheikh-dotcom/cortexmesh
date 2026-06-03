from engine.meta_cognition import MetaCognition
from engine.performance_memory import PerformanceMemory


class Ledger:

    def __init__(self):
        self.entries = []
        self.memory = PerformanceMemory()
        self.meta = MetaCognition()
        self.rebalance = {}

    def add(self, tag, content):
        self.entries.append({
            "tag": tag,
            "content": content
        })

        if tag == "FINAL":
            result = content
            agent = result.get("agent", "unknown")
            score = result["scores"]["total"] if "scores" in result else 5
            self.memory.log_agent(agent, score)

    def get(self, tag, default=None):
        for entry in reversed(self.entries):
            if entry["tag"] == tag:
                return entry["content"]

        return default
