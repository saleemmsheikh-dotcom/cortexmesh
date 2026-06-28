from core.capability_guardrails import SecurityError


class CapabilitySandbox:
    """
    Deprecated by D+ architecture.

    In-process sandboxing is not a security boundary. Use
    CapabilityGuardrails for project-maintained accident prevention, or
    ExternalRunner for untrusted capability isolation.
    """

    def __init__(self, *_args, **_kwargs):
        raise SecurityError(
            "CapabilitySandbox is deprecated by D+. "
            "Use CapabilityGuardrails for core/certified code or "
            "ExternalRunner for external code."
        )
