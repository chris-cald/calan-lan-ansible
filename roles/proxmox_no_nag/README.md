# Proxmox no-nag

A guarded Ansible translation of the selected PVE 9 behavior from the
community-scripts post-install tool:

- disable PVE enterprise apt sources;
- add the reviewed PVE no-subscription deb822 source; and
- maintain a local post-DPkg subscription-banner patch.

It does not execute upstream code, send telemetry, add Ceph sources, enable
high availability, upgrade packages, or alter guest/VM state.

The role is disabled by default. It requires a typed confirmation:

```sh
-e proxmox_no_nag_apply=true \
-e proxmox_no_nag_confirmation=apply-proxmox-no-nag
```

The implementation supports the reviewed Proxmox VE 9.0–9.2 source layout.
Browser clients may need to clear cached UI assets after the patch.
