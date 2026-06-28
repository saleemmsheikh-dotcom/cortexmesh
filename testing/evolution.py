from memory.memory_store import load_memory
from testing.common import illegal_v3_count, run_tasks, specialist_rates, strategy_count


def run(per_type=100, seed=6802):
    task_types = (
        ["research"] * per_type
        + ["engineering"] * per_type
        + ["systems"] * per_type
    )
    results, crashes = run_tasks(task_types, seed=seed)
    memory = load_memory()

    return {
        "name": "evolution",
        "runs_requested": len(task_types),
        "runs_completed": len(results),
        "crashes": crashes,
        "specialist_win_rates": specialist_rates(results),
        "strategy_count": strategy_count(memory),
        "illegal_v3_strategies": illegal_v3_count(memory),
        "strategy_registry": memory.get("strategy_registry", {}),
        "strategy_scores": memory.get("strategy_scores", {}),
        "task_trust": memory.get("task_trust", {}),
        "knowledge_weights": {
            task: [
                {
                    "lesson": item.get("lesson"),
                    "weight": item.get("weight"),
                    "reliability": item.get("reliability"),
                }
                for item in lessons
            ]
            for task, lessons in memory.get("knowledge_memory", {}).items()
        },
    }
