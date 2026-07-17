import subprocess
import json


def run_capability_external(capability_request):
    proc = subprocess.run(
        ["docker", "run", "-i", "--rm", "cortexmesh-capability"],
        input=json.dumps(capability_request),
        capture_output=True,
        text=True,
        timeout=30
    )
    return json.loads(proc.stdout)


result = run_capability_external({"capability": "test", "input": {"task": "analyze"}})
print(json.dumps(result, indent=2))
