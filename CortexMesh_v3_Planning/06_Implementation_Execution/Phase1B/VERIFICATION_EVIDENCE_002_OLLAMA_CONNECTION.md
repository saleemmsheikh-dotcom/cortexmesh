# Verification Evidence 002 - Ollama Live Connection

## Verification ID

PHASE1B-VE-002

## Date

2026-07-06

## Purpose

Validate the Phase 1B Ollama adapter against a live local Ollama endpoint and record connection/generation evidence without runtime integration.

## Scope Verified

- Ollama service availability.
- Available local model listing.
- Minimal provider-independent generation request through the Phase 1B Ollama adapter.
- Response success/failure recording.
- Errors, limitations, and environment assumptions.

## Governance Boundary Check

| Check | Result |
| ----- | ------ |
| LOCKED components modified | PASS - none modified |
| Runtime orchestration integration performed | PASS - none performed |
| Phase 1B reference implementation used | PASS |
| Provider-specific logic kept in adapter | PASS |
| Evidence-only verification scope preserved | PASS |

## Environment Assumptions

- Verification host: Ubuntu shell environment.
- Ollama endpoint: `http://localhost:11434`.
- Provider: `ollama`.
- Adapter under test: `CortexMesh_v3_Planning/06_Implementation_Execution/Phase1B/local_ai/ollama.py`.
- Network scope: localhost only.
- Initial sandboxed socket access was blocked with `Operation not permitted`; the live localhost checks were rerun with approved elevated command permissions.

## Service Availability

Command:

```text
curl --silent --show-error --max-time 10 http://localhost:11434/api/tags
```

Result: PASS

Observed model payload:

```text
qwen2.5-coder:7b
```

## Available Models

Command:

```text
ollama list
```

Result:

```text
NAME                ID              SIZE      MODIFIED
qwen2.5-coder:7b    dae161e27b0e    4.7 GB    2 weeks ago
```

## Minimal Adapter Request

Command executed through the Phase 1B reference implementation:

```text
python3 -c "import json, sys; sys.path.insert(0, 'CortexMesh_v3_Planning/06_Implementation_Execution/Phase1B'); from local_ai.config import LocalAIConfig; from local_ai.ollama import OllamaProvider; from local_ai.provider import LocalAIRequest; from local_ai.verification import verify_connection; cfg=LocalAIConfig(provider='ollama', base_url='http://localhost:11434', model='qwen2.5-coder:7b', timeout_seconds=60.0, temperature=0.0, max_tokens=8); provider=OllamaProvider(); record=verify_connection(provider, cfg, 'PHASE1B-VE-002'); req=LocalAIRequest(prompt='Reply with exactly: OK', model=cfg.model, request_id='PHASE1B-VE-002-REQ-001', objective_ref='PHASE1B-OLLAMA-CONNECTION', temperature=0.0, max_tokens=8, timeout_seconds=60.0); resp=provider.generate(req, cfg); print(json.dumps({'connection': record.__dict__, 'generation': {'request_id': resp.request_id, 'provider': resp.provider, 'model': resp.model, 'content': resp.content, 'status': resp.status, 'latency_ms': resp.latency_ms, 'finish_reason': resp.finish_reason, 'diagnostics': dict(resp.diagnostics)}}, indent=2))"
```

Connection result:

```text
verification_id: PHASE1B-VE-002
timestamp_utc: 2026-07-06T08:26:40.125688+00:00
provider: ollama
model: qwen2.5-coder:7b
endpoint_ref: http://localhost:11434/api/tags
result: PASS
latency_ms: 142
diagnostics: model_available=true, model_count=1
failure_reason: none
```

Generation result:

```text
request_id: PHASE1B-VE-002-REQ-001
provider: ollama
model: qwen2.5-coder:7b
endpoint_ref: http://localhost:11434/api/generate
status: complete
latency_ms: 11942
finish_reason: done
content: OK
```

## Errors and Limitations

- No Ollama adapter error was observed.
- No provider response normalization error was observed.
- The live check depends on a running local Ollama service and installed local model.
- The verification environment required elevated localhost socket access because the managed sandbox blocked socket creation.
- The generation latency was approximately 11.9 seconds for the first minimal request in this session; no performance claim is made from this single verification sample.

## Evidence Artifacts

- `local_ai/ollama.py`
- `local_ai/config.py`
- `local_ai/provider.py`
- `local_ai/verification.py`
- `PHASE1B_STATUS.md`
- `RISKS_AND_BLOCKERS.md`
- `VERIFICATION_EVIDENCE_002_OLLAMA_CONNECTION.md`

## Result

PASS FOR OLLAMA LIVE CONNECTION VERIFICATION

Runtime integration remains deferred pending LOCKED component boundary review.
