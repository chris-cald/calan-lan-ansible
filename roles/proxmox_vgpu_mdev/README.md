# Proxmox vGPU mediated device

Creates one persistent mediated device after `proxmox_vgpu_host` has installed
the Manager and the host has rebooted. It validates the supplied type against
`mdevctl types` before defining and starting the UUID.

It is disabled by default. Supply the PCI parent, mdev type, UUID, and:

```sh
-e proxmox_vgpu_mdev_apply=true \
-e proxmox_vgpu_mdev_confirmation=apply-proxmox-vgpu-mdev
```

Pass the same UUID and PCI device to the test-only OpenTofu VM root. Keep all
values in a caller-owned protected file.
