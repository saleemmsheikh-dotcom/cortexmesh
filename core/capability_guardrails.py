import builtins
import copy
import io
import os
from types import MappingProxyType

from core.external_runner import ExternalRunner


class CapabilityGuardrails:
    """
    Accident prevention for in-process capabilities.
    NOT a security boundary. Does NOT prevent hostile code.
    """

    def __init__(self, memory, task):
        self._memory = memory
        self._task = str(task)
        self._violations = []
        self._original_open = builtins.open
        self._original_io_open = io.open

    def _guarded_open(self, path, *args, **kwargs):
        mode = _extract_mode(args, kwargs)

        if _is_write_mode(mode):
            abs_path = os.path.abspath(path)
            self._violations.append(f"guardrail:filesystem:{abs_path}")
            raise PermissionError(f"Guardrail: blocked write to {path}")

        return self._original_open(path, *args, **kwargs)

    def _guarded_io_open(self, path, *args, **kwargs):
        mode = _extract_mode(args, kwargs)

        if _is_write_mode(mode):
            abs_path = os.path.abspath(path)
            self._violations.append(f"guardrail:filesystem:{abs_path}")
            raise PermissionError(f"Guardrail: blocked write to {path}")

        return self._original_io_open(path, *args, **kwargs)

    def __enter__(self):
        builtins.open = self._guarded_open
        io.open = self._guarded_io_open
        return self

    def __exit__(self, *args):
        builtins.open = self._original_open
        io.open = self._original_io_open

    def get_memory_view(self):
        return _readonly(copy.deepcopy(self._memory))

    @property
    def violations(self):
        return list(self._violations)


class SecurityError(Exception):
    """Untrusted capability attempted in-process execution."""


class SecurityBoundaryViolation(SecurityError):
    """External capability attempted to bypass ExternalRunner isolation."""


class CapabilityContext:
    TRUST_LEVELS = {"core", "certified", "external"}

    def __init__(self, memory, task, trust_level="external"):
        if trust_level not in self.TRUST_LEVELS:
            raise ValueError(f"Invalid trust_level: {trust_level}")

        self.trust_level = trust_level
        self.task = str(task)
        self._memory = memory

        if trust_level == "external":
            self._guardrails = None
        else:
            self._guardrails = CapabilityGuardrails(memory, task)

    @property
    def memory(self):
        if self.trust_level == "external":
            raise SecurityError(
                "External trust_level requires ExternalRunner. "
                "In-process memory access denied."
            )

        return self._guardrails.get_memory_view() if self._guardrails else None

    def submit_proposal(self, proposal):
        return {
            "proposal": copy.deepcopy(proposal),
            "final": False,
            "requires_authority": True,
        }

    def execute(self, capability_func):
        if self.trust_level == "external":
            return ExternalRunner.execute(
                capability_module=capability_func.__module__,
                capability_request={"task": self.task, "input": {}},
                memory_context=self._memory,
            )

        with self._guardrails as guardrails:
            try:
                result = capability_func(self)
            except PermissionError as exc:
                return {
                    "result": None,
                    "error": str(exc),
                    "guardrail_violations": guardrails.violations,
                    "violations": guardrails.violations,
                    "blocked": True,
                }

            return {
                "result": result,
                "guardrail_violations": guardrails.violations,
                "violations": guardrails.violations,
                "blocked": len(guardrails.violations) > 0,
            }

    def execute_capability(self, capability_func):
        return self.execute(capability_func)


def execute_capability(
    capability_module,
    capability_request=None,
    memory_context=None,
    trust_level="external",
    bypass_runner=False,
):
    if trust_level == "external":
        if bypass_runner:
            raise SecurityBoundaryViolation(
                "External capabilities cannot execute in-process. "
                "Use ExternalRunner isolation."
            )

        return ExternalRunner.execute(
            capability_module=capability_module,
            capability_request=capability_request or {},
            memory_context=memory_context,
        )

    raise ValueError(
        "In-process execution requires a callable and CapabilityContext."
    )


def _extract_mode(args, kwargs):
    if args:
        return str(args[0])

    return str(kwargs.get("mode", "r"))


def _is_write_mode(mode):
    return any(flag in mode for flag in ("w", "a", "x", "+"))


def _readonly(value):
    if isinstance(value, dict):
        return MappingProxyType({
            key: _readonly(item)
            for key, item in value.items()
        })

    if isinstance(value, list):
        return tuple(_readonly(item) for item in value)

    if isinstance(value, set):
        return frozenset(_readonly(item) for item in value)

    return value
