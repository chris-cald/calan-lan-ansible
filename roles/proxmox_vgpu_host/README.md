# Proxmox vGPU host

Bootstraps a vanilla Proxmox host for the self-supported vGPU lab path:
IOMMU, VFIO, prerequisites, a SHA-256-verified prepatched NVIDIA Manager, and
SHA-256-verified unlock service overrides.

It discovers PCI devices by default. Mutation requires protected artifact paths
and these inputs:

```sh
-e proxmox_vgpu_host_apply=true \
-e proxmox_vgpu_host_reboot=true \
-e proxmox_vgpu_host_confirmation=apply-proxmox-vgpu-host
```

The role intentionally does not create mediated devices. Run
`proxmox_vgpu_mdev` after the reboot and after the Manager exposes the selected
type. There is no automatic host rollback; preserve a protected pre-change
checkpoint.
