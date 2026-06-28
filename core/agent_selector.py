import random


def weighted_choice(weight_map):
    agents = list(weight_map.keys())
    weights = list(weight_map.values())

    return random.choices(
        agents,
        weights=weights,
        k=1
    )[0]


def select_unique_agents(agent_weights, k=3, strategy_registry=None):
    """
    Returns unique agents.
    No duplicates allowed.
    """

    available = {}

    for agent, weight in agent_weights.items():
        if strategy_registry and _strategy_quarantined(agent, strategy_registry):
            continue

        available[agent] = weight

    selected = []

    count = min(k, len(available))

    for _ in range(count):
        chosen = weighted_choice(available)

        selected.append(chosen)

        del available[chosen]

    return selected


def _strategy_quarantined(strategy_name, strategy_registry):
    for family_data in strategy_registry.values():
        strategy = family_data.get("strategies", {}).get(strategy_name)

        if strategy and strategy.get("status") == "quarantined":
            return True

    return False
