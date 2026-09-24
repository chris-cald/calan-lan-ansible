# Platform orchestration guard

Shared guard for every play in `playbooks/platform-orchestration.yml`. It
requires one caller-owned inventory, defaults to discovery, and records the
checkpoint/Talos handoff state in Ansible run statistics. Discovery persists
its protected checkpoint under the controller state directory.

`apply` requires that checkpoint, an explicit selected-role list, and the typed
`apply-selected-platform-roles` confirmation. `rollback` makes no changes;
Proxmox installation and cluster membership have no safe automatic rollback,
so the operator must restore the checkpoint.
