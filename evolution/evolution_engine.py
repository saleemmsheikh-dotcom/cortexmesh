from evolution.mutator import trait_for_failure
from evolution.strategy_registry import (
    MAX_GENERATION,
    base_agent_name,
    ensure_strategy_registry,
)


FAILURE_TRIGGER = 5
SURVIVAL_SAMPLE_SIZE = 3


def dominant_failure(memory, agent):
    failures = memory.get("failure_memory", {}).get(agent, {})

    if not failures:
        return None, 0

    reason = max(failures, key=failures.get)
    return reason, failures.get(reason, 0)


def spawn_successors(memory):
    registry = ensure_strategy_registry(memory)
    events = []

    for base_agent, data in registry.items():
        strategies = data["strategies"]

        if any(strategy.get("version", 1) >= MAX_GENERATION for strategy in strategies.values()):
            continue

        reason, count = dominant_failure(memory, base_agent)

        if count < FAILURE_TRIGGER:
            continue

        trait = trait_for_failure(reason)

        if not trait:
            continue

        child_name = f"{base_agent}_v2"

        if child_name in strategies:
            continue

        strategies[child_name] = {
            "version": 2,
            "traits": ["default", trait],
            "status": "challenger",
            "parent": base_agent,
            "created_from": reason
        }
        events.append({
            "event": "spawned",
            "agent": child_name,
            "parent": base_agent,
            "trait": trait,
            "reason": reason
        })

    return events


def log_strategy_scores(memory, scored_solutions):
    memory.setdefault("strategy_scores", {})

    for item in scored_solutions:
        agent = item["solution"]["agent"]
        score = item["scores"].get(
            "authority_total",
            item["scores"].get("total", 0)
        )

        memory["strategy_scores"].setdefault(agent, [])
        memory["strategy_scores"][agent].append(score)
        memory["strategy_scores"][agent] = memory["strategy_scores"][agent][-20:]


def average_score(memory, agent):
    scores = memory.get("strategy_scores", {}).get(agent, [])

    if not scores:
        return 0

    return sum(scores) / len(scores)


def promote_survivors(memory):
    registry = ensure_strategy_registry(memory)
    events = []

    for base_agent, data in registry.items():
        strategies = data["strategies"]

        for name, strategy in list(strategies.items()):
            if strategy.get("status") != "challenger":
                continue

            parent = strategy.get("parent") or base_agent_name(name)
            child_scores = memory.get("strategy_scores", {}).get(name, [])
            parent_scores = memory.get("strategy_scores", {}).get(parent, [])

            if (
                len(child_scores) < SURVIVAL_SAMPLE_SIZE
                or len(parent_scores) < SURVIVAL_SAMPLE_SIZE
            ):
                continue

            child_avg = average_score(memory, name)
            parent_avg = average_score(memory, parent)

            if child_avg > parent_avg:
                strategy["status"] = "active"
                data["active"] = name

                if parent in strategies:
                    strategies[parent]["status"] = "retired"

                events.append({
                    "event": "promoted",
                    "agent": name,
                    "retired": parent,
                    "child_avg": child_avg,
                    "parent_avg": parent_avg
                })
            else:
                strategy["status"] = "retired"
                data["active"] = parent

                events.append({
                    "event": "retired",
                    "agent": name,
                    "survivor": parent,
                    "child_avg": child_avg,
                    "parent_avg": parent_avg
                })

    return events


def run_evolution(memory, scored_solutions):
    if memory.get("governance_frozen"):
        return []

    ensure_strategy_registry(memory)
    allowed_solutions = [
        item
        for item in scored_solutions
        if _strategy_allowed(memory, item.get("solution", {}).get("agent"))
    ]
    log_strategy_scores(memory, allowed_solutions)

    events = []
    events.extend(spawn_successors(memory))
    events.extend(promote_survivors(memory))

    memory.setdefault("evolution_events", [])
    memory["evolution_events"].extend(events)
    memory["evolution_events"] = memory["evolution_events"][-50:]

    return events


def _strategy_allowed(memory, agent_name):
    if not agent_name:
        return False

    registry = memory.get("strategy_registry", {})

    for data in registry.values():
        strategy = data.get("strategies", {}).get(agent_name)

        if strategy:
            return (
                strategy.get("status") != "quarantined"
                and strategy.get("version", 1) <= MAX_GENERATION
            )

    return False
