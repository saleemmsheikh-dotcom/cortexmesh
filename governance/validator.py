from governance.constitution import CONSTITUTION


def validate_governance(memory):
    issues = []
    limits = CONSTITUTION["hard_limits"]
    registry = memory.get("strategy_registry", {})

    for family, data in registry.items():
        strategies = data.get("strategies", {})
        participating = [
            strategy
            for strategy in strategies.values()
            if strategy.get("status") != "quarantined"
        ]

        if len(participating) > limits["max_active_strategies_per_agent"]:
            issues.append(f"{family}: strategy overflow")

        for name, strategy in strategies.items():
            version = strategy.get("version", 1)

            if version > limits["max_strategy_version"]:
                issues.append(f"{name}: illegal version")

    return issues
