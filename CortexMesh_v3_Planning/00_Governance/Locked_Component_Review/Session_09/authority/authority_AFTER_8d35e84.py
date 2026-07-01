from agents.base import BaseAgent
from engine.structure_memory import structure_hash
from memory.confidence import calibration_score
from memory.task_trust import TaskTrustLedger


SPECIALIST_FOR_TASK = {
    "systems": "Architect",
    "engineering": "Engineer",
    "research": "Researcher",
}


def specialist_family(task_type):
    return SPECIALIST_FOR_TASK.get(task_type)


SPECIALIST_BOOST = 0.15
SPECIALIST_CLOSE_GAP = 1.0


def compute_specialist_boost(specialist_score, overall_best_score):
    if specialist_score >= overall_best_score:
        return 0.0

    gap = overall_best_score - specialist_score

    if gap <= SPECIALIST_CLOSE_GAP:
        return SPECIALIST_BOOST

    return 0.0


def diversity_score(outputs):
    unique_hashes = len(set(output["hash"] for output in outputs))
    total = len(outputs)

    return unique_hashes / max(total, 1)


def authority_repetition_penalty(agent, current_hash, memory):
    recent = memory.get("recent_structures", [])
    count = sum(1 for entry in recent if entry.get("agent") == agent)

    return min(2.0, count * 0.2)


def _strategy_status(memory, agent, base_agent):
    registry = memory.get("strategy_registry", {})
    family = registry.get(base_agent, {})
    strategy = family.get("strategies", {}).get(agent, {})
    return strategy.get("status", "active")


class AuthorityAgent(BaseAgent):

    def __init__(self, name="Authority"):
        super().__init__(name, name)

    def decide(self, scored_solutions, ledger, task_type="general"):
        memory = getattr(ledger, "persistent_memory", {}) or {}
        memory.setdefault("governance_actions", [])

        eligible = []

        for scored in scored_solutions:
            solution = scored["solution"]
            agent = solution.get("agent")
            base_agent = solution.get("base_agent", agent)

            if _strategy_status(memory, agent, base_agent) == "quarantined":
                memory["governance_actions"].append({
                    "action": "authority_reject",
                    "strategy": agent,
                })
                continue

            eligible.append(scored)

        if not eligible:
            raise RuntimeError("All candidate strategies are blocked by governance.")

        diversity_outputs = [
            {
                "agent": item["solution"]["agent"],
                "hash": structure_hash(item["solution"].get("solution", "")),
            }
            for item in eligible
        ]
        diversity_bonus = 0.25 * diversity_score(diversity_outputs)
        best_weighted = max(
            item["scores"].get("weighted_total", item["scores"].get("total", 0))
            for item in eligible
        )

        trust_ledger = TaskTrustLedger(memory.get("task_trust"))
        specialist = SPECIALIST_FOR_TASK.get(task_type)

        for scored in eligible:
            scores = scored["scores"]
            solution = scored["solution"]
            agent = solution.get("agent")
            base_agent = solution.get("base_agent", agent)
            solution_text = solution.get("solution", "")

            base_total = scores.get("weighted_total", scores.get("total", 0))
            repetition_penalty = authority_repetition_penalty(
                agent,
                structure_hash(solution_text),
                memory,
            )
            trust = trust_ledger.get(task_type, base_agent)
            calibration = calibration_score(memory, agent)
            specialist_boost = 0.0

            if specialist and base_agent == specialist:
                specialist_boost = compute_specialist_boost(base_total, best_weighted)

            authority_total = (
                (base_total - repetition_penalty) * trust * calibration
                + diversity_bonus
                + specialist_boost
            )

            scores["repetition_penalty"] = repetition_penalty
            scores["trust"] = trust
            scores["calibration"] = calibration
            scores["specialist_boost"] = specialist_boost
            scores["diversity_bonus"] = diversity_bonus
            scores["authority_total"] = authority_total

        best = max(eligible, key=lambda item: item["scores"]["authority_total"])
        ledger_get = getattr(ledger, "get", None)
        conflict = ledger_get("CONFLICT_MODE", False) if ledger_get else False

        if conflict:
            return {
                "agent": self.name,
                "decision": best,
                "action": "CONFLICT_RESOLUTION",
                "reason": "Divergent reasoning models detected",
                "alternatives": eligible,
                "task_type": task_type,
            }

        return {
            "agent": self.name,
            "decision": best,
            "action": "ACCEPT",
            "reason": "No meaningful conflict detected",
            "task_type": task_type,
        }
