# DEBT-010 Study D Benchmark Report

## Evidence Frozen

- `results/docker_baseline.csv`
- `results/firecracker_boot_10_direct.csv`
- `raw/firecracker/direct_boot_stdout.txt`
- `raw/firecracker/direct_boot_time.txt`
- `raw/firecracker/repeats/`
- `results/firecracker_boot_notes.md`
- `results/firecracker_version.txt`
- `results/host_baseline.md`

## OBSERVED

- Firecracker v1.13.1 installed
- Ubuntu 26.04 LTS
- KVM available
- 10/10 successful boots
- Mean boot time: 2.320 s
- Mean RSS: 35,026.8 KB

## INFERRED

- Path D is technically feasible on Linux
- Additional operational complexity exists compared to Docker
- Firecracker startup overhead is materially higher than Docker baseline

## LIMITATIONS

- Boot benchmark only
- No application workload executed inside guest
- Single host
- Single CPU class

## Docker Baseline Reference

| Workload | Elapsed seconds | Max RSS KB |
| --- | ---: | ---: |
| startup | 0.02 | 9,520 |
| cpu | 0.10 | 14,404 |
| memory | 0.09 | 111,884 |

## Firecracker Boot Results

| Metric | Value |
| --- | ---: |
| Successful boots | 10/10 |
| Mean boot time | 2.320 s |
| Mean RSS | 35,026.8 KB |

## Workload Comparison Status

The same CPU and memory workloads used for the Docker baseline were identified:

- CPU: `python3 workloads/cpu.py`
- Memory: `python3 workloads/memory.py`

These workloads were not executed inside Firecracker in this study because the current guest rootfs does not reach usable userspace. The Firecracker boot logs show kernel startup followed by root filesystem mount failure:

- `EXT4-fs (vda): bad geometry: block count 307200 exceeds size of device (53976 blocks)`
- `Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(254,0)`

A separate repaired working copy was attempted at `raw/firecracker/workload-rootfs.ext4`, but filesystem repair removed key userspace paths including `/bin`, `/usr/bin`, and `/etc`. That copy is not suitable for benchmark evidence.

## Recommended Order

### Phase 1

Freeze evidence:

- `docker_baseline.csv`
- `firecracker_boot_10_direct.csv`
- `DEBT010_StudyD_Benchmark_Report.md`

### Phase 2

Create a separate artifact:

- `DEBT010_StudyD_Optimization_Experiment.md`

Then test:

1. Strip guest kernel config
2. Minimal kernel boot args
3. Smaller rootfs
4. Memory tuning
5. CPU tuning

Record each change independently.

## Next Evidence Needed

For board-grade Path D vs Docker evidence, create or obtain a clean Firecracker guest rootfs that:

- Mounts successfully
- Contains Python 3
- Contains `workloads/cpu.py` and `workloads/memory.py`, or an equivalent init command that runs the same logic
- Emits workload timing and completion markers to the serial console

Then run the same CPU and memory workloads inside Firecracker and compare them directly with `results/docker_baseline.csv`.
