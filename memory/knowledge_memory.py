from memory.reliability import adjust_reliability, reliable


def initialize_knowledge_memory(memory):
    if "knowledge_memory" not in memory:
        memory["knowledge_memory"] = {
            "research": [],
            "engineering": [],
            "systems": [],
            "general": []
        }

    for task_type in ("research", "engineering", "systems", "general"):
        memory["knowledge_memory"].setdefault(task_type, [])

    for lessons in memory["knowledge_memory"].values():
        for item in lessons:
            item.setdefault("weight", 1.0)
            item.setdefault("uses", 0)
            item.setdefault("successes", 0)
            item.setdefault("reliability", 1.0)


def record_lesson(memory, task_type, agent, solution, score, winner_agent=None):
    initialize_knowledge_memory(memory)

    lesson = extract_lesson(solution)

    if not should_store_lesson(
        memory=memory,
        task_type=task_type,
        agent=agent,
        winner_agent=winner_agent,
        lesson=lesson,
        score=score
    ):
        return False

    memory["knowledge_memory"].setdefault(task_type, [])
    memory["knowledge_memory"][task_type].append({
        "agent": agent,
        "score": score,
        "lesson": lesson,
        "weight": 1.0,
        "uses": 0,
        "successes": 0,
        "reliability": 1.0
    })

    memory["knowledge_memory"][task_type] = memory["knowledge_memory"][task_type][-20:]

    return True


def should_store_lesson(memory, task_type, agent, winner_agent, lesson, score):
    return (
        score_gate(score)
        and winner_gate(agent, winner_agent)
        and task_fit_gate(lesson, task_type)
        and novelty_gate(memory, task_type, lesson)
        and usefulness_gate(lesson)
    )


def score_gate(score):
    return score >= 6.5


def winner_gate(agent, winner_agent):
    if winner_agent is None:
        return True

    return agent == winner_agent


def task_fit_gate(lesson, task_type):
    text = lesson.lower()

    keywords = {
        "research": [
            "compare",
            "alternative",
            "evidence",
            "trade-off",
            "method",
            "approach"
        ],
        "engineering": [
            "implement",
            "step",
            "validate",
            "complexity",
            "execution",
            "iterate"
        ],
        "systems": [
            "system",
            "structure",
            "constraint",
            "dependency",
            "component",
            "stability"
        ],
        "general": []
    }

    if task_type == "general":
        return True

    return any(k in text for k in keywords.get(task_type, []))


def novelty_gate(memory, task_type, lesson):
    existing = memory.get("knowledge_memory", {}).get(task_type, [])
    normalized = normalize_lesson(lesson)

    for item in existing:
        if normalize_lesson(item.get("lesson", "")) == normalized:
            return False

    return True


def usefulness_gate(lesson):
    text = lesson.lower().strip()

    generic_rejects = [
        "define objectives",
        "think clearly",
        "improve solution",
        "provide answer",
        "solve problem",
        "be clear"
    ]

    if len(text) < 20:
        return False

    return not any(g in text for g in generic_rejects)


def normalize_lesson(text):
    return " ".join(
        text.lower()
        .replace(".", "")
        .replace(",", "")
        .replace(";", "")
        .split()
    )


def cleanup_knowledge_memory(memory):
    initialize_knowledge_memory(memory)

    for task_type, lessons in memory["knowledge_memory"].items():
        deduped = {}

        for item in lessons:
            key = normalize_lesson(item.get("lesson", ""))

            if not key:
                continue

            existing = deduped.get(key)

            if existing is None:
                deduped[key] = item
                continue

            if item.get("score", 0) > existing.get("score", 0):
                deduped[key] = item

        memory["knowledge_memory"][task_type] = list(deduped.values())


def reinforce_lesson(memory, task_type, lesson_text, success):
    initialize_knowledge_memory(memory)

    lessons = memory["knowledge_memory"].get(task_type, [])
    target = normalize_lesson(lesson_text)

    for item in lessons:
        if normalize_lesson(item.get("lesson", "")) == target:
            item["uses"] = item.get("uses", 0) + 1

            if success:
                item["successes"] = item.get("successes", 0) + 1
                item["weight"] = min(
                    2.0,
                    item.get("weight", 1.0) + 0.05
                )
                adjust_reliability(item, success=True)
            else:
                item["weight"] = max(
                    0.5,
                    item.get("weight", 1.0) - 0.03
                )
                adjust_reliability(item, success=False)

            return True

    return False


def update_used_lessons(memory, task_type, success):
    initialize_knowledge_memory(memory)

    used_lessons = memory.get("active_lessons", {}).get(task_type, [])

    for lesson in used_lessons:
        reinforce_lesson(
            memory,
            task_type,
            lesson,
            success=success
        )


def decay_lessons(memory, decay=0.995):
    initialize_knowledge_memory(memory)

    for task_type, lessons in memory["knowledge_memory"].items():
        for item in lessons:
            item["weight"] = max(
                0.5,
                item.get("weight", 1.0) * decay
            )


def reliable_lessons(memory, task_type):
    initialize_knowledge_memory(memory)

    return [
        lesson
        for lesson in memory["knowledge_memory"].get(task_type, [])
        if reliable(lesson)
    ]


def extract_lesson(solution):
    lines = [
        line.strip("- ").strip()
        for line in solution.splitlines()
        if line.strip().startswith("-")
    ]

    if not lines:
        return solution[:200]

    return "; ".join(lines[:3])
