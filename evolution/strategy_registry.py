BASE_AGENTS = ("Architect", "Researcher", "Engineer")
MAX_GENERATION = 2

TRAIT_INSTRUCTIONS = {
    "default": "Use the agent's standard reasoning style.",
    "anti_repetition": "Generate a structurally different solution than prior attempts.",
    "stronger_reasoning": "Make assumptions and reasoning steps explicit.",
    "risk_expansion": "Add risks, edge cases, failure modes, and safeguards.",
    "coverage_expansion": "Add missing coverage, alternatives, and edge cases.",
    "confidence_reduction": "Be conservative with confidence unless the task match is direct.",
    "task_alignment": "Align tightly with the task type and expected specialist role."
}


def base_agent_name(agent_name):
    if "_v" in agent_name:
        return agent_name.split("_v", 1)[0]

    return agent_name


def default_registry():
    return {
        agent: {
            "active": agent,
            "strategies": {
                agent: {
                    "version": 1,
                    "traits": ["default"],
                    "status": "active",
                    "parent": None
                }
            }
        }
        for agent in BASE_AGENTS
    }


def ensure_strategy_registry(memory):
    memory.setdefault("strategy_registry", default_registry())
    registry = memory["strategy_registry"]

    for agent, defaults in default_registry().items():
        registry.setdefault(agent, defaults)
        registry[agent].setdefault("active", agent)
        registry[agent].setdefault("strategies", {})
        registry[agent]["strategies"].setdefault(
            agent,
            defaults["strategies"][agent]
        )

    memory.setdefault("strategy_scores", {})

    return registry


def strategy_for_agent(memory, agent_name):
    registry = ensure_strategy_registry(memory)
    base_agent = base_agent_name(agent_name)

    return registry.get(base_agent, {}).get("strategies", {}).get(
        agent_name,
        {
            "version": 1,
            "traits": ["default"],
            "status": "active",
            "parent": None
        }
    )


def active_strategy_specs(memory):
    registry = ensure_strategy_registry(memory)
    specs = []

    for base_agent, data in registry.items():
        strategies = data.get("strategies", {})

        for name, strategy in strategies.items():
            if (
                strategy.get("status") in ("active", "challenger")
                and strategy.get("version", 1) <= MAX_GENERATION
            ):
                specs.append({
                    "name": name,
                    "base_agent": base_agent,
                    "version": strategy.get("version", 1),
                    "traits": strategy.get("traits", ["default"]),
                    "parent": strategy.get("parent")
                })

    return specs


def trait_prompt(traits):
    instructions = [
        TRAIT_INSTRUCTIONS[trait]
        for trait in traits
        if trait in TRAIT_INSTRUCTIONS and trait != "default"
    ]

    if not instructions:
        return None

    return "\n".join(f"- {instruction}" for instruction in instructions)
