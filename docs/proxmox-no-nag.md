# Guarded Proxmox no-subscription and no-nag role

`playbooks/proxmox-no-nag.yml` applies the selected scope of the
community-scripts Proxmox post-install tool as auditable local Ansible tasks.
It requires one caller-owned inventory and an explicit typed confirmation.

The role supports PVE 9.0–9.2 only. It disables `pve-enterprise` sources, adds
PVE's `pve-no-subscription` source for Debian trixie, updates the apt cache,
and installs a local post-DPkg patch for the subscription banner.

It deliberately excludes the upstream script's telemetry, dynamic downloads,
Ceph source management, HA controls, package upgrades, and VM changes. Review
and back up apt source files before apply; the role does not claim automatic
rollback.
