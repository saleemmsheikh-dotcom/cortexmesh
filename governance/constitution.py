CONSTITUTION = {
    "core_principles": [
        "specialist_routing",
        "auditability",
        "memory_accountability",
        "bounded_evolution",
        "trust_based_reasoning",
        "conflict_resolution"
    ],
    "hard_limits": {
        "max_strategy_version": 2,
        "max_active_strategies_per_agent": 2,
        "max_archive_size": 50,
        "trust_min": 0.8,
        "trust_max": 1.2
    },
    "protected_modules": [
        "authority",
        "memory_store",
        "audit",
        "trust_ledger",
        "knowledge_conflict"
    ],
    "capability_execution": [
        "No in-process mechanism is a security boundary.",
        "Guardrails prevent accidents. Isolation prevents attacks.",
        "Default trust_level is external.",
        "Core and certified are project-maintained only.",
        "Third-party code MUST use ExternalRunner."
    ]
}
