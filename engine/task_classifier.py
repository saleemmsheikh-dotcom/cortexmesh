def classify_task(task: str):
    t = task.lower()

    if any(k in t for k in ["design", "system", "architecture"]):
        return "systems"

    if any(k in t for k in ["compare", "research", "analyze"]):
        return "research"

    if any(k in t for k in ["build", "implement", "code", "execute"]):
        return "engineering"

    return "general"
