import hashlib


def structure_hash(text: str):
    normalized = " ".join(text.lower().split())
    return hashlib.md5(normalized.encode()).hexdigest()


def repetition_penalty(agent, current_hash, memory):
    recent = memory.get("recent_structures", [])

    count = sum(
        1 for x in recent
        if x["agent"] == agent and x["hash"] == current_hash
    )

    return min(2.0, count * 0.5)
