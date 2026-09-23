# Platform orchestration guard

Shared guard for every play in `playbooks/platform-orchestration.yml`. It
requires one caller-owned inventory, defaults to discovery, and records the
checkpoint/Talos handoff state in Ansible run statistics.

`apply` requires an existing caller-owned checkpoint and the typed
`apply-platform-orchestration` confirmation. `rollback` makes no changes;
Proxmox installation and cluster membership have no safe automatic rollback,
so the operator must restore the checkpoint.
