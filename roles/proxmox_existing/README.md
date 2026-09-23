# Existing Proxmox node

Validates an installed Proxmox node and can guardedly create or join a cluster.
It never installs or upgrades Proxmox packages. Mixed architecture membership
is self-supported and requires a separate typed acknowledgement.

The role is discovery-only by default. Membership changes require protected
inputs and `proxmox_existing_confirmation=configure-existing-proxmox`.
