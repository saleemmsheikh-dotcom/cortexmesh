def get_agent_weights(ledger, solvers):
    memory = ledger.memory

    weights = {}
    total = 0

    for s in solvers:
        f = memory.fitness(s.role)
        weights[s.role] = f
        total += f

    # normalise
    for k in weights:
        weights[k] /= total if total > 0 else 1

    return weights
