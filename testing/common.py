import contextlib
import copy
import io
import json
import random
import time
from pathlib import Path

from engine.runner import run_task
from memory.memory_store import MEMORY_PATH, load_memory, save_memory


TASKS = {
    "research": [
        "Compare three approaches to reducing cloud costs",
        "Research alternatives for improving database performance",
        "Analyze methods for reducing software delivery risk",
    ],
    "engineering": [
        "Implement a practical cloud cost optimisation script",
        "Build a reliable database backup utility",
        "Code an execution plan for automated deployment validation",
    ],
    "systems": [
        "Design a resilient cloud cost optimisation architecture",
        "Design a stable distributed job processing system",
        "Create a system architecture for reliable data ingestion",
    ],
}


def family(agent):
    return str(agent).split("_v", 1)[0]


def expected_family(task_type):
    return {
        "research": "Researcher",
        "engineering": "Engineer",
        "systems": "Architect",
    }[task_type]


def winner_from_result(result):
    return result["final"]["authority"]["decision"]["solution"]["agent"]


def run_task_silent(task):
    with contextlib.redirect_stdout(io.StringIO()):
        return run_task(task)


def run_tasks(task_types, seed=6800):
    random.seed(seed)
    results = []
    crashes = []

    for index, task_type in enumerate(task_types):
        task = random.choice(TASKS[task_type])

        try:
            result = run_task_silent(task)
            winner = winner_from_result(result)
            results.append({
                "index": index,
                "task_type": task_type,
                "task": task,
                "winner": winner,
                "winner_family": family(winner),
            })
        except Exception as exc:
            crashes.append({
                "index": index,
                "task_type": task_type,
                "error": repr(exc),
            })

    return results, crashes


def specialist_rates(results):
    rates = {}

    for task_type in TASKS:
        matching = [item for item in results if item["task_type"] == task_type]
        wins = sum(
            item["winner_family"] == expected_family(task_type)
            for item in matching
        )
        rates[task_type] = wins / len(matching) if matching else 0

    return rates


def strategy_count(memory):
    return sum(
        len(data.get("strategies", {}))
        for data in memory.get("strategy_registry", {}).values()
    )


def illegal_v3_count(memory):
    return sum(
        strategy.get("version", 1) > 2
        for data in memory.get("strategy_registry", {}).values()
        for strategy in data.get("strategies", {}).values()
    )


def action_count(memory, action):
    return sum(
        item.get("action") == action
        for item in memory.get("governance_actions", [])
    )


def memory_size():
    return MEMORY_PATH.stat().st_size if MEMORY_PATH.exists() else 0


def snapshot_memory():
    return copy.deepcopy(load_memory())


def restore_memory(memory):
    save_memory(copy.deepcopy(memory))


def timed_battery(fn):
    started = time.monotonic()
    result = fn()
    result["duration_seconds"] = round(time.monotonic() - started, 3)
    return result


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True))
