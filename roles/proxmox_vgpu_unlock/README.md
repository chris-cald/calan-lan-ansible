# Proxmox vGPU unlock

Builds a local Podman payload image from a pinned and SHA-256-verified
`DualCoder/vgpu_unlock` source archive on the controller. The image uses
`FROM scratch`; it is loaded and copied from on the Proxmox host, never run and
never privileged.

The guarded host tasks then add the upstream wrapper to the NVIDIA vGPU service
units, patch the selected NVIDIA DKMS source tree, rebuild the module, and
reboot. This is self-supported lab work, not a vendor-supported configuration.

The role is disabled by default. It requires a typed confirmation, an approved
reboot, and the Manager's exact DKMS version:

```sh
-e proxmox_vgpu_unlock_apply=true \
-e proxmox_vgpu_unlock_reboot=true \
-e proxmox_vgpu_unlock_confirmation=apply-proxmox-vgpu-unlock \
-e proxmox_vgpu_unlock_dkms_version=570.148.06
```

The controller must have Podman. The Proxmox host receives only the local OCI
archive and uses Podman only to extract `/payload`; it never fetches or runs
upstream code in a container.
