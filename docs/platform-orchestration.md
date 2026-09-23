# Platform orchestration

`playbooks/platform-orchestration.yml` is the single staged Ansible entrypoint.
It accepts one caller-owned inventory outside the checkout and uses these
inventory groups:

- `proxmox_pi` for an SSH-ready, self-supported Raspberry Pi;
- `proxmox_x64` for SSH-ready x64 hosts;
- `proxmox_arm64` for supported UEFI/ACPI ARM hosts;
- `proxmox_existing` for installed Proxmox nodes; and
- `proxmox_vgpu` for optional x64 NVIDIA host and mdev phases.

The default `platform_orchestration_mode=discover` needs only the protected
inventory. It probes architecture, PVE, PCI/NVIDIA, IOMMU, and `mdevctl`, then
writes protected durable state to `~/.local/state/calan-platform/` on the
controller. `apply` needs that inventory plus one protected pipeline input
file containing `platform_orchestration_requested_roles` and only the
non-discoverable choices for those roles. It requires the typed
`apply-selected-platform-roles` confirmation and maps that confirmation to
the selected roles' guards. `rollback` is fail-closed: it records no
desired-state changes and directs the operator to restore the protected
checkpoint. Proxmox installation and cluster membership do not have a safe
automatic rollback.

After a selected Talos handoff, the playbook prints the protected OpenTofu
`init` and `plan` commands and the Flux reconciliation command. It does not
execute them or take ownership of their state.

Raspberry Pi and mixed-architecture PVE clusters are self-supported. Pi create
or join requires both the hardware acknowledgement and
`accept-mixed-architecture-proxmox-cluster` acknowledgement. The BMC/Pixie
play is an interface-only handoff and never contacts a BMC or PXE service.

The final play writes a protected handoff record for a caller-owned OpenTofu
Talos root. Ansible does not own OpenTofu state, Talos VM lifecycle, Talos
bootstrap, or Flux reconciliation.
