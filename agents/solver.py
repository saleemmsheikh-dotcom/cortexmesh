from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.base import BaseAgent
from engine.model_router import call_model


class SolverAgent(BaseAgent):

    def __init__(self, name, role="general"):
        super().__init__(name, role)

    def _role_prompt(self):

        if self.role == "architect":
            return """
You are a Systems Architect.
Focus on structure, constraints, trade-offs, and long-term system stability.
Think in terms of components and interactions.
"""

        if self.role == "researcher":
            return """
You are a Research Analyst.
Focus on known methods, comparisons, literature-style reasoning, and alternatives.
Prioritise evidence and conceptual grounding.
"""

        if self.role == "engineer":
            return """
You are an Implementation Engineer.
Focus on feasibility, execution steps, and practical constraints.
Optimise for buildability and simplicity.
"""

        return """
You are a general solver.
Provide clear structured solutions.
"""

    def act(self, task, ledger):
        profile = self.profile

        system_prompt = f"""
You are {self.name}.

Your reasoning bias is: {profile.get('bias')}
Your strength is: {profile.get('strength')}
Your weakness is: {profile.get('weakness')}

You MUST reflect this cognitive style in your solution.
"""

        return {
            "agent": f"{self.name}:{self.role}",
            "solution": call_model(system_prompt, task)
        }


if __name__ == "__main__":
    print(SolverAgent("Test", "architect").act("Test task", None))
