# CortexMesh Environment Contract

## Contract status

CortexMesh is a repository-first engineering and research platform. Commands
in this guide run from the repository root; no installed-package behavior is
defined.

Environment terms have precise meanings:

- **Verified:** required CI gates continuously exercise the stated profile.
- **Observed:** a recorded execution exists without a continuing compatibility
  commitment.
- **Expected:** no incompatibility is known, but the profile is not certified.
- **Not certified:** CortexMesh makes no compatibility assurance.

## Environment support

| Environment | Status | Meaning |
| --- | --- | --- |
| CPython 3.14 on Ubuntu CI | VERIFIED | Required and observational GitHub workflows exercise this profile |
| Recorded macOS and Ubuntu executions outside CI | OBSERVED | Evidence exists, but it is not a compatibility promise |
| CPython 3.14 on other operating systems | may be attempted | Results are observations unless separately validated |
| Other Python versions, Windows, and alternative Python implementations | NOT CERTIFIED | No current support claim |

The verified dependency constraints are specific to CPython 3.14 on Ubuntu CI.
They are not a universal or cross-platform lock.

## Repository-root requirement

Clone using an authorized GitHub identity, enter the clone, and run every
general setup and verification command from its root:

```bash
git clone https://github.com/saleemmsheikh-dotcom/cortexmesh.git
cd cortexmesh
git status --short
git rev-parse HEAD
```

Some controlled harnesses resolve their own paths, but that does not establish
an installed import contract or general location independence.

## Dependency profiles

| Profile | Declaration | Purpose |
| --- | --- | --- |
| Default verification/development | `requirements.txt` | pytest parity and descriptive coverage tooling |
| Optional OpenAI | `requirements-openai.txt` | Default profile plus the OpenAI SDK |
| Verified Ubuntu resolution | `constraints/cpython314-ubuntu.txt` | Exact versions demonstrated for the verified profile |
| Default runtime/reference/replay | Python standard library | Fallback CLI, Phase 2C reference logic, Phase 3A replay model, and RP-001 harness code inspected during F1.1-E |
| Local AI | Operator-supplied service and model | Repository adapters use Python standard-library HTTP transport |
| External capability | Operator-supplied Docker environment and base image | Separate optional isolation path |

`pip-audit==2.10.1` remains a CI-only descriptive inspection tool. It is not an
application dependency or a security certification.

## Verification-first fresh clone

Do not begin with the live CLI, a provider, research execution, or Docker.

### 1. Verify Python and create isolation

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip --version
```

The verified profile requires CPython 3.14.

### 2. Install the verified default profile

```bash
python -m pip install \
  -c constraints/cpython314-ubuntu.txt \
  -r requirements.txt
python -m pip check
```

### 3. Record the local environment

```bash
python --version
python -m pip --version
shasum -a 256 \
  requirements.txt \
  requirements-openai.txt \
  constraints/cpython314-ubuntu.txt
python -m pip freeze
```

`shasum` is used by Ubuntu CI. On an unverified environment, use an available
SHA-256 utility and record that substitution as an observation.

### 4. Run authoritative verification

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover tests
```

The `unittest` command is the authoritative regression. Pytest is optional
parity:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

### 5. Confirm repository state

```bash
git diff --check
git status --short
```

Verification must not modify tracked runtime memory, governance, research
evidence, replay assets, validation certification, or LOCKED components.

## Stateful CLI contract

Read this section before running:

```bash
python3 main.py "<task>"
```

The command calls `engine.runner.run_task`, which loads and persists
`memory/memory.json`. Current persistence can also create or replace
`memory/memory.json.bak`.

Before a task:

1. complete the verification-first procedure;
2. inspect `git status --short`;
3. understand that the tracked memory file can change.

After a task:

1. inspect `git status --short`;
2. review the memory diff;
3. retain state only through the project's authorized Git and provenance
   process.

This guide does not authorize deleting, silently regenerating, automatically
resetting, or relocating state. F1.1-E does not change the state path, schema,
initialization, backup, or persistence behavior.

## Optional OpenAI profile

The default no-key path uses existing internal fallback behavior and does not
require the OpenAI SDK.

Install the optional profile without making a request:

```bash
python -m pip install \
  -c constraints/cpython314-ubuntu.txt \
  -r requirements-openai.txt
python -m pip check
```

Activation conditions:

- `OPENAI_API_KEY` or `OPENAI_ADMIN_KEY` is supplied through the environment;
- the optional SDK profile is installed;
- external network and service access are available.

`OPENAI_API_KEY` also participates in current execution-mode availability.
Missing keys remain a valid fallback condition. A configured keyed path without
the SDK raises the existing installation error; external authentication,
service, and model errors remain external failures.

Never commit credentials. Do not place real values in examples, logs,
constraints, evidence, or issue reports. `.env` is ignored, but CortexMesh does
not load `.env` files automatically.

## Optional Local AI profile

CortexMesh does not install a Local AI service or model. The operator supplies
and manages:

- Ollama or LM Studio;
- a loaded/available model;
- endpoint reachability;
- adequate local resources.

Current configuration variables:

| Variable | Current role/default |
| --- | --- |
| `CORTEX_LOCAL_AI_ENABLED` | Opt in when set to `1`, `true`, or `yes`; disabled otherwise |
| `CORTEX_LOCAL_AI_PROVIDER` | Provider selection; default `ollama` |
| `CORTEX_LOCAL_AI_PROVIDER_OPTIONS` | Comma-separated candidates; default `ollama` |
| `CORTEX_LOCAL_AI_BASE_URL` | Endpoint override; registry defaults apply when empty |
| `CORTEX_LOCAL_AI_MODEL` | Operator-supplied model identifier |
| `CORTEX_LOCAL_AI_TIMEOUT` | Request timeout; default `60` seconds |
| `CORTEX_LOCAL_AI_TEMPERATURE` | Generation temperature; default `0` |
| `CORTEX_LOCAL_AI_MAX_TOKENS` | Output limit; default `256` |

The current registry defaults are:

- Ollama: `http://localhost:11434`
- LM Studio: `http://localhost:1234`

Defaults do not prove that a service or model is available. Existing provider
health and contract tests do not make a live service part of default
verification.

When Local AI is disabled, current internal solver behavior remains available.
When it is enabled but unavailable or misconfigured, existing validation or
request behavior may fail. F1.1-E adds no retry, fallback, provider preference,
or selection semantics.

Docker is not required for the SAFE Local AI bridge in
`agents/local_ai_bridge.py`.

## Docker external-capability limitation

Docker belongs to the separate external capability boundary in
`core/external_runner.py`. That LOCKED runner expects a local base image named
`cortexmesh-capability` and constructs derived capability images under its
existing isolation rules.

The current repository does not provide:

- an authoritative base-image Dockerfile;
- a build or pull procedure;
- an image digest or registry source;
- a fresh-clone capability-execution guarantee.

The base image and Docker environment are operator-supplied. The repository can
verify the runner's recorded code boundary, but cannot certify repository-
portable external capability execution. This limitation is intentional until a
separate provisioning and protected-boundary review is authorized.

## Environment-variable reference

| Variable | Scope |
| --- | --- |
| `OPENAI_API_KEY` | Optional OpenAI request and mode availability |
| `OPENAI_ADMIN_KEY` | Optional OpenAI model-router activation |
| `CORTEX_MODE` | Optional `dev`, `audit`, or conditional `prod` selection |
| `CORTEX_LOCAL_AI_ENABLED` | Local AI opt-in |
| `CORTEX_LOCAL_AI_PROVIDER` | Local provider selection |
| `CORTEX_LOCAL_AI_PROVIDER_OPTIONS` | Local provider candidates |
| `CORTEX_LOCAL_AI_BASE_URL` | Local endpoint override |
| `CORTEX_LOCAL_AI_MODEL` | Local model identifier |
| `CORTEX_LOCAL_AI_TIMEOUT` | Local request timeout |
| `CORTEX_LOCAL_AI_TEMPERATURE` | Local generation temperature |
| `CORTEX_LOCAL_AI_MAX_TOKENS` | Local output limit |
| `CORTEXMESH_STABILITY_QUICK` | Development stability-battery size |
| `CORTEX_PATCH` | Research comparison utility selection |
| `PYTHONDONTWRITEBYTECODE` | Verification bytecode control |

Record whether optional variables are present, never their secret values.

## Dependency updates and rollback

Direct requirements express dependency intent. The constraints file records one
known-good Ubuntu/CPython 3.14 resolution.

A constraints update requires:

1. a clean verified-profile environment;
2. recorded Python, pip, input hashes, and resolved versions;
3. descriptive dependency audit;
4. full regression and contract tests;
5. protected-identity verification;
6. reviewed Git history and rollback.

Do not automatically update dependencies. If requirements and workflow install
commands change together, revert them together so CI never references missing
or incompatible constraints. Preserve CI and resolution evidence.

## Packaging deferral threshold

Installable packaging remains deferred. Reassessment requires evidence of a
durable need such as repeated external-project reuse, a stable public import
surface, multiple entry points that benefit from installation, or an external
distribution requirement.

Before packaging could be authorized, CortexMesh would also need approved
mutable-state semantics, package-data boundaries, installed-import tests,
dependency profiles, compatibility/versioning commitments, proprietary
distribution terms, and review of affected protected surfaces.

Meeting a need threshold permits assessment; it does not authorize packaging.

## Unsupported and externally provisioned capabilities

The environment contract does not certify:

- other Python versions, Windows, or alternative Python implementations;
- production, security, scalability, or service-level readiness;
- provider or model availability;
- Docker capability-image provisioning;
- installed-package imports, wheels, console scripts, or external
  distribution;
- PyPI or container-registry publication.
