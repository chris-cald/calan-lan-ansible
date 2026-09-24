# Self-supported NVIDIA vGPU lab workflow

`host-playbook.yml` is discovery-only by default. It can mutate a disposable
Proxmox host only when the caller supplies protected, external artifacts and:

```sh
-e nvidia_vgpu_apply=true \
-e nvidia_vgpu_reboot=true \
-e nvidia_vgpu_confirmation=apply-self-supported-vgpu
```

The caller must also provide a prepatched vGPU Manager installer and unlock
library with their SHA-256 values. Keep artifact paths, inventory, GPU details,
and hashes outside Git. The workflow intentionally does not clone, build, or
patch third-party software on the host.

This is a self-supported lab path. Validate mediated-device types and the
Talos extension in a disposable VM before Flux deploys any GPU workload.

`guest-playbook.yml` is only for a bespoke Linux VM. It likewise defaults to
no mutation and accepts an optional NVENC session-limit patch only as a
caller-supplied SHA-256-verified artifact. Never use it for Talos; add the
same optional patch during the Talos extension build instead.

Offline checks:

```sh
python3 tests/test_nvidia_vgpu_workflow.py
ansible-playbook --syntax-check nvidia/host-playbook.yml
ansible-lint --offline nvidia
```
