"""Phase 1B Local AI reference implementation.

This package is intentionally isolated from runtime integration points until
the required governance and LOCKED-component boundaries are cleared.
"""

from .config import LocalAIConfig, LocalAIConfigError
from .ollama import OllamaProvider
from .provider import LocalAIProvider, LocalAIRequest, LocalAIResponse
from .verification import VerificationRecord, verify_connection

__all__ = [
    "LocalAIConfig",
    "LocalAIConfigError",
    "LocalAIProvider",
    "LocalAIRequest",
    "LocalAIResponse",
    "OllamaProvider",
    "VerificationRecord",
    "verify_connection",
]
