def compute_rebalance(memory):
    dist = memory.imbalance()

    if not dist:
        return {}

    adjustments = {}

    for agent, ratio in dist.items():
        if ratio > 0.5:
            adjustments[agent] = -0.2  # suppress dominant agent

        elif ratio < 0.2:
            adjustments[agent] = +0.15  # boost weak agent

        else:
            adjustments[agent] = 0.0

    return adjustments
