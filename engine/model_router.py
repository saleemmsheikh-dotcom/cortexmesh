import os
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.model import MODEL_NAME


STYLE_INJECTION = {
    "Architect": "prioritise structure and system-level abstraction",
    "Researcher": "prioritise evidence comparison and alternatives",
    "Engineer": "prioritise step-by-step execution clarity"
}


def _style_instruction(system_prompt):
    for agent, instruction in STYLE_INJECTION.items():
        if agent in system_prompt:
            return instruction

    return None


def _fallback_response(system_prompt, user_prompt):

    prompt = str(user_prompt).strip()
    style = _style_instruction(system_prompt)

    # -------------------------
    # SOLVERS
    # -------------------------

    if "Systems Architect" in system_prompt or "Architect" in system_prompt:

        return (
            "SYSTEMS VIEW\n"
            f"Style: {style or STYLE_INJECTION['Architect']}\n"
            "- Define system objectives.\n"
            "- Map constraints and dependencies.\n"
            "- Optimise interactions between components.\n"
            "- Monitor feedback loops.\n"
            "- Design for long-term stability."
        )

    if "Research Analyst" in system_prompt or "Researcher" in system_prompt:

        return (
            "RESEARCH VIEW\n"
            f"Style: {style or STYLE_INJECTION['Researcher']}\n"
            "- Compare alternative approaches.\n"
            "- Identify best practices.\n"
            "- Evaluate trade-offs.\n"
            "- Review known methods.\n"
            "- Recommend evidence-based options."
        )

    if "Implementation Engineer" in system_prompt or "Engineer" in system_prompt:

        return (
            "ENGINEERING VIEW\n"
            f"Style: {style or STYLE_INJECTION['Engineer']}\n"
            "- Define implementation phases.\n"
            "- Prioritise high-impact actions.\n"
            "- Reduce complexity.\n"
            "- Validate results continuously.\n"
            "- Iterate and improve."
        )

    # -------------------------
    # CRITICS
    # -------------------------

    if "Logic Critic" in system_prompt:

        return f"""
LOGIC REVIEW (variant)
Hash:{hash(user_prompt) % 100}

Focus:
- hidden assumptions
- logical gaps
- internal consistency
"""

    if "Risk Critic" in system_prompt:

        return f"""
RISK REVIEW (variant)
Hash:{hash(user_prompt) % 100}

Focus:
- failure modes
- operational risks
- edge cases
"""

    if "Completeness Critic" in system_prompt:

        return f"""
COMPLETENESS REVIEW (variant)
Hash:{hash(user_prompt) % 100}

Focus:
- missing components
- blind spots
- coverage gaps
"""

    # -------------------------
    # GENERIC FALLBACK
    # -------------------------

    return (
        "1. Define the goal and constraints clearly.\n"
        "2. Rank resources by impact, cost, and urgency.\n"
        "3. Allocate incrementally, measure results, and rebalance.\n"
        f"\nTask: {prompt}"
    )


def call_model(system_prompt, user_prompt):
    style = _style_instruction(system_prompt)
    if style:
        system_prompt = f"{system_prompt.strip()}\n\nStyle directive: {style}"

    if not os.getenv("OPENAI_API_KEY") and not os.getenv("OPENAI_ADMIN_KEY"):
        return _fallback_response(system_prompt, user_prompt)

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "Install the OpenAI SDK with: pip install openai"
        ) from exc

    client = OpenAI()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt.strip()
            },
            {
                "role": "user",
                "content": str(user_prompt).strip()
            },
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content
