from __future__ import annotations

import dataclasses
import hashlib
import importlib.util
import json
import locale
import math
import os
from pathlib import Path
import platform
import statistics
import sys
import time


ROOT = Path("/Users/saleemsheikh/Documents/cortexmesh")
ORCH = ROOT / "CortexMesh_v3_Planning/06_Implementation_Execution/Phase2C/orchestration"
CORPUS = ROOT / "CortexMesh_v3_Planning/06_Implementation_Execution/Phase3A/replay/v1.1"
OUTPUT = ROOT / "CortexMesh_v3_Planning/07_Research/RP-001/EXP-001/raw"
EXPECTED_ENGINE = "a72d11fe57f9026ab307efeaf962b97095527039"
EXPECTED_VALIDATION = "6c41364c56883043c20d237d37b8fcd83ec02547"
EXPECTED_CORPUS_HASH = "20e4b446097db5b3dcaa6fbf214218038c9c297d2e60bbbc57b9d24bc1e59788"
REPETITIONS = 10


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ORCH / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


resolver_mod = load("exp001_resolver", "capability_resolver.py")
agent_mod = load("exp001_agent", "agent_planner.py")
execution_mod = load("exp001_execution", "execution_plan.py")
evidence_mod = load("exp001_evidence", "evidence.py")
consensus_mod = load("exp001_consensus", "consensus.py")
synthesis_mod = load("exp001_synthesis", "synthesis.py")
engine_mod = load("exp001_engine", "engine.py")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value) -> str:
    if dataclasses.is_dataclass(value):
        value = dataclasses.asdict(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def verify_corpus() -> dict:
    manifest = json.loads((CORPUS / "MANIFEST.json").read_text())
    if manifest["status"] != "CERTIFIED" or manifest["corpus_version"] != "1.1.0":
        raise RuntimeError("corpus identity or certification mismatch")
    entries = []
    for item in manifest["files"]:
        digest = sha256(CORPUS / item["path"])
        if digest != item["sha256"]:
            raise RuntimeError("corpus file hash mismatch: " + item["path"])
        entries.append((item["path"], digest))
    payload = "\n".join(f"{path}:{digest}" for path, digest in entries)
    content_hash = hashlib.sha256(payload.encode()).hexdigest()
    if content_hash != manifest["content_hash"] or content_hash != EXPECTED_CORPUS_HASH:
        raise RuntimeError("corpus content hash mismatch")
    return manifest


def engine():
    return engine_mod.OrchestrationEngine(
        capability_resolver=resolver_mod.CapabilityResolver(),
        agent_planner=agent_mod.AgentPlanner(),
        execution_planner=execution_mod.ExecutionPlanner(),
        evidence_collector=evidence_mod.EvidenceCollector(),
        consensus_evaluator=consensus_mod.ConsensusEvaluator(),
        evidence_synthesizer=synthesis_mod.EvidenceSynthesizer(),
    )


def plan_steps(components, intent: dict):
    resolution = components._resolver.resolve(intent)
    agent_plan = components._agent_planner.plan(resolution)
    return components._execution_planner.plan(agent_plan).steps


def supplied_output(claims: list[str]) -> dict:
    return {
        "output": {"claims": claims},
        "assumptions": ["simulated replay input"],
        "limitations": ["no runtime or provider invocation"],
        "diagnostics": [],
    }


def outputs_for(case: dict, steps) -> dict:
    mode = case["payload"]["mode"]
    claims = list(case["payload"].get("claims", []))
    ids = [step.step_id for step in steps]
    if mode in {"reject", "missing"}:
        outputs = {}
    elif mode == "single":
        outputs = {ids[0]: supplied_output([claims[0]])} if ids else {}
    elif mode == "same":
        outputs = {step_id: supplied_output([claims[0]]) for step_id in ids}
    elif mode == "aliases":
        outputs = {
            step_id: supplied_output([claims[index % len(claims)]])
            for index, step_id in enumerate(ids)
        }
    elif mode == "minority":
        minority = claims[-1]
        outputs = {
            step_id: supplied_output([minority if index == len(ids) - 1 else claims[0]])
            for index, step_id in enumerate(ids)
        }
    elif mode == "conflict":
        outputs = {
            step_id: supplied_output([claims[index % len(claims)]])
            for index, step_id in enumerate(ids)
        }
    elif mode == "conflict-minority":
        outputs = {
            step_id: supplied_output([claims[-1] if index == len(ids) - 1 else claims[0]])
            for index, step_id in enumerate(ids)
        }
    elif mode == "claimless":
        outputs = {step_id: supplied_output([]) for step_id in ids}
    elif mode == "extra-step":
        outputs = {step_id: supplied_output(["valid"]) for step_id in ids}
        outputs["step-999-unplanned"] = supplied_output(["unplanned"])
    else:
        raise RuntimeError("unknown payload mode: " + mode)
    return outputs


def policy_for(case: dict):
    policy = case.get("policy", {})
    return consensus_mod.ConsensusPolicy(
        compatible_claims=dict(policy.get("aliases", {})),
        material_conflicts=tuple(tuple(pair) for pair in policy.get("conflicts", [])),
    )


def environment() -> dict:
    dependency_manifest = {
        "python": platform.python_version(),
        "stdlib_only": True,
        "modules": {
            path.name: sha256(path)
            for path in sorted(ORCH.glob("*.py"))
        },
    }
    configuration = {
        "repetitions": REPETITIONS,
        "case_order": "manifest",
        "network_required": False,
        "provider_invocation": False,
        "runtime_invocation": False,
        "random_seed": None,
    }
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "os": platform.system(),
        "os_release": platform.release(),
        "machine": platform.machine(),
        "processor": "Intel Core i5, 1.4 GHz, 4 cores",
        "locale": locale.setlocale(locale.LC_ALL, None),
        "timezone": time.tzname,
        "random_seed": "not applicable",
        "dependency_manifest_sha256": hashlib.sha256(canonical(dependency_manifest).encode()).hexdigest(),
        "configuration_sha256": hashlib.sha256(canonical(configuration).encode()).hexdigest(),
        "dependency_manifest": dependency_manifest,
        "configuration": configuration,
        "network_required": False,
        "provider_invocation": False,
        "runtime_invocation": False,
    }


def main() -> None:
    if OUTPUT.exists() and any(OUTPUT.iterdir()):
        raise RuntimeError("raw output directory is not empty")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = verify_corpus()
    cases_doc = json.loads((CORPUS / "cases/cases.json").read_text())
    cases = cases_doc["cases"]
    if len(cases) != 24 or [case["id"] for case in cases] != sorted(case["id"] for case in cases):
        raise RuntimeError("case count or ordering mismatch")

    harness_hash = sha256(Path(__file__))
    started = time.time_ns()
    observations = []
    for repetition in range(1, REPETITIONS + 1):
        component = engine()
        for case in cases:
            observation_start = time.perf_counter_ns()
            intent = dict(case["intent"])
            try:
                steps = plan_steps(component, intent)
                outputs = outputs_for(case, steps)
                request = engine_mod.OrchestrationRequest(
                    request_id=f"exp001:{case['id']}",
                    intent=intent,
                    simulated_outputs=outputs,
                    consensus_policy=policy_for(case),
                    scope=f"rp-001/exp-001/{case['id']}",
                )
                result = component.run(request)
                elapsed = time.perf_counter_ns() - observation_start
                result_data = dataclasses.asdict(result)
                observation = {
                    "repetition": repetition,
                    "case_id": case["id"],
                    "expected_consensus": case["consensus"],
                    "expected_diagnostics": case["diagnostics"],
                    "expected_statements": case["statements"],
                    "input": {"intent": intent, "simulated_outputs": outputs, "scope": request.scope},
                    "status": "completed",
                    "exception": None,
                    "result": result_data,
                    "canonical_sha256": hashlib.sha256(canonical(result_data).encode()).hexdigest(),
                    "elapsed_ns": elapsed,
                }
            except Exception as exc:
                elapsed = time.perf_counter_ns() - observation_start
                error = {"type": type(exc).__name__, "message": str(exc)}
                observation = {
                    "repetition": repetition,
                    "case_id": case["id"],
                    "expected_consensus": case["consensus"],
                    "expected_diagnostics": case["diagnostics"],
                    "expected_statements": case["statements"],
                    "input": {"intent": intent, "payload": case["payload"]},
                    "status": "rejected",
                    "exception": error,
                    "result": None,
                    "canonical_sha256": hashlib.sha256(canonical(error).encode()).hexdigest(),
                    "elapsed_ns": elapsed,
                }
            observations.append(observation)

    ended = time.time_ns()
    lines = [canonical(item) for item in observations]
    observations_path = OUTPUT / "observations.jsonl"
    observations_path.write_text("\n".join(lines) + "\n")
    raw_hash = sha256(observations_path)
    harness_path = OUTPUT / "exp001_runner.py"
    harness_path.write_bytes(Path(__file__).read_bytes())
    run_manifest = {
        "experiment": "RP-001/EXP-001",
        "status": "collection complete; analysis not performed",
        "started_unix_ns": started,
        "ended_unix_ns": ended,
        "planned_executions": 240,
        "recorded_executions": len(observations),
        "repetitions": REPETITIONS,
        "cases": len(cases),
        "engine_commit": EXPECTED_ENGINE,
        "validation_commit": EXPECTED_VALIDATION,
        "corpus_version": manifest["corpus_version"],
        "corpus_content_hash": manifest["content_hash"],
        "harness_sha256": harness_hash,
        "observations_sha256": raw_hash,
        "environment": environment(),
    }
    manifest_path = OUTPUT / "RUN_MANIFEST.json"
    manifest_path.write_text(json.dumps(run_manifest, indent=2, sort_keys=True) + "\n")
    package_entries = [
        {"path": "RUN_MANIFEST.json", "sha256": sha256(manifest_path), "size": manifest_path.stat().st_size},
        {"path": "exp001_runner.py", "sha256": sha256(harness_path), "size": harness_path.stat().st_size},
        {"path": "observations.jsonl", "sha256": raw_hash, "size": observations_path.stat().st_size},
    ]
    package_path = OUTPUT / "PACKAGE_MANIFEST.json"
    package_path.write_text(json.dumps({"files": package_entries}, indent=2, sort_keys=True) + "\n")
    print(canonical({
        "recorded": len(observations),
        "harness_sha256": harness_hash,
        "observations_sha256": raw_hash,
        "package_manifest_sha256": sha256(package_path),
        "status": "collection complete; analysis not performed",
    }))


if __name__ == "__main__":
    main()
