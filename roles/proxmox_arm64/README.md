# `proxmox_arm64`

Wrapper for Proxmox VE's currently supported ARM platforms: NVIDIA Grace Hopper
and NVIDIA Vera. It requires a caller declaration of one of those platforms and
verifies UEFI plus ACPI before composing [`proxmox_ve`](../proxmox_ve/README.md).
Other ARM hardware is not accepted by this role.

```yaml
proxmox_arm64_apply: true
proxmox_arm64_confirm: provision-proxmox-arm64
proxmox_arm64_supported_platform: nvidia-grace-hopper # or nvidia-vera
proxmox_arm64_node_address: 192.0.2.30
proxmox_arm64_node_hostname: pve-arm-01
proxmox_arm64_cluster_mode: single # or create, join
```

Set `proxmox_arm64_manage_network: true` only with a separately planned,
console-tested bridge activation. Create and join use the same guarded cluster
inputs and `/etc/pve` data-loss acknowledgement as `proxmox_ve`.
