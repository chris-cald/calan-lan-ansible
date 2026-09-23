# `proxmox_ve`

Reusable, guarded implementation of the common Proxmox VE-on-Debian Trixie
workflow. It owns no hardware identity: compose it through `proxmox_pi`,
`proxmox_x64`, or `proxmox_arm64`, which constrain the platform before mapping
their caller-facing variables here.

All mutations are default-disabled. It stages an optional `vmbr0` bridge,
installs the official signed PVE repository and packages, and supports `single`,
`create`, and protected `join` cluster modes. It does not reload the active
network, provision storage or guests, configure qdevice, or claim rollback.
