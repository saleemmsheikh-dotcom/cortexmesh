def diversity_bonus(solutions):
    unique_agents = len(
        set(
            s["agent"]
            for s in solutions
        )
    )

    return unique_agents / 4.0
