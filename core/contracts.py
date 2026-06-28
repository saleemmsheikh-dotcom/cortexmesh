import ast
from pathlib import Path

from core.capability_guardrails import (
    CapabilityContext,
    SecurityBoundaryViolation,
    SecurityError,
    execute_capability,
)


PROTECTED_IMPORT_PREFIXES = (
    "agents.authority",
    "_thread",
    "concurrent",
    "ctypes",
    "evolution.evolution_engine",
    "governance.enforcement",
    "governance.snapshot",
    "memory.memory_store",
    "multiprocessing",
    "subprocess",
    "threading",
)


def readonly_memory(memory):
    return CapabilityContext(memory, "", trust_level="core").memory


def validate_capability_source(path):
    path = Path(path)
    tree = ast.parse(path.read_text(), filename=str(path))
    violations = []
    aliases = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
            for name in names:
                if name.startswith(PROTECTED_IMPORT_PREFIXES):
                    violations.append(f"forbidden import: {name}")
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
            for name in names:
                if name.startswith(PROTECTED_IMPORT_PREFIXES):
                    violations.append(f"forbidden import: {name}")

        if isinstance(node, ast.Assign):
            if _is_context_memory(node.value):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        aliases.add(target.id)

        if isinstance(node, (ast.Assign, ast.AugAssign, ast.Delete)):
            targets = []

            if isinstance(node, ast.Assign):
                targets = node.targets
            elif isinstance(node, ast.Delete):
                targets = node.targets
            else:
                targets = [node.target]

            for target in targets:
                if _writes_context_memory(target, aliases):
                    violations.append("forbidden memory mutation")

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if _writes_context_memory(node.func.value, aliases):
                violations.append(f"forbidden memory method: {node.func.attr}")

    return violations


def _is_context_memory(node):
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "memory"
        and isinstance(node.value, ast.Name)
        and node.value.id == "context"
    )


def _writes_context_memory(node, aliases):
    root = node

    while isinstance(root, ast.Subscript):
        root = root.value

    return (
        _is_context_memory(root)
        or (
            isinstance(root, ast.Name)
            and root.id in aliases
        )
    )
