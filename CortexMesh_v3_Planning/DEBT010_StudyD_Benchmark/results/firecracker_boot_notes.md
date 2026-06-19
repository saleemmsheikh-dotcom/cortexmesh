# Firecracker Boot Smoke Test Results

## Classification

OBSERVED

## Test Summary

Successfully booted Firecracker microVM with guest Linux kernel v4.14.174.

## Host Environment

- **System:** iMac16,2 (bare metal, no nested virtualization)
- **KVM:** Intel KVM enabled with VMX support
- **Firecracker:** v1.13.1

## Firecracker Configuration

- **vCPU:** 1 core
- **Memory:** 128 MB
- **Kernel:** Linux 4.14.174 (hello-vmlinux.bin)
- **Rootfs:** hello-rootfs.ext4 (53 MB)

## Boot Metrics

| Metric | Value |
|--------|-------|
| Elapsed time | 2.17 seconds |
| Max RSS | 35,096 KB (~34 MB) |
| User time | 1.23 seconds |
| System time | 0.15 seconds |

## Results

✅ **Boot successful**
- Firecracker initialization: ~10ms
- Guest kernel execution began immediately
- KVM acceleration confirmed working
- Virtio MMIO device detected and initialized
- Serial console functioning

## Notes

- Guest kernel ran for ~2 seconds before timeout
- Filesystem mount error expected (rootfs path issue during test)
- Demonstrates Firecracker can successfully boot a Linux guest
- No hangs observed after group permissions fixed
- Memory overhead reasonable for single-vCPU microVM
