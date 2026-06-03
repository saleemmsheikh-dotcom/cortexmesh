import os


class ModeConfig:
    """
    Central control for CortexMesh execution mode.
    """

    FORCE_MODE = os.getenv("CORTEX_MODE")

    @staticmethod
    def get_mode(api_available: bool, budget_ok: bool):

        if ModeConfig.FORCE_MODE == "dev":
            return "dev"

        if ModeConfig.FORCE_MODE == "prod":
            if api_available and budget_ok:
                return "prod"
            return "dev"

        if api_available and budget_ok:
            return "prod"

        return "dev"