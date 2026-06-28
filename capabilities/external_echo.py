def run(context):
    return {
        "task": context.task,
        "input": context.input,
        "memory_keys": sorted(context.memory_context.keys()),
    }
