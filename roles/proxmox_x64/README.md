# `proxmox_x64`

x86-64 wrapper around [`proxmox_ve`](../proxmox_ve/README.md). It accepts only
`x86_64`/`amd64` facts, remains default-disabled, and maps all caller-owned
network and cluster inputs to the common guarded workflow.

```yaml
proxmox_x64_apply: true
proxmox_x64_confirm: provision-proxmox-x64
proxmox_x64_node_address: 192.0.2.20
proxmox_x64_node_hostname: pve-x64-01
proxmox_x64_cluster_mode: single # or create, join
```

Set `proxmox_x64_manage_network: true` only when a console-tested bridge
activation is separately planned. `create` requires a cluster name; `join`
requires protected credentials, a pinned API certificate fingerprint, and an
explicit acknowledgement that local `/etc/pve` will be replaced.
