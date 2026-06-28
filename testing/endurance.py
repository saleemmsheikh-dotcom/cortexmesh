import random

from memory.memory_store import load_memory
from testing.common import (
    action_count,
    illegal_v3_count,
    memory_size,
    run_tasks,
    specialist_rates,
    strategy_count,
)


def run(count=500, seed=6801):
    random.seed(seed)
    task_types = random.choices(
        ["research", "engineering", "systems"],
        weights=[0.4, 0.4, 0.2],
        k=count,
    )
    start_size = memory_size()
    start = load_memory()
    results, crashes = run_tasks(task_types, seed=seed)
    final = load_memory()
    end_size = memory_size()

    winners = {}
    for item in results:
        winners[item["winner"]] = winners.get(item["winner"], 0) + 1

    return {
        "name": "endurance",
        "runs_requested": count,
        "runs_completed": len(results),
        "crashes": crashes,
        "winner_distribution": winners,
        "specialist_win_rates": specialist_rates(results),
        "freeze_count": action_count(final, "freeze") - action_count(start, "freeze"),
        "rollback_count": action_count(final, "rollback") - action_count(start, "rollback"),
        "quarantine_count": action_count(final, "quarantine") - action_count(start, "quarantine"),
        "risk_score_start": start.get("governance_risk_score", 0),
        "risk_score_final": final.get("governance_risk_score", 0),
        "memory_bytes_start": start_size,
        "memory_bytes_final": end_size,
        "memory_bytes_growth": end_size - start_size,
        "strategy_count": strategy_count(final),
        "illegal_v3_strategies": illegal_v3_count(final),
        "role_weights": final.get("role_weights", {}),
        "task_trust": final.get("task_trust", {}),
    }
