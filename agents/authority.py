from agents.base import BaseAgent
from engine.structure_memory import structure_hash


def get_weights(task_type):
    if task_type == "systems":
        return {"logic": 0.5, "risk": 0.2, "completeness": 0.3}

    if task_type == "engineering":
        return {"logic": 0.2, "risk": 0.5, "completeness": 0.3}

    if task_type == "research":
        return {"logic": 0.3, "risk": 0.2, "completeness": 0.5}

    return {"logic": 0.33, "risk": 0.33, "completeness": 0.34}


def diversity_score(outputs):
    unique_hashes = len(set(o["hash"] for o in outputs))
    total = len(outputs)

    return unique_hashes / max(total, 1)


class AuthorityAgent(BaseAgent):

    def __init__(self, name="Authority"):
        super().__init__(name, name)

    def decide(self, scored_solutions, ledger, task_type="general"):
        weights = get_weights(task_type)
        diversity_outputs = [
            {
                "agent": scored_solution["solution"]["agent"],
                "hash": structure_hash(scored_solution["solution"]["solution"])
            }
            for scored_solution in scored_solutions
        ]
        diversity_score_weight = 0.25
        diversity_bonus = diversity_score_weight * diversity_score(diversity_outputs)

        for scored_solution in scored_solutions:
            scores = scored_solution["scores"]
            scores["authority_total"] = (
                scores["logic"] * weights["logic"] +
                scores["risk"] * weights["risk"] +
                scores["completeness"] * weights["completeness"]
            ) + diversity_bonus
            scores["diversity_bonus"] = diversity_bonus

        best = max(scored_solutions, key=lambda x: x["scores"]["authority_total"])

        conflict = ledger.get("CONFLICT_MODE", False)

        if conflict:
            return {
                "agent": self.name,
                "decision": best,
                "action": "CONFLICT_RESOLUTION",
                "reason": "Divergent reasoning models detected",
                "alternatives": scored_solutions,
                "task_type": task_type,
                "weights": weights
            }

        return {
            "agent": self.name,
            "decision": best,
            "action": "ACCEPT",
            "reason": "No meaningful conflict detected",
            "task_type": task_type,
            "weights": weights
        }
