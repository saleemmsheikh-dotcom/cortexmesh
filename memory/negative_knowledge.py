from memory.reliability import adjust_reliability, reliable


def initialize_negative_knowledge(memory):
    if "negative_knowledge" not in memory:
        memory["negative_knowledge"] = {
            "research": [],
            "engineering": [],
            "systems": [],
            "general": []
        }

    for task_type in ("research", "engineering", "systems", "general"):
        memory["negative_knowledge"].setdefault(task_type, [])
        upgraded = []

        for item in memory["negative_knowledge"][task_type]:
            if isinstance(item, str):
                upgraded.append({
                    "warning": item,
                    "reliability": 1.0,
                    "uses": 0,
                    "successes": 0
                })
            else:
                item.setdefault("reliability", 1.0)
                item.setdefault("uses", 0)
                item.setdefault("successes", 0)
                upgraded.append(item)

        memory["negative_knowledge"][task_type] = upgraded


def record_negative_lesson(memory, task_type, losing_pattern):
    initialize_negative_knowledge(memory)

    if any(
        item.get("warning") == losing_pattern
        for item in memory["negative_knowledge"][task_type]
    ):
        return False

    memory["negative_knowledge"][task_type].append({
        "warning": losing_pattern,
        "reliability": 1.0,
        "uses": 0,
        "successes": 0
    })
    memory["negative_knowledge"][task_type] = memory["negative_knowledge"][task_type][-20:]

    return True


def get_negative_lessons(memory, task_type, limit=3):
    initialize_negative_knowledge(memory)
    warnings = [
        item
        for item in memory["negative_knowledge"].get(task_type, [])
        if reliable(item)
    ]
    return warnings[-limit:]


def update_used_negative_lessons(memory, task_type, success):
    initialize_negative_knowledge(memory)

    used_warnings = memory.get("active_negative_lessons", {}).get(task_type, [])

    for warning in used_warnings:
        target = warning.get("warning") if isinstance(warning, dict) else warning

        for item in memory["negative_knowledge"].get(task_type, []):
            if item.get("warning") != target:
                continue

            item["uses"] = item.get("uses", 0) + 1

            if success:
                item["successes"] = item.get("successes", 0) + 1

            adjust_reliability(item, success=success)
            break
