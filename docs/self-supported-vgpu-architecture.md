# Self-supported vGPU architecture

This is a self-supported lab design for the P400/GTX 1660 path. It makes no
vendor-support claim. All inventories, artifact paths, hashes, GPU profiles,
and credentials stay in protected operator inputs.

## Ownership

| Layer | Owner | Responsibility |
| --- | --- | --- |
| Proxmox host | Guarded Ansible | `proxmox_vgpu_host` bootstraps IOMMU, VFIO, and Manager; `proxmox_vgpu_unlock` builds a pinned local Podman payload and applies the self-supported DKMS/service changes; `proxmox_vgpu_mdev` creates one validated mediated device after reboot. |
| VM lifecycle | OpenTofu | Disposable VM, snapshot lifecycle, and mediated-device attachment after host discovery passes. |
| Talos guest | Image/system-extension build | Pinned guest driver and, if selected, the NVENC patch. Talos is not SSH-managed. |
| Kubernetes workloads | Flux | NVIDIA device plugin, optional monitoring, and constrained GPU test workload. |
| Bespoke Linux VM | Guarded Ansible | Optional hash-verified guest driver and NVENC patch; never used for Talos. |

## Inputs and checkpoints

1. Validate the protected compatibility manifest with
   `tests/validate_vgpu_compatibility_manifest.py`.
2. Run `playbooks/proxmox-vgpu.yml` with a caller-owned inventory. Mutation
   remains disabled unless both roles receive their typed confirmations. The
   Manager is a SHA-256-verified protected artifact. The unlock role fetches a
   pinned, SHA-256-verified source archive on the protected controller, builds
   a local `FROM scratch` Podman payload image, and extracts it on the host
   without running a container. The host never clones third-party sources.
3. After the host role reboots and `mdevctl types` exposes the intended profile,
   run the mdev role, then let OpenTofu attach that UUID to the disposable VM.
   Record the VM and snapshot outside Git.
4. Build a custom Talos kernel, signed GRID/vGPU extension, and installer from
   pinned protected Talos/extensions forks with
   `talos/vgpu-extension/build.py`. Record the immutable installer and
   extension digests outside Git. If `nvenc_patch_enabled` is true, the
   protected fork must verify and apply the reviewed patch during its build.
   Do not patch a running Talos node.
5. Boot the disposable Talos VM and create the suspended `vgpu-test` Flux
   Kustomization only after the prior checkpoints. Resume and reconcile it to
   apply the NVIDIA device plugin and constrained smoke workload:

   ```sh
   kubectl apply -f kubernetes/clusters/talos/tests/vgpu-flux.yaml
   flux resume kustomization vgpu-test
   flux reconcile kustomization vgpu-test --with-source
   ```

## Test-only stack artifacts

- `tofu/vgpu-test` creates one cloned VM with an externally created mdev. It is
  disabled until protected variables and `apply-disposable-vgpu-test` are
  supplied.
- `talos/vgpu-extension/build.py` executes the protected-fork custom-kernel
  builder and records immutable image references after validation.
- `kubernetes/clusters/talos/tests/vgpu` contains a node-label-scoped device
  plugin and GPU smoke Job. `kubernetes/clusters/talos/tests/vgpu-flux.yaml`
  declares a separate, suspended Flux Kustomization; it is deliberately absent
  from the default infrastructure entrypoint.

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
