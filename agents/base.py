from config.roles import AGENT_PROFILES


class BaseAgent:
    def __init__(self, name, role=None):
        self.name = name
        self.role = role or name
        self.profile = (
            AGENT_PROFILES.get(role)
            or AGENT_PROFILES.get(name)
            or AGENT_PROFILES.get(str(role).title())
            or {}
        )

    def act(self, task, ledger):
        raise NotImplementedError
