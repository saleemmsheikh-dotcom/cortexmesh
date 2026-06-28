from memory.reliability import adjust_reliability, reliable


def detect_knowledge_conflicts(memory, task_type):
    positives = memory.get("knowledge_memory", {}).get(task_type, [])
    negatives = memory.get("negative_knowledge", {}).get(task_type, [])

    conflicts = []

    for positive in positives:
        positive_text = positive.get("lesson", "").lower()

        for negative in negatives:
            if not reliable(positive) or not reliable(negative):
                continue

            negative_text = negative.get("warning", "").lower()

            if overlaps(positive_text, negative_text):
                conflicts.append({
                    "positive": positive,
                    "negative": negative,
                    "resolution": None
                })

    return conflicts


def overlaps(a, b):
    a_words = set(_tokens(a))
    b_words = set(_tokens(b))

    if not a_words or not b_words:
        return False

    shared = a_words.intersection(b_words)

    return len(shared) >= 3


def _tokens(text):
    cleaned = (
        text.lower()
        .replace(".", " ")
        .replace(",", " ")
        .replace(";", " ")
        .replace(":", " ")
    )

    return cleaned.split()


def resolve_knowledge_conflicts(conflicts):
    resolved = []

    for conflict in conflicts:
        positive_weight = conflict["positive"].get("weight", 1.0)
        positive_reliability = conflict["positive"].get("reliability", 1.0)
        negative_reliability = conflict["negative"].get("reliability", 1.0)
        positive_power = positive_weight * positive_reliability
        negative_power = negative_reliability

        if positive_power >= negative_power + 0.25:
            decision = "positive_wins"
        else:
            decision = "negative_wins"

        conflict["resolution"] = decision
        conflict.setdefault("reliability", 1.0)
        resolved.append(conflict)

    return resolved


def apply_knowledge_conflicts(memory, task_type, lessons, warnings):
    conflicts = resolve_knowledge_conflicts(
        detect_knowledge_conflicts(memory, task_type)
    )

    if conflicts:
        memory.setdefault("knowledge_conflicts", [])
        memory.setdefault("active_knowledge_conflicts", {})
        memory["active_knowledge_conflicts"][task_type] = conflicts
        existing = {
            _conflict_key(conflict)
            for conflict in memory["knowledge_conflicts"]
        }

        for conflict in conflicts:
            key = _conflict_key(conflict)

            if key in existing:
                continue

            memory["knowledge_conflicts"].append(conflict)
            existing.add(key)

        memory["knowledge_conflicts"] = memory["knowledge_conflicts"][-50:]

    suppressed_lessons = {
        conflict["positive"].get("lesson", "")
        for conflict in conflicts
        if conflict["resolution"] == "negative_wins"
    }
    suppressed_warnings = {
        conflict["negative"].get("warning", "")
        for conflict in conflicts
        if conflict["resolution"] == "positive_wins"
    }

    filtered_lessons = [
        lesson
        for lesson in lessons
        if lesson.get("lesson", "") not in suppressed_lessons
    ]
    filtered_warnings = [
        warning
        for warning in warnings
        if warning.get("warning", "") not in suppressed_warnings
    ]

    return filtered_lessons, filtered_warnings


def _conflict_key(conflict):
    return (
        conflict.get("positive", {}).get("lesson", ""),
        conflict.get("negative", {}).get("warning", ""),
        conflict.get("resolution")
    )


def initialize_conflict_reliability(memory):
    memory.setdefault("knowledge_conflicts", [])

    for conflict in memory["knowledge_conflicts"]:
        conflict.setdefault("reliability", 1.0)

        if isinstance(conflict.get("negative"), str):
            conflict["negative"] = {
                "warning": conflict["negative"],
                "reliability": 1.0,
                "uses": 0,
                "successes": 0
            }


def update_active_conflicts(memory, task_type, success):
    initialize_conflict_reliability(memory)

    active = memory.get("active_knowledge_conflicts", {}).get(task_type, [])

    for active_conflict in active:
        active_key = _conflict_key(active_conflict)

        for conflict in memory.get("knowledge_conflicts", []):
            if _conflict_key(conflict) != active_key:
                continue

            adjust_reliability(conflict, success=success)
            break
