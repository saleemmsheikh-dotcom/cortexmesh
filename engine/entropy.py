import math


def compute_entropy(role_weights):
    values = list(role_weights.values())

    if not values:
        return 0.0

    total = sum(values)
    if total <= 0:
        return 0.0

    probs = [v / total for v in values if v > 0]
    max_entropy = math.log(len(values)) if len(values) > 1 else 1

    entropy = -sum(p * math.log(p) for p in probs)
    return entropy / max_entropy if max_entropy else 0.0
