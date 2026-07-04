# DEBT-010 Study F Operational Review

## Classification
OBSERVED / INFERRED / PROPOSED review.

## Purpose
Review operational implications of hardening Docker-based external capability execution.

## Scope
Study F covers:
- Rootless Docker requirements
- Signed image requirements
- Runtime monitoring requirements
- Operational burden
- Deployment impact

## Sources Reviewed
- Docker Rootless Mode documentation: https://docs.docker.com/engine/security/rootless/
- Docker Content Trust documentation: https://docs.docker.com/engine/security/trust/
- Docker Scout documentation: https://docs.docker.com/scout/

## 1. Rootless Docker Requirements

### OBSERVED
Docker documents rootless mode as a Docker Engine security mode intended to run both daemon and containers without root privileges.

### INFERRED
Rootless mode can reduce host impact from daemon/container compromise, but it does not eliminate all container escape or host compromise risk.

### Operational Considerations
- Requires host support for unprivileged user namespaces and subordinate UID/GID mappings.
- May require separate setup from Docker Desktop defaults.
- Can change networking, storage, and privileged-operation behavior.
- May break workflows that assume privileged Docker daemon behavior.

### Deployment Impact
Moderate to high. Requires environment-specific validation before adoption.

## 2. Signed Image Requirements

### OBSERVED
Docker Content Trust supports signed image verification, but Docker documentation notes Docker is retiring DCT for Docker Official Images and advises planning transition to alternatives such as Sigstore or Notation.

### INFERRED
For CortexMesh, signed image policy should not depend solely on legacy DCT if long-term maintainability is required.

### Operational Considerations
- Define trusted registry sources.
- Pin image digests.
- Require signature verification for externally executed capability images.
- Decide whether to use Notation, Sigstore, or another signing workflow.
- Maintain signing keys and rotation procedures.

### Deployment Impact
Moderate. Strong policy value, but introduces key management and CI/CD integration work.

## 3. Runtime Monitoring Requirements

### OBSERVED
Docker Scout provides image analysis, SBOM generation, vulnerability matching, policy evaluation, and integrations with CI and registries.

### INFERRED
Docker Scout and similar tools primarily address supply-chain and image risk. They do not replace runtime isolation, process supervision, or daemon-level monitoring.

### Operational Considerations
- Capture container start/stop/kill outcomes.
- Monitor timeout kills and zombie-process cleanup.
- Record image digest, runtime flags, and exit status per external capability run.
- Preserve failure logs without leaking host paths or secrets.
- Add daemon health monitoring if Docker remains in the trusted execution path.

### Deployment Impact
Moderate. Most requirements can be implemented as audit logging and wrapper checks, but daemon monitoring may require host-level integration.

## 4. Operational Burden

### OBSERVED
Current CortexMesh ExternalRunner already applies isolation flags such as disabled networking, read-only filesystem, memory limits, and CPU limits.

### INFERRED
The largest remaining operational burden is not adding more Docker flags, but controlling the Docker daemon trust boundary and ensuring failure handling is observable.

### Burden Areas
- Rootless Docker setup and compatibility testing
- Image signing policy selection
- Digest pinning
- Runtime audit logging
- Kill/cleanup verification
- Documentation and operator training

## 5. Deployment Impact

### Low Impact
- Record image digests in audit trail.
- Record runtime flags in audit trail.
- Document unsupported raw Docker execution.

### Medium Impact
- Enforce signed/pinned images.
- Add runtime monitoring records for kill/timeout paths.
- Add daemon health preflight checks.

### High Impact
- Move to rootless Docker in all environments.
- Replace Docker daemon trust boundary with a stronger isolation runtime.
- Require signing infrastructure and key rotation.

## 6. Recommendation

### PROPOSED
Commission a follow-up design study for a staged hardening path:

1. Require digest-pinned images.
2. Add runtime audit records for image digest, flags, timeout, kill result, and exit status.
3. Evaluate Notation or Sigstore for signing policy.
4. Test rootless Docker compatibility in a non-production environment.
5. Defer replacing Docker until Study D feasibility is complete.

## Evidence Boundary
This is a documentation and operational review. It does not prove runtime security and does not benchmark alternative isolation technologies.
