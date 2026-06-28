import importlib.util
import json
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.contracts import CapabilityContext


def load_temp_capability(source):
    directory = tempfile.TemporaryDirectory()
    path = Path(directory.name) / "probe.py"
    path.write_text(source)
    spec = importlib.util.spec_from_file_location("r65_probe", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return directory, module


def run_probe(name, source, memory=None, wait_seconds=0.0, target=None):
    holder, module = load_temp_capability(source)
    memory = memory or {
        "governance_frozen": True,
        "strategy_registry": {"Architect": {"strategies": {}}},
    }

    try:
        execution = CapabilityContext(memory, name).execute_capability(module.run)
        if wait_seconds:
            time.sleep(wait_seconds)
        target_exists = Path(target).exists() if target else None
    finally:
        holder.cleanup()

    return {
        "execution": execution,
        "target_exists": target_exists,
        "memory_after": memory,
    }


def monkey_patch_setitem_probe():
    source = (
        "def run(context):\n"
        "    results = {}\n"
        "    try:\n"
        "        context.memory.__setitem__ = lambda key, value: None\n"
        "        results['instance_setitem_patch'] = True\n"
        "    except Exception as exc:\n"
        "        results['instance_setitem_patch'] = False\n"
        "        results['instance_error'] = type(exc).__name__\n"
        "    try:\n"
        "        type(context.memory).__setitem__ = lambda self, key, value: None\n"
        "        results['type_setitem_patch'] = True\n"
        "    except Exception as exc:\n"
        "        results['type_setitem_patch'] = False\n"
        "        results['type_error'] = type(exc).__name__\n"
        "    return results\n"
    )
    result = run_probe("monkey_patch_setitem", source)
    payload = result["execution"].get("result") or {}
    succeeded = any(
        payload.get(key)
        for key in ("instance_setitem_patch", "type_setitem_patch")
    )
    return {"blocked": not succeeded, **result}


def setattr_memory_probe():
    source = (
        "def run(context):\n"
        "    results = {}\n"
        "    try:\n"
        "        setattr(context.memory, 'governance_frozen', False)\n"
        "        results['root_setattr'] = True\n"
        "    except Exception as exc:\n"
        "        results['root_setattr'] = False\n"
        "        results['root_error'] = type(exc).__name__\n"
        "    try:\n"
        "        nested = context.memory['strategy_registry']\n"
        "        setattr(nested, 'Architect_v99', {'version': 99})\n"
        "        results['nested_setattr'] = True\n"
        "    except Exception as exc:\n"
        "        results['nested_setattr'] = False\n"
        "        results['nested_error'] = type(exc).__name__\n"
        "    return results\n"
    )
    result = run_probe("setattr_memory", source)
    payload = result["execution"].get("result") or {}
    succeeded = any(payload.get(key) for key in ("root_setattr", "nested_setattr"))
    return {"blocked": not succeeded, **result}


def ctypes_native_write_probe():
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory) / "ctypes_bypass.txt"
        source = (
            "def run(context):\n"
            "    import ctypes\n"
            "    libc = ctypes.CDLL(None)\n"
            f"    command = b'printf ctypes_bypass > {str(target).encode().decode()}'\n"
            "    code = libc.system(command)\n"
            "    return {'ctypes_system_code': int(code)}\n"
        )
        result = run_probe("ctypes_native_write", source, target=target)
        return {"blocked": not result["target_exists"], **result}


def ctypes_mappingproxy_mutation_probe():
    source = (
        "def run(context):\n"
        "    import ctypes\n"
        "    try:\n"
        "        setter = ctypes.pythonapi.PyObject_SetItem\n"
        "        setter.argtypes = [ctypes.py_object, ctypes.py_object, ctypes.py_object]\n"
        "        setter.restype = ctypes.c_int\n"
        "        code = setter(context.memory, 'governance_frozen', False)\n"
        "        return {'pyobject_setitem_code': int(code)}\n"
        "    except Exception as exc:\n"
        "        return {'pyobject_setitem_error': type(exc).__name__}\n"
    )
    memory = {"governance_frozen": True}
    result = run_probe("ctypes_mappingproxy_mutation", source, memory=memory)
    changed = memory.get("governance_frozen") is False
    payload = result["execution"].get("result") or {}
    succeeded = changed or payload.get("pyobject_setitem_code") == 0
    return {"blocked": not succeeded, **result}


def thread_delayed_write_probe():
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory) / "thread_bypass.txt"
        source = (
            "def run(context):\n"
            "    import threading\n"
            "    import time\n"
            "    from pathlib import Path\n"
            "    def delayed_write():\n"
            "        time.sleep(0.2)\n"
            f"        Path({str(target)!r}).write_text('thread_bypass')\n"
            "    thread = threading.Thread(target=delayed_write)\n"
            "    thread.start()\n"
            "    return {'thread_started': True}\n"
        )
        result = run_probe(
            "thread_delayed_write",
            source,
            wait_seconds=0.5,
            target=target,
        )
        return {"blocked": not result["target_exists"], **result}


def main():
    probes = {
        "monkey_patch_memory_setitem": monkey_patch_setitem_probe(),
        "setattr_on_memory_objects": setattr_memory_probe(),
        "ctypes_native_filesystem_write": ctypes_native_write_probe(),
        "ctypes_mappingproxy_mutation": ctypes_mappingproxy_mutation_probe(),
        "thread_delayed_filesystem_write": thread_delayed_write_probe(),
    }
    vulnerabilities = [
        name
        for name, result in probes.items()
        if not result["blocked"]
    ]
    print(json.dumps({
        "overall_status": "vulnerable" if vulnerabilities else "blocked",
        "vulnerabilities": vulnerabilities,
        "probes": probes,
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
