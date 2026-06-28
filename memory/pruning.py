def should_prune(item):
    reliability = item.get("reliability", 1.0)
    uses = item.get("uses", 0)
    successes = item.get("successes", 0)

    if reliability < 0.5:
        return True

    if uses >= 5 and successes == 0:
        return True

    if uses >= 10:
        success_rate = successes / uses

        if success_rate < 0.3:
            return True

    return False


def archive_item(memory, category, task_type, item):
    if "memory_archive" not in memory:
        memory["memory_archive"] = {}

    memory["memory_archive"].setdefault(category, {})
    memory["memory_archive"][category].setdefault(task_type, [])
    memory["memory_archive"][category][task_type].append(item)
    memory["memory_archive"][category][task_type] = (
        memory["memory_archive"][category][task_type][-50:]
    )


def prune_knowledge(memory):
    for task_type, lessons in memory.get("knowledge_memory", {}).items():
        kept = []

        for item in lessons:
            if should_prune(item):
                archive_item(memory, "knowledge_memory", task_type, item)
            else:
                kept.append(item)

        memory["knowledge_memory"][task_type] = kept


def prune_negative_knowledge(memory):
    for task_type, warnings in memory.get("negative_knowledge", {}).items():
        kept = []

        for item in warnings:
            if isinstance(item, str):
                item = {
                    "warning": item,
                    "reliability": 1.0,
                    "uses": 0,
                    "successes": 0
                }

            if should_prune(item):
                archive_item(memory, "negative_knowledge", task_type, item)
            else:
                kept.append(item)

        memory["negative_knowledge"][task_type] = kept


def prune_conflicts(memory):
    conflicts = memory.get("knowledge_conflicts", [])
    kept = []

    for item in conflicts:
        if should_prune(item):
            archive_item(memory, "knowledge_conflicts", "general", item)
        else:
            kept.append(item)

    memory["knowledge_conflicts"] = kept[-50:]


def prune_memory(memory):
    prune_knowledge(memory)
    prune_negative_knowledge(memory)
    prune_conflicts(memory)
