ROLES = {
    "solver": "generates solutions",
    "reviewer": "evaluates solutions",
    "authority": "final selection"
}


AGENT_PROFILES = {
    "Architect": {
        "bias": "systems",
        "strength": "structure",
        "weakness": "over-generalisation",
        "scoring_focus": ["completeness", "logic"]
    },

    "Researcher": {
        "bias": "evidence",
        "strength": "comparison",
        "weakness": "indecision",
        "scoring_focus": ["logic", "risk"]
    },

    "Engineer": {
        "bias": "execution",
        "strength": "implementation",
        "weakness": "under-explaining",
        "scoring_focus": ["risk", "completeness"]
    }
}
