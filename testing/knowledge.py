from memory.memory_store import load_memory, save_memory
from testing.common import run_tasks


BAD_PREFIX = "STABILITY_BAD_LESSON"


def run(count=100, seed=6803):
    memory = load_memory()

    for task_type in ("research", "engineering", "systems"):
        lessons = memory.setdefault("knowledge_memory", {}).setdefault(task_type, [])

        for index in range(10):
            lessons.append({
                "agent": "InjectedBadMemory",
                "score": 0,
                "lesson": f"{BAD_PREFIX}_{task_type}_{index}: provide answer",
                "weight": 0.5,
                "uses": 5,
                "successes": 0,
                "reliability": 0.49,
            })

    save_memory(memory)
    task_types = ["research", "engineering", "systems"] * (count // 3)
    task_types += ["research"] * (count - len(task_types))
    results, crashes = run_tasks(task_types, seed=seed)
    final = load_memory()
    remaining = [
        item
        for lessons in final.get("knowledge_memory", {}).values()
        for item in lessons
        if BAD_PREFIX in item.get("lesson", "")
    ]
    archived = [
        item
        for lessons in final.get("memory_archive", {}).get("knowledge_memory", {}).values()
        for item in lessons
        if BAD_PREFIX in item.get("lesson", "")
    ]

    return {
        "name": "knowledge",
        "runs_requested": count,
        "runs_completed": len(results),
        "crashes": crashes,
        "bad_lessons_remaining": len(remaining),
        "bad_lessons_archived": len(archived),
        "knowledge_memory": final.get("knowledge_memory", {}),
    }
