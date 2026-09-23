# Platform orchestration

`playbooks/platform-orchestration.yml` is the single staged Ansible entrypoint.
It accepts one caller-owned inventory outside the checkout and uses these
inventory groups:

- `proxmox_pi` for an SSH-ready, self-supported Raspberry Pi;
- `proxmox_x64` for SSH-ready x64 hosts;
- `proxmox_arm64` for supported UEFI/ACPI ARM hosts;
- `proxmox_existing` for installed Proxmox nodes; and
- `proxmox_vgpu` for optional x64 NVIDIA host and mdev phases.

The default `platform_orchestration_mode=discover` makes no changes. `apply`
requires `apply-platform-orchestration`, an existing caller-owned checkpoint,
and every selected role's own typed confirmation. `rollback` is fail-closed:
it records no desired-state changes and directs the operator to restore the
protected checkpoint. Proxmox installation and cluster membership do not have
a safe automatic rollback.

Raspberry Pi and mixed-architecture PVE clusters are self-supported. Pi create
or join requires both the hardware acknowledgement and
`accept-mixed-architecture-proxmox-cluster` acknowledgement. The BMC/Pixie
play is an interface-only handoff and never contacts a BMC or PXE service.

The final play writes a protected handoff record for a caller-owned OpenTofu
Talos root. Ansible does not own OpenTofu state, Talos VM lifecycle, Talos
bootstrap, or Flux reconciliation.
