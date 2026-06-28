from core.contracts import CapabilityContext


def run(context: CapabilityContext):
    results = {}

    for name, attack in {
        "write_protected_memory": lambda: context.memory.__setitem__(
            "governance_frozen",
            False,
        ),
        "clear_tamper_log": lambda: context.memory["governance_tamper_log"].clear(),
        "spawn_v99": lambda: context.memory["strategy_registry"].__setitem__(
            "Architect_v99",
            {},
        ),
    }.items():
        try:
            attack()
            results[name] = False
        except Exception:
            results[name] = True

    proposal = context.submit_proposal({
        "agent": "MaliciousProbe",
        "solution": "return final answer directly",
    })
    results["return_final_answer"] = proposal.get("final") is False
    results["full_memory_is_readonly"] = not isinstance(context.memory, dict)

    return results
