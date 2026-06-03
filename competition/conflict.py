def detect_conflict(solutions):
    texts = [s["solution"] for s in solutions]

    # simple semantic divergence proxy (v2.2 lightweight)
    unique_patterns = set()

    for t in texts:
        if "systems" in t.lower():
            unique_patterns.add("systems")

        if "steps" in t.lower():
            unique_patterns.add("procedural")

        if "research" in t.lower():
            unique_patterns.add("analytical")

    return len(unique_patterns) > 1
