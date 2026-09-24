# Self-supported vGPU architecture

This is a self-supported lab design for the P400/GTX 1660 path. It makes no
vendor-support claim. All inventories, artifact paths, hashes, GPU profiles,
and credentials stay in protected operator inputs.

## Ownership

| Layer | Owner | Responsibility |
| --- | --- | --- |
| Proxmox host | Guarded Ansible | IOMMU, VFIO, prepatched Manager, unlock library, systemd overrides, and mediated-device discovery. |
| VM lifecycle | OpenTofu | Disposable VM, snapshot lifecycle, and mediated-device attachment after host discovery passes. |
| Talos guest | Image/system-extension build | Pinned guest driver and, if selected, the NVENC patch. Talos is not SSH-managed. |
| Kubernetes workloads | Flux | NVIDIA device plugin, optional monitoring, and constrained GPU test workload. |
| Bespoke Linux VM | Guarded Ansible | Optional hash-verified guest driver and NVENC patch; never used for Talos. |

## Inputs and checkpoints

1. Validate the protected compatibility manifest with
   `tests/validate_vgpu_compatibility_manifest.py`.
2. Run Ansible host discovery. Mutation remains disabled unless the caller sets
   `nvidia_vgpu_apply=true`, `nvidia_vgpu_reboot=true`, and the typed
   confirmation. The Manager and unlock library are prebuilt artifacts verified
   by SHA-256; the host never clones or builds third-party sources.
3. After `mdevctl types` exposes the intended profile, OpenTofu attaches that
   profile to a disposable VM. Record the VM and snapshot outside Git.
4. Build a Talos extension from the manifest's pinned guest-driver artifact.
   If `nvenc_patch_enabled` is true, apply the reviewed patch during the build,
   verify the output hash, and record its source/revision/hash in the protected
   manifest. Do not patch a running Talos node.
5. Boot the disposable Talos VM and use Flux to reconcile only the NVIDIA
   device plugin and a constrained test workload.

## Test-only stack artifacts

- `tofu/vgpu-test` creates one cloned VM with an externally created mdev. It is
  disabled until protected variables and `apply-disposable-vgpu-test` are
  supplied.
- `talos/vgpu-extension` defines the protected-builder contract for the
  immutable guest-driver and optional NVENC patch.
- `kubernetes/clusters/talos/tests/vgpu` contains a node-label-scoped device
  plugin and GPU smoke Job. It is deliberately absent from the default Flux
  infrastructure entrypoint; reconcile it only after the prior checkpoints.

## Bespoke Linux VM option

`nvidia/guest-playbook.yml` is for a non-Talos disposable Linux VM. It is
discovery-only unless `nvidia_guest_apply=true`,
`nvidia_guest_reboot=true`, and the typed confirmation are provided. The guest
driver and optional NVENC patch are local protected artifacts with SHA-256
inputs. The NVENC patch is optional and cannot run unless
`nvidia_guest_nvenc_patch_apply=true`.

## Instrumentation

Capture each checkpoint as protected operational evidence:

- **Host:** kernel command line, loaded NVIDIA modules, Manager version,
  `systemctl status nvidia-vgpud nvidia-vgpu-mgr`, `mdevctl types`, and reboot
  result.
- **VM:** assigned mediated-device UUID/profile, guest driver version, and
  `nvidia-smi` output.
- **Talos/Kubernetes:** extension image digest, node allocatable GPU resource,
  device-plugin readiness, and constrained workload result. Add DCGM exporter
  through Flux only after the device-plugin proof succeeds.

A failed checkpoint stops progression. Restore the disposable VM snapshot for
guest or Flux failures. For host failures, use the protected controller's
pre-change checkpoint; no automatic rollback is claimed.
